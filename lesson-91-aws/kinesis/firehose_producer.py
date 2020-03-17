import boto3
import json
import uuid
import random
import time
from datetime import datetime
import calendar

region_name   = 'us-east-1'
firehose_name = 'WildRydesFirehose'
doc_prefix    = 'MaaS-'
firehose_client = boto3.client("firehose", region_name=region_name)

def put_to_firehose(doc_id, property_timestamp, property_value):
    payload = { 'doc_id': doc_id, 'timestamp': str(property_timestamp), 'prop': str(property_value) }

    print(payload)

    put_response = firehose_client.put_record(
                        DeliveryStreamName=firehose_name,
                        Record={'Data': (json.dumps(payload)+'\n').encode('utf-8')}
                  )

while True:
    doc_id = doc_prefix + str(uuid.uuid4())
    property_timestamp = calendar.timegm(datetime.utcnow().timetuple())
    property_value = random.randint(40, 120)

    put_to_firehose(doc_id, property_timestamp, property_value)

    # wait for 5 second
    time.sleep(5)