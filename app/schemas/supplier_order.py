from pydantic import BaseModel
from datetime import date, datetime
from typing import Optional

class SupplierOrderCreate(BaseModel):
    product_id: int
    quantity: int
    expected_delivery_date: Optional[date] = None
    status: Optional[str] = "pending"
    created_at: Optional[datetime] = None
    batch_number: Optional[str] = None
    expiration_date: Optional[date] = None

class SupplierOrderReceive(BaseModel):
    batch_number: str
    expiration_date: date

class SupplierOrderOut(BaseModel):
    id: int
    product_id: int
    quantity: int
    status: str
    expected_delivery_date: Optional[date]
    received_at: Optional[datetime]
    created_at: datetime
    product_name: Optional[str] = None

    class Config:
        from_attributes = True
