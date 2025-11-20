from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.order import OrderCreate, OrderOut, OrderUpdate
from app.crud import order as crud_order

router = APIRouter(prefix="/orders", tags=["Orders"])

@router.post("/", response_model=OrderOut)
def create_order(order_data: OrderCreate, db: Session = Depends(get_db)):
    try:
        order = crud_order.create_order(
            db=db,
            user_id=order_data.user_id,
            items_data=order_data.items,
            payment_method=order_data.payment_method or "cash"
        )
        if not order:
            raise HTTPException(status_code=400, detail="Could not create order")
        return order
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

@router.get("/", response_model=list[OrderOut])
def list_orders(db: Session = Depends(get_db)):
    return crud_order.list_orders(db)

@router.put("/{order_id}", response_model=OrderOut)
def update_order(order_id: int, order_update: OrderUpdate, db: Session = Depends(get_db)):
    updated_order = crud_order.update_order(db, order_id, order_update.dict(exclude_unset=True))
    if not updated_order:
        raise HTTPException(status_code=404, detail="Order not found")
    return updated_order
