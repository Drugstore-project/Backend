from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductOut
from app.crud.product import create_product, list_products

router = APIRouter()

@router.post("/", response_model=ProductOut)
def create_product_endpoint(payload: ProductCreate, db: Session = Depends(get_db)):
    return create_product(db, payload)

@router.get("/", response_model=list[ProductOut])
def list_products_endpoint(db: Session = Depends(get_db)):
    return list_products(db)
