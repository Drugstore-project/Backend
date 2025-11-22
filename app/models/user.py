"""
User model definition.
"""
from sqlalchemy import Column, Integer, String, Boolean, ForeignKey
from sqlalchemy.orm import relationship
from app.db.base import Base

class User(Base):
    """
    Represents a user in the system.
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único do usuário")
    name = Column(String(100), nullable=False, comment="Nome completo do usuário")
    email = Column(String(100), unique=True, index=True, nullable=False, comment="Endereço de email do usuário")
    cpf = Column(String(14), unique=True, index=True, nullable=True, comment="CPF do usuário")
    phone = Column(String(20), nullable=True, comment="Telefone de contato")
    address = Column(String(255), nullable=True, comment="Endereço completo")
    birth_date = Column(String(20), nullable=True, comment="Data de nascimento")
    client_type = Column(String(50), nullable=True, comment="Tipo de cliente (regular, elderly, insurance)")
    password_hash = Column(String(255), nullable=False, comment="Hash da senha do usuário")
    is_active = Column(Boolean, default=True, comment="Indica se o usuário está ativo")
    orders = relationship("Order", back_populates="user")
    # aponta para a tabela definida em app.models.role -> __tablename__ = 'user_roles'
    role_id = Column(Integer, ForeignKey("user_roles.id"), nullable=False, comment="ID do papel (role) do usuário")
    # relation por string evita circular imports; atualizada para o novo nome da classe
    role = relationship("UserRole", back_populates="users")

    def __repr__(self):
        return f"<User(id={self.id}, email='{self.email}', name='{self.name}')>"
