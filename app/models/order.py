from sqlalchemy import Column, Integer, Float, String, ForeignKey, DateTime, func
from sqlalchemy.orm import relationship
from app.db.base import Base

class Order(Base):
    __tablename__ = "orders"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único do pedido")
    user_id = Column(Integer, ForeignKey("users.id", ondelete="CASCADE"), comment="ID do cliente que fez o pedido")
    seller_id = Column(Integer, ForeignKey("users.id", ondelete="SET NULL"), nullable=True, comment="ID do vendedor que processou o pedido")
    total_value = Column(Float, default=0, comment="Valor total do pedido")
    status = Column(String(50), default="pending", comment="Status do pedido (pending, paid, shipped, etc.)")
    created_at = Column(DateTime(timezone=True), server_default=func.now(), comment="Data e hora de criação do pedido")
    payment_method = Column(String(50), nullable=True, comment="Método de pagamento escolhido")

    user = relationship("User", foreign_keys=[user_id], back_populates="orders")
    seller = relationship("User", foreign_keys=[seller_id], back_populates="sales")
    items = relationship("OrderItem", back_populates="order", cascade="all, delete-orphan")
    payments = relationship("Payment", back_populates="order", cascade="all, delete-orphan") 

class OrderItem(Base):
    __tablename__ = "order_items"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único do item do pedido")
    order_id = Column(Integer, ForeignKey("orders.id", ondelete="CASCADE"), comment="ID do pedido relacionado")
    product_id = Column(Integer, ForeignKey("products.id", ondelete="RESTRICT"), comment="ID do produto comprado")
    quantity = Column(Integer, nullable=False, comment="Quantidade comprada")
    unit_price = Column(Float, nullable=False, comment="Preço unitário no momento da compra")


    order = relationship("Order", back_populates="items")
    product = relationship("app.models.product.Product")
    prescription = relationship("app.models.prescription.Prescription", uselist=False, back_populates="order_item", cascade="all, delete-orphan")
