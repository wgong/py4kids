import ast
import boto3
from datetime import datetime
import json
import os

_BUCKET_NAME = os.environ.get('MAAS_BUCKET_NAME')
_AWS_ACCESS_KEY_ID = os.environ.get('MAAS_ACCESS_KEY_ID')
_AWS_SECRET_ACCESS_KEY = os.environ.get('MAAS_SECRET_ACCESS_KEY')

s3 = boto3.resource('s3'
    ,aws_access_key_id=_AWS_ACCESS_KEY_ID
    ,aws_secret_access_key=_AWS_SECRET_ACCESS_KEY
)

prefix_ok = "fact"
prefix_nok = "fact-error"
SAVE_TO_S3_FLAG = True

def lambda_handler(event, context):
    payload = event
    # [ERROR] TypeError: Object of type LambdaContext is not JSON serializable

    maas_data = json.dumps(payload)
    print(maas_data)
    # assume single msg event
    # get body
    body = ast.literal_eval(payload["Records"][0]["body"])
    msg_type = body['msgType']
    print(msg_type)

    # write to S3
    if msg_type == 'OK':
        ts = datetime.now()
        s3object = s3.Object(_BUCKET_NAME, f"{prefix_ok}/{ts}.json")
        s3object.put(
            Body=(bytes(maas_data.encode('UTF-8')))
        )

    elif msg_type == 'ERROR':
        ts = datetime.now()
        s3object = s3.Object(_BUCKET_NAME, f"{prefix_nok}/{ts}.json")
        s3object.put(
            Body=(bytes(maas_data.encode('UTF-8')))
        )

    else:
        # send TIMEOUT msg to DLQ
        raise ValueError('send TIMEOUT msg to DLQ')

    response = {
        "statusCode": 200,
        "body": maas_data
    }

    return response
