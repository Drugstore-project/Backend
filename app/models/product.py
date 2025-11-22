"""
Product model definition.
"""
from sqlalchemy import Column, Integer, String, Numeric, Boolean, Date
from sqlalchemy.orm import relationship
from app.db.base import Base

class Product(Base):
    """
    Represents a product in the inventory.
    """
    __tablename__ = "products"

    id = Column(Integer, primary_key=True, index=True, comment="Identificador único do produto")
    name = Column(String(120), nullable=False, comment="Nome do produto")
    category = Column(String(100), nullable=True, comment="Categoria do produto (ex: Medicamento, Higiene)")
    barcode = Column(String(100), unique=True, nullable=True, comment="Código de barras do produto")
    description = Column(String, nullable=True, comment="Descrição detalhada do produto")
    price = Column(Numeric(10, 2), nullable=False, comment="Preço unitário do produto")
    stock_quantity = Column(Integer, default=0, comment="Quantidade em estoque")
    validity = Column(Date, nullable=True, comment="Data de validade do produto")
    min_stock_level = Column(Integer, default=10, comment="Nível mínimo de estoque para alerta")
    stripe = Column(String(100), nullable=True, comment="Tarja do medicamento (ex: Preta, Vermelha)")
    requires_prescription = Column(Boolean, default=False, comment="Indica se requer receita médica")

    batches = relationship("ProductBatch", back_populates="product", order_by="ProductBatch.expiration_date")

    def __repr__(self):
        return f"<Product(id={self.id}, name='{self.name}', price={self.price})>"
