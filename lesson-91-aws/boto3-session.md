https://docs.aws.amazon.com/elasticsearch-service/latest/developerguide/es-aws-integrations.html

import boto3
from requests_aws4auth import AWS4Auth
service='s3'
region='us-east-1'
credentials = boto3.Session().get_credentials()
awsauth = AWS4Auth(credentials.access_key, credentials.secret_key, region, service, session_token=credentials.token)
