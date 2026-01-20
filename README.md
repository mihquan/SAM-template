# AWS SAM Teamplate:
## 1. Prerequisites
* [AWS CLI](https://aws.amazon.com/cli/)
* [AWS SAM CLI](https://docs.aws.amazon.com/serverless-application-model/latest/developerguide/serverless-sam-cli-install.html)
* [Docker](https://www.docker.com/get-started/)

```bash
aws --version
sam --version
docker --version

aws configure
```

## 2. Initialize and Build
Prepare your deployment artifacts and install dependencies:
```bash
sam validate
sam build
```

Deploy AWS SAM application for the first time:
```bash
sam deploy --guided --stack-name true-profit-mvp --region us-east-1 --capabilities CAPABILITY_IAM --confirm-changeset
```

Invoke transaction function for verification:
```bash
Invoke-RestMethod -Method Post -Uri "<IngestionQueueUrl>" -ContentType "application/json" -Body '{"merchant_id":"M123","revenue":150.00,"ad_spend":10.00,"fees":2.50,"cost":80.00}'
```

test GitHub Actions pipeline