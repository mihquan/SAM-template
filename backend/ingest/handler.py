import json
import os
import uuid
from datetime import datetime, timezone

import boto3

sqs = boto3.client("sqs")
QUEUE_URL = os.environ["QUEUE_URL"]

IS_LOCAL = os.environ.get("AWS_SAM_LOCAL") == "true"

REQUIRED_FIELDS = ["merchant_id", "revenue", "ad_spend", "fees", "cost"]

# Declare shared headers so we don't have to copy-paste many times
CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,POST,GET"
}

def lambda_handler(event, context):
    try:
        body = json.loads(event["body"])
    except Exception:
        return {
            "statusCode": 400, 
            "headers": CORS_HEADERS, # headers
            "body": "Invalid JSON"
        }

    # Validate payload
    for field in REQUIRED_FIELDS:
        if field not in body:
            return {
                "statusCode": 400, 
                "headers": CORS_HEADERS, #  headers
                "body": f"Missing field: {field}"
            }

    # Enrich data
    transaction = {
        "transaction_id": str(uuid.uuid4()),
        "merchant_id": body["merchant_id"],
        "date": datetime.now(timezone.utc).strftime("%Y-%m-%d"),
        "created_at": datetime.now(timezone.utc).isoformat(),
        "revenue": float(body["revenue"]),
        "ad_spend": float(body["ad_spend"]),
        "fees": float(body["fees"]),
        "cost": float(body["cost"]),
    }

    # Push to SQS
    if not IS_LOCAL:
        sqs.send_message(
            QueueUrl=os.environ["QUEUE_URL"],
            MessageBody=json.dumps(transaction)
        )
    else:
        print("LOCAL MODE: Skipping SQS send")

    return {
        "statusCode": 200,
        "headers": CORS_HEADERS, # Dùng biến đã khai báo
        "body": json.dumps({
            "message": "Transaction received successfully",
            "id": transaction["transaction_id"]  # FIXED: Read from the transaction dict
        })
    }