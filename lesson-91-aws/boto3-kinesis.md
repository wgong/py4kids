## Kinesis/Lambda
[Projects on AWS: Build a Serverless Real-Time Data Processing App
with AWS Lambda, Amazon Kinesis, Amazon S3, Amazon DynamoDB, Amazon Cognito, and Amazon Athena](https://aws.amazon.com/getting-started/projects/build-serverless-real-time-data-processing-app-lambda-kinesis-s3-dynamodb-cognito-athena/)

## Kinesis with Python
[Real-Time Data Streaming with Python + AWS Kinesis part 1 by Tom Thornton](https://link.medium.com/DLT9q4pu93)

[Getting started with AWS Kinesis using Python](https://www.arundhaj.com/blog/getting-started-kinesis-python.html)


## IoT monitoring
[AWS Solution: Real-Time IoT Device Monitoring with Kinesis Data Analytics](https://aws.amazon.com/solutions/real-time-iot-device-monitoring-with-kinesis/)
local: ~/projects/aws/real-time-iot-monitor-kinesis


## IoT data ingestion
[Introduction to AWS IoT: Getting your sensor data into AWS](https://blog.codecentric.de/en/2018/03/aws-iot-getting-sensordata/)


## All roads to AWS
* AWS GUI Management Console that administrates AWS services
* AWS CLI command line tool that interacts with AWS services
* AWS SDK boto3 python interface that manages AWS services
* AWS CloudFormation that automates provisioning AWS services




## CLI

aws kinesis help
aws kinesis list-streams
aws kinesis describe-stream <stream-name>
aws kinesis put-record --stream-name <stream-name> --data (base64-encoded) --partition_key <user_123>
get-records
aws get-shared-iterator --stream-name <value> --shard-id   --shard-iterator-type TRIM_HORIZON


## Tutorials
### 2020-02-17
$ aws kinesis list-streams
{
    "StreamNames": [
        "wildrydes", 
        "wildrydes-summary"
    ]
}

1) create a stream='python-stream'
$ aws kinesis create-stream --stream-name python-stream --shard-count 1

4) delete the stream='python-stream'
$ aws kinesis delete-stream --stream-name python-stream


2) run producer
$ python kinesis_producer.py
{'prop': '94', 'timestamp': '1581954222', 'thing_id': 'wen-g2g'}
{'prop': '112', 'timestamp': '1581954227', 'thing_id': 'wen-g2g'}

3) run consumer
{'Records': [{'SequenceNumber': '49604317378590711795652913693984942379460845201405247490', 'ApproximateArrivalTimestamp': datetime.datetime(2020, 2, 17, 15, 43, 40, 277000, tzinfo=tzlocal()), 'Data': b'{"prop": "94", "timestamp": "1581954222", "thing_id": "wen-g2g"}', 'PartitionKey': 'wen-g2g'}], 'NextShardIterator': 'AAAAAAAAAAG1Z5ozSvc26kWvbkeQvo+EochP6kbyVWewnijHJX+9UsSn/XThxjQnboIUQU+klBi49Wx9gQDfRFBdqsDOcpPSZ8f0rer/2+c8myvJRz+hkDQ4OtHv9N7dpg1gOq96lTN/f1gJu6oiZlwRSH76HOTCh73qJi13wfesNwYOXRHu6hdwWj9P3cZ49G76WBJwfKod/aoRAfWoP8sHMErTw71m', 'MillisBehindLatest': 0, 'ResponseMetadata': {'RequestId': 'f925c921-1a31-0360-afe1-7fd1f2f4078d', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'f925c921-1a31-0360-afe1-7fd1f2f4078d', 'x-amz-id-2': 'fsnP6R9KUw4qgeyFKYfaf4q7Hsl6pGoB8AcH+HyxEVSJgwc5pis08O7kZoBcKd0v2ve5+Ro2rZ0/1Mv7/kSVN3ahBJR82Z4k', 'date': 'Mon, 17 Feb 2020 15:43:44 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '531'}, 'RetryAttempts': 0}}
{'Records': [{'SequenceNumber': '49604317378590711795652913708373577484514161982355537922', 'ApproximateArrivalTimestamp': datetime.datetime(2020, 2, 17, 15, 43, 45, 313000, tzinfo=tzlocal()), 'Data': b'{"prop": "112", "timestamp": "1581954227", "thing_id": "wen-g2g"}', 'PartitionKey': 'wen-g2g'}], 'NextShardIterator': 'AAAAAAAAAAGBbYR2ZVErUkjl/+Un8zrCQg3C0iDo5MVxC7DGJCCNDKr3DurUS03dihq3nUA2vQJ4BURKu3WTp+DBoMvhxZQGaYos/0uafH/TmLRTmoRO2lQSpRSPknaJufcp3/6fFcTAfyp1paer0pKo3Ed9tWfilerl8Mxs9E0QVbYxlKTZNzTobA+Cm+M8hYk8ccH4zs1CRDdb3MPaCNFoe4jRv/B1', 'MillisBehindLatest': 0, 'ResponseMetadata': {'RequestId': 'e34e80d8-e322-7782-b58a-362d0be7736f', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'e34e80d8-e322-7782-b58a-362d0be7736f', 'x-amz-id-2': 'LLvXEBgTQxF4RlmO4ihqWcV2lggjGPmAMKFxlBokEEkHxN/g/CqcjeOECsfgyDoR2jPma9uLV5+eyCobXUJVrJMY/5Hh1IY5', 'date': 'Mon, 17 Feb 2020 15:43:49 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '531'}, 'RetryAttempts': 0}}
{'Records': [], 'NextShardIterator': 'AAAAAAAAAAHQnJ5tdy5FqisOXQTwcUnmoXWSAsFbITB1RljwM6s8AujXeofxxoUKT0P4xMKUgnAks3pryiRNmh1XElMw4R6C0hfDE+rqjrhjQe/aKUacXapcyULWbp8pBChYFDnPpgBoO1LsipzEZqsYW1iVPdqPtlfcJFqjfemb97zvJ1zJdhlP8RgfUNt307QPE9ujUScVNpKAJSWNBNb3Ovnw8FOd', 'MillisBehindLatest': 0, 'ResponseMetadata': {'RequestId': 'cedd0523-2fc6-0176-9819-b3d9c703059b', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amzn-requestid': 'cedd0523-2fc6-0176-9819-b3d9c703059b', 'x-amz-id-2': 'mJDFpxGIUaaHv5bq0trqDaHf6JONUlDqarzNuiH840TTVpqjKt8yeV3S1qT/wRB9X6QdVGC4Nj6AnCYvsYtq5qmBvZQ82F77', 'date': 'Mon, 17 Feb 2020 15:43:54 GMT', 'content-type': 'application/x-amz-json-1.1', 'content-length': '284'}, 'RetryAttempts': 0}}