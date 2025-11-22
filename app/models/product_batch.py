from sqlalchemy import Column, Integer, String, ForeignKey, Date, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class ProductBatch(Base):
    __tablename__ = "product_batches"

    id = Column(Integer, primary_key=True, index=True)
    product_id = Column(Integer, ForeignKey("products.id"), nullable=False)
    batch_number = Column(String(50), nullable=False)
    quantity = Column(Integer, nullable=False)
    expiration_date = Column(Date, nullable=False)
    created_at = Column(DateTime(timezone=True), server_default=func.now())
    
    product = relationship("app.models.product.Product", back_populates="batches")
