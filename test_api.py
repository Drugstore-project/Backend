import requests
import json

API_URL = "http://127.0.0.1:8000"

def test_create_and_list():
    # 1. List existing
    print("Listing products before creation...")
    try:
        r = requests.get(f"{API_URL}/products/")
        if r.status_code != 200:
            print(f"Failed to list products: {r.status_code} {r.text}")
            return
        products = r.json()
        print(f"Found {len(products)} products.")
        initial_count = len(products)
    except Exception as e:
        print(f"Error connecting to API: {e}")
        return

    # 2. Create new product
    print("Creating new product...")
    payload = {
        "name": "API Test Product",
        "price": 15.50,
        "stock_quantity": 50,
        "min_stock_level": 5,
        "barcode": "API123456",
        "validity": "2026-01-01",
        "stripe": "over-the-counter",
        "category": "analgesics"
    }
    
    try:
        r = requests.post(f"{API_URL}/products/", json=payload)
        if r.status_code == 200:
            print("Product created successfully.")
            new_product = r.json()
            print(f"New Product ID: {new_product['id']}")
        else:
            print(f"Failed to create product: {r.status_code} {r.text}")
            # If it fails because barcode exists, try to delete it first or use random barcode
            if "already registered" in r.text or "IntegrityError" in r.text:
                print("Product might already exist.")
    except Exception as e:
        print(f"Error creating product: {e}")
        return

    # 3. List again
    print("Listing products after creation...")
    r = requests.get(f"{API_URL}/products/")
    products = r.json()
    print(f"Found {len(products)} products.")
    
    # Check if new product is in the list
    found = False
    for p in products:
        if p['name'] == "API Test Product":
            found = True
            print(f"Found created product: {p}")
            break
    
    if not found:
        print("ERROR: Created product NOT found in the list!")
    else:
        print("SUCCESS: Created product found in the list.")
        
    # 4. Delete the product
    print(f"Deleting product {new_product['id']}...")
    try:
        r = requests.delete(f"{API_URL}/products/{new_product['id']}")
        if r.status_code == 200:
            print("Product deleted successfully.")
        else:
            print(f"Failed to delete product: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Error deleting product: {e}")

if __name__ == "__main__":
    test_create_and_list()
