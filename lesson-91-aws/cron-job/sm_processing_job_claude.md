# SageMaker Processing Jobs Production Deployment Guide

## Overview
SageMaker Processing Jobs provide a managed way to run data processing workloads with automatic scaling, monitoring, and integration with other AWS ML services.

## Architecture
```
EventBridge (cron) → Lambda → SageMaker Processing Job → Your Shell Script (in container)
                                     ↓
                            CloudWatch Logs & Metrics
```

## Step 1: Create Docker Container with Your Shell Script

### Dockerfile
```dockerfile
FROM amazonlinux:2

# Install system dependencies
RUN yum update -y && yum install -y \
    bash \
    curl \
    wget \
    awscli \
    python3 \
    python3-pip \
    git \
    unzip \
    tar \
    gzip \
    jq \
    && yum clean all

# Install Python packages if needed
RUN pip3 install boto3 pandas numpy

# Create processing directories (SageMaker convention)
RUN mkdir -p /opt/ml/processing/input
RUN mkdir -p /opt/ml/processing/output
RUN mkdir -p /opt/ml/processing/code

# Copy your shell script
COPY process_data.sh /opt/ml/processing/code/
RUN chmod +x /opt/ml/processing/code/process_data.sh

# Set working directory
WORKDIR /opt/ml/processing

# Set entrypoint
ENTRYPOINT ["/opt/ml/processing/code/process_data.sh"]
```

### Update Your Shell Script for SageMaker
```bash
#!/bin/bash

# SageMaker Processing Job Environment Variables
echo "Job Name: $SAGEMAKER_JOB_NAME"
echo "Region: $AWS_DEFAULT_REGION"
echo "Start Time: $(date)"

# Input and output paths (SageMaker convention)
INPUT_PATH="/opt/ml/processing/input"
OUTPUT_PATH="/opt/ml/processing/output"
CODE_PATH="/opt/ml/processing/code"

# Your data processing logic here
echo "Starting data processing..."

# Example: Download data from S3 (if not using input channels)
# aws s3 cp s3://your-bucket/input-data/ $INPUT_PATH/ --recursive

# Process your data
# python3 $CODE_PATH/data_processor.py --input $INPUT_PATH --output $OUTPUT_PATH

# Example processing commands
find $INPUT_PATH -name "*.csv" -exec echo "Processing: {}" \;
# Add your actual processing commands here

# Upload results (if not using output channels)
# aws s3 cp $OUTPUT_PATH/ s3://your-bucket/output-data/ --recursive

echo "Data processing completed at $(date)"
```

### Build and Push Docker Image
```bash
# Set variables
AWS_ACCOUNT_ID=$(aws sts get-caller-identity --query Account --output text)
AWS_REGION="us-east-1"
IMAGE_NAME="data-processor"
IMAGE_TAG="latest"

# Create ECR repository
aws ecr create-repository \
    --repository-name $IMAGE_NAME \
    --region $AWS_REGION

# Get ECR login
aws ecr get-login-password --region $AWS_REGION | \
    docker login --username AWS --password-stdin \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com

# Build image
docker build -t $IMAGE_NAME:$IMAGE_TAG .

# Tag for ECR
docker tag $IMAGE_NAME:$IMAGE_TAG \
    $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_NAME:$IMAGE_TAG

# Push to ECR
docker push $AWS_ACCOUNT_ID.dkr.ecr.$AWS_REGION.amazonaws.com/$IMAGE_NAME:$IMAGE_TAG
```

## Step 2: Create IAM Roles

### SageMaker Execution Role
```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "sagemaker.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
```

### Create Role and Policies
```bash
# Create execution role
aws iam create-role \
    --role-name SageMakerProcessingExecutionRole \
    --assume-role-policy-document file://sagemaker-trust-policy.json

# Attach basic SageMaker policy
aws iam attach-role-policy \
    --role-name SageMakerProcessingExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

# Create custom policy for your specific needs
cat > processing-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "s3:GetObject",
                "s3:PutObject",
                "s3:DeleteObject",
                "s3:ListBucket"
            ],
            "Resource": [
                "arn:aws:s3:::your-data-bucket/*",
                "arn:aws:s3:::your-data-bucket"
            ]
        },
        {
            "Effect": "Allow",
            "Action": [
                "logs:CreateLogGroup",
                "logs:CreateLogStream",
                "logs:PutLogEvents"
            ],
            "Resource": "arn:aws:logs:*:*:*"
        },
        {
            "Effect": "Allow",
            "Action": [
                "ecr:GetAuthorizationToken",
                "ecr:BatchCheckLayerAvailability",
                "ecr:GetDownloadUrlForLayer",
                "ecr:BatchGetImage"
            ],
            "Resource": "*"
        }
    ]
}
EOF

# Create and attach custom policy
aws iam create-policy \
    --policy-name SageMakerProcessingPolicy \
    --policy-document file://processing-policy.json

aws iam attach-role-policy \
    --role-name SageMakerProcessingExecutionRole \
    --policy-arn arn:aws:iam::$AWS_ACCOUNT_ID:policy/SageMakerProcessingPolicy
```

## Step 3: Create Lambda Function to Trigger Processing Jobs

### Lambda Function Code
```python
import boto3
import json
import time
from datetime import datetime

def lambda_handler(event, context):
    sagemaker_client = boto3.client('sagemaker')
    
    # Generate unique job name
    timestamp = datetime.now().strftime('%Y%m%d-%H%M%S')
    job_name = f'data-processing-{timestamp}'
    
    # Get account ID and region
    account_id = context.invoked_function_arn.split(':')[4]
    region = context.invoked_function_arn.split(':')[3]
    
    # Container image URI
    image_uri = f'{account_id}.dkr.ecr.{region}.amazonaws.com/data-processor:latest'
    
    # SageMaker execution role
    role_arn = f'arn:aws:iam::{account_id}:role/SageMakerProcessingExecutionRole'
    
    try:
        response = sagemaker_client.create_processing_job(
            ProcessingJobName=job_name,
            ProcessingResources={
                'ClusterConfig': {
                    'InstanceCount': 1,
                    'InstanceType': 'ml.t3.medium',  # Adjust based on your needs
                    'VolumeSizeInGB': 30
                }
            },
            AppSpecification={
                'ImageUri': image_uri,
                'ContainerEntrypoint': ['/opt/ml/processing/code/process_data.sh']
            },
            ProcessingInputs=[
                {
                    'InputName': 'input-data',
                    'S3Input': {
                        'S3Uri': 's3://your-data-bucket/input/',
                        'LocalPath': '/opt/ml/processing/input/',
                        'S3DataType': 'S3Prefix',
                        'S3InputMode': 'File',
                        'S3DataDistributionType': 'FullyReplicated'
                    }
                }
            ],
            ProcessingOutputs=[
                {
                    'OutputName': 'output-data',
                    'S3Output': {
                        'S3Uri': f's3://your-data-bucket/output/{job_name}/',
                        'LocalPath': '/opt/ml/processing/output/',
                        'S3UploadMode': 'EndOfJob'
                    }
                }
            ],
            RoleArn=role_arn,
            StoppingCondition={
                'MaxRuntimeInSeconds': 7200  # 2 hours max
            },
            Environment={
                'JOB_TIMESTAMP': timestamp,
                'ENVIRONMENT': 'production'
            },
            Tags=[
                {
                    'Key': 'Project',
                    'Value': 'DataProcessing'
                },
                {
                    'Key': 'Environment',
                    'Value': 'Production'
                },
                {
                    'Key': 'Owner',
                    'Value': 'DataTeam'
                }
            ]
        )
        
        print(f"Processing job started successfully: {job_name}")
        print(f"Job ARN: {response['ProcessingJobArn']}")
        
        return {
            'statusCode': 200,
            'body': json.dumps({
                'message': 'Processing job started successfully',
                'jobName': job_name,
                'jobArn': response['ProcessingJobArn']
            })
        }
        
    except Exception as e:
        print(f"Error starting processing job: {str(e)}")
        return {
            'statusCode': 500,
            'body': json.dumps(f'Error: {str(e)}')
        }
```

### Deploy Lambda Function
```bash
# Create Lambda execution role
cat > lambda-trust-policy.json << EOF
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Principal": {
                "Service": "lambda.amazonaws.com"
            },
            "Action": "sts:AssumeRole"
        }
    ]
}
EOF

aws iam create-role \
    --role-name LambdaSageMakerExecutionRole \
    --assume-role-policy-document file://lambda-trust-policy.json

# Attach policies
aws iam attach-role-policy \
    --role-name LambdaSageMakerExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/service-role/AWSLambdaBasicExecutionRole

aws iam attach-role-policy \
    --role-name LambdaSageMakerExecutionRole \
    --policy-arn arn:aws:iam::aws:policy/AmazonSageMakerFullAccess

# Package and deploy Lambda
zip lambda_function.zip lambda_function.py

aws lambda create-function \
    --function-name trigger-sagemaker-processing \
    --runtime python3.9 \
    --role arn:aws:iam::$AWS_ACCOUNT_ID:role/LambdaSageMakerExecutionRole \
    --handler lambda_function.lambda_handler \
    --zip-file fileb://lambda_function.zip \
    --timeout 60
```

## Step 4: Set Up Scheduling with EventBridge

```bash
# Create EventBridge rule
aws events put-rule \
    --name "daily-data-processing" \
    --schedule-expression "cron(0 2 * * ? *)" \
    --state ENABLED \
    --description "Run SageMaker data processing daily at 2 AM UTC"

# Add Lambda as target
aws events put-targets \
    --rule "daily-data-processing" \
    --targets "Id"="1","Arn"="arn:aws:lambda:$AWS_REGION:$AWS_ACCOUNT_ID:function:trigger-sagemaker-processing"

# Give EventBridge permission to invoke Lambda
aws lambda add-permission \
    --function-name trigger-sagemaker-processing \
    --statement-id allow-eventbridge \
    --action lambda:InvokeFunction \
    --principal events.amazonaws.com \
    --source-arn arn:aws:events:$AWS_REGION:$AWS_ACCOUNT_ID:rule/daily-data-processing
```

## Step 5: Production Deployment Extras

### 1. Infrastructure as Code (CloudFormation/CDK)

#### CloudFormation Template (partial)
```yaml
AWSTemplateFormatVersion: '2010-09-09'
Description: 'SageMaker Processing Job Infrastructure'

Parameters:
  Environment:
    Type: String
    Default: production
    AllowedValues: [dev, staging, production]
  
  ProcessingSchedule:
    Type: String
    Default: "cron(0 2 * * ? *)"
    Description: "Cron expression for processing schedule"

Resources:
  ECRRepository:
    Type: AWS::ECR::Repository
    Properties:
      RepositoryName: !Sub "${Environment}-data-processor"
      LifecyclePolicy:
        LifecyclePolicyText: |
          {
            "rules": [
              {
                "rulePriority": 1,
                "selection": {
                  "tagStatus": "untagged",
                  "countType": "sinceImagePushed",
                  "countUnit": "days",
                  "countNumber": 7
                },
                "action": {
                  "type": "expire"
                }
              }
            ]
          }

  SageMakerExecutionRole:
    Type: AWS::IAM::Role
    Properties:
      RoleName: !Sub "${Environment}-SageMakerProcessingRole"
      AssumeRolePolicyDocument:
        Version: '2012-10-17'
        Statement:
          - Effect: Allow
            Principal:
              Service: sagemaker.amazonaws.com
            Action: sts:AssumeRole
      ManagedPolicyArns:
        - arn:aws:iam::aws:policy/AmazonSageMakerFullAccess
      Policies:
        - PolicyName: ProcessingJobPolicy
          PolicyDocument:
            Version: '2012-10-17'
            Statement:
              - Effect: Allow
                Action:
                  - s3:GetObject
                  - s3:PutObject
                  - s3:ListBucket
                Resource:
                  - !Sub "${DataBucket}/*"
                  - !Ref DataBucket

  ProcessingScheduleRule:
    Type: AWS::Events::Rule
    Properties:
      Name: !Sub "${Environment}-data-processing-schedule"
      Description: "Schedule for data processing jobs"
      ScheduleExpression: !Ref ProcessingSchedule
      State: ENABLED
      Targets:
        - Arn: !GetAtt TriggerLambda.Arn
          Id: "TriggerLambdaTarget"
```

### 2. Monitoring and Alerting

#### CloudWatch Alarms
```bash
# Create alarm for failed processing jobs
aws cloudwatch put-metric-alarm \
    --alarm-name "SageMaker-Processing-Job-Failures" \
    --alarm-description "Alert when SageMaker processing jobs fail" \
    --metric-name ProcessingJobsFailed \
    --namespace AWS/SageMaker \
    --statistic Sum \
    --period 300 \
    --threshold 1 \
    --comparison-operator GreaterThanOrEqualToThreshold \
    --evaluation-periods 1 \
    --alarm-actions arn:aws:sns:$AWS_REGION:$AWS_ACCOUNT_ID:processing-alerts

# Create alarm for long-running jobs
aws cloudwatch put-metric-alarm \
    --alarm-name "SageMaker-Processing-Job-Duration" \
    --alarm-description "Alert when processing jobs run too long" \
    --metric-name ProcessingJobDuration \
    --namespace AWS/SageMaker \
    --statistic Average \
    --period 3600 \
    --threshold 5400 \
    --comparison-operator GreaterThanThreshold \
    --evaluation-periods 1 \
    --alarm-actions arn:aws:sns:$AWS_REGION:$AWS_ACCOUNT_ID:processing-alerts
```

#### Custom Metrics in Your Script
```bash
#!/bin/bash
# Add to your process_data.sh

# Function to send custom metrics
send_metric() {
    local metric_name=$1
    local value=$2
    local unit=$3
    
    aws cloudwatch put-metric-data \
        --namespace "DataProcessing/Custom" \
        --metric-data MetricName=$metric_name,Value=$value,Unit=$unit,Dimensions=JobName=$SAGEMAKER_JOB_NAME
}

# Example usage
RECORDS_PROCESSED=0
ERRORS_COUNT=0

# Your processing logic here
# ... processing files ...

# Send metrics
send_metric "RecordsProcessed" $RECORDS_PROCESSED "Count"
send_metric "ErrorsEncountered" $ERRORS_COUNT "Count"
```

### 3. Environment Management

#### Environment-specific Configurations
```python
# In your Lambda function
import os

def get_config():
    environment = os.environ.get('ENVIRONMENT', 'dev')
    
    configs = {
        'dev': {
            'instance_type': 'ml.t3.small',
            'volume_size': 10,
            'max_runtime': 1800,  # 30 minutes
            'input_bucket': 'dev-data-bucket',
            'output_bucket': 'dev-output-bucket'
        },
        'staging': {
            'instance_type': 'ml.t3.medium',
            'volume_size': 20,
            'max_runtime': 3600,  # 1 hour
            'input_bucket': 'staging-data-bucket',
            'output_bucket': 'staging-output-bucket'
        },
        'production': {
            'instance_type': 'ml.m5.large',
            'volume_size': 50,
            'max_runtime': 7200,  # 2 hours
            'input_bucket': 'prod-data-bucket',
            'output_bucket': 'prod-output-bucket'
        }
    }
    
    return configs.get(environment, configs['dev'])
```

### 4. Security Hardening

#### VPC Configuration
```python
# Add to your Lambda function
vpc_config = {
    'SecurityGroupIds': ['sg-12345678'],  # Restrict outbound access
    'SubnetIds': ['subnet-12345678', 'subnet-87654321']  # Private subnets
}

# In create_processing_job call
NetworkConfig={
    'EnableInterContainerTrafficEncryption': True,
    'EnableNetworkIsolation': True,
    'VpcConfig': {
        'SecurityGroupIds': vpc_config['SecurityGroupIds'],
        'Subnets': vpc_config['SubnetIds']
    }
}
```

#### Encryption
```python
# Add encryption to your processing job
response = sagemaker_client.create_processing_job(
    # ... other parameters ...
    ProcessingResources={
        'ClusterConfig': {
            'InstanceCount': 1,
            'InstanceType': 'ml.t3.medium',
            'VolumeSizeInGB': 30,
            'VolumeKmsKeyId': 'arn:aws:kms:region:account:key/key-id'  # Encrypt EBS volumes
        }
    }
)
```

### 5. Cost Optimization

#### Spot Instances (for non-critical workloads)
```python
ProcessingResources={
    'ClusterConfig': {
        'InstanceCount': 1,
        'InstanceType': 'ml.m5.large',
        'VolumeSizeInGB': 30,
        'InstanceType': 'ml.m5.large',
        'ManagedSpotTraining': True,  # Use spot instances
        'MaxWaitTimeInSeconds': 86400  # Wait up to 24 hours for spot capacity
    }
}
```

#### Auto-scaling Based on Data Size
```python
def determine_instance_config(input_size_gb):
    if input_size_gb < 1:
        return 'ml.t3.small', 10
    elif input_size_gb < 10:
        return 'ml.t3.medium', 20
    elif input_size_gb < 100:
        return 'ml.m5.large', 50
    else:
        return 'ml.m5.xlarge', 100

# Use in Lambda
instance_type, volume_size = determine_instance_config(estimated_data_size)
```

## Step 6: Testing and Validation

### Local Testing
```bash
# Test your Docker container locally
docker run --rm \
    -v $(pwd)/test-data:/opt/ml/processing/input \
    -v $(pwd)/test-output:/opt/ml/processing/output \
    -e AWS_DEFAULT_REGION=us-east-1 \
    data-processor:latest
```

### Integration Testing
```python
# Test script for processing job
import boto3
import time

def test_processing_job():
    sagemaker = boto3.client('sagemaker')
    
    # Submit test job
    response = sagemaker.create_processing_job(
        ProcessingJobName=f'test-job-{int(time.time())}',
        # ... other parameters
    )
    
    job_name = response['ProcessingJobArn'].split('/')[-1]
    
    # Wait for completion
    while True:
        status = sagemaker.describe_processing_job(ProcessingJobName=job_name)
        current_status = status['ProcessingJobStatus']
        
        if current_status in ['Completed', 'Failed', 'Stopped']:
            print(f"Job {job_name} finished with status: {current_status}")
            break
            
        time.sleep(30)
    
    return current_status == 'Completed'

if __name__ == "__main__":
    success = test_processing_job()
    print(f"Test {'PASSED' if success else 'FAILED'}")
```

## Step 7: Deployment Pipeline

### CI/CD with GitHub Actions (example)
```yaml
name: Deploy SageMaker Processing Job

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
    - uses: actions/checkout@v2
    
    - name: Configure AWS credentials
      uses: aws-actions/configure-aws-credentials@v1
      with:
        aws-access-key-id: ${{ secrets.AWS_ACCESS_KEY_ID }}
        aws-secret-access-key: ${{ secrets.AWS_SECRET_ACCESS_KEY }}
        aws-region: us-east-1
    
    - name: Build and push Docker image
      run: |
        aws ecr get-login-password | docker login --username AWS --password-stdin $ECR_REGISTRY
        docker build -t $IMAGE_TAG .
        docker push $IMAGE_TAG
    
    - name: Deploy Lambda function
      run: |
        zip lambda_function.zip lambda_function.py
        aws lambda update-function-code --function-name trigger-sagemaker-processing --zip-file fileb://lambda_function.zip
    
    - name: Run integration tests
      run: python test_processing_job.py
```

## Summary

### Advantages of SageMaker Processing Jobs:
- **Managed infrastructure**: No server management
- **Automatic scaling**: Scales based on your requirements
- **Built-in monitoring**: CloudWatch integration
- **Cost-effective**: Pay only for compute time used
- **Integration**: Works seamlessly with other SageMaker services
- **Security**: VPC support, encryption, IAM integration

### Production Considerations:
- **Multi-environment setup**: Dev, staging, production
- **Monitoring and alerting**: CloudWatch alarms and custom metrics
- **Security**: VPC, encryption, least privilege IAM
- **Cost optimization**: Spot instances, right-sizing
- **CI/CD pipeline**: Automated testing and deployment
- **Disaster recovery**: Cross-region backup strategies

This approach provides enterprise-grade reliability and scalability for your shell script processing workloads.