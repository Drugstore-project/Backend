import pytest

def test_create_order(client):
    payload = {
        "payment_method": "pix",
        "status": "pending",
        "user_id": 1,
        "items": []
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["payment_method"] == "pix"
    assert data["status"] == "pending"

def test_add_item_to_order(client):
    # First, create an order
    order_payload = {
        "payment_method": "credit_card",
        "status": "pending",
        "user_id": 1,
        "items": []
    }
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 200
    order_data = order_response.json()
    order_id = order_data["id"]

    # Now, add an item to the created order
    item_payload = {
        "product_id": 1,
        "quantity": 2,
        "price": 19.99
    }
    item_response = client.post(f"/orders/{order_id}/items/", json=item_payload)
    assert item_response.status_code == 200
    item_data = item_response.json()
    assert item_data["product_id"] == 1
    assert item_data["quantity"] == 2
    assert item_data["price"] == 19.99

def test_calculate_order_total(client):
    # Create an order
    order_payload = {
        "payment_method": "debit_card",
        "status": "pending",
        "user_id": 1,
        "items": []
    }
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 200
    order_data = order_response.json()
    order_id = order_data["id"]

    # Add items to the order
    items = [
        {"product_id": 1, "quantity": 1, "price": 10.00},
        {"product_id": 2, "quantity": 2, "price": 15.00}
    ]
    for item in items:
        item_response = client.post(f"/orders/{order_id}/items/", json=item)
        assert item_response.status_code == 200

    # Retrieve the order and check total
    final_order_response = client.get(f"/orders/{order_id}/")
    assert final_order_response.status_code == 200
    final_order_data = final_order_response.json()
    assert final_order_data["total"] == 40.00  # 10 + (2 * 15)

def test_order_status_pending(client):
    # Create an order with pending status
    payload = {
        "payment_method": "pix",
        "status": "pending",
        "user_id": 1,
        "items": []
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"

def test_order_status_paid(client):
    # Create an order with pending status
    order_payload = {
        "payment_method": "credit_card",
        "status": "pending",
        "user_id": 1,
        "items": []
    }
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 200
    order_data = order_response.json()
    order_id = order_data["id"]

    # Update the order status to paid
    update_payload = {
        "status": "paid"
    }
    update_response = client.put(f"/orders/{order_id}/", json=update_payload)
    assert update_response.status_code == 200
    updated_order_data = update_response.json()
    assert updated_order_data["status"] == "paid"

def test_order_status_cancelled(client):
    # Create an order with pending status
    order_payload = {
        "payment_method": "debit_card",
        "status": "pending",
        "user_id": 1,
        "items": []
    }
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 200
    order_data = order_response.json()
    order_id = order_data["id"]

    # Update the order status to cancelled
    update_payload = {
        "status": "cancelled"
    }
    update_response = client.put(f"/orders/{order_id}/", json=update_payload)
    assert update_response.status_code == 200
    updated_order_data = update_response.json()
    assert updated_order_data["status"] == "cancelled"

