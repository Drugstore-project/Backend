from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Payment(Base):
    __tablename__ = "payments"

    id = Column(Integer, primary_key=True, index=True)
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"))
    type = Column(String(50), nullable=False, comment="Tipo de pagamento (pix, cartão, boleto, etc.)")
    amount = Column(Float, nullable=False, comment="Valor pago")
    invoice_file = Column(String(255), nullable=True, comment="Arquivo da nota fiscal")
    created_at = Column(DateTime(timezone=True), server_default=func.now())

    order = relationship("Order", back_populates="payments")
