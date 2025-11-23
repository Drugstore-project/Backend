import pytest
from app.models.product import Product
from app.models.order import Order
from app.models.user import User
from app.models.role import UserRole as Role
from datetime import date, timedelta

@pytest.fixture
def setup_report_data(db):
    # Create Role
    role = db.query(Role).filter_by(name="report_user").first()
    if not role:
        role = Role(name="report_user")
        db.add(role)
        db.commit()

    # Create User
    user = User(name="Report User", email="report@test.com", password_hash="hash", role_id=role.id)
    db.add(user)
    db.commit()

    # Create Products
    p1 = Product(name="Normal Med", price=10.0, stock_quantity=50, requires_prescription=False)
    p2 = Product(name="Controlled Med", price=20.0, stock_quantity=5, requires_prescription=True)
    db.add_all([p1, p2])
    db.commit()

    # Create Orders
    o1 = Order(user_id=user.id, seller_id=user.id, total_value=100.0, created_at=date.today())
    o2 = Order(user_id=user.id, seller_id=user.id, total_value=50.0, created_at=date.today() - timedelta(days=1))
    db.add_all([o1, o2])
    db.commit()
    
    # Add items to orders for Top Products test
    from app.models.order import OrderItem
    oi1 = OrderItem(order_id=o1.id, product_id=p1.id, quantity=5, unit_price=10.0)
    oi2 = OrderItem(order_id=o2.id, product_id=p2.id, quantity=2, unit_price=20.0)
    db.add_all([oi1, oi2])
    db.commit()

    return {"user": user, "products": [p1, p2], "orders": [o1, o2]}

def test_sales_report(client, setup_report_data):
    response = client.get("/reports/sales")
    assert response.status_code == 200
    data = response.json()
    assert data["total_sales"] == 150.0
    assert data["orders_count"] == 2

    # Test date filter
    today = date.today().isoformat()
    response = client.get(f"/reports/sales?start_date={today}")
    assert response.status_code == 200
    data = response.json()
    assert data["total_sales"] == 100.0
    assert data["orders_count"] == 1

def test_stock_report(client, setup_report_data):
    response = client.get("/reports/stock")
    assert response.status_code == 200
    data = response.json()
    assert len(data) >= 2
    
    # Check for low stock alert
    controlled_med = next(p for p in data if p["name"] == "Controlled Med")
    assert controlled_med["status"] == "Low Stock"
    
    normal_med = next(p for p in data if p["name"] == "Normal Med")
    assert normal_med["status"] == "OK"

def test_controlled_medications_report(client, setup_report_data):
    response = client.get("/reports/controlled-medications")
    assert response.status_code == 200
    data = response.json()
    
    # Should only contain controlled medications
    assert len(data) >= 1
    for item in data:
        assert item["requires_prescription"] is True
        assert item["name"] == "Controlled Med"

def test_analytics_report(client, setup_report_data):
    response = client.get("/reports/analytics")
    assert response.status_code == 200
    data = response.json()
    
    # Check structure
    assert "topSellers" in data
    assert "salesHistory" in data
    assert "monthlyProgress" in data
    assert "topProducts" in data
    
    # Check Top Sellers
    assert len(data["topSellers"]) > 0
    assert data["topSellers"][0]["name"] == "Report User"
    assert data["topSellers"][0]["value"] == 150.0
    
    # Check Top Products
    assert len(data["topProducts"]) > 0
    # p1 (Normal Med) sold 5 units, p2 (Controlled Med) sold 2 units
    # So p1 should be first
    assert data["topProducts"][0]["name"] == "Normal Med"
    assert data["topProducts"][0]["quantity"] == 5
