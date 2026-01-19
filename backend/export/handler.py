import os
import csv
import io
import boto3
import json
from datetime import datetime
from decimal import Decimal  # Import additionally to check type

dynamodb = boto3.resource("dynamodb")
s3 = boto3.client("s3")

TABLE_NAME = os.environ["DAILY_METRICS_TABLE"]
BUCKET = os.environ["EXPORT_BUCKET"]
PREFIX = os.environ.get("EXPORT_PREFIX", "exports/")

CSV_FIELDS = [
    "merchant_id", "date",
    "total_revenue", "total_cost", "total_ad_spend", "total_fees",
    "total_profit", "transaction_count"
]

def _scan_all_items(table):
    items = []
    resp = table.scan()
    items.extend(resp.get("Items", []))
    while "LastEvaluatedKey" in resp:
        resp = table.scan(ExclusiveStartKey=resp["LastEvaluatedKey"])
        items.extend(resp.get("Items", []))
    return items

def handler(event, context):
    try:
        table = dynamodb.Table(TABLE_NAME)
        items = _scan_all_items(table)

        # Sort: merchant_id tăng dần, date giảm dần (mới nhất lên đầu)
        items.sort(key=lambda x: (x.get("merchant_id", ""), x.get("date", "")), reverse=True)

        buf = io.StringIO()
        writer = csv.DictWriter(buf, fieldnames=CSV_FIELDS)
        writer.writeheader()

        for it in items:
            row = {}
            for k in CSV_FIELDS:
                val = it.get(k, "")
                # Convert Decimal to float so the CSV looks nicer
                if isinstance(val, Decimal):
                    row[k] = float(val)
                else:
                    row[k] = val
            writer.writerow(row)

        csv_bytes = buf.getvalue().encode("utf-8")
        timestamp = datetime.utcnow().strftime("%Y%m%d_%H%M%S")
        
        # Key file
        key_latest = f"{PREFIX}daily_metrics_latest.csv"
        key_versioned = f"{PREFIX}daily_metrics_{timestamp}.csv"

        print(f"Uploading to s3://{BUCKET}/{key_latest}")

        # Upload
        s3.put_object(Bucket=BUCKET, Key=key_latest, Body=csv_bytes, ContentType="text/csv")
        s3.put_object(Bucket=BUCKET, Key=key_versioned, Body=csv_bytes, ContentType="text/csv")

        return {
            "statusCode": 200,
            "body": json.dumps({
                "message": "Export successful",
                "exported_rows": len(items),
                "s3_path": f"s3://{BUCKET}/{key_latest}"
            })
        }
    except Exception as e:
        print(e)
        return {"statusCode": 500, "body": str(e)}