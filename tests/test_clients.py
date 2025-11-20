import pytest
from app.models.role import UserRole as Role

@pytest.fixture
def setup_client_role(db):
    role = db.query(Role).filter_by(name="client").first()
    if not role:
        role = Role(name="client", description="Client role")
        db.add(role)
        db.commit()
        db.refresh(role)
    return role

def test_create_client(client, db, setup_client_role):
    role = setup_client_role
    payload = {
        "name": "Joao Client",
        "email": "joao.client@example.com",
        "password": "password123",
        "role_id": role.id
    }
    response = client.post("/users/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Joao Client"
    assert data["email"] == "joao.client@example.com"
    assert data["role_id"] == role.id

def test_get_clients(client, db, setup_client_role):
    # This assumes /users/ returns all users. 
    # If there was a filter for clients, we would test that.
    # For now, just check if the created client is in the list.
    role = setup_client_role
    payload = {
        "name": "Maria Client",
        "email": "maria.client@example.com",
        "password": "password123",
        "role_id": role.id
    }
    client.post("/users/", json=payload)
    
    response = client.get("/users/")
    assert response.status_code == 200
    data = response.json()
    found = any(u["email"] == "maria.client@example.com" for u in data)
    assert found

def test_update_client(client, db, setup_client_role):
    role = setup_client_role
    payload = {
        "name": "Pedro Client",
        "email": "pedro.client@example.com",
        "password": "password123",
        "role_id": role.id
    }
    create_res = client.post("/users/", json=payload)
    user_id = create_res.json()["id"]
    
    update_payload = {
        "name": "Pedro Updated",
        "email": "pedro.updated@example.com"
    }
    response = client.put(f"/users/{user_id}", json=update_payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "Pedro Updated"
    assert data["email"] == "pedro.updated@example.com"

def test_delete_client(client, db, setup_client_role):
    role = setup_client_role
    payload = {
        "name": "Ana Client",
        "email": "ana.client@example.com",
        "password": "password123",
        "role_id": role.id
    }
    create_res = client.post("/users/", json=payload)
    user_id = create_res.json()["id"]
    
    response = client.delete(f"/users/{user_id}")
    assert response.status_code == 200
    
    get_res = client.get(f"/users/{user_id}")
    assert get_res.status_code == 404