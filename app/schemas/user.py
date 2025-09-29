from pydantic import BaseModel, EmailStr

class UserCreate(BaseModel):
    name: str
    email: EmailStr
    password: str

class UserOut(BaseModel):
    id: int
    name: str
    email: EmailStr
    is_active: bool
    is_admin: bool

    class Config:
        from_attributes = True  # (Pydantic v2) habilita ORM mode
