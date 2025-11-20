"""
Models package initialization.
Imports all models to ensure they are registered with SQLAlchemy Base.
"""
from app.models.user import User
from app.models.role import UserRole
from app.models.product import Product
from app.models.order import Order, OrderItem
from app.models.payment import Payment
from app.models.prescription import Prescription

__all__ = [
    "User",
    "UserRole",
    "Product",
    "Order",
    "OrderItem",
    "Payment",
    "Prescription"
]
