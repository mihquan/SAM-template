import requests
import json
import random
import time
import uuid
from datetime import datetime

API_URL = "https://9g9ndnpw3h.execute-api.us-east-1.amazonaws.com/Prod/ingest/transaction"

merchants = ["SHOP_A", "SHOP_B", "SHOP_C"]

print("🚀 Bắt đầu bơm traffic vào hệ thống...")

for i in range(300): # Gửi 50 transaction
    # Random số liệu
    merchant = random.choice(merchants)
    revenue = round(random.uniform(50.0, 200.0), 2)
    cost = round(revenue * random.uniform(0.3, 0.6), 2) # Cost chiếm 30-60%
    ad_spend = round(revenue * random.uniform(0.1, 0.3), 2) # Ads chiếm 10-30%
    
    payload = {
        "transaction_id": str(uuid.uuid4()),
        "merchant_id": merchant,
        "date": datetime.utcnow().strftime("%Y-%m-%d"),
        "revenue": revenue,
        "cost": cost,
        "ad_spend": ad_spend,
        "fees": 5.0 # Phí cố định
    }

    try:
        response = requests.post(API_URL, json=payload)
        if response.status_code == 200:
            print(f"[{i+1}/50] ✅ Sent {merchant}: Rev=${revenue} | Ads=${ad_spend}")
        else:
            print(f"[{i+1}/50] ❌ Error: {response.text}")
    except Exception as e:
        print(f"Error: {e}")

    # Nghỉ 1 xíu để biểu đồ dãn ra (không bị dồn cục)
    time.sleep(1) 

print("🎉 Hoàn tất! Hãy qua CloudWatch xem Dashboard.")