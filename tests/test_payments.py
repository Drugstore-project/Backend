import pytest
from app.models.role import UserRole as Role
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.schemas.product import ProductCreate
from app.crud.product import create_product

@pytest.fixture
def setup_order(db, client):
    # Create role and user
    role = Role(name="customer_payment", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)
    user = create_user(db, UserCreate(name="Payment User", email="payment@example.com", password="password123", role_id=role.id))
    
    # Create product
    p = create_product(db, ProductCreate(name="P1", price=10.0, stock_quantity=100))
    
    # Create order
    order_payload = {
        "payment_method": "pending",
        "status": "pending",
        "user_id": user.id,
        "items": [{"product_id": p.id, "quantity": 1, "unit_price": 10.0}]
    }
    response = client.post("/orders/", json=order_payload)
    return response.json()

def test_create_payment(client, setup_order):
    order = setup_order
    payload = {
        "order_id": order["id"],
        "type": "pix",
        "amount": 10.0
    }
    response = client.post("/payments/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["type"] == "pix"
    assert data["amount"] == 10.0
    assert data["order_id"] == order["id"]

def test_payment_pix(client, setup_order):
    order = setup_order
    payload = {
        "order_id": order["id"],
        "type": "pix",
        "amount": 10.0
    }
    response = client.post("/payments/", json=payload)
    assert response.status_code == 200
    assert response.json()["type"] == "pix"

def test_payment_card(client, setup_order):
    order = setup_order
    payload = {
        "order_id": order["id"],
        "type": "credit_card",
        "amount": 10.0
    }
    response = client.post("/payments/", json=payload)
    assert response.status_code == 200
    assert response.json()["type"] == "credit_card"

def test_payment_boleto(client, setup_order):
    order = setup_order
    payload = {
        "order_id": order["id"],
        "type": "boleto",
        "amount": 10.0
    }
    response = client.post("/payments/", json=payload)
    assert response.status_code == 200
    assert response.json()["type"] == "boleto"

def test_upload_invoice(client, setup_order):
    # Since invoice_file is just a string in schema, we test passing a string
    order = setup_order
    payload = {
        "order_id": order["id"],
        "type": "pix",
        "amount": 10.0,
        "invoice_file": "path/to/invoice.pdf"
    }
    response = client.post("/payments/", json=payload)
    assert response.status_code == 200
    assert response.json()["invoice_file"] == "path/to/invoice.pdf"

def test_order_payment_relation(client, setup_order):
    order = setup_order
    payload = {
        "order_id": order["id"],
        "type": "pix",
        "amount": 10.0
    }
    response = client.post("/payments/", json=payload)
    assert response.status_code == 200
    
    # Verify we can retrieve payment by id
    payment_id = response.json()["id"]
    get_response = client.get(f"/payments/{payment_id}")
    assert get_response.status_code == 200
    assert get_response.json()["order_id"] == order["id"]

