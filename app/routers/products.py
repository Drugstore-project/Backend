"""
Endpoints for product management.
"""
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.product import ProductCreate, ProductOut, ProductUpdate
from app.schemas.product_batch import ProductBatchOut
from app.models.product_batch import ProductBatch
from app.crud.product import create_product, list_products, get_product, update_product, delete_product

router = APIRouter()

@router.get("/{product_id}/batches", response_model=list[ProductBatchOut])
def get_product_batches(product_id: int, db: Session = Depends(get_db)):
    """
    Lists all batches for a specific product.
    """
    batches = db.query(ProductBatch).filter(ProductBatch.product_id == product_id).all()
    return batches

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
    
    # Enrich with batch info
    for p in products:
        # Filter for batches with quantity > 0 and sort by expiration (relationship is already sorted but filter creates new list)
        active_batches = [b for b in p.batches if b.quantity > 0]
        if active_batches:
            # Sort again to be safe or rely on relationship order if preserved
            active_batches.sort(key=lambda x: x.expiration_date)
            next_batch = active_batches[0]
            p.next_expiration_date = next_batch.expiration_date
            p.next_batch_number = next_batch.batch_number
        else:
            p.next_expiration_date = p.validity

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
    try:
        product = delete_product(db, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found")
        return {"detail": "Product deleted"}
    except Exception as e:
        # Log the error for debugging (optional, but good practice)
        print(f"Error deleting product {product_id}: {e}")
        # Return the error message to the client
        raise HTTPException(status_code=400, detail=str(e))
