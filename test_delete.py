import requests

API_URL = "http://127.0.0.1:8000"

def delete_product(product_id):
    print(f"Deleting product {product_id}...")
    try:
        r = requests.delete(f"{API_URL}/products/{product_id}")
        if r.status_code == 200:
            print("Product deleted successfully.")
        else:
            print(f"Failed to delete product: {r.status_code} {r.text}")
    except Exception as e:
        print(f"Error deleting product: {e}")

if __name__ == "__main__":
    delete_product(17)
