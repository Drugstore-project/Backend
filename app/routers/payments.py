from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.core.deps import get_db
from app.schemas.payment import PaymentCreate, PaymentOut
from app.crud import payment as crud_payment

router = APIRouter(prefix="/payments", tags=["Payments"])

@router.post("/", response_model=PaymentOut)
def create_payment(data: PaymentCreate, db: Session = Depends(get_db)):
    payment = crud_payment.create_payment(db, data)
    if not payment:
        raise HTTPException(404, detail="Order not found")
    return payment

@router.get("/", response_model=list[PaymentOut])
def list_payments(db: Session = Depends(get_db)):
    return crud_payment.list_payments(db)

@router.get("/{payment_id}", response_model=PaymentOut)
def get_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = crud_payment.get_payment(db, payment_id)
    if not payment:
        raise HTTPException(404, detail="Payment not found")
    return payment

@router.delete("/{payment_id}")
def delete_payment(payment_id: int, db: Session = Depends(get_db)):
    payment = crud_payment.delete_payment(db, payment_id)
    if not payment:
        raise HTTPException(404, detail="Payment not found")
    return {"detail": "Deleted successfully"}
