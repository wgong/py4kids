# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html

import boto3
sns = boto3.client("sns")
response = sns.publish( 
    TopicArn='arn:aws:sns:us-east-1:578247465916:MaasSNSTestTopic', 
    Message='Hello Wen @ AWS', 
)  

print(response)

# https://boto3.amazonaws.com/v1/documentation/api/latest/guide/sqs.html
# using existing queue
# Get the service resource
sqs = boto3.resource('sqs')

# Get the queue. This returns an SQS.Queue instance
queue = sqs.get_queue_by_name(QueueName='MaasSQSBackup')

# You can now access identifiers and attributes
print(queue.url)
print(queue.attributes.get('DelaySeconds'))

# Print out each queue name, which is part of its ARN
for queue in sqs.queues.all():
    print(queue.url)
    
response = queue.send_message(MessageBody='Hell AWS world')

print(response)  

# processing msg
q2 = sqs.get_queue_by_name(QueueName='MaasDLQ')
for msg in q2.receive_messages():
    print(msg.body)
    msg.delete()
