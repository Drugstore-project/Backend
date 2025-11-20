import pytest

def test_create_role(client):
    payload = {
        "name": "manager",
        "description": "Store manager"
    }
    response = client.post("/roles/", json=payload)
    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "manager"
    assert data["description"] == "Store manager"
    assert "id" in data

def test_list_roles(client):
    # Create a role first to ensure list is not empty
    payload = {
        "name": "supervisor",
        "description": "Shift supervisor"
    }
    client.post("/roles/", json=payload)

    response = client.get("/roles/")
    assert response.status_code == 200
    data = response.json()
    assert isinstance(data, list)
    assert len(data) >= 1
    found = any(r["name"] == "supervisor" for r in data)
    assert found
