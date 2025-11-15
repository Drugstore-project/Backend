from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.user import User
from app.models.role import UserRole
from app.schemas.user import UserCreate, UserUpdate
from app.core.security import hash_password

def get_user_by_email(db: Session, email: str) -> User | None:
    return db.execute(select(User).where(User.email == email)).scalar_one_or_none()

def create_user(db: Session, data: UserCreate) -> User:
    if get_user_by_email(db, data.email):
        raise ValueError("Email already registered")

    # verifica se a role existe
    # role = db.execute(select(UserRole).where(UserRole.id == data.role_id)).scalar_one_or_none()
    role = db.query(UserRole).filter(UserRole.id == data.role_id).first()
    if not role:
        raise ValueError("Role not found")

    user = User(
        name=data.name,
        email=data.email,
        password_hash=hash_password(data.password),
        role_id=data.role_id
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session) -> list[User]:
    return db.query(User).all()

def get_user(db: Session, user_id: int) -> User | None:
    return db.query(User).filter(User.id == user_id).first()

def update_user(db: Session, user_id: int, data: UserUpdate) -> User | None:
    user = get_user(db, user_id)
    if not user:
        return None

    if data.name:
        user.name = data.name
    if data.email:
        user.email = data.email
    if data.password:
        user.password_hash = hash_password(data.password)
    if data.role_id:
        role = db.execute(select(UserRole).where(UserRole.id == data.role_id)).scalar_one_or_none()
        if not role:
            raise ValueError("Role not found")
        user.role_id = data.role_id
    if data.is_active is not None:
        user.is_active = data.is_active

    db.commit()
    db.refresh(user)
    return user

def delete_user(db: Session, user_id: int) -> bool:
    user = get_user(db, user_id)
    if user:
        db.delete(user)
        db.commit()
        return True
    return False
