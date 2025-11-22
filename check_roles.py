from app.database import SessionLocal
from app.models.role import UserRole

db = SessionLocal()
roles = db.query(UserRole).all()
for role in roles:
    print(f"ID: {role.id}, Name: {role.name}")
db.close()
