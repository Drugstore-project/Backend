from sqlalchemy.orm import Session
from app.models.role import UserRole
from app.database import SessionLocal

def ensure_client_role():
    db: Session = SessionLocal()
    role_name = "client"
    role = db.query(UserRole).filter(UserRole.name == role_name).first()
    if not role:
        print(f"Creating role: {role_name}")
        new_role = UserRole(name=role_name)
        db.add(new_role)
        db.commit()
        print(f"Role created with ID: {new_role.id}")
    else:
        print(f"Role '{role_name}' already exists with ID: {role.id}")
    db.close()

if __name__ == "__main__":
    ensure_client_role()
