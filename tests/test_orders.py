import pytest
from app.models.order import OrderItem 
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.models.role import UserRole as Role 
from app.schemas.product import ProductCreate
from app.crud.product import create_product, list_products

@pytest.mark.parametrize(
        "payment_method, items", 
        [ ("pix",[] ),
           ("credit_card", []),
           ("debit_card", [{"product_id" : 1, "quantity" : 100, "unit_price" : 1}])])
def test_create_order(db,client,payment_method, items):
    role = Role(name="customer", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)

    payload = UserCreate(
        name="Test User",
        email="test@example.com",
        password="password123",
        role_id=role.id,
    )
    user = create_user(db, payload)
    payload = {
        "payment_method": payment_method,
        "status": "pending",
        "user_id": user.id,
        "items": items
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["payment_method"] == payment_method
    assert data["status"] == "pending"



# def test_add_item_to_order(client, db):
#     # First, create an order
#     order_payload = {
#         "payment_method": "credit_card",
#         "status": "pending",
#         "user_id": 1,
#         "items": ["ibuprofeno"]
#     }
#     order_response = client.post("/orders/", json=order_payload)
#     assert order_response.status_code == 200
#     order_data = order_response.json()
#     order_id = order_data["id"]

#     # Now, add an item to the created order
#     order_item = db.query(OrderItem).filter_by(order_id=order_id)
    
    # item_payload = {
    #     "product_id": 1,
    #     "quantity": 2,
    #     "price": 19.99
    # }
    # item_response = client.post(f"/orders/{order_id}/items/", json=item_payload)
    # assert item_response.status_code == 200
    # item_data = item_response.json()
    # assert item_data["product_id"] == 1
    # assert item_data["quantity"] == 2
    # assert item_data["price"] == 19.99


def test_calculate_order_total(db,client):
    role = Role(name="customer", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)

    payload = UserCreate(
        name="Test User",
        email="test@example.com",
        password="password123",
        role_id=role.id,
    )
    user = create_user(db, payload)
    
    payload = ProductCreate(
        name="Aspirin",
        description="Pain reliever",
        price=9.99,
        stock_quantity=10,
        requires_prescription=False,
    )
    p = create_product(db, payload)
    # Create an order
    order_payload = {
        "payment_method": "debit_card",
        "status": "pending",
        "user_id": user.id,
        "items": [ {"product_id": p.id, "quantity": 1, "unit_price": float(p.price) } ]
    }
    order_response = client.post("/orders/", json=order_payload)
    assert order_response.status_code == 200
    order_data = order_response.json()
    assert order_data["total_value"] == 9.99
    order_id = order_data["id"]

    # # Add items to the order
    # items = [
    #     {"product_id": 1, "quantity": 1, "price": 10.00},
    #     {"product_id": 2, "quantity": 2, "price": 15.00}
    # ]
    # for item in items:
    #     item_response = client.post(f"/orders/{order_id}/items/", json=item)
    #     assert item_response.status_code == 200

    # Retrieve the order and check total
    # final_order_response = client.get(f"/orders/{order_id}/")
    # assert final_order_response.status_code == 200
    # final_order_data = final_order_response.json()
    # assert final_order_data["total"] == 40.00  # 10 + (2 * 15)

def test_order_status_pending(db, client):
    # Create user
    role = Role(name="customer_pending", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)

    user_payload = UserCreate(
        name="Test User Pending",
        email="pending@example.com",
        password="password123",
        role_id=role.id,
    )
    user = create_user(db, user_payload)

    # Create an order with pending status
    payload = {
        "payment_method": "pix",
        "status": "pending",
        "user_id": user.id,
        "items": []
    }
    response = client.post("/orders/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["status"] == "pending"

def test_order_status_paid(db, client):
    # Create user
    role = Role(name="customer_paid", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)

    user_payload = UserCreate(
        name="Test User Paid",
        email="paid@example.com",
        password="password123",
        role_id=role.id,
    )
    user = create_user(db, user_payload)

    # Create an order with pending status
    order_payload = {
        "payment_method": "credit_card",
        "status": "pending",
        "user_id": user.id,
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

def test_order_status_cancelled(db, client):
    # Create user
    role = Role(name="customer_cancelled", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)

    user_payload = UserCreate(
        name="Test User Cancelled",
        email="cancelled@example.com",
        password="password123",
        role_id=role.id,
    )
    user = create_user(db, user_payload)

    # Create an order with pending status
    order_payload = {
        "payment_method": "debit_card",
        "status": "pending",
        "user_id": user.id,
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

