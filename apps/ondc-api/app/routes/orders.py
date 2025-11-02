from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.db.models import Order, Product, Store
from app.db.base import get_db
from app.routes.auth import get_current_user_id
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])

def get_user_store_id(user_id: str, db: Session) -> str:
    store = db.query(Store).filter(Store.user_id == user_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store.id

@router.get("", response_model=List[OrderResponse])
async def list_orders(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    status: Optional[str] = None
):
    store_id = get_user_store_id(user_id, db)
    
    query = db.query(Order).filter(Order.store_id == store_id)
    
    if status:
        query = query.filter(Order.status == status)
    
    orders = query.order_by(Order.created_at.desc()).all()
    
    return [OrderResponse(
        id=o.id,
        store_id=o.store_id,
        customer_name=o.customer_name,
        customer_phone=o.customer_phone,
        customer_email=o.customer_email,
        total_amount=o.total_amount,
        status=o.status.value,
        items=o.items,
        created_at=o.created_at,
        updated_at=o.updated_at
    ) for o in orders]

@router.post("", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    total_amount = 0.0
    items = []
    
    for item in order.items:
        product = db.query(Product).filter(Product.id == item.product_id).first()
        
        if not product:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        if product.store_id != store_id:
            raise HTTPException(status_code=403, detail="Product not in your store")
        
        if product.stock < item.quantity:
            raise HTTPException(status_code=400, detail=f"Insufficient stock for {product.name}")
        
        item_total = item.price * item.quantity
        total_amount += item_total
        
        items.append({
            "product_id": item.product_id,
            "product_name": product.name,
            "quantity": item.quantity,
            "price": item.price,
            "total": item_total
        })
    
    new_order = Order(
        store_id=store_id,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_email=order.customer_email,
        total_amount=total_amount,
        items=items
    )
    
    db.add(new_order)
    db.commit()
    db.refresh(new_order)
    
    return OrderResponse(
        id=new_order.id,
        store_id=new_order.store_id,
        customer_name=new_order.customer_name,
        customer_phone=new_order.customer_phone,
        customer_email=new_order.customer_email,
        total_amount=new_order.total_amount,
        status=new_order.status.value,
        items=new_order.items,
        created_at=new_order.created_at,
        updated_at=new_order.updated_at
    )

@router.post("/{order_id}/confirm")
async def confirm_order(
    order_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    order = db.query(Order).filter(Order.id == order_id).first()
    
    if not order:
        raise HTTPException(status_code=404, detail="Order not found")
    
    if order.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if order.status.value != "pending":
        raise HTTPException(status_code=400, detail="Order already processed")
    
    for item in order.items:
        product_id = item["product_id"]
        quantity = item["quantity"]
        
        product = db.query(Product).filter(Product.id == product_id).first()
        if product:
            product.stock -= quantity
            product.updated_at = datetime.utcnow()
    
    order.status = "confirmed"
    order.updated_at = datetime.utcnow()
    
    db.commit()
    
    print(f"Order {order_id} confirmed - WhatsApp notification would be sent here")
    
    return {"message": "Order confirmed", "order_id": order_id}

@router.post("/export")
async def export_orders(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    orders = db.query(Order).filter(Order.store_id == store_id).all()
    
    return {
        "message": "Export ready",
        "total_orders": len(orders)
    }
