import requests
import sys

def create_prod_admin():
    print("--- Create Admin User on Remote Server ---")
    print("The logs indicate that your production database (on Railway) is missing the admin user.")
    print("This script will use the public API to register the admin user.")
    print("")
    
    url = input("Please enter your deployed Backend URL (e.g. https://drugstore-backend.up.railway.app): ").strip()
    
    if not url:
        print("URL is required.")
        return
        
    # Remove trailing slash
    if url.endswith("/"):
        url = url[:-1]
        
    print(f"\nTargeting: {url}")
    
    # 1. Ensure Role Exists
    print("1. Checking 'admin' role...")
    try:
        # Try to list roles to see if we can connect
        try:
            resp = requests.get(f"{url}/roles/")
        except requests.exceptions.ConnectionError:
            print(f"ERROR: Could not connect to {url}. Please check the URL.")
            return

        if resp.status_code != 200:
            print(f"Error connecting to API: {resp.status_code} - {resp.text}")
            return
            
        roles = resp.json()
        admin_role = next((r for r in roles if r['name'] == 'admin'), None)
        
        if not admin_role:
            print("   Admin role not found. Creating...")
            resp = requests.post(f"{url}/roles/", json={"name": "admin", "description": "Administrator"})
            if resp.status_code == 200:
                admin_role = resp.json()
                print("   Admin role created.")
            else:
                print(f"   Failed to create role: {resp.text}")
                return
        else:
            print(f"   Admin role exists (ID: {admin_role['id']}).")
            
        # 2. Register User
        print("2. Registering admin@example.com...")
        payload = {
            "name": "Admin User",
            "email": "admin@example.com",
            "password": "admin",
            "role_id": admin_role['id']
        }
        
        resp = requests.post(f"{url}/auth/register", json=payload)
        if resp.status_code == 200:
            print("\nSUCCESS! Admin user created.")
            print("You can now login with:")
            print("   Email: admin@example.com")
            print("   Password: admin")
        elif resp.status_code == 400 and "Email already registered" in resp.text:
            print("\nUser already exists (unexpected given the logs).")
        else:
            print(f"\nFailed to register: {resp.status_code} - {resp.text}")
            
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    create_prod_admin()
