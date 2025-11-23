from typing import Optional
from sqlalchemy.orm import Session
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.product_batch import ProductBatch

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

        # If batch_id is provided, use that specific batch
        if hasattr(item, 'batch_id') and item.batch_id:
            batch = db.query(ProductBatch).filter(ProductBatch.id == item.batch_id).first()
            if not batch:
                # If batch not found by ID, try to find by batch_number if possible or just ignore and fallback to FIFO?
                # For now, let's raise error as user explicitly selected a batch
                raise ValueError(f"Batch {item.batch_id} not found")
            
            if batch.product_id != product.id:
                raise ValueError(f"Batch {batch.batch_number} does not belong to product {product.name}")
            
            if batch.quantity < item.quantity:
                raise ValueError(f"Insufficient stock in batch {batch.batch_number}. Available: {batch.quantity}, Requested: {item.quantity}")
            
            batch.quantity -= item.quantity
            # product.stock_quantity is total stock, so we must decrease it too
            product.stock_quantity -= item.quantity
            subtotal = product.price * item.quantity
            total += subtotal
            
            db.add(OrderItem(
                order_id=order.id, 
                product_id=product.id, 
                quantity=item.quantity, 
                unit_price=product.price,
                batch_id=batch.id
            ))
            continue

        remaining_qty = item.quantity
        
        # Get batches ordered by expiration date (FIFO)
        batches = db.query(ProductBatch).filter(
            ProductBatch.product_id == product.id,
            ProductBatch.quantity > 0
        ).order_by(ProductBatch.expiration_date.asc()).all()

        batches_used = []
        
        for batch in batches:
            if remaining_qty <= 0:
                break
            
            take_qty = min(remaining_qty, batch.quantity)
            batch.quantity -= take_qty
            remaining_qty -= take_qty
            
            batches_used.append((batch, take_qty))

        # Update product total stock
        product.stock_quantity -= item.quantity
        subtotal = product.price * item.quantity
        total += subtotal

        # Create OrderItems for used batches
        for batch, qty in batches_used:
            db.add(OrderItem(
                order_id=order.id, 
                product_id=product.id, 
                quantity=qty, 
                unit_price=product.price,
                batch_id=batch.id
            ))
            
        # If there is remaining quantity (stock exists but not in batches, or inconsistency), create item without batch
        if remaining_qty > 0:
             db.add(OrderItem(
                order_id=order.id, 
                product_id=product.id, 
                quantity=remaining_qty, 
                unit_price=product.price,
                batch_id=None
            ))

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



