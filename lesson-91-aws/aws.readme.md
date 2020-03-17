$ login to AWS console, start EC2 instance "dev-cert", get public IP=35.174.3.39

$ cd ~/projects/aws/cert-developer

$ ssh -i ~/.ssh/g2g-iam.pem ec2-user@52.91.243.82
$ source /home/ec2-user/cert/env/bin/activate

$ pip install jupyter







AWS Chalice - Quickstart
https://chalice.readthedocs.io/en/latest/quickstart.html

How do I create a Python 3 virtual environment with the Boto 3 library on Amazon Linux 2
https://aws.amazon.com/premiumsupport/knowledge-center/ec2-linux-python3-boto3/

[ec2-user ~]

$ yum list installed | grep -i python3

$ sudo yum install python3 -y

$ which python3
/usr/bin/python3

$ python3 -m venv cert/env
$ source ~/cert/env/bin/activate

$ which python3
~/cert/env/bin/python3

$ pip install boto3

$ python --version
Python 3.7.4


(env) [ec2-user ~]$ deactivate

$ pip install chalice
$ chalice --help

$ chalice new-project helloworld
$ cd helloworld
$ chalice deploy
Creating deployment package.
Creating IAM role: helloworld-dev
Creating lambda function: helloworld-dev
Creating Rest API
Resources deployed:
  - Lambda ARN: arn:aws:lambda:us-east-1:1234567:function:helloworld-dev
  - Rest API URL: https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/

# tests
$ curl https://imw4ml0pn4.execute-apnaws.com/api/
{"hello":"world"}

$ curl https://imw4ml0pn4.execute-apnaws.com/api/hello/g2g 
{"hello":"g2g"}

$ pip install httpie

$ http https://imw4ml0pn4.execute-apnaws.com/api/
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 17
Content-Type: application/json
Date: Wed, 12 Feb 2020 02:17:47 GMT
Via: 1.1 85fc1201a1918facbeb30836e7391661.cloudfront.net (CloudFront)
X-Amz-Cf-Id: kvMUcMcvYb77XCkQUUewzsnR5fuMuJIsXL2HeNKd9CpD96HFIOVs5g==
X-Amz-Cf-Pop: IAD89-C1
X-Amzn-Trace-Id: Root=1-5e43604b-10f848723989f2f49f67c469;Sampled=0
X-Cache: Miss from cloudfront
x-amz-apigw-id: Hwv73GSMIAMFkHg=
x-amzn-RequestId: 40b1eb94-3db9-45d4-840e-82f64e1225be

{
    "hello": "world"
}


$ http https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/cities/portland
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 14
Content-Type: application/json
Date: Wed, 12 Feb 2020 02:21:53 GMT
Via: 1.1 077b94dab77b8114aebf503be197d7d9.cloudfront.net (CloudFront)
X-Amz-Cf-Id: vnjNljE_T3ffIDAuDPwlAA2BNMjGJw7JDie2Td3VcPgvh9CWfIb8Ww==
X-Amz-Cf-Pop: IAD89-C3
X-Amzn-Trace-Id: Root=1-5e436141-77a1fdda8bbf792439ffff72;Sampled=0
X-Cache: Miss from cloudfront
x-amz-apigw-id: HwwiSFxkoAMFTzg=
x-amzn-RequestId: 8651e51d-2b1a-4c34-af30-8f570317d2fc

{
    "state": "OR"
}


$ http PUT https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/resource/foo
HTTP/1.1 200 OK
{
    "value": "foo"
}

$ http PUT https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/myview/
HTTP/1.1 200 OK
{
    "methor": "PUT"
}

$ http POST https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/myview/
HTTP/1.1 200 OK
{
    "methor": "POST"
}

$ http GET https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/objects/mykey

$ echo '{"foo": "bar"}' | http PUT https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/objects/mykey

$ http GET https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/objects/mykey


$ http https://imw4ml0pn4.execute-api.us-east-1.amazonaws.com/api/introspect?query1=value1 "X-TestHeader: Foo"
HTTP/1.1 200 OK
Connection: keep-alive
Content-Length: 1515
Content-Type: application/json
Date: Wed, 12 Feb 2020 02:52:42 GMT
Via: 1.1 c84ecfd128e1f4c41a53a2b42410f3b8.cloudfront.net (CloudFront)
X-Amz-Cf-Id: n4yd2srHN9pbdzGF9f2D1zEXLDA9se45czvP70omuEhqfKq1fb-Q2g==
X-Amz-Cf-Pop: IAD89-C3
X-Amzn-Trace-Id: Root=1-5e43687a-8965a9d2faf2871f985aaf09;Sampled=0
X-Cache: Miss from cloudfront
x-amz-apigw-id: Hw1DNHpQIAMF-pQ=
x-amzn-RequestId: b07c0074-ff35-4f8c-b47d-019595d1b9c0

{
    "context": {
        "accountId": "578247465916",
        "apiId": "imw4ml0pn4",
        "domainName": "imw4ml0pn4.execute-api.us-east-1.amazonaws.com",
        "domainPrefix": "imw4ml0pn4",
        "extendedRequestId": "Hw1DNHpQIAMF-pQ=",
        "httpMethod": "GET",
        "identity": {
            "accessKey": null,
            "accountId": null,
            "caller": null,
            "cognitoAuthenticationProvider": null,
            "cognitoAuthenticationType": null,
            "cognitoIdentityId": null,
            "cognitoIdentityPoolId": null,
            "principalOrgId": null,
            "sourceIp": "3.86.26.30",
            "user": null,
            "userAgent": "HTTPie/2.0.0",
            "userArn": null
        },
        "path": "/api/introspect",
        "protocol": "HTTP/1.1",
        "requestId": "b07c0074-ff35-4f8c-b47d-019595d1b9c0",
        "requestTime": "12/Feb/2020:02:52:42 +0000",
        "requestTimeEpoch": 1581475962848,
        "resourceId": "idt1te",
        "resourcePath": "/introspect",
        "stage": "api"
    },
    "headers": {
        "accept": "*/*",
        "accept-encoding": "gzip, deflate",
        "cloudfront-forwarded-proto": "https",
        "cloudfront-is-desktop-viewer": "true",
        "cloudfront-is-mobile-viewer": "false",
        "cloudfront-is-smarttv-viewer": "false",
        "cloudfront-is-tablet-viewer": "false",
        "cloudfront-viewer-country": "US",
        "host": "imw4ml0pn4.execute-api.us-east-1.amazonaws.com",
        "user-agent": "HTTPie/2.0.0",
        "via": "1.1 c84ecfd128e1f4c41a53a2b42410f3b8.cloudfront.net (CloudFront)",
        "x-amz-cf-id": "n4yd2srHN9pbdzGF9f2D1zEXLDA9se45czvP70omuEhqfKq1fb-Q2g==",
        "x-amzn-trace-id": "Root=1-5e43687a-8965a9d2faf2871f985aaf09",
        "x-forwarded-for": "3.86.26.30, 130.176.98.140",
        "x-forwarded-port": "443",
        "x-forwarded-proto": "https",
        "x-testheader": "Foo"
    },
    "method": "GET",
    "query_params": {
        "query1": "value1"
    },
    "stage_vars": null,
    "uri_params": null
}



