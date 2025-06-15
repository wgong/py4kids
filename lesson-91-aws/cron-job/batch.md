AWS Batch is indeed the simplest approach for long-running shell scripts. Here's how to set it up step by step:

## Step 1: Create a Docker Image with Your Script

**Create a Dockerfile:**
```dockerfile
FROM amazonlinux:2

# Install basic tools (add what your script needs)
RUN yum update -y && yum install -y \
    bash \
    curl \
    wget \
    awscli \
    python3 \
    git \
    && yum clean all

# Copy your bash script
COPY your_script.sh /usr/local/bin/process_data.sh
RUN chmod +x /usr/local/bin/process_data.sh

# Set the script as entrypoint
ENTRYPOINT ["/usr/local/bin/process_data.sh"]
```

**Build and push to ECR:**
```bash
# Create ECR repository
aws ecr create-repository --repository-name data-processor

# Get login token
aws ecr get-login-password --region us-east-1 | docker login --username AWS --password-stdin 123456789012.dkr.ecr.us-east-1.amazonaws.com

# Build image
docker build -t data-processor .

# Tag and push
docker tag data-processor:latest 123456789012.dkr.ecr.us-east-1.amazonaws.com/data-processor:latest
docker push 123456789012.dkr.ecr.us-east-1.amazonaws.com/data-processor:latest
```

## Step 2: Create IAM Role for Batch

**Create execution role (save as `batch-execution-role.json`):**
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "ecs-tasks.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

**Create the role and attach policies:**
```bash
# Create role
aws iam create-role --role-name BatchExecutionRole --assume-role-policy-document file://batch-execution-role.json

# Attach basic execution policy
aws iam attach-role-policy --role-name BatchExecutionRole --policy-arn arn:aws:iam::aws:policy/service-role/AmazonECSTaskExecutionRolePolicy

# If your script needs S3 access, attach S3 policy too
aws iam attach-role-policy --role-name BatchExecutionRole --policy-arn arn:aws:iam::aws:policy/AmazonS3FullAccess
```

## Step 3: Create Compute Environment

```bash
aws batch create-compute-environment \
    --compute-environment-name data-processing-compute-env \
    --type MANAGED \
    --state ENABLED \
    --compute-resources type=FARGATE
```

## Step 4: Create Job Queue

```bash
aws batch create-job-queue \
    --job-queue-name data-processing-queue \
    --state ENABLED \
    --priority 1 \
    --compute-environment-order order=1,computeEnvironment=data-processing-compute-env
```

## Step 5: Create Job Definition

**Save as `job-definition.json`:**
```json
{
    "jobDefinitionName": "data-processing-job",
    "type": "container",
    "platformCapabilities": ["FARGATE"],
    "containerProperties": {
        "image": "123456789012.dkr.ecr.us-east-1.amazonaws.com/data-processor:latest",
        "executionRoleArn": "arn:aws:iam::123456789012:role/BatchExecutionRole",
        "resourceRequirements": [
            {
                "type": "VCPU",
                "value": "0.25"
            },
            {
                "type": "MEMORY",
                "value": "512"
            }
        ],
        "networkConfiguration": {
            "assignPublicIp": "ENABLED"
        },
        "logConfiguration": {
            "logDriver": "awslogs",
            "options": {
                "awslogs-group": "/aws/batch/job",
                "awslogs-region": "us-east-1"
            }
        }
    },
    "timeout": {
        "attemptDurationSeconds": 3600
    },
    "retryStrategy": {
        "attempts": 2
    }
}
```

**Create the job definition:**
```bash
aws batch register-job-definition --cli-input-json file://job-definition.json
```

## Step 6: Create Lambda Function to Submit Jobs

**Lambda function code:**
```python
import boto3
import json
import time

def lambda_handler(event, context):
    batch_client = boto3.client('batch')
    
    # Generate unique job name
    job_name = f'data-processing-{int(time.time())}'
    
    try:
        response = batch_client.submit_job(
            jobName=job_name,
            jobQueue='data-processing-queue',
            jobDefinition='data-processing-job'
        )
        
        print(f"Job submitted successfully: {response['jobId']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Job submitted successfully',
                'jobId': response['jobId'],
                'jobName': job_name
            })
        }
        
    except Exception as e:
        print(f"Error submitting job: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
```

**Create Lambda function:**
```bash
# Create Lambda function (assuming you've zipped the code as lambda_function.zip)
aws lambda create-function \
    --function-name trigger-batch-job \
    --runtime python3.9 \
    --role arn:aws:iam::123456789012:role/lambda-execution-role \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://lambda_function.zip
```

## Step 7: Schedule with EventBridge

```bash
# Create EventBridge rule
aws events put-rule \
    --name "daily-data-processing" \
    --schedule-expression "cron(0 2 * * ? *)" \
    --state ENABLED \
    --description "Run data processing daily at 2 AM"

# Add Lambda as target
aws events put-targets \
    --rule "daily-data-processing" \
    --targets "Id"="1","Arn"="arn:aws:lambda:us-east-1:123456789012:function:trigger-batch-job"

# Give EventBridge permission to invoke Lambda
aws lambda add-permission \
    --function-name trigger-batch-job \
    --statement-id allow-eventbridge \
    --action lambda:InvokeFunction \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:us-east-1:123456789012:rule/daily-data-processing
```

## Step 8: Test Your Setup

**Submit a test job:**
```bash
aws batch submit-job \
    --job-name test-job-$(date +%s) \
    --job-queue data-processing-queue \
    --job-definition data-processing-job
```

**Check job status:**
```bash
# List jobs
aws batch list-jobs --job-queue data-processing-queue

# Describe specific job
aws batch describe-jobs --jobs <job-id>
```

## Monitoring and Logs

**View logs in CloudWatch:**
```bash
# List log streams
aws logs describe-log-streams --log-group-name /aws/batch/job

# View specific log stream
aws logs get-log-events \
    --log-group-name /aws/batch/job \
    --log-stream-name <stream-name>
```

## Quick Summary

Your final architecture:
```
EventBridge (cron) → Lambda → AWS Batch → Your Shell Script (in container)
```

**Costs:**
- Lambda: ~$0.0000002 per trigger (practically free)
- Batch: Only pay for compute time when job runs
- ECR: ~$0.10/GB/month for image storage

**Benefits:**
- No 15-minute time limit
- Automatic scaling
- Built-in retry logic
- Comprehensive logging
- Easy to modify resource requirements

Replace the account ID `123456789012` with your actual AWS account ID, and update the region if you're not using `us-east-1`.