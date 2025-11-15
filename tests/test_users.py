# import pytest
# from app.crud.role_crud import create_role
# from app.schemas.role import RoleCreate
# from app.models.role import UserRole as Role



# def test_create_user(client,db):
#     role = Role(name="customer2", description="Customer role")
#     db.add(role)
#     db.commit()
#     db.refresh(role)
#     payload = {
#         "name": "Teste User",
#         "email": "teste@example.com",
#         "password": "123456",
#         "role_id": role.id,
#     }
#     response = client.post("/users/", json=payload)
#     assert response.status_code == 200, response.text
#     data = response.json()
#     assert "email" in data
