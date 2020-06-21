import os
import sys
import boto3

defaultRegion = 'us-east-1'
defaultUrl = f'https://polly.{defaultRegion}.amazonaws.com'

polly_client = boto3.client('polly', region_name=defaultRegion, endpoint_url=defaultUrl)

def polly_speak(polly, input_file, format='mp3', voice='Joanna'):
    with open(input_file) as f:
        text = f.read()
        resp = polly.synthesize_speech(OutputFormat=format, Text=text, VoiceId=voice)
        soundBytes = resp['AudioStream'].read()

        filename, _ = os.path.splitext(input_file)
        output_file = f"{filename}-{voice}.{format}"
        with open(output_file, 'wb') as soundfile:
            soundfile.write(soundBytes)

if __name__ == "__main__":
    if len(sys.argv) > 1:
        polly_speak(polly_client, sys.argv[1])
        sys.exit(0)
    else:
        print(f"python {__file__} f1.txt")
        sys.exit(1)   