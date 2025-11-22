"""
Endpoints for product management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.crud.product import create_product, list_products, get_product, update_product, delete_product

router = APIRouter()

@router.post("/", response_model=ProductOut)
def create_product_endpoint(payload: ProductCreate, db: Session = Depends(get_db)):
    """
    Creates a new product.
    """
    return create_product(db, payload)

@router.get("/", response_model=list[ProductOut])
def list_products_endpoint(db: Session = Depends(get_db)):
    """
    Lists all products.
    """
    products = list_products(db)
    print(f"DEBUG: Found {len(products)} products in DB")
    return products

@router.get("/{product_id}", response_model=ProductOut)
def get_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    """
    Retrieves a product by ID.
    """
    product = get_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.put("/{product_id}", response_model=ProductOut)
def update_product_endpoint(product_id: int, payload: ProductUpdate, db: Session = Depends(get_db)):
    """
    Updates a product.
    """
    product = update_product(db, product_id, payload.dict(exclude_unset=True))
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return product

@router.delete("/{product_id}")
def delete_product_endpoint(product_id: int, db: Session = Depends(get_db)):
    """
    Deletes a product.
    """
    product = delete_product(db, product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    return {"detail": "Product deleted"}
