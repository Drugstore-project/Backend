from sqlalchemy.orm import Session
from app.database import SessionLocal, engine, Base
from app.models import User, UserRole
from app.core.security import hash_password

def create_admin_user():
    db = SessionLocal()
    try:
        # Ensure tables exist
        # Base.metadata.create_all(bind=engine) # Tables should already exist via Alembic or previous runs

        # Check/Create Role
        admin_role = db.query(UserRole).filter(UserRole.name == "admin").first()
        if not admin_role:
            print("Creating admin role...")
            admin_role = UserRole(name="admin", description="Administrator")
            db.add(admin_role)
            db.commit()
            db.refresh(admin_role)
        else:
            print("Admin role exists.")

        # Check/Create User
        email = "admin@example.com"
        password = "admin"
        
        user = db.query(User).filter(User.email == email).first()
        if user:
            print(f"User {email} already exists. Updating password...")
            user.password_hash = hash_password(password)
            user.is_active = True
            user.role_id = admin_role.id
            db.commit()
            print("Password updated.")
        else:
            print(f"Creating user {email}...")
            new_user = User(
                name="Admin User",
                email=email,
                password_hash=hash_password(password),
                role_id=admin_role.id,
                is_active=True
            )
            db.add(new_user)
            db.commit()
            print("User created successfully.")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    create_admin_user()
