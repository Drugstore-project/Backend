"""
Pydantic schemas for Authentication.
"""
from pydantic import BaseModel, EmailStr

class LoginInput(BaseModel):
    """
    Schema for login input.
    """
    email: EmailStr
    password: str

class TokenOut(BaseModel):
    """
    Schema for token output.
    """
    access_token: str
    token_type: str = "bearer"
