from sqlalchemy.orm import Session
from app.models.supplier_order import SupplierOrder
from app.models.product import Product
from app.models.product_batch import ProductBatch
from app.schemas.supplier_order import SupplierOrderCreate, SupplierOrderReceive
from datetime import datetime

def create_supplier_order(db: Session, order: SupplierOrderCreate):
    db_order = SupplierOrder(
        product_id=order.product_id,
        quantity=order.quantity,
        expected_delivery_date=order.expected_delivery_date,
        status=order.status
    )
    
    if order.created_at:
        db_order.created_at = order.created_at
        
    if order.status == 'received':
        db_order.received_at = order.created_at or datetime.now()
        
        # Create batch if info provided
        if order.batch_number and order.expiration_date:
            batch = ProductBatch(
                product_id=order.product_id,
                batch_number=order.batch_number,
                quantity=order.quantity,
                expiration_date=order.expiration_date,
                created_at=db_order.received_at
            )
            db.add(batch)

        # Update stock if creating as received
        product = db.query(Product).filter(Product.id == order.product_id).first()
        if product:
            product.stock_quantity += order.quantity

    db.add(db_order)
    db.commit()
    db.refresh(db_order)
    return db_order

def get_supplier_orders(db: Session):
    return db.query(SupplierOrder).order_by(SupplierOrder.created_at.desc()).all()

def receive_order(db: Session, order_id: int, receive_data: SupplierOrderReceive = None):
    order = db.query(SupplierOrder).filter(SupplierOrder.id == order_id).first()
    if not order or order.status == 'received':
        return None
    
    order.status = 'received'
    order.received_at = datetime.now()
    
    # Create Product Batch if data provided
    if receive_data:
        batch = ProductBatch(
            product_id=order.product_id,
            batch_number=receive_data.batch_number,
            quantity=order.quantity,
            expiration_date=receive_data.expiration_date
        )
        db.add(batch)

    # Update product stock
    product = db.query(Product).filter(Product.id == order.product_id).first()
    if product:
        product.stock_quantity += order.quantity
        
    db.commit()
    db.refresh(order)
    return order
