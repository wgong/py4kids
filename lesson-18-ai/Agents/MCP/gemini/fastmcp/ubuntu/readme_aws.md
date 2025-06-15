# AWS Bedrock Claude 3.5 Setup Guide

## Prerequisites

1. **Install boto3**:
   ```bash
   pip install boto3
   ```

2. **AWS Account with Bedrock Access**:
   - AWS account with appropriate permissions
   - Access to Amazon Bedrock service
   - Claude 3.5 Sonnet model enabled in your region

## AWS Credentials Configuration

Choose one of these methods to configure AWS credentials:

### Method 1: AWS CLI (Recommended for Development)
```bash
# Install AWS CLI
pip install awscli

# Configure credentials
aws configure
# Enter: Access Key ID, Secret Access Key, Default region, Output format

# Test access
aws bedrock-runtime list-foundation-models --region us-east-1
```

### Method 2: Environment Variables
```bash
# Windows
set AWS_ACCESS_KEY_ID=your_access_key
set AWS_SECRET_ACCESS_KEY=your_secret_key
set AWS_DEFAULT_REGION=us-east-1

# Linux/Mac
export AWS_ACCESS_KEY_ID=your_access_key
export AWS_SECRET_ACCESS_KEY=your_secret_key
export AWS_DEFAULT_REGION=us-east-1
```

### Method 3: IAM Roles (For EC2/Lambda)
If running on AWS infrastructure, attach an IAM role with Bedrock permissions.

### Method 4: AWS SSO (For Enterprise)
```bash
# Configure SSO
aws configure sso

# Login
aws sso login
```

## Required IAM Permissions

Your AWS user/role needs these permissions:

```json
{
    "Version": "2012-10-17",
    "Statement": [
        {
            "Effect": "Allow",
            "Action": [
                "bedrock:InvokeModel",
                "bedrock:InvokeModelWithResponseStream"
            ],
            "Resource": [
                "arn:aws:bedrock:*::foundation-model/anthropic.claude-3-5-sonnet-20241022-v2:0"
            ]
        }
    ]
}
```

## Enable Claude 3.5 Sonnet in Bedrock

1. **Go to AWS Bedrock Console**:
   - Navigate to https://console.aws.amazon.com/bedrock/
   - Select your preferred region (us-east-1, us-west-2, etc.)

2. **Model Access**:
   - Click "Model access" in the left sidebar
   - Find "Anthropic" in the list
   - Request access to "Claude 3.5 Sonnet"
   - Wait for approval (usually instant for most accounts)

3. **Verify Access**:
   ```bash
   # Test if you can access the model
   aws bedrock-runtime invoke-model \
     --model-id anthropic.claude-3-5-sonnet-20241022-v2:0 \
     --body '{"anthropic_version":"bedrock-2023-05-31","max_tokens":10,"messages":[{"role":"user","content":"Hello"}]}' \
     --cli-binary-format raw-in-base64-out \
     --region us-east-1 \
     output.json
   ```

## Regional Availability

Claude 3.5 Sonnet is available in these AWS regions:
- `us-east-1` (N. Virginia)
- `us-west-2` (Oregon) 
- `eu-west-1` (Ireland)
- `ap-southeast-1` (Singapore)
- `ap-northeast-1` (Tokyo)

Update the `AWS_DEFAULT_REGION` environment variable accordingly.

## Usage in MCP Client

1. **Set the provider**:
   ```python
   LLM_PROVIDER = "bedrock"
   ```

2. **Run the client**:
   ```bash
   python mcp_client_llm.py
   ```

## Troubleshooting

### Common Issues:

1. **"NoCredentialsError"**:
   - AWS credentials not configured
   - Follow credential setup methods above

2. **"AccessDeniedException"**:
   - User doesn't have Bedrock permissions
   - Add the IAM policy above
   - Ensure Claude 3.5 access is approved

3. **"ValidationException: The model ID is invalid"**:
   - Model not available in your region
   - Check regional availability above
   - Ensure model access is approved

4. **"ThrottlingException"**:
   - Too many requests
   - Implement retry logic or slow down requests

### Debug Commands:
```bash
# Check AWS configuration
aws sts get-caller-identity

# List available models
aws bedrock list-foundation-models --region us-east-1

# Check model access
aws bedrock get-model-invocation-logging-configuration --region us-east-1
```

## Cost Considerations

Claude 3.5 Sonnet on Bedrock pricing (as of 2024):
- Input tokens: ~$3.00 per 1M tokens
- Output tokens: ~$15.00 per 1M tokens

For the MCP client usage (short queries), costs are typically minimal.

## Security Best Practices

1. **Use IAM roles** instead of access keys when possible
2. **Rotate access keys** regularly
3. **Use least privilege** - only grant necessary Bedrock permissions
4. **Enable CloudTrail** for audit logging
5. **Use VPC endpoints** for private connectivity (enterprise)

## Enterprise Features

- **VPC Endpoints**: Private connectivity without internet
- **CloudWatch Integration**: Monitoring and logging
- **AWS PrivateLink**: Secure model access
- **Compliance**: SOC, PCI DSS, HIPAA eligible