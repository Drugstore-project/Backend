from sqlalchemy.orm import Session
from models.role import Role
from database import SessionLocal

def seed_roles():
    db: Session = SessionLocal()
    roles = ["admin", "pharmacist", "seller"]

    for r in roles:
        if not db.query(Role).filter(Role.name == r).first():
            db.add(Role(name=r))
    db.commit()
    db.close()

if __name__ == "__main__":
    seed_roles()
