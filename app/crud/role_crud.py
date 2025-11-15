from sqlalchemy.orm import Session
from app.models.role import UserRole
from app.schemas.role import RoleCreate

def create_role(db: Session, role: RoleCreate):
    db_role = UserRole(name=role.name)
    db.add(db_role)
    db.commit()
    db.refresh(db_role)
    return db_role

def get_roles(db: Session):
    return db.query(UserRole).all()

def get_role(db: Session, role_id: int):
    return db.query(UserRole).filter(UserRole.id == role_id).first()