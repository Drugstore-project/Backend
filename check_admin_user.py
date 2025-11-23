from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.user import User
from app.core.security import verify_password

def check_admin():
    db = SessionLocal()
    try:
        email = "admin@example.com"
        user = db.query(User).filter(User.email == email).first()
        
        if user:
            print(f"User found: ID={user.id}, Email='{user.email}', RoleID={user.role_id}")
            print(f"Password Hash: {user.password_hash}")
            
            # Verify password
            is_valid = verify_password("admin", user.password_hash)
            print(f"Password 'admin' is valid: {is_valid}")
        else:
            print(f"User {email} NOT found.")
            
            # List all users
            users = db.query(User).all()
            print(f"Total users: {len(users)}")
            for u in users:
                print(f" - {u.email}")

    except Exception as e:
        print(f"Error: {e}")
    finally:
        db.close()

if __name__ == "__main__":
    check_admin()
