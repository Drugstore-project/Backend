from pydantic import BaseModel
from datetime import date, datetime

class ProductBatchBase(BaseModel):
    product_id: int
    batch_number: str
    quantity: int
    expiration_date: date

class ProductBatchCreate(ProductBatchBase):
    pass

class ProductBatchOut(ProductBatchBase):
    id: int
    created_at: datetime

    class Config:
        from_attributes = True
