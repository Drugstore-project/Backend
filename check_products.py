from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product

def check_products():
    db = SessionLocal()
    products = db.query(Product).all()
    print(f"Found {len(products)} products:")
    for p in products:
        print(f"- {p.name} (Stock: {p.stock_quantity})")
    db.close()

if __name__ == "__main__":
    check_products()
