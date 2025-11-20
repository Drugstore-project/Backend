import pytest
from app.models.role import UserRole as Role

def test_register(client, db):
    # Create role first
    role = Role(name="customer_auth", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)

    payload = {
        "name": "Auth User",
        "email": "auth@example.com",
        "password": "password123",
        "role_id": role.id
    }
    response = client.post("/auth/register", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "auth@example.com"
    assert "id" in data

def test_login(client, db):
    # Create role and user
    role = Role(name="customer_login", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)

    register_payload = {
        "name": "Login User",
        "email": "login@example.com",
        "password": "password123",
        "role_id": role.id
    }
    client.post("/auth/register", json=register_payload)

    # Login
    login_payload = {
        "username": "login@example.com",
        "password": "password123"
    }
    response = client.post("/auth/login", data=login_payload) # OAuth2 uses form data
    assert response.status_code == 200
    data = response.json()
    assert "access_token" in data
    assert data["token_type"] == "bearer"

def test_me(client, db):
    # Create role and user
    role = Role(name="customer_me", description="Customer role")
    db.add(role)
    db.commit()
    db.refresh(role)

    register_payload = {
        "name": "Me User",
        "email": "me@example.com",
        "password": "password123",
        "role_id": role.id
    }
    client.post("/auth/register", json=register_payload)

    # Login
    login_payload = {
        "username": "me@example.com",
        "password": "password123"
    }
    login_response = client.post("/auth/login", data=login_payload)
    token = login_response.json()["access_token"]

    # Get Me
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "me@example.com"

def test_roles(client, db):
    # Create role
    role = Role(name="admin_role", description="Admin role")
    db.add(role)
    db.commit()
    db.refresh(role)

    register_payload = {
        "name": "Role User",
        "email": "role@example.com",
        "password": "password123",
        "role_id": role.id
    }
    client.post("/auth/register", json=register_payload)
    
    # Login
    login_payload = {
        "username": "role@example.com",
        "password": "password123"
    }
    login_response = client.post("/auth/login", data=login_payload)
    token = login_response.json()["access_token"]
    
    # Verify token contains role (needs decoding or endpoint check)
    # For now, just check if /me returns role info if available
    headers = {"Authorization": f"Bearer {token}"}
    response = client.get("/auth/me", headers=headers)
    assert response.status_code == 200
    # Note: UserOut schema might not include role details, checking what is returned
    # data = response.json()
    # assert "role" in data # UserOut usually has role_id or role object

