import pytest
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.user import User
from app.models.role import UserRole as Role

@pytest.fixture
def setup_data(db):
    # Create Role
    role = db.query(Role).filter_by(name="client").first()
    if not role:
        role = Role(name="client")
        db.add(role)
        db.commit()

    # Create User
    user = User(name="Test User Presc", email="presc@test.com", password_hash="hashedpassword", role_id=role.id)
    db.add(user)
    db.commit()

    # Create Product
    product = Product(name="Prescription Drug", price=50.0, stock_quantity=10, requires_prescription=True)
    db.add(product)
    db.commit()

    # Create Order
    order = Order(user_id=user.id, total_value=50.0)
    db.add(order)
    db.commit()

    # Create OrderItem
    order_item = OrderItem(order_id=order.id, product_id=product.id, quantity=1, unit_price=50.0)
    db.add(order_item)
    db.commit()
    db.refresh(order_item)
    
    return order_item

def test_upload_prescription_file(client, setup_data):
    order_item = setup_data
    
    # Create a dummy file
    file_content = b"fake prescription content"
    files = {"file": ("prescription.pdf", file_content, "application/pdf")}
    data = {
        "order_item_id": order_item.id,
        "doctor_name": "Dr. House",
        "crm": "12345"
    }
    
    response = client.post("/prescriptions/", data=data, files=files)
    assert response.status_code == 200
    json_data = response.json()
    assert json_data["doctor_name"] == "Dr. House"
    assert json_data["crm"] == "12345"
    assert "file_path" in json_data

def test_validate_crm(client):
    response = client.post("/prescriptions/validate-crm", data={"crm": "12345"})
    assert response.status_code == 200
    assert response.json()["valid"] is True

    response = client.post("/prescriptions/validate-crm", data={"crm": "123"})
    assert response.status_code == 400

def test_attach_prescription_to_order_item(client, setup_data):
    # This is essentially covered by upload, but let's verify the DB state or try to attach again
    order_item = setup_data
    
    file_content = b"fake prescription content"
    files = {"file": ("prescription.pdf", file_content, "application/pdf")}
    data = {
        "order_item_id": order_item.id,
        "doctor_name": "Dr. Strange",
        "crm": "54321"
    }
    
    response = client.post("/prescriptions/", data=data, files=files)
    assert response.status_code == 200
    
    # Try to attach again to same item
    response = client.post("/prescriptions/", data=data, files=files)
    assert response.status_code == 400 # Already exists

def test_invalid_prescription_file(client, setup_data):
    # Test with missing file or invalid data
    order_item = setup_data
    
    data = {
        "order_item_id": order_item.id,
        "doctor_name": "Dr. Who",
        "crm": "99999"
    }
    # Missing file
    response = client.post("/prescriptions/", data=data)
    assert response.status_code == 422 # Validation error for missing field
