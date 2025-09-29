from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date
from app.database import Base

class Product(Base):
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(120), nullable=False)
    description = Column(String, nullable=True)
    price = Column(Numeric(10, 2), nullable=False)
    stock_quantity = Column(Integer, default=0)
    validity = Column(Date, nullable=True)
    stripe = Column(String(100), nullable=True)
    requires_prescription = Column(Boolean, default=False)
