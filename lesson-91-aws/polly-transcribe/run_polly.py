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
    if len(sys.argv) < 2:
        print(f"python {__file__} file.txt [Voice]")
        sys.exit(1)
    if len(sys.argv) > 1:
        input_file = sys.argv[1]

    # https://docs.aws.amazon.com/polly/latest/dg/voicelist.html
    # Female: Joanna, Kendra, Salli, Kimberly
    # Female/Child: Ivy
    # Male: Joey, Matthew
    # Male/Child: Justin, Kevin
    voice = 'Joanna'
    if len(sys.argv) > 2:
        voice = sys.argv[2]

    polly_speak(polly_client, input_file, voice=voice)
    sys.exit(0)
