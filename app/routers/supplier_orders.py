from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.supplier_order import SupplierOrderCreate, SupplierOrderOut, SupplierOrderReceive
from app.crud.supplier_order import create_supplier_order, get_supplier_orders, receive_order

router = APIRouter(tags=["Supplier Orders"])

@router.post("/", response_model=SupplierOrderOut)
def create_order(order: SupplierOrderCreate, db: Session = Depends(get_db)):
    return create_supplier_order(db, order)

@router.put("/{order_id}/receive", response_model=SupplierOrderOut)
def receive_order_endpoint(order_id: int, receive_data: SupplierOrderReceive, db: Session = Depends(get_db)):
    order = receive_order(db, order_id, receive_data)
    if not order:
        raise HTTPException(status_code=404, detail="Order not found or already received")
    if order.product:
        order.product_name = order.product.name
    return order

@router.get("/", response_model=list[SupplierOrderOut])
def list_orders(db: Session = Depends(get_db)):
    orders = get_supplier_orders(db)
    # Enrich with product name manually if needed
    for o in orders:
        if o.product:
            o.product_name = o.product.name
    return orders
