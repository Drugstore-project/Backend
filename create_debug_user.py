from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.crud.user import create_user, get_user_by_email
from app.schemas.user import UserCreate
from app.models.role import UserRole

def create_debug_user():
    db = SessionLocal()
    email = "debug@example.com"
    password = "debugpassword123"
    
    # Check if role exists
    role = db.query(UserRole).filter(UserRole.name == "manager").first()
    if not role:
        print("Role 'manager' not found. Seeding...")
        role = UserRole(name="manager")
        db.add(role)
        db.commit()
        db.refresh(role)
    
    # Check if user exists
    existing = get_user_by_email(db, email)
    if existing:
        print(f"User {email} already exists. Deleting...")
        db.delete(existing)
        db.commit()
    
    print(f"Creating user {email} with password '{password}'...")
    user_in = UserCreate(
        name="Debug User",
        email=email,
        password=password,
        role_id=role.id,
        cpf="00000000000",
        phone="000000000",
        address="Debug Address"
    )
    
    try:
        user = create_user(db, user_in)
        print(f"User created successfully. ID: {user.id}")
        print(f"Password Hash: {user.password_hash}")
    except Exception as e:
        print(f"Error creating user: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_debug_user()
