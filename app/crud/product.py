from sqlalchemy.orm import Session
from app.models.product import Product
from app.schemas.product import ProductCreate

def create_product(db: Session, data: ProductCreate) -> Product:
    p = Product(
        name=data.name,
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
    return db.query(Product).all()
