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

sam local start-api

Invoke-RestMethod -Method Post -Uri "http://127.0.0.1:3000/ingest" -ContentType "application/json" -Body '{"merchant_id":"M123","order_id":"ORD-001","amount":150.00}'
sam deploy --guided
```