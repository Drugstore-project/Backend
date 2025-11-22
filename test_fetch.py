import requests
import time

print("Attempting to fetch products...")
try:
    r = requests.get("http://127.0.0.1:8000/products/")
    print(f"Status Code: {r.status_code}")
    print(f"Response: {r.text}")
except Exception as e:
    print(f"Error: {e}")
