import pytest
from sqlalchemy.exc import IntegrityError

def test_create_role(client, db):
    # Clean up any existing role with the same name to avoid unique constraint violation
    # This is needed because other tests might have created this role and the transaction rollback
    # might not have cleaned it up if it was committed in the app code (which uses a different session if not properly overridden)
    # However, with our conftest setup, the client uses the same session.
    # But let's be safe and check/delete.
    from app.models.role import UserRole
    existing = db.query(UserRole).filter(UserRole.name == "manager").first()
    if existing:
        db.delete(existing)
        db.commit()

    payload = {
        "name": "manager",
        "description": "Store manager"
    }
    response = client.post("/roles/", json=payload)
    
    # If it fails with 500, it might be an integrity error not handled
    if response.status_code != 200:
        print(f"Error creating role: {response.text}")

    assert response.status_code == 200
    data = response.json()
    assert data["name"] == "manager"
    assert data["description"] == "Store manager"
    assert "id" in data

def test_list_roles(client, db):
    # Create a role first to ensure list is not empty
    # Check if exists first
    from app.models.role import UserRole
    existing = db.query(UserRole).filter(UserRole.name == "supervisor").first()
    if not existing:
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
