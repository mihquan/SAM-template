import json
import boto3
import os

cw = boto3.client('cloudwatch')
ALARM_NAME = os.environ.get('ALARM_NAME') 


CORS_HEADERS = {
    "Access-Control-Allow-Origin": "*",
    "Access-Control-Allow-Headers": "Content-Type",
    "Access-Control-Allow-Methods": "OPTIONS,GET"
}

def lambda_handler(event, context):
    try:

        if not ALARM_NAME:
            return {
                "statusCode": 200,
                "headers": CORS_HEADERS,
                "body": json.dumps({"status": "OK", "message": "Config Warning: Missing ALARM_NAME"})
            }

        # Call CloudWatch to check the alarm health
        response = cw.describe_alarms(AlarmNames=[ALARM_NAME])
        
        # Default is OK
        status = "OK"
        message = "System is operating normally."
        
        # Kiểm tra danh sách MetricAlarms trả về
        if response['MetricAlarms']:
            state = response['MetricAlarms'][0]['StateValue']
            if state == 'ALARM':
                status = "DANGER"
                message = "ALERT: Profit is unusually high (>120)!"
            elif state == 'INSUFFICIENT_DATA':
                status = "WARNING"
                message = "Waiting for data..."
        
        return {
            "statusCode": 200,
            "headers": CORS_HEADERS,
            "body": json.dumps({
                "status": status,  # OK, DANGER, hoặc WARNING
                "message": message
            })
        }

    except Exception as e:
        return {
            "statusCode": 500,
            "headers": CORS_HEADERS,
            "body": json.dumps({"error": str(e)})
        }