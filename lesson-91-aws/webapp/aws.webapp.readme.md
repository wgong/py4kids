https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/
https://aws.amazon.com/getting-started/projects/build-serverless-web-app-lambda-apigateway-s3-dynamodb-cognito/module-4/


download https://github.com/awslabs/aws-serverless-workshops/archive/master.zip to local
~/Downloads/aws/aws-serverless-workshops-master

PROBLEM: 1st attempt failed due to below error:
    An error occured when requesting your unicorn: undefined

    Access to XMLHttpRequest at 'https://3k0q7o3v90.execute-api.us-east-1.amazonaws.com/prod/ride' from origin 'http://wildrydes-wengong.s3-website-us-east-1.amazonaws.com' has been blocked by CORS policy: Response to preflight request doesn't pass access control check: No 'Access-Control-Allow-Origin' header is present on the requested resource.

FIX:  API action: Enable CORS for POST

REDO worked!

Module 1. Static Web Hosting

$ aws s3 sync s3://wildrydes-us-east-1/WebApplication/1_StaticWebHosting/website s3://wildrydes-wen-gong --region us-east-1

run cloudformation template to create stack=wildrydes-webapp-1

bucket policy
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow", 
            "Principal": "*", 
            "Action": "s3:GetObject", 
            "Resource": "arn:aws:s3:::wildrydes-wen-gong/*" 
        } 
    ] 
}

Enable CORS rule
https://docs.aws.amazon.com/AmazonS3/latest/dev/cors.html#how-do-i-enable-cors
<CORSConfiguration>
 <CORSRule>
   <AllowedOrigin>*</AllowedOrigin>
   <AllowedMethod>GET</AllowedMethod>
   <AllowedHeader>*</AllowedHeader>
  <MaxAgeSeconds>3000</MaxAgeSeconds>
 </CORSRule>
</CORSConfiguration>

static website hosting endpoint:
  http://wildrydes-wen-gong.s3-website-us-east-1.amazonaws.com
    /index.html
    /signin.html
    /register.html
    /ride.html

Module 2. User Management

user pool name: WildRydes
Pool Id:    us-east-1_SUYRSp1aN
Pool ARN:   arn:aws:cognito-idp:us-east-1:555555555555:userpool/us-east-1_SUYRSp1aN

add an app client
App client name = WildRydesWebApp
App client id = 7n27vbfpqj0c64ub22nptj7ig2
refresh token expire: 30 days

ALLOW_CUSTOM_AUTH: true
ALLOW_USER_SRP_AUTH: true
ALLOW_REFRESH_TOKEN_AUTH: true

update js/config.js

window._config = {
    cognito: {
        userPoolId: 'us-east-1_SUYRSp1aN', // e.g. us-east-2_uXboG5pAb
        userPoolClientId: '7n27vbfpqj0c64ub22nptj7ig2', // e.g. 25ddkmj4v6hfsfvruhpfi7n4hv
        region: 'us-east-1' // e.g. us-east-2
    },
    api: {
        invokeUrl: '' // e.g. https://rc7nyt4tql.execute-api.us-west-2.amazonaws.com/prod,
    }
};

$ aws s3 cp config.js s3://wildrydes-wen-gong/js/config.js


Module 3: Serverless Service Backend

DynamoDB table Rides (ARN) = arn:aws:dynamodb:us-east-1:555555555555:table/Rides

Create an IAM Role for Your Lambda function

arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "*"
        }
    ]
}

inline policy=DynamoDBWriteAccess
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Sid": "VisualEditor0",
            "Effect": "Allow",
            "Action": "dynamodb:PutItem",
            "Resource": "arn:aws:dynamodb:us-east-1:555555555555:table/Rides"
        }
    ]
}

Every Lambda function has an IAM role associated with it. This role defines what other AWS services the function is allowed to interact with. For the purposes of this workshop, you'll need to create an IAM role that grants your Lambda function permission to write logs to Amazon CloudWatch Logs and access to write items to your DynamoDB table.

Lambda function
index.js => https://github.com/aws-samples/aws-serverless-workshops/blob/master/WebApplication/3_ServerlessBackend/requestUnicorn.js

test event:
{
  "path": "/ride",
  "httpMethod": "POST",
  "headers": {
    "Accept": "*/*",
    "Authorization": "eyJraWQiOiJLTzRVMWZs",
    "content-type": "application/json; charset=UTF-8"
  },
  "queryStringParameters": null,
  "pathParameters": null,
  "requestContext": {
    "authorizer": {
      "claims": {
        "cognito:username": "the_username"
      }
    }
  },
  "body": "{\"PickupLocation\":{\"Latitude\":47.6174755835663,\"Longitude\":-122.28837066650185}}"
}

Module 4. RESTful APIs

This module will focus on the steps required to build the cloud components of the API, but if you're interested in how the browser code works that calls this API, you can inspect the ride.js file of the website. In this case the application uses jQuery's ajax() method to make the remote request.



Deploy API
stage=prod

 Invoke URL: https://7lv43wq2c0.execute-api.us-east-1.amazonaws.com/prod



update js/config.js
by adding invokeUrl: 
$ aws s3 cp config.js s3://wildrydes-wen-gong/js/config.js

verify https://wildrydes-wen-gong.s3.us-east-1.amazonaws.com/js/config.js
