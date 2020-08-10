

#!/usr/bin/env python
# ddb_lsi_example: A sample program to show how to use Local Secondary Indexes
# in DynamoDB, using Python and boto3.
#
# Copyright 2016 Parijat Mishra
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

""" 
 revised from  https://gist.github.com/parijatmishra/6560564a681c17e5ecf6

 1) python3 print()
 2) xrange to range()
"""

import boto3
import random
import time

## Uncomment only one of the 'client' lines below
## Real dynamoDB -- Note: this may cost you money!
# client = boto3.client('dynamodb')
## DynamoDB local -- for testing. Set the port in endpoint_url to whatever port your
## DDB local is listening on. The region is just for simulation and to satisfy the API

dynamodb_client = boto3.client('dynamodb', endpoint_url='http://localhost:8000', region_name='us-east-1')

# Constants
TABLE_NAME='UserImages'
LSI_NAME='LatestLikes'
userids = ['parijat', 'james', 'marcus']
N = 10 # each user has uploaded many images previously
M = 5  # each user will randomly like these many other users' images
Y = 5  # for each user, we want to list these many most recent liked images

def create_table():
    # skip if table already exists
    try:
        response = dynamodb_client.describe_table(TableName=TABLE_NAME)
        # table exists...bail
        print (f"Table [{TABLE_NAME}] already exists. Skipping table creation.")
        return
    except:
        pass # no table... good
    print (f"Creating table [{TABLE_NAME}]")
    response = dynamodb_client.create_table(
        TableName=TABLE_NAME,
        KeySchema=[
            {
                'KeyType': 'HASH',
                'AttributeName': 'userid'
            },
            {
                'KeyType': 'RANGE',
                'AttributeName': 'imageid'
            }
        ],
        LocalSecondaryIndexes=[
            {
                'IndexName': LSI_NAME,
                'KeySchema': [
                    {
                        'KeyType': 'HASH',
                        'AttributeName': 'userid'
                    },
                    {
                        'KeyType': 'RANGE',
                        'AttributeName': 'last_like_time'
                    }
                ],
                # Note: since we are projecting all the attributes of the table
                # into the LSI, we could have set ProjectionType=ALL and
                # skipped specifying the NonKeyAttributes
                'Projection': {
                    'ProjectionType': 'INCLUDE',
                    'NonKeyAttributes': ['imageid', 'last_like_userid', 'total_likes']
                }
            }
        ],
        AttributeDefinitions=[
            {
                'AttributeName': 'userid',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'imageid',
                'AttributeType': 'S'
            },
            {
                'AttributeName': 'last_like_time', # timestamp in secs
                'AttributeType': 'N'
            }            
        ],
        ProvisionedThroughput={
            'ReadCapacityUnits': 2,
            'WriteCapacityUnits': 2
        }
    )
    print (f"Waiting for table [{TABLE_NAME}] to be created")
    waiter = dynamodb_client.get_waiter('table_exists')
    waiter.wait(TableName=TABLE_NAME)
    # if no exception, continue
    print ("Table created")

def populate_UserImageInfo():
    # assume each user has posted N images, with imageids named
    # <userid>-<#>, where # is a number between 1 and N inclusive.
    # 
    # each user randomly likes M other images across all images
    #
    # since this is random, a user may like the same image more than once,
    # but hey, this is a simulation
    random.seed()

    print ("Updating likes...")
    print ("%10s | %15s | %15s | %24s | %10s | TWCU | IWCU" % ('Userid', 'ImageId', 'LastLikeUserId', 'LastLikeTime', 'TotalLikes'))
    for last_like_userid in userids:
        candidate_userids = [u for u in userids if u != last_like_userid]
        for i in range(M):
            time.sleep(1) # pace the writes to respect provisioned capacity, and to ensure last_like_time changes
            userid = random.choice(candidate_userids)
            num = random.randint(1, N)
            imageid = f"{userid}-{str(num)}"
            last_like_time = int(time.time())

            # insert or update a record with PK={userid, imageid}
            # with last_like_userid, last_like_time and total_likes.
            # total_likes is incremented from its existing value.
            response = dynamodb_client.update_item(
                TableName=TABLE_NAME,
                Key={
                    'userid': {"S": userid},
                    'imageid': {"S": imageid}
                },
                ReturnValues='ALL_NEW',
                UpdateExpression="SET last_like_userid=:u, last_like_time=:t ADD total_likes :i",
                ExpressionAttributeValues={
                    ":u": {"S": last_like_userid},
                    ":t": {"N": str(last_like_time)},
                    ":i": {"N": "1"}
                },
                ReturnConsumedCapacity='INDEXES'
            )
            if 'ConsumedCapacity' in response:
                # write capacity units - table
                t_wcu = response['ConsumedCapacity']['Table']['CapacityUnits']
                # write capacity units - index
                i_wcu = response['ConsumedCapacity']['LocalSecondaryIndexes'][LSI_NAME]['CapacityUnits']
            else:
                # DDB local does not return consumed capacity
                t_wcu = 0.0
                i_wcu = 0.0
            # New values of attrs. userid, imageid, last_like_userid,
            # last_like_time should be the same as we specified above
            new_attrs = response['Attributes']
            # new_attrs is a nested dict. E.g.
            # new_attrs = {"userid": {"S": "pariajt"}, "imageid": {"S": "parijat-1"}, ...}
            n_userid = new_attrs['userid']['S']
            n_imageid = new_attrs['imageid']['S']
            n_last_like_userid = new_attrs['last_like_userid']['S']
            n_last_like_time = float(new_attrs['last_like_time']['N'])
            n_last_like_time_str = time.ctime(n_last_like_time)
            n_total_likes = new_attrs['total_likes']['N']
            print ("%10s | %15s | %15s | %24s | %10s | %4.0f | %4.0f" % \
                (n_userid, n_imageid, n_last_like_userid, n_last_like_time_str, n_total_likes, t_wcu, i_wcu))

def query_LatestLikes():
    # for each user, query last Y liked images
    for userid in userids:
        print (f"Querying latest [{Y}] liked images for user [{userid}]")
        response = dynamodb_client.query(
            TableName=TABLE_NAME,
            IndexName=LSI_NAME,
            Select='ALL_PROJECTED_ATTRIBUTES',
            ConsistentRead=True,
            ReturnConsumedCapacity='INDEXES',
            ScanIndexForward=False, # return results in descending order of sort key
            Limit=Y,
            KeyConditionExpression='userid = :userid',
            ExpressionAttributeValues={":userid": {"S": userid}}
        )
        if 'ConsumedCapacity' in response:
            t_rcu = response['ConsumedCapacity']['Table']['CapacityUnits']
            i_rcu = response['ConsumedCapacity']['LocalSecondaryIndexes'][LSI_NAME]['CapacityUnits']
        else:
            t_rcu = 0.0
            i_rcu = 0.0
        print (f"Query consumed [{t_rcu}] RCUs on table, [{i_rcu}] RCUs on Index.")
        print ("%15s | %15s | %24s | %10s" % ('ImageId', 'LastLikeUserId', 'LastLikeTime', 'TotalLikes'))
        for item in response['Items']:
            imageid = item['imageid']['S']
            last_like_userid = item['last_like_userid']['S']
            last_like_time = float(item['last_like_time']['N'])
            last_like_time_str = time.ctime(last_like_time)
            total_likes = item['total_likes']['N']
            print ("%15s | %15s | %24s | %10s" % (imageid, last_like_userid, last_like_time_str, total_likes))

if __name__ == "__main__":
    create_table()
    populate_UserImageInfo()
    query_LatestLikes()