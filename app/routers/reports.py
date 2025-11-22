"""
Endpoints for generating reports.
"""
from datetime import date, datetime, timedelta
from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from app.database import get_db
from app.models.order import Order, OrderItem
from app.models.product import Product
from app.models.user import User
from app.models.role import UserRole

router = APIRouter(prefix="/reports", tags=["Reports"])

@router.get("/analytics")
def analytics_report(db: Session = Depends(get_db)):
    """
    Returns detailed analytics for charts:
    - Top Sellers (Donut)
    - Sales History (Bar)
    - Monthly Goal Progress
    - Top Products (List)
    """
    # 1. Top Sellers
    # Group by seller_id, sum total_value
    top_sellers_query = (
        db.query(User.name, func.sum(Order.total_value).label("total_sales"))
        .join(Order, Order.seller_id == User.id)
        .group_by(User.name)
        .order_by(func.sum(Order.total_value).desc())
        .limit(5)
        .all()
    )
    top_sellers = [{"name": r[0], "value": float(r[1])} for r in top_sellers_query]

    # 2. Sales History (Last 30 days)
    thirty_days_ago = datetime.now() - timedelta(days=30)
    sales_history_query = (
        db.query(func.date(Order.created_at).label("date"), func.sum(Order.total_value).label("total"))
        .filter(Order.created_at >= thirty_days_ago)
        .group_by(func.date(Order.created_at))
        .order_by(func.date(Order.created_at))
        .all()
    )
    sales_history = [{"date": str(r[0]), "sales": float(r[1])} for r in sales_history_query]

    # 3. Monthly Goal Progress
    current_month = datetime.now().month
    current_year = datetime.now().year
    
    monthly_sales = (
        db.query(func.sum(Order.total_value))
        .filter(extract('month', Order.created_at) == current_month)
        .filter(extract('year', Order.created_at) == current_year)
        .scalar()
    ) or 0

    monthly_goal = 50000.0 # Hardcoded goal for now

    # 4. Top Products (Most sold by quantity)
    top_products_query = (
        db.query(Product.name, func.sum(OrderItem.quantity).label("total_quantity"), func.sum(OrderItem.quantity * OrderItem.unit_price).label("total_revenue"))
        .join(OrderItem, OrderItem.product_id == Product.id)
        .group_by(Product.name)
        .order_by(func.sum(OrderItem.quantity).desc())
        .limit(5)
        .all()
    )
    top_products = [
        {"name": r[0], "quantity": int(r[1]), "revenue": float(r[2])} 
        for r in top_products_query
    ]

    return {
        "topSellers": top_sellers,
        "salesHistory": sales_history,
        "monthlyProgress": {
            "current": float(monthly_sales),
            "goal": monthly_goal,
            "percentage": min(int((float(monthly_sales) / monthly_goal) * 100), 100)
        },
        "topProducts": top_products
    }

@router.get("/dashboard")
def dashboard_stats(db: Session = Depends(get_db)):
    """
    Returns aggregated statistics for the admin dashboard.
    """
    # Total Revenue
    total_revenue = db.query(func.sum(Order.total_value)).scalar() or 0

    # Total Products
    total_products = db.query(Product).count()

    # Low Stock Count
    low_stock_count = db.query(Product).filter(Product.stock_quantity <= Product.min_stock_level).count()

    # Staff Count (Users that are not clients)
    staff_count = db.query(User).join(UserRole).filter(UserRole.name != 'client').count()

    return {
        "totalRevenue": total_revenue,
        "totalProducts": total_products,
        "lowStockCount": low_stock_count,
        "staffCount": staff_count
    }

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
