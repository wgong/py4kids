import boto3
import json
from datetime import datetime
import calendar
import random
import time

my_stream_name = 'python-stream'
region_name = 'us-east-1'
kinesis_client = boto3.client('kinesis', region_name=region_name)


def put_to_stream(thing_id, property_value, property_timestamp):
    payload = {
                'prop': str(property_value),
                'timestamp': str(property_timestamp),
                'thing_id': thing_id
              }

    print(payload)

    put_response = kinesis_client.put_record(
                        StreamName=my_stream_name,
                        Data=json.dumps(payload),
                        PartitionKey=thing_id)

while True:
    property_value = random.randint(40, 120)
    property_timestamp = calendar.timegm(datetime.utcnow().timetuple())
    thing_id = 'wen-g2g'

    put_to_stream(thing_id, property_value, property_timestamp)

    # wait for 5 second
    time.sleep(5)