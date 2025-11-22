import requests
import json

url = "http://127.0.0.1:8000/orders/"
payload = {
    "user_id": 1,
    "payment_method": "cash",
    "status": "paid",
    "items": [
        {
            "product_id": 1,
            "quantity": 1,
            "unit_price": 10.0
        }
    ]
}

try:
    response = requests.post(url, json=payload)
    print(f"Status Code: {response.status_code}")
    print(f"Response Body: {response.text}")
except Exception as e:
    print(f"Error: {e}")
