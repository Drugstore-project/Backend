from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PaymentBase(BaseModel):
    order_id: int
    type: str
    amount: float
    invoice_file: str | None = None

class PaymentCreate(PaymentBase):
    pass

class PaymentUpdate(BaseModel):
    type: Optional[str] = None
    amount: Optional[float] = None
    invoice_file: Optional[str] = None

class PaymentOut(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
