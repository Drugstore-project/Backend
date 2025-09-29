from sqlalchemy.orm import Session
from passlib.hash import bcrypt
from app.models.user import User
from app.schemas.user import UserCreate

def create_user(db: Session, data: UserCreate) -> User:
    hashed = bcrypt.hash(data.password)
    user = User(name=data.name, email=data.email, password_hash=hashed)
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def list_users(db: Session) -> list[User]:
    return db.query(User).all()
