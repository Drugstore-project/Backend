from pydantic import BaseModel, EmailStr, constr
from typing import Optional
from .role import RoleOut

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6)
    role_id: int   # referencia para a tabela roles

class UserUpdate(BaseModel):
    name: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None
    role_id: Optional[int] = None
    is_active: Optional[bool] = None

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: RoleOut

    class Config:
        from_attributes = True
