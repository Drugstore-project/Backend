from sqlalchemy import Column, Integer, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Prescription(Base):
    __tablename__ = "prescriptions"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único da receita")
    order_item_id = Column(Integer, ForeignKey("order_items.id", ondelete="CASCADE"), unique=True, comment="ID do item do pedido associado")
    doctor_name = Column(String, nullable=False, comment="Nome do médico prescritor")
    crm = Column(String, nullable=False, comment="CRM do médico")
    file_path = Column(String, nullable=False, comment="Caminho do arquivo da receita (upload)")
    issued_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Data de emissão/upload da receita")

    order_item = relationship("app.models.order.OrderItem", back_populates="prescription")
