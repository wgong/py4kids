import os
import sys
import boto3
import time
import datetime
import requests

defaultRegion = 'us-east-1'
bucket_name = "wengong-lambda101"

s3 = boto3.resource('s3')


transcribe_client = boto3.client('transcribe')

def transcribe(voice_file, bucket, format='mp3', lang='en-US'):
    ts_start = datetime.datetime.now()
    basename = os.path.basename(voice_file)
    jobname, _ = os.path.splitext(basename)
    
    file_url = f"https://{bucket}.s3.amazonaws.com/{basename}"
    print(f"{file_url}")

    try:
        response = transcribe_client.start_transcription_job(
            TranscriptionJobName=jobname,
            Media={'MediaFileUri': file_url},
            MediaFormat=format,
            LanguageCode=lang)
        print(f"Request submitted: {response['ResponseMetadata']['RequestId']}")

    except Exception as e:
        print(e)
        sys.exit()

    for i in range(1,3600): # max wait = 1 hr
        status = transcribe_client.get_transcription_job(TranscriptionJobName=jobname)
        if status['TranscriptionJob']['TranscriptionJobStatus'] in ['COMPLETED', 'FAILED']:
            ts_end = datetime.datetime.now()
            break
        print(f"{i}")
        time.sleep(1)

    print(f"processing time is {ts_end - ts_start}")

    url_transcript = status['TranscriptionJob']['Transcript']['TranscriptFileUri']
    print(f"transcript URL is {url_transcript}")

    # extract transcript
    response = requests.get(url_transcript)
    response.raise_for_status()
    # access JSOn content
    jsonResponse = response.json()
    transcript = " ".join([x['transcript'] for x in jsonResponse['results']['transcripts']])

    tx_file = f"{jobname}-tx.txt"
    with open(tx_file, "w") as f:
        f.write(transcript)
    return tx_file

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(f"python {__file__} file.mp3")
        sys.exit(1)

    voice_file = sys.argv[1]


    # upload voice file to S3
    s3.Bucket(bucket_name).upload_file(voice_file, voice_file)

    # run transcribe job
    tx_file = transcribe(voice_file, bucket_name)
    print(f"transcript saved in {tx_file}")

    sys.exit(0)
