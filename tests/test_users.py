import pytest
from app.models.role import UserRole as Role
from app.schemas.user import UserCreate
from app.crud.user import create_user

@pytest.fixture
def setup_role(db):
    role = Role(name="customer_users_test", description="Customer role for users test")
    db.add(role)
    db.commit()
    db.refresh(role)
    return role

def test_create_user_endpoint(client, db, setup_role):
    role = setup_role
    payload = {
        "name": "Test User Create",
        "email": "create_user@example.com",
        "password": "password123",
        "role_id": role.id,
        "cpf": "123.456.789-00",
        "phone": "(11) 99999-9999",
        "address": "Rua Teste, 123"
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["email"] == "create_user@example.com"
    assert data["name"] == "Test User Create"
    assert data["cpf"] == "123.456.789-00"
    assert data["phone"] == "(11) 99999-9999"
    assert data["address"] == "Rua Teste, 123"
    assert "id" in data

def test_list_users_endpoint(client, db, setup_role):
    role = setup_role
    # Create a user first
    user_payload = UserCreate(
        name="List User",
        email="list_user@example.com",
        password="password123",
        role_id=role.id
    )
    create_user(db, user_payload)

    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    # Check if our user is in the list
    found = any(u["email"] == "list_user@example.com" for u in data)
    assert found

def test_get_user_endpoint(client, db, setup_role):
    role = setup_role
    user_payload = UserCreate(
        name="Get User",
        email="get_user@example.com",
        password="password123",
        role_id=role.id
    )
    user = create_user(db, user_payload)

    response = client.get(f"/users/{user.id}")
    assert response.status_code == 200
    data = response.json()
    assert data["id"] == user.id
    assert data["email"] == "get_user@example.com"

def test_update_user_endpoint(client, db, setup_role):
    role = setup_role
    user_payload = UserCreate(
        name="Update User",
        email="update_user@example.com",
        password="password123",
        role_id=role.id
    )
    user = create_user(db, user_payload)

    update_payload = {
        "name": "Updated Name",
        "email": "updated_email@example.com",
        "cpf": "000.000.000-00",
        "phone": "(00) 00000-0000",
        "address": "Rua Atualizada, 000"
    }
    response = client.put(f"/users/{user.id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Updated Name"
    assert data["email"] == "updated_email@example.com"
    assert data["cpf"] == "000.000.000-00"
    assert data["phone"] == "(00) 00000-0000"
    assert data["address"] == "Rua Atualizada, 000"

def test_delete_user_endpoint(client, db, setup_role):
    role = setup_role
    user_payload = UserCreate(
        name="Delete User",
        email="delete_user@example.com",
        password="password123",
        role_id=role.id
    )
    user = create_user(db, user_payload)

    response = client.delete(f"/users/{user.id}")
    assert response.status_code == 200
    assert response.json()["detail"] == "User deleted"

    # Verify deletion
    get_response = client.get(f"/users/{user.id}")
    assert get_response.status_code == 404

