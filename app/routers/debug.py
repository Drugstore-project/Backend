from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.models.product import Product

router = APIRouter()

@router.get("/db-content")
def debug_db_content(db: Session = Depends(get_db)):
    """
    Dumps the product table for debugging.
    """
    products = db.query(Product).all()
    result = []
    for p in products:
        result.append({
            "id": p.id,
            "name": p.name,
            "barcode": p.barcode
        })
    print(f"DEBUG: DB Content: {result}")
    return {"count": len(products), "products": result}
