https://realpython.com/python-boto3-aws-s3/



import boto3
# connect to the low-level client interface
s3_client = boto3.client('s3')

# connect to the high-level interface
s3_resource = boto3.resource('s3')

# diff between client and resource
# With clients, there is more programmatic work to be done. The majority of the client operations give you a dictionary response. To get the exact information that you need, you’ll have to parse that dictionary yourself. With resource methods, the SDK does that work for you.

# create bucket
import uuid
def create_bucket_name(bucket_prefix):
    # The generated bucket name must be between 3 and 63 chars long
    return ''.join([bucket_prefix, str(uuid.uuid4())])
    
def create_bucket(bucket_prefix, s3_connection):
    session = boto3.session.Session()
    current_region = session.region_name
    bucket_name = create_bucket_name(bucket_prefix)
    bucket_response = s3_connection.create_bucket(
        Bucket=bucket_name)
    print(bucket_name, current_region)
    return bucket_name, bucket_response
    
first_bucket_name, first_response = create_bucket(
    bucket_prefix='weng2g',
    s3_connection=s3_resource.meta.client)
    
>>> first_response
{'ResponseMetadata': {'RequestId': '0D7AF4E4FEF8EC7C', 'HostId': 'Nufd1hRCGgcOPwDzqzzqsdXB1M8v39imyT63/g5HIdW3KWIieDhPCWy5BHxIkwaurFAE2stRFkk=', 'HTTPStatusCode': 200, 'HTTPHeaders': {'x-amz-id-2': 'Nufd1hRCGgcOPwDzqzzqsdXB1M8v39imyT63/g5HIdW3KWIieDhPCWy5BHxIkwaurFAE2stRFkk=', 'x-amz-request-id': '0D7AF4E4FEF8EC7C', 'date': 'Fri, 14 Feb 2020 16:53:37 GMT', 'location': '/weng2g917badf2-937e-4d1f-a077-fceaca13693f', 'content-length': '0', 'server': 'AmazonS3'}, 'RetryAttempts': 0}, 'Location': '/weng2g917badf2-937e-4d1f-a077-fceaca13693f'}

second_bucket_name, second_response = create_bucket(
    bucket_prefix='weng2g', s3_connection=s3_resource)
    
>>> second_response
s3.Bucket(name='weng2g8a0a4e3d-4490-4604-9b94-30f715a6de13')

# create file
def create_temp_file(size, file_name, file_content):
    random_file_name = ''.join([str(uuid.uuid4().hex[:6]), file_name])
    with open(random_file_name, 'w') as f:
        f.write(str(file_content) * size)
    return random_file_name
    
# upload file    
first_bucket = s3_resource.Bucket(name=first_bucket_name)
first_object = s3_resource.Object(
    bucket_name=first_bucket_name, key=first_file_name)
    
first_object.upload_file(first_file_name)

s3_resource.Bucket(first_bucket_name).upload_file(
    Filename="firstfile.txt", Key="firstfile.txt")
    
# Download file
s3_resource.Object(first_bucket_name, first_file_name).download_file(
    f'/tmp/{first_file_name}')
    
# Copying an Object Between Buckets
def copy_to_bucket(bucket_from_name, bucket_to_name, file_name):
    copy_source = {
        'Bucket': bucket_from_name,
        'Key': file_name
    }
    s3_resource.Object(bucket_to_name, file_name).copy(copy_source)

copy_to_bucket(first_bucket_name, second_bucket_name, first_file_name)

# delete object
s3_resource.Object(second_bucket_name, first_file_name).delete()

# Access Control List
>>> first_obj_acl = first_object.Acl()
>>> first_obj_acl.grants
[{'Grantee': {'DisplayName': 'weng2g', 'ID': 'd9e52cf2e5671a8ed6a7fc3073b7a70a6cae7dc2c2c7c8466390dd63d201103a', 'Type': 'CanonicalUser'}, 'Permission': 'FULL_CONTROL'}]

# encryption
>>> third_file_name = create_temp_file(300, 'thirdfile.txt', 't')
>>> third_object = s3_resource.Object(first_bucket_name, third_file_name)
>>> third_object.upload_file(third_file_name, ExtraArgs={
...                          'ServerSideEncryption': 'AES256'})
>>> third_object.server_side_encryption
'AES256'

# Traversals
for bucket in s3_resource.buckets.all():
    print(bucket.name)
    for obj in bucket.objects.all():
        print('\t'+obj.key)
        
# Deleting Buckets and Objects
# To remove all the buckets and objects you have created, you must first make sure that your buckets have no objects within them.

def delete_all_objects(bucket_name):
    res = []
    bucket=s3_resource.Bucket(bucket_name)
    for obj_version in bucket.object_versions.all():
        res.append({'Key': obj_version.object_key,
                    'VersionId': obj_version.id})
    print(res)
    bucket.delete_objects(Delete={'Objects': res})

s3_resource.Bucket(first_bucket_name).delete()    
s3_resource.Bucket(second_bucket_name).delete()


https://boto3.amazonaws.com/v1/documentation/api/latest/guide/s3-examples.html

# use client
import boto3                                                                                   s3 = boto3.client("s3")                                                                        resp = s3.list_buckets()    
for b in resp['Buckets']: 
    print(f" {b['Name']}") 

# AWS CLI

$ aws s3 help
$ aws s3 ls
# create a bucket at console
$ aws s3 ls weng2g-cert-dev

# download
aws s3 cp s3://weng2g-cert-dev/aws.readme.md .
aws s3 cp s3://weng2g-cert-dev/boto3-dynamodb.md .
aws s3 cp s3://weng2g-cert-dev/boto3-kinesis.md .
aws s3 cp s3://weng2g-cert-dev/boto3-sqs.md .
aws s3 cp s3://weng2g-cert-dev/boto3-s3.md .

# upload
aws s3 cp aws.readme.md s3://weng2g-cert-dev
aws s3 cp boto3-dynamodb.md s3://weng2g-cert-dev
aws s3 cp boto3-kinesis.md s3://weng2g-cert-dev
aws s3 cp boto3-sqs.md s3://weng2g-cert-dev
aws s3 cp boto3-s3.md s3://weng2g-cert-dev
