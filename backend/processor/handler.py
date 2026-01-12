import json
import os
import logging
from decimal import Decimal


import boto3
from botocore.exceptions import ClientError

from processor.business_logic import calculate_profit_and_margin

logger = logging.getLogger()
logger.setLevel(logging.INFO)

dynamodb = boto3.resource("dynamodb")

TRANSACTIONS_TABLE = os.environ["TRANSACTIONS_TABLE"]
DAILY_METRICS_TABLE = os.environ["DAILY_METRICS_TABLE"]

transactions_table = dynamodb.Table(TRANSACTIONS_TABLE)
daily_metrics_table = dynamodb.Table(DAILY_METRICS_TABLE)


def lambda_handler(event, context):
    for record in event["Records"]:
        tx = json.loads(record["body"])
        transaction_id = tx["transaction_id"]

        # 1️⃣ IDEMPOTENCY CHECK
        try:
            transactions_table.put_item(
                Item={
                    "transaction_id": transaction_id,
                    "merchant_id": tx["merchant_id"],
                    "date": tx["date"],
                },
                ConditionExpression="attribute_not_exists(transaction_id)",
            )
        except ClientError as e:
            if e.response["Error"]["Code"] == "ConditionalCheckFailedException":
                logger.info(f"Duplicate transaction skipped: {transaction_id}")
                continue
            else:
                raise

        # 2️⃣ BUSINESS LOGIC
        profit, margin = calculate_profit_and_margin(tx)

        # 3️⃣ UPDATE DAILY METRICS (ATOMIC)
        daily_metrics_table.update_item(
            Key={
                "merchant_id": tx["merchant_id"],
                "date": tx["date"],
            },
            UpdateExpression="""
                ADD total_revenue :r,
                    total_ad_spend :a,
                    total_fees :f,
                    total_profit :p,
                    transaction_count :c
            """,
            ExpressionAttributeValues={
                ":r": Decimal(str(tx["revenue"])),
                ":a": Decimal(str(tx["ad_spend"])),
                ":f": Decimal(str(tx["fees"])),
                ":p": Decimal(str(profit)),
                ":c": Decimal(1),

            },
        )

        logger.info(f"Processed transaction {transaction_id}")
