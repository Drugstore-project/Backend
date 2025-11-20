"""
UserRole model definition.
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship
from app.db.base import Base


class UserRole(Base):
    """
    Represents a user role (e.g., admin, pharmacist, cashier).
    """
    __tablename__ = "user_roles"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único do papel")
    name = Column(String(50), unique=True, nullable=False, comment="Nome do papel (ex: admin, pharmacist)")
    description = Column(String(255), nullable=True, comment="Descrição das permissões do papel")

    users = relationship("User", back_populates="role")

    def __repr__(self):
        return f"<UserRole(id={self.id}, name='{self.name}')>"
