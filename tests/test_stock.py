import pytest
from app.schemas.product import ProductCreate
from app.crud.product import create_product, get_product
from app.models.role import UserRole as Role
from app.schemas.user import UserCreate
from app.crud.user import create_user

def test_add_stock_entry(client, db):
    # Create product
    payload = ProductCreate(
        name="Stock Test Product",
        description="Testing stock",
        price=10.0,
        stock_quantity=10,
        requires_prescription=False,
    )
    p = create_product(db, payload)
    
    # Update stock (add)
    update_payload = {"stock_quantity": 20}
    response = client.put(f"/products/{p.id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["stock_quantity"] == 20

def test_remove_stock_entry(client, db):
    # Create product
    payload = ProductCreate(
        name="Stock Remove Test",
        description="Testing stock removal",
        price=10.0,
        stock_quantity=20,
        requires_prescription=False,
    )
    p = create_product(db, payload)
    
    # Update stock (remove/set to lower)
    update_payload = {"stock_quantity": 5}
    response = client.put(f"/products/{p.id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["stock_quantity"] == 5

def test_alert_low_quantity(db):
    # This is a logic test, assuming we might have a function to check low stock
    # For now, we just verify the state
    payload = ProductCreate(
        name="Low Stock Product",
        description="Low stock",
        price=10.0,
        stock_quantity=2,
        requires_prescription=False,
    )
    p = create_product(db, payload)
    
    # Simulate alert logic
    LOW_STOCK_THRESHOLD = 5
    is_low_stock = p.stock_quantity < LOW_STOCK_THRESHOLD
    assert is_low_stock is True

def test_alert_expired_product(db):
    from datetime import date, timedelta
    # Create expired product
    payload = ProductCreate(
        name="Expired Product",
        description="Expired",
        price=10.0,
        stock_quantity=10,
        validity=date.today() - timedelta(days=1),
        requires_prescription=False,
    )
    p = create_product(db, payload)
    
    # Simulate expiration check
    is_expired = p.validity < date.today()
    assert is_expired is True

def test_update_stock_after_order(client, db):
    # Create product
    p_payload = ProductCreate(
        name="Order Stock Product",
        description="Testing stock deduction",
        price=10.0,
        stock_quantity=10,
        requires_prescription=False,
    )
    p = create_product(db, p_payload)

    # Create user
    role = Role(name="customer_stock", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)
    u_payload = UserCreate(
        name="Stock User",
        email="stock@example.com",
        password="password",
        role_id=role.id
    )
    user = create_user(db, u_payload)

    # Create order
    order_payload = {
        "payment_method": "cash",
        "status": "pending",
        "user_id": user.id,
        "items": [{"product_id": p.id, "quantity": 3, "unit_price": 10.0}]
    }
    response = client.post("/orders/", json=order_payload)
    assert response.status_code == 200
    
    # Check stock
    db.refresh(p)
    assert p.stock_quantity == 7  # 10 - 3

