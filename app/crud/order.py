from typing import Optional
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product

def create_order(db: Session, user_id: Optional[int], items_data: list, payment_method: str, seller_id: Optional[int] = None):
    total = 0
    order = Order(user_id=user_id, seller_id=seller_id, payment_method=payment_method, status="pending")
    db.add(order)
    db.flush()

    for item in items_data:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        if not product:
            continue
        
        if product.stock_quantity < item.quantity:
            raise ValueError(f"Insufficient stock for product {product.name}")

        product.stock_quantity -= item.quantity
        subtotal = product.price * item.quantity
        total += subtotal
        db.add(OrderItem(order_id=order.id, product_id=product.id, quantity=item.quantity, unit_price=product.price))

    order.total_value = total
    db.commit()
    db.refresh(order)
    return order

def list_orders(db: Session):
    return db.query(Order).all()

def get_order(db: Session, order_id: int):
    return db.query(Order).filter(Order.id == order_id).first()

def delete_order(db: Session, order_id: int):
    order = db.query(Order).filter(Order.id == order_id).first()
    if order:
        db.delete(order)
        db.commit()
    return order

def update_order(db: Session, order_id: int, order_data: dict):
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        return None
    
    for key, value in order_data.items():
        setattr(order, key, value)
    
    db.commit()
    db.refresh(order)
    return order



