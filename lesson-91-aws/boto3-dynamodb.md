https://boto3.amazonaws.com/v1/documentation/api/latest/guide/dynamodb.html
https://read.acloud.guru/why-amazon-dynamodb-isnt-for-everyone-and-how-to-decide-when-it-s-for-you-aefc52ea9476

# Creating a new table
import boto3

# Get the service resource.
dynamodb = boto3.resource('dynamodb')

# Create the DynamoDB table.
table = dynamodb.create_table(
    TableName='users',
    KeySchema=[
        {
            'AttributeName': 'username',
            'KeyType': 'HASH'
        },
        {
            'AttributeName': 'last_name',
            'KeyType': 'RANGE'
        }
    ],
    AttributeDefinitions=[
        {
            'AttributeName': 'username',
            'AttributeType': 'S'
        },
        {
            'AttributeName': 'last_name',
            'AttributeType': 'S'
        },
    ],
    ProvisionedThroughput={
        'ReadCapacityUnits': 5,
        'WriteCapacityUnits': 5
    }
)

# Wait until the table exists.
table.meta.client.get_waiter('table_exists').wait(TableName='users')

# Print out some data about the table.
print(table.item_count)

print(table.creation_date_time)

# Creating a New Item
table.put_item(
   Item={
        'username': 'janedoe',
        'first_name': 'Jane',
        'last_name': 'Doe',
        'age': 25,
        'account_type': 'standard_user',
    }
)

table.put_item(
   Item={
        'username': 'yanggang',
        'first_name': 'Andrew',
        'last_name': 'Yang',
        'age': 45,
        'account_type': 'standard_user',
    }
)

# Getting an Item
response = table.get_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)
item = response['Item']
print(item)
{'username': 'janedoe', 'account_type': 'standard_user', 'last_name': 'Doe', 'first_name': 'Jane', 'age': Decimal('25')}

# Updating Item
table.update_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    },
    UpdateExpression='SET age = :val1',
    ExpressionAttributeValues={
        ':val1': 26
    }
)

# Deleting Item
table.delete_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)

response = table.get_item(
    Key={
        'username': 'janedoe',
        'last_name': 'Doe'
    }
)
item = response['Item']
## threw KeyError: 'Item'

# Batch Writing
## If you are loading a lot of data at a time, you can make use of DynamoDB.Table.batch_writer() so you can both speed up the process and reduce the number of write requests made to the service.

with table.batch_writer() as batch:
    batch.put_item(
        Item={
            'account_type': 'standard_user',
            'username': 'johndoe',
            'first_name': 'John',
            'last_name': 'Doe',
            'age': 25,
            'address': {
                'road': '1 Jefferson Street',
                'city': 'Los Angeles',
                'state': 'CA',
                'zipcode': 90001
            }
        }
    )
    batch.put_item(
        Item={
            'account_type': 'super_user',
            'username': 'janedoering',
            'first_name': 'Jane',
            'last_name': 'Doering',
            'age': 40,
            'address': {
                'road': '2 Washington Avenue',
                'city': 'Seattle',
                'state': 'WA',
                'zipcode': 98109
            }
        }
    )
    batch.put_item(
        Item={
            'account_type': 'standard_user',
            'username': 'bobsmith',
            'first_name': 'Bob',
            'last_name':  'Smith',
            'age': 18,
            'address': {
                'road': '3 Madison Lane',
                'city': 'Louisville',
                'state': 'KY',
                'zipcode': 40213
            }
        }
    )
    batch.put_item(
        Item={
            'account_type': 'super_user',
            'username': 'alicedoe',
            'first_name': 'Alice',
            'last_name': 'Doe',
            'age': 27,
            'address': {
                'road': '1 Jefferson Street',
                'city': 'Los Angeles',
                'state': 'CA',
                'zipcode': 90001
            }
        }
    )

with table.batch_writer() as batch:
    for i in range(20):
        batch.put_item(
            Item={
                'account_type': 'anonymous',
                'username': 'user' + str(i),
                'first_name': 'unknown',
                'last_name': 'Lastname-' + str(i)
            }
        )

with table.batch_writer() as batch:
    for i in range(10):
        batch.delete_item(
            Key={
                'username': 'user' + str(i),
                'last_name': 'Lastname-' + str(i)
            }
        )

with table.batch_writer() as batch:
    for i in range(10,15):
        batch.delete_item(
            Key={
                'username': 'user' + str(i),
                'last_name': 'Lastname-' + str(i)
            }
        )

# Querying and Scanning
from boto3.dynamodb.conditions import Key, Attr
response = table.query(
    KeyConditionExpression=Key('username').eq('johndoe')
)
items = response['Items']
print(items)

response = table.scan(
    FilterExpression=Attr('age').lt(27)
)
items = response['Items']
print(items)

response = table.scan(
    FilterExpression=Attr('first_name').begins_with('J') & Attr('account_type').eq('super_user')
)
items = response['Items']
print(items)

response = table.scan(
    FilterExpression=Attr('first_name').begins_with('unk')
)
items = response['Items']
print(items)

response = table.scan(
    FilterExpression=Attr('address.state').eq('WA')
)
items = response['Items']
print(items)

# Deleting a Table
table.delete()