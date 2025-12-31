import os
import boto3
import json
import datetime
import time
import random
import socket

# --- Configuration ---
S3_BUCKET = os.environ.get('S3_BUCKET', 'your-default-s3-bucket')
# The date-stamped key format will be used, e.g., '2025-10-13-batch-run.json'
S3_PREFIX = 'batch-job-history/' 
MAX_JITTER_SECONDS = 300  # Max 5 minutes delay (0-300 seconds)
JOB_DURATION_MINUTES = 60 # Maximum time the job should run (for lease checking)

# --- Identifiers ---
INSTANCE_ID = socket.gethostname() # Unique ID for this container
S3_CLIENT = boto3.client('s3')

def get_proof_key():
    """Generates the date-stamped S3 key for the batch run."""
    # The job runs at 1 AM EST, but is logically for the day that just ended.
    # However, since you want it to act as a lock for the current run, 
    # we'll date it for the current calendar day (e.g., runs 1am Oct 13 -> uses Oct 13)
    today_date_str = datetime.date.today().strftime('%Y-%m-%d')
    return f"{S3_PREFIX}{today_date_str}-batch-run.json"

def acquire_lock_and_run_job():
    """
    Attempts to acquire the lock (create the S3 proof file).
    If successful, runs the batch job and updates the file.
    """
    lock_key = get_proof_key()
    now_utc = datetime.datetime.now(datetime.timezone.utc)
    
    print(f"[{INSTANCE_ID}] Checking S3 for existing proof file: {lock_key}")

    # 1. CHECK FOR EXISTING PROOF/LOCK (Atomic Check)
    try:
        S3_CLIENT.head_object(Bucket=S3_BUCKET, Key=lock_key)
        print(f"[{INSTANCE_ID}] Proof file already exists. Job already claimed or completed. Standing down.")
        return False
    except S3_CLIENT.exceptions.ClientError as e:
        # 404 error means the object doesn't exist, which is what we want.
        if e.response['Error']['Code'] != '404':
            print(f"[{INSTANCE_ID}] Error checking S3: {e}")
            return False
        # File not found (404), continue to acquire the lock

    # 2. ATTEMPT TO ACQUIRE THE LOCK (Initial Atomic Write)
    initial_content = {
        'leader_id': INSTANCE_ID,
        'started_at': now_utc.isoformat(),
        'status': 'RUNNING',
        'expected_finish_by': (now_utc + datetime.timedelta(minutes=JOB_DURATION_MINUTES)).isoformat(),
        'message': 'Lock claimed. Job running...'
    }
    
    try:
        # Use a PUT operation. The first one to successfully write the new object wins.
        # This relies on S3's strong consistency for new object PUTs.
        S3_CLIENT.put_object(
            Bucket=S3_BUCKET,
            Key=lock_key,
            Body=json.dumps(initial_content),
            ContentType='application/json'
        )
        print(f"[{INSTANCE_ID}] Successfully ACQUIRED the lock. Starting batch job.")
        
    except Exception as e:
        # In case of any race condition or error during PUT, assume another won.
        print(f"[{INSTANCE_ID}] Failed to acquire lock during PUT operation: {e}. Another instance likely won the race.")
        return False

    # 3. RUN THE BATCH JOB (WINNER ONLY)
    try:
        print("--- STARTING BATCH JOB EXECUTION ---")
        run_the_batch_logic() # <-- REPLACE with your actual job function
        print("--- BATCH JOB EXECUTION FINISHED ---")

        # 4. UPDATE S3 WITH SUCCESS STATUS
        final_content = initial_content.copy()
        final_content['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        final_content['status'] = 'SUCCESS'
        final_content['message'] = 'Batch job completed successfully.'

        S3_CLIENT.put_object(
            Bucket=S3_BUCKET,
            Key=lock_key,
            Body=json.dumps(final_content),
            ContentType='application/json'
        )
        print(f"[{INSTANCE_ID}] S3 Proof-of-Run updated to SUCCESS.")
        return True

    except Exception as job_error:
        print(f"[{INSTANCE_ID}] BATCH JOB FAILED: {job_error}")
        
        # 4. UPDATE S3 WITH FAILURE STATUS
        fail_content = initial_content.copy()
        fail_content['finished_at'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
        fail_content['status'] = 'FAILURE'
        fail_content['error'] = str(job_error)
        fail_content['message'] = 'Batch job failed during execution.'
        
        S3_CLIENT.put_object(
            Bucket=S3_BUCKET,
            Key=lock_key,
            Body=json.dumps(fail_content),
            ContentType='application/json'
        )
        print(f"[{INSTANCE_ID}] S3 Proof-of-Run updated to FAILURE.")
        return False

def run_the_batch_logic():
    """
    *** REPLACE THIS FUNCTION WITH YOUR ACTUAL BATCH JOB CODE ***
    This is where your long-running tasks go.
    """
    # Simulate a job that takes between 30 and 60 minutes
    run_time = random.randint(30 * 60, 60 * 60)
    print(f"[{INSTANCE_ID}] Simulating batch job for {run_time / 60:.2f} minutes.")
    
    # Placeholder for actual job code (e.g., data processing, S3-to-DB sync, etc.)
    time.sleep(run_time) 
    
    # Example to simulate a random failure 
    if random.random() < 0.05: # 5% chance of failure
         raise Exception("Simulated critical processing error.")
    
    print(f"[{INSTANCE_ID}] Batch job logic completed.")


if __name__ == '__main__':
    # 1. Apply Jitter
    delay = random.randint(0, MAX_JITTER_SECONDS)
    print(f"[{INSTANCE_ID}] Batch job trigger received. Applying random jitter: {delay} seconds.")
    time.sleep(delay)

    # 2. Attempt to Acquire Lock and Run
    success = acquire_lock_and_run_job()
    if success:
        print(f"[{INSTANCE_ID}] Job finished successfully.")
    else:
        print(f"[{INSTANCE_ID}] Job either failed or was skipped due to existing lock.")