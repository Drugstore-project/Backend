from sqlalchemy.orm import Session
from app.models.role import UserRole
from app.database import SessionLocal


def seed_roles():
    db: Session = SessionLocal()
    roles = ["admin", "pharmacist", "seller"]

    for r in roles:
        if not db.query(UserRole).filter(UserRole.name == r).first():
            db.add(UserRole(name=r))
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_roles()
