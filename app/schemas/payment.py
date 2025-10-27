from pydantic import BaseModel
from datetime import datetime

class PaymentBase(BaseModel):
    order_id: int
    type: str
    amount: float
    invoice_file: str | None = None

class PaymentCreate(PaymentBase):
    pass

class PaymentOut(PaymentBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
