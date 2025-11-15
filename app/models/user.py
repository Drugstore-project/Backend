from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, index=True, nullable=False)
    password_hash = Column(String(255), nullable=False)
    is_active = Column(Boolean, default=True)
    orders = relationship("Order", back_populates="user")
    # aponta para a tabela definida em app.models.role -> __tablename__ = 'user_roles'
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False)
    # relation por string evita circular imports; atualizada para o novo nome da classe
    role = relationship("UserRole", back_populates="users")
