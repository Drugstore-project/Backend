from sqlalchemy.orm import Session
from sqlalchemy import select
from app.models.payment import Payment
from app.models.order import Order

def create_payment(db: Session, data):
    order = db.query(Order).filter(Order.id == data.order_id).first()
    if not order:
        return None

    payment = Payment(
        order_id=data.order_id,
        type=data.type,
        amount=data.amount,
        invoice_file=data.invoice_file,
    )
    db.add(payment)

    # Atualiza o status do pedido
    order.status = "paid"
    db.commit()
    db.refresh(payment)
    return payment

def list_payments(db: Session):
    return db.query(Payment).all()

def get_payment(db: Session, payment_id: int):
    return db.query(Payment).filter(Payment.id == payment_id).first()

def delete_payment(db: Session, payment_id: int):
    payment = db.query(Payment).filter(Payment.id == payment_id).first()
    if payment:
        db.delete(payment)
        db.commit()
    return payment
