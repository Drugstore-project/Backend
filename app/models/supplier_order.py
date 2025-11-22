from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func, Date
from sqlalchemy.orm import relationship
from app.db.base import Base

class SupplierOrder(Base):
    __tablename__ = "supplier_orders"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    quantity = Column(Integer, nullable=False)
    status = Column(String(50), default="pending") # pending, received
    expected_delivery_date = Column(Date, nullable=True)
    received_at = Column(DateTime(timezone=True), nullable=True)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    product = relationship("app.models.product.Product")
