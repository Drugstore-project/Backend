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


def test_add_item_to_order():
    pass

def test_calculate_order_total():
    pass

def test_order_status_pending():
    pass

def test_order_status_paid():
    pass

def test_order_status_delivered():
    pass

def test_order_client_relation():
    pass