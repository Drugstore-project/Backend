"""
Pydantic schemas for User operations.
"""
from typing import Optional
from pydantic import BaseModel, EmailStr, constr

class UserCreate(BaseModel):
    """
    Schema for creating a new user.
    """
    name: str
    email: EmailStr
    cpf: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[str] = None
    client_type: Optional[str] = None
    password: constr(min_length=6)
    role_id: int   # referencia para a tabela roles

class UserUpdate(BaseModel):
    """
    Schema for updating an existing user.
    """
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    cpf: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    birth_date: Optional[str] = None
    client_type: Optional[str] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None

class UserOut(BaseModel):
    """
    Schema for user output response.
    """
    id: int
    name: str
    email: EmailStr
    cpf: Optional[str]
    phone: Optional[str]
    address: Optional[str]
    birth_date: Optional[str]
    client_type: Optional[str]
    is_active: bool
    role_id: int

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes = True
