from pydantic import BaseModel
from datetime import datetime
from typing import Optional

class PrescriptionBase(BaseModel):
    doctor_name: str
    crm: str

class PrescriptionCreate(PrescriptionBase):
    order_item_id: int

class PrescriptionResponse(PrescriptionBase):
    id: int
    order_item_id: int
    file_path: str
    issued_at: datetime

    class Config:
        from_attributes = True
