from app.database import SessionLocal
from app.models.role import UserRole

db = SessionLocal()

roles_to_add = ["manager", "seller", "pharmacist"]
existing_roles = [r.name for r in db.query(UserRole).all()]

for role_name in roles_to_add:
    if role_name not in existing_roles:
        new_role = UserRole(name=role_name)
        db.add(new_role)
        print(f"Added role: {role_name}")
    else:
        print(f"Role already exists: {role_name}")

db.commit()
db.close()
