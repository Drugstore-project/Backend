from pydantic import BaseModel
from typing import List
from datetime import datetime

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    payment_method: str | None = None
    status: str | None = "pending"

class OrderCreate(OrderBase):
    user_id: int
    items: List[OrderItemCreate]

class OrderOut(OrderBase):
    id: int
    total_value: float
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True
