from pydantic import BaseModel
from typing import Optional
from datetime import date

class ProductCreate(BaseModel):
    name: str
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    validity: Optional[date] = None
    stripe: Optional[str] = None
    requires_prescription: bool = False

class ProductOut(BaseModel):
    id: int
    name: str
    description: Optional[str]
    price: float
    stock_quantity: int
    validity: Optional[date]
    stripe: Optional[str]
    requires_prescription: bool

    class Config:
        from_attributes = True

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    validity: Optional[date] = None
    stripe: Optional[str] = None
    requires_prescription: Optional[bool] = None
