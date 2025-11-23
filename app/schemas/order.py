from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime
from app.schemas.product import ProductOut
from app.schemas.user import UserOut
from app.schemas.product_batch import ProductBatchOut

class OrderItemBase(BaseModel):
    product_id: int
    quantity: int
    unit_price: float
    batch_id: Optional[int] = None

class OrderItemCreate(OrderItemBase):
    pass

class OrderItemOut(OrderItemBase):
    id: int
    product: Optional[ProductOut] = None
    batch: Optional[ProductBatchOut] = None

    class Config:
        from_attributes = True

class OrderBase(BaseModel):
    payment_method: str | None = None
    status: str | None = "pending"

class OrderCreate(OrderBase):
    user_id: Optional[int] = None
    seller_id: Optional[int] = None
    items: List[OrderItemCreate]

class OrderOut(OrderBase):
    id: int
    user_id: Optional[int] = None
    seller_id: Optional[int] = None
    user: Optional[UserOut] = None
    total_value: float
    created_at: datetime
    items: List[OrderItemOut]

    class Config:
        from_attributes = True

class OrderUpdate(BaseModel):
    status: str | None = None
    payment_method: str | None = None
