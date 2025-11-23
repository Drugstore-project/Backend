"""
Pydantic schemas for Product operations.
"""
from typing import Optional
from datetime import date
from pydantic import BaseModel

class ProductCreate(BaseModel):
    """
    Schema for creating a new product.
    """
    name: str
    category: Optional[str] = None
    barcode: Optional[str] = None
    description: Optional[str] = None
    price: float
    stock_quantity: int = 0
    min_stock_level: int = 10
    validity: Optional[date] = None
    stripe: Optional[str] = None
    requires_prescription: bool = False
    batch_number: Optional[str] = None

class ProductOut(BaseModel):
    """
    Schema for product output response.
    """
    id: int
    name: str
    category: Optional[str]
    barcode: Optional[str]
    description: Optional[str]
    price: float
    stock_quantity: int
    min_stock_level: int
    validity: Optional[date]
    stripe: Optional[str]
    requires_prescription: bool
    next_expiration_date: Optional[date] = None
    next_batch_number: Optional[str] = None

    class Config:
        """
        Pydantic configuration.
        """
        from_attributes = True

class ProductUpdate(BaseModel):
    """
    Schema for updating an existing product.
    """
    name: Optional[str] = None
    category: Optional[str] = None
    barcode: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = None
    stock_quantity: Optional[int] = None
    min_stock_level: Optional[int] = None
    validity: Optional[date] = None
    stripe: Optional[str] = None
    requires_prescription: Optional[bool] = None
