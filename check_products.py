from sqlalchemy.orm import Session
from app.database import SessionLocal
from app.models.product import Product

def check_products():
    db = SessionLocal()
    products = db.query(Product).all()
    print(f"Found {len(products)} products:")
    for p in products:
        print(f"- ID: {p.id}, Name: {p.name}, Stock: {p.stock_quantity}, Stripe: {p.stripe}, Validity: {p.validity}")
    db.close()

if __name__ == "__main__":
    check_products()
