from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from app.schemas.analytics import SalesAnalytics, TopProductsAnalytics, SalesDataPoint, TopProduct
from app.db.models import Order, Store
from app.db.base import get_db
from app.routes.auth import get_current_user_id
from datetime import datetime, timedelta
from collections import defaultdict

router = APIRouter(prefix="/analytics", tags=["analytics"])

def get_user_store_id(user_id: str, db: Session) -> str:
    store = db.query(Store).filter(Store.user_id == user_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store.id

@router.get("/sales", response_model=SalesAnalytics)
async def get_sales_analytics(
    days: int = 30,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    orders = db.query(Order).filter(
        Order.store_id == store_id,
        Order.status == "confirmed"
    ).all()
    
    daily_sales = defaultdict(lambda: {"sales": 0.0, "orders": 0})
    
    for order in orders:
        date_key = order.created_at.strftime("%Y-%m-%d")
        daily_sales[date_key]["sales"] += order.total_amount
        daily_sales[date_key]["orders"] += 1
    
    data = []
    for i in range(days):
        date = datetime.utcnow() - timedelta(days=days - i - 1)
        date_key = date.strftime("%Y-%m-%d")
        data.append(SalesDataPoint(
            date=date_key,
            sales=daily_sales[date_key]["sales"],
            orders=daily_sales[date_key]["orders"]
        ))
    
    return SalesAnalytics(data=data)

@router.get("/top-products", response_model=TopProductsAnalytics)
async def get_top_products(
    limit: int = 10,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    orders = db.query(Order).filter(
        Order.store_id == store_id,
        Order.status == "confirmed"
    ).all()
    
    product_stats = defaultdict(lambda: {"sales": 0.0, "units": 0, "name": ""})
    
    for order in orders:
        for item in order.items:
            product_id = item["product_id"]
            product_stats[product_id]["sales"] += item["total"]
            product_stats[product_id]["units"] += item["quantity"]
            product_stats[product_id]["name"] = item["product_name"]
    
    sorted_products = sorted(
        product_stats.items(),
        key=lambda x: x[1]["sales"],
        reverse=True
    )[:limit]
    
    products = [
        TopProduct(
            product_id=product_id,
            product_name=stats["name"],
            total_sales=stats["sales"],
            units_sold=stats["units"]
        )
        for product_id, stats in sorted_products
    ]
    
    return TopProductsAnalytics(products=products)
