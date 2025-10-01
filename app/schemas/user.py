from pydantic import BaseModel, EmailStr, constr
from typing import Literal

RoleLiteral = Literal["admin", "pharmacist", "seller"]

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: constr(min_length=6)
    role: RoleLiteral = "seller"

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    role: RoleLiteral

    class Config:
        from_attributes = True  # Pydantic v2
