import os
import json
import boto3
from decimal import Decimal 

dynamodb = boto3.resource("dynamodb")
table = dynamodb.Table(os.environ["DAILY_METRICS_TABLE"])


class DecimalEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, Decimal):
            return float(obj) 
        return super(DecimalEncoder, self).default(obj)

def lambda_handler(event, context):
    params = event.get("queryStringParameters") or {}
    merchant_id = params.get("merchant_id")

    if not merchant_id:
        return {"statusCode": 400, "body": "merchant_id is required"}

    response = table.query(
        KeyConditionExpression="merchant_id = :m",
        ExpressionAttributeValues={":m": merchant_id},
    )

    return {
        "statusCode": 200,
        "body": json.dumps(response.get("Items", []), cls=DecimalEncoder),
    }