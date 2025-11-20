from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True)
    order_item_id = Column(Integer, ForeignKey("order_items.id", ondelete="CASCADE"), unique=True)
    doctor_name = Column(String, nullable=False)
    crm = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    issued_at = Column(DateTime(timezone=True), server_default=func.now())

    order_item = relationship("app.models.order.OrderItem", back_populates="prescription")
