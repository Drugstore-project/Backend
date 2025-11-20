"""
Endpoints for generating reports.
"""
from datetime import date
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func
from app.database import get_db
from app.models.order import Order
from app.models.product import Product

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/sales")
def sales_report(
    start_date: date = None,
    end_date: date = None,
    db: Session = Depends(get_db)
):
    """
    Generates a sales report for a given period.
    """
    query = db.query(Order)
    if start_date:
        query = query.filter(func.date(Order.created_at) >= start_date)
    if end_date:
        query = query.filter(func.date(Order.created_at) <= end_date)

    orders = query.all()
    total_sales = sum(o.total_value for o in orders)
    return {
        "period": {"start": start_date, "end": end_date},
        "total_sales": total_sales,
        "orders_count": len(orders),
        "orders": orders
    }

@router.get("/stock")
def stock_report(db: Session = Depends(get_db)):
    """
    Generates a stock report indicating low stock items.
    """
    products = db.query(Product).all()
    return [
        {
            "id": p.id,
            "name": p.name,
            "stock_quantity": p.stock_quantity,
            "status": "Low Stock" if p.stock_quantity < 10 else "OK"
        }
        for p in products
    ]

@router.get("/controlled-medications")
def controlled_medications_report(db: Session = Depends(get_db)):
    """
    Lists all controlled medications (requiring prescription).
    """
    # Filter products that require prescription (controlled)
    products = db.query(Product).filter(Product.requires_prescription.is_(True)).all()
    return products
