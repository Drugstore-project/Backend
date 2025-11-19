import pytest
from app.schemas.user import UserCreate
from app.crud.user import create_user
from app.models.role import UserRole as Role


def test_create_user_success(db):
    # criar role necessária
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
    assert user.id is not None
    assert user.email == "test@example.com"
    # senha deve ser armazenada como hash
    assert user.password_hash != "password123"


# def test_create_user_duplicate_email(db):
#     role = Role(name="customer2", description="Customer role")
#     db.add(role)
#     db.commit()
#     db.refresh(role)

#     payload = UserCreate(
#         name="User1",
#         email="dup@example.com",
#         password="password123",
#         role_id=role.id,
#     )
#     u1 = create_user(db, payload)
#     with pytest.raises(ValueError):
#         create_user(db, payload)
