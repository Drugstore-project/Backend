from app.database import SessionLocal
from app.models.role import UserRole

db = SessionLocal()
roles = db.query(UserRole).all()
print("--- Roles in DB ---")
for r in roles:
    print(f"ID: {r.id}, Name: {r.name}")
db.close()
