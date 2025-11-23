"""
CRUD operations for Product model.
"""
from sqlalchemy.orm import Session
from app.models.product import Product
from app.models.product_batch import ProductBatch
from app.models.order import OrderItem
from app.models.supplier_order import SupplierOrder
from app.schemas.product import ProductCreate

def create_product(db: Session, data: ProductCreate) -> Product:
    """
    Creates a new product.
    """
    p = Product(
        name=data.name,
        category=data.category,
        barcode=data.barcode,
        description=data.description,
        price=data.price,
        stock_quantity=data.stock_quantity,
        min_stock_level=data.min_stock_level,
        validity=data.validity,
        stripe=data.stripe,
        requires_prescription=data.requires_prescription,
    )
    db.add(p)
    db.commit()
    db.refresh(p)

    # Create initial batch if provided
    if data.batch_number and data.stock_quantity > 0 and data.validity:
        batch = ProductBatch(
            product_id=p.id,
            batch_number=data.batch_number,
            quantity=data.stock_quantity,
            expiration_date=data.validity
        )
        db.add(batch)
        db.commit()

    return p

def list_products(db: Session) -> list[Product]:
    """
    Lists all products.
    """
    return db.query(Product).all()

def get_product(db: Session, product_id: int) -> Product | None:
    """
    Retrieves a product by ID.
    """
    return db.query(Product).filter(Product.id == product_id).first()

def update_product(db: Session, product_id: int, data: dict) -> Product | None:
    """
    Updates a product.
    """
    p = get_product(db, product_id)
    if not p:
        return None
    for key, value in data.items():
        setattr(p, key, value)
    db.commit()
    db.refresh(p)
    return p

def delete_product(db: Session, product_id: int) -> Product | None:
    """
    Deletes a product and its dependencies (batches, orders, supplier orders).
    """
    p = get_product(db, product_id)
    if not p:
        return None
    
    try:
        # Delete OrderItems (Sales)
        db.query(OrderItem).filter(OrderItem.product_id == product_id).delete(synchronize_session=False)
        
        # Delete SupplierOrders
        db.query(SupplierOrder).filter(SupplierOrder.product_id == product_id).delete(synchronize_session=False)
        
        # Delete ProductBatches
        db.query(ProductBatch).filter(ProductBatch.product_id == product_id).delete(synchronize_session=False)
        
        db.delete(p)
        db.commit()
        return p
    except Exception as e:
        db.rollback()
        raise e
