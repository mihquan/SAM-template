import requests
import json
import random
import time
import uuid
from datetime import datetime


#IMPORTANT NOTE: CHANGE THE API URL ACCORING TO THE TIME YOU RECIEVE EACH ONE
API_URL = "https://p060sgpky2.execute-api.us-east-1.amazonaws.com/Prod/ingest/transaction" 

merchants = ["SHOP_A", "SHOP_B", "SHOP_C"]

print("🚀 Starting to pump traffic into the system...")

for i in range(300):  # Send 300 transactions
    # Randomize metrics
    merchant = random.choice(merchants)
    revenue = round(random.uniform(50.0, 200.0), 2)
    cost = round(revenue * random.uniform(0.3, 0.6), 2)      # Cost is 30–60%
    ad_spend = round(revenue * random.uniform(0.1, 0.3), 2)  # Ads are 10–30%

    payload = {
        "transaction_id": str(uuid.uuid4()),
        "merchant_id": merchant,
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "revenue": revenue,
        "cost": cost,
        "ad_spend": ad_spend,
        "fees": 5.0  # Fixed fee
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"[{i+1}/300] ✅ Sent {merchant}: Rev=${revenue} | Ads=${ad_spend}")
        else:
            print(f"[{i+1}/300] ❌ Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Sleep a bit so the chart spreads out (not clustered)
    time.sleep(1)

print("🎉 Done! Go to CloudWatch to view the Dashboard.")
