"""
CRUD operations for Product model.
"""
from sqlalchemy.orm import Session
from app.models.product import Product
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
        validity=data.validity,
        stripe=data.stripe,
        requires_prescription=data.requires_prescription,
    )
    db.add(p)
    db.commit()
    db.refresh(p)
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
    Deletes a product.
    """
    p = get_product(db, product_id)
    if not p:
        return None
    db.delete(p)
    db.commit()
    return p
