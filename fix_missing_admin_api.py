import requests
import json

API_URL = "http://localhost:8000"

def fix_missing_admin():
    print(f"Checking API at {API_URL}...")
    
    # 1. Check Roles
    try:
        resp = requests.get(f"{API_URL}/roles/")
        if resp.status_code != 200:
            print(f"Failed to list roles: {resp.status_code} {resp.text}")
            return
        
        roles = resp.json()
        print(f"Found {len(roles)} roles.")
        
        admin_role = next((r for r in roles if r["name"] == "admin"), None)
        if not admin_role:
            print("Admin role not found via API. Attempting to create...")
            # Create admin role
            resp = requests.post(f"{API_URL}/roles/", json={"name": "admin", "description": "Administrator"})
            if resp.status_code == 200:
                admin_role = resp.json()
                print("Admin role created.")
            else:
                print(f"Failed to create admin role: {resp.text}")
                return
        else:
            print(f"Admin role exists (ID: {admin_role['id']}).")
            
        # 2. Try to Register Admin
        print("Attempting to register admin user...")
        payload = {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "admin",
            "role_id": admin_role['id']
        }
        
        resp = requests.post(f"{API_URL}/auth/register", json=payload)
        if resp.status_code == 200:
            print("SUCCESS: Admin user registered via API.")
        elif resp.status_code == 400 and "Email already registered" in resp.text:
            print("User already exists according to API (but login failed?).")
        else:
            print(f"Failed to register admin: {resp.status_code} {resp.text}")

    except Exception as e:
        print(f"Connection error: {e}")

if __name__ == "__main__":
    fix_missing_admin()
