import requests

API_URL = "http://localhost:8000"

def test_login():
    print(f"Testing login at {API_URL}...")
    
    data = {
        "username": "admin@example.com",
        "password": "admin"
    }
    
    try:
        resp = requests.post(f"{API_URL}/auth/login", data=data)
        print(f"Status: {resp.status_code}")
        print(f"Response: {resp.text}")
        
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_login()
