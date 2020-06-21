
## evaluate AWS Polly and Transcribe

$ cd ~/projects/aws/polly-transcribe

$ python run_polly.py preamble.txt                                     # polly

$ aws s3 cp preamble-Joanna.mp3 s3://wengong-lambda101/                # upload to S3
$ python run_transcribe.py s3://wengong-lambda101/preamble-Joanna.mp3  # transcribe

$ aws s3 cp s3://wengong-lambda101/test-transcribe.json preamble-transcribed.json

$ python compare_2text_files.py preamble.txt preamble-transcribed.txt   # check accuracy
# 0.97058


## References

- https://medium.com/@labrlearning/a-deep-dive-into-amazon-polly-3672baf6c624
- https://medium.com/@labrlearning/a-five-minute-overview-of-aws-transcribe-514b6cfeeddd

