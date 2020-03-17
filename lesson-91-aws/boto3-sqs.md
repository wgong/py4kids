https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html

import boto3
# Get the service resource
sqs = boto3.resource('sqs')

# Create the queue. This returns an SQS.Queue instance
queue = sqs.create_queue(QueueName='test', Attributes={'DelaySeconds': '1'})

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))

for queue in sqs.queues.all():
    print(queue.url)

# Create a new message
response = queue.send_message(MessageBody='hello world')
print(response.get('MessageId'))

# create messages with custom attributes:
queue.send_message(MessageBody='boto3', MessageAttributes={
    'Author': {
        'StringValue': 'Daniel',
        'DataType': 'String'
    }
})

# send msg in batch
response = queue.send_messages(Entries=[
    {
        'Id': '1001',
        'MessageBody': 'wuhan virus'
    },
    {
        'Id': '1002',
        'MessageBody': 'how is it introduced',
        'MessageAttributes': {
            'Story': {
                'StringValue': 'P4 virus lab',
                'DataType': 'String'
            }
        }
    }
])

# Print out any failures
print(response.get('Successful'))
print(response.get('Failed'))

# Processing Messages

# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue
queue = sqs.get_queue_by_name(QueueName='test')

# Process messages by printing out body and optional author name
for message in queue.receive_messages():
    # Get the custom author message attribute if it was set
    author_text = ''
    if message.message_attributes is not None:
        author_name = message.message_attributes.get('Author').get('StringValue')
        if author_name:
            author_text = ' ({0})'.format(author_name)

    # Print out the body and author (if set)
    print('Hello, {0}!{1}'.format(message.body, author_text))

    # Let the queue know that the message is processed
    # message.delete()


# https://alexwlchan.net/2018/01/downloading-sqs-queues/

import boto3

sqs_client = boto3.client('sqs')
resp = sqs_client.receive_message(
    QueueUrl='https://queue.amazonaws.com/578247465916/test',
    AttributeNames=['All'],
    MaxNumberOfMessages=10
)

try:
    messages = resp['Messages']
except KeyError:
    print('No messages on the queue!')
    messages = []

entries = [
    {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
    for msg in resp['Messages']
]


import boto3


def get_messages_from_queue(queue_url):
    """Generates messages from an SQS queue.

    Note: this continues to generate messages until the queue is empty.
    Every message on the queue will be deleted.

    :param queue_url: URL of the SQS queue to drain.

    """
    sqs_client = boto3.client('sqs')

    while True:
        resp = sqs_client.receive_message(
            QueueUrl=queue_url,
            AttributeNames=['All'],
            MaxNumberOfMessages=10
        )

        try:
            yield from resp['Messages']
        except KeyError:
            return

        entries = [
            {'Id': msg['MessageId'], 'ReceiptHandle': msg['ReceiptHandle']}
            for msg in resp['Messages']
        ]

        resp = sqs_client.delete_message_batch(
            QueueUrl=queue_url, Entries=entries
        )

        if len(resp['Successful']) != len(entries):
            raise RuntimeError(
                f"Failed to delete messages: entries={entries!r} resp={resp!r}"
            )

# dump msg to json
import json
for message in get_messages_from_queue(queue.url):
    print(json.dumps(message))

{"MessageId": "a664fdea-12a0-4932-bbc0-200209bd6774", "ReceiptHandle": "AQEBMB6RDd5gOvkcaHGi50pnXgD4FvrxY5YPekwnpDUavAIOsYPHkapFiZ/ZGzgIzCZqAMcLrWXrC80a0u754MkX/X7Y5s8NpHt4YmWoQsRI05FnB7R5xUbeWIUhIOyA+70cePMx35uKAjpT28UIND/S5RKw4Ex6mUscetgbTbBbiE6nxuIaHh922tIZmZLlQdHqA4qWRcK3i5fXCCzdIcUZkpnHH+APEeiqQ/uQetmjRyYCqzinoKPK/PArDYPyrUYLnVKx+5XD9KuI8LWNmQ8p6g6Fv8yo6vo2qAxKbAEyKqK852sJZ9uHJUsuljKTlVrdAQ8ncajt9qfkfW7TgxvZUenNcR5isBHyqVuzKvBwkzWfmy6CHsMwc3Mp9A2hNsoa", "MD5OfBody": "6686853da3491a56c98917cc5c4ddea2", "Body": "boto3", "Attributes": {"SenderId": "AIDAYNIR4DO6G4R5LUA5S", "ApproximateFirstReceiveTimestamp": "1581791709909", "ApproximateReceiveCount": "10", "SentTimestamp": "1581791709909"}}