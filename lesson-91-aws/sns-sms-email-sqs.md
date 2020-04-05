pub msg to SNS:
{
    "msgId": "73195b72-67f7-11ea-9dd0-3398176b7012",
    "ts": "2020-03-21T22:31:47.384675",
    "msgSeq": 274,
    "msgBody": "Test message 274",
    "msgType": "OK"
}

3 subscribers:
1) email
{
    "msgId": "73195b72-67f7-11ea-9dd0-3398176b7012",
    "ts": "2020-03-21T22:31:47.384675",
    "msgSeq": 274,
    "msgBody": "Test message 274",
    "msgType": "OK"
}
2) SMS/phone
{
    "msgId": "73195b72-67f7-11ea-9dd0-3398176b7012",
    "ts": "2020-03-21T22:31:47.384675",
    "msgSeq": 274,
    "msgBody": "Test message 274",
    "msgType": "OK"
}
3) SQS
triggers lambda=MaasSQSTriggerTest 
failed due to msg format mismatch
landed to DLQ
{
  "Type" : "Notification",
  "MessageId" : "55cdb836-482a-519c-8bf1-eec6fd085f41",
  "TopicArn" : "arn:aws:sns:us-east-1:578247465916:MaasSNSTestTopic",
  "Subject" : "Test SNS",
  "Message" : "{\n    \"msgId\": \"73195b72-67f7-11ea-9dd0-3398176b7012\",\n    \"ts\": \"2020-03-21T22:31:47.384675\",\n    \"msgSeq\": 274,\n    \"msgBody\": \"Test message 274\",\n    \"msgType\": \"OK\"\n}",
  "Timestamp" : "2020-03-22T00:35:46.915Z",
  "SignatureVersion" : "1",
  "Signature" : "JkI/cQEL/8TNr17yDkSurEvLvL1vyCofKnhRe+aYmNViErxYOYH60cZc9rmdia9Ik7DGuTqkFpgHIfJWMMVndY6QbfdI3RTrRR5Lze5paAS2g00gjPs7kzdGNVRHuGiiPFF23WrMpHe6H8lZJrle1SelViqR/OG0sKkqmFgzMUJnQOdzzjXuMVcrYHYu+SW6cKhIk5fuJ60HHnNYK01JoeenEqzzzQUFyY/uOkk+abI4Ve5pKyN/uXCoiGmbnZbwQLRftwZFVAcCc1pmHu9O1R2vgjEoaQzdhYPrzuFQSqBJbDvL+gaTgA3GV7a8Twgh7kKWLE4sQRJNXAqy1vDveg==",
  "SigningCertURL" : "https://sns.us-east-1.amazonaws.com/SimpleNotificationService-a86cb10b4e1f29c941702d737128f7b6.pem",
  "UnsubscribeURL" : "https://sns.us-east-1.amazonaws.com/?Action=Unsubscribe&SubscriptionArn=arn:aws:sns:us-east-1:578247465916:MaasSNSTestTopic:17b08138-5765-440c-894a-6b83d9496465"
}

if sending msg to SQS directly
{
    "msgId": "73195b72-67f7-11ea-9dd0-3398176b7012",
    "ts": "2020-03-16T22:31:47.384675",
    "msgSeq": 275,
    "msgBody": "Test message 275",
    "msgType": "OK"
}

msg received at Lambda
{
    "Records": [
        {
            "messageId": "fc942fc3-5d6f-4c5f-b0ff-190ac017c74d",
            "receiptHandle": "AQEBrbqfIUpZZTiIK+xrFukwjK2ATHfoFe5Z5UUy6lDDkKSmdnT9IND00qafYbZp/pKNMWRe2UTig/rqvQAd7XjzGLIrO582s+GtJ7PvmAQP8hWhjzbg9ziooZ1D8I0gDbrgUuefAXnDeRaWx78QYp16QgPar1lFKf4cvNxVkMiRRSJUsGEZiEfAXh9/MJwAWcfeAjtuiveoBTEwT7nPyD+pi0htDwGS9oxj7quQ5J9B52eFOWhTEmtL0dtoyIqGm46+NFiUte4tN7J3qgTjAhsBYQVT1GQrhmTPhEUFJ4IirbhZtmRiJRwzJ+l5SXPZOnUCHQSsdak8rdwtQfjNESfzVvI3mvxQd0f1umspF+NFAx2xBdevdC3rUGdl+X6mbXD+gu8DQX6p/I0SXaodb0ejdw==",
            "body": "{\n    \"msgId\": \"73195b72-67f7-11ea-9dd0-3398176b7012\",\n    \"ts\": \"2020-03-16T22:31:47.384675\",\n    \"msgSeq\": 275,\n    \"msgBody\": \"Test message 275\",\n    \"msgType\": \"OK\"\n}",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1584838004278",
                "SenderId": "AIDAYNIR4DO6G4R5LUA5S",
                "ApproximateFirstReceiveTimestamp": "1584838004279"
            },
            "messageAttributes": {},
            "md5OfBody": "91e1143c928ae59564c13cb69a216782",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-1:578247465916:MaasSQSLambda",
            "awsRegion": "us-east-1"
        }
    ]
}

create a lambda=MaasSnsSqsLambda
no processing, just dump event


testEvent
1) sqs
{
  "Records": [
    {
      "messageId": "19dd0b57-b21e-4ac1-bd88-01bbb068cb78",
      "receiptHandle": "MessageReceiptHandle",
      "body": "Hello from SQS!",
      "attributes": {
        "ApproximateReceiveCount": "1",
        "SentTimestamp": "1523232000000",
        "SenderId": "123456789012",
        "ApproximateFirstReceiveTimestamp": "1523232000001"
      },
      "messageAttributes": {},
      "md5OfBody": "7b270e59b47ff90a553787216d55d91d",
      "eventSource": "aws:sqs",
      "eventSourceARN": "arn:aws:sqs:us-east-1:123456789012:MyQueue",
      "awsRegion": "us-east-1"
    }
  ]
}

2) sns
{
    "Records": [
        {
            "EventSource": "aws:sns",
            "EventVersion": "1.0",
            "EventSubscriptionArn": "arn:aws:sns:us-east-1:{{{accountId}}}:ExampleTopic",
            "Sns": {
                "Type": "Notification",
                "MessageId": "95df01b4-ee98-5cb9-9903-4c221d41eb5e",
                "TopicArn": "arn:aws:sns:us-east-1:123456789012:ExampleTopic",
                "Subject": "example subject",
                "Message": "example message",
                "Timestamp": "1970-01-01T00:00:00.000Z",
                "SignatureVersion": "1",
                "Signature": "EXAMPLE",
                "SigningCertUrl": "EXAMPLE",
                "UnsubscribeUrl": "EXAMPLE",
                "MessageAttributes": {
                    "Test": {
                        "Type": "String",
                        "Value": "TestString"
                    },
                    "TestBinary": {
                        "Type": "Binary",
                        "Value": "TestBinary"
                    }
                }
            }
        }
    ]
}



sns:
{
    "msgId": "73195b72-67f7-11ea-9dd0-3398176b7012",
    "ts": "2020-03-21T22:31:47.384675",
    "msgSeq": 274,
    "msgBody": "Test SNS fanout - email/sms/sqs/lambda",
    "msgType": "OK"
}

sqs/lambda:
{
    "Records": [
        {
            "messageId": "dcc73e9c-3757-4e67-a6c1-89a25ddedc53",
            "receiptHandle": "AQEBgIVUsWIeREvzWHjwSSxCqbtueKZb/1VrJx6HwWEmP+KSN02SU30SKMK7pvFrjYD9kP0ntnjxQnngo5EBYgkGUFqWt7uUx6/cUJxUkKwbhuFRx6HMEMU/8rQ/c7nebPGuI9ufcRj9uT+Umzr5RNtl4lVDxfRTlppc0Rwc/pWG1PGD/Hn6LojRsjlutjscG6iusXQed2FjbA/LfMZ30/OpWxS6SN5UgTcd2EOddFEtThBDxu3UStY2s8NDZHFyjLu4wp/ZkPOYDQysqF8fgyQGdWm3ItJtLgb8UtaK+NKJxJCWCv9AdlcyL8cxg6ZgciTLRUFhomv1didzN5muqXBb2WO8jos0qMyxc+YkwwgzABvStlsEv5sdwBoPkUnbY5oh",
            "body": "{\n    \"msgId\": \"73195b72-67f7-11ea-9dd0-3398176b7012\",\n    \"ts\": \"2020-03-21T22:31:47.384675\",\n    \"msgSeq\": 274,\n    \"msgBody\": \"Test SNS fanout - email/sms/sqs/lambda\",\n    \"msgType\": \"OK\"\n}",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1584839513071",
                "SenderId": "AIDAIT2UOQQY3AUEKVGXU",
                "ApproximateFirstReceiveTimestamp": "1584839513081"
            },
            "messageAttributes": {},
            "md5OfBody": "262c72522c7375b560cdb53dce3992ef",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-1:578247465916:MaasSQSBackup",
            "awsRegion": "us-east-1"
        }
    ]
}

sqs:
{
    "msgId": "73195b72-67f7-11ea-9dd0-3398176b7012",
    "ts": "2020-03-21T22:31:47.384675",
    "msgSeq": 274,
    "msgBody": "Test SNS fanout - email/sms/sqs/lambda",
    "msgType": "OK"
}

sqs/lambda:
{
    "Records": [
        {
            "messageId": "a31ea961-d071-4440-8bc9-58942e65d6cb",
            "receiptHandle": "AQEBt+mE7I744y6RAdMKx8iX/sllIDSvG3iwHyABGkx82l/u/SBJyDKGkSk++D0Ai3Y6ZcYrAzMMOMClvIx8tdSAdG5RvsaAV+PP94H09dduI1DaTVuL7hzC41Smz6CNxVmLjI1D2P1LiGmWDjq70G6W8vM9VhDaPyKNklJFCBs5V73ffwIZyvZxod4QuimLJEuB6Wyk2B0ra1VAuiG1FHJi/d/OJ5AHTCUmzGUG1irL9VYmtDQMEQXKKMUnrDt267pHZOk4bRZntJWsUEriej30xbA3aOombdPhjnwU2uBK1S/bGMQANlZawBeYkF5JGrACVAhaQVumjos7oZmtvKCPfdCfBSFryQAXZ0/JeWiITJ1n0PO8VR5eC2k40e992Shx",
            "body": "{\n    \"msgId\": \"73195b72-67f7-11ea-9dd0-3398176b7012\",\n    \"ts\": \"2020-03-21T22:31:47.384675\",\n    \"msgSeq\": 274,\n    \"msgBody\": \"Test SNS fanout - email/sms/sqs/lambda\",\n    \"msgType\": \"OK\"\n}",
            "attributes": {
                "ApproximateReceiveCount": "1",
                "SentTimestamp": "1584841050137",
                "SenderId": "AIDAYNIR4DO6G4R5LUA5S",
                "ApproximateFirstReceiveTimestamp": "1584841050139"
            },
            "messageAttributes": {},
            "md5OfBody": "262c72522c7375b560cdb53dce3992ef",
            "eventSource": "aws:sqs",
            "eventSourceARN": "arn:aws:sqs:us-east-1:578247465916:MaasSQSBackup",
            "awsRegion": "us-east-1"
        }
    ]
}