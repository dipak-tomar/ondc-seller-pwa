from fastapi import APIRouter, HTTPException, Depends
from typing import List, Optional
from app.schemas.order import OrderCreate, OrderResponse, OrderStatusUpdate
from app.models.database import db, Order
from app.routes.auth import get_current_user_id
from datetime import datetime

router = APIRouter(prefix="/orders", tags=["orders"])

def get_user_store_id(user_id: str) -> str:
    for store in db.stores.values():
        if store.user_id == user_id:
            return store.id
    raise HTTPException(status_code=404, detail="Store not found")

@router.get("", response_model=List[OrderResponse])
async def list_orders(
    user_id: str = Depends(get_current_user_id),
    status: Optional[str] = None
):
    store_id = get_user_store_id(user_id)
    orders = []
    
    for order in db.orders.values():
        if order.store_id != store_id:
            continue
        
        if status and order.status != status:
            continue
        
        orders.append(OrderResponse(
            id=order.id,
            store_id=order.store_id,
            customer_name=order.customer_name,
            customer_phone=order.customer_phone,
            customer_email=order.customer_email,
            total_amount=order.total_amount,
            status=order.status,
            items=order.items,
            created_at=order.created_at,
            updated_at=order.updated_at
        ))
    
    return sorted(orders, key=lambda x: x.created_at, reverse=True)

@router.post("", response_model=OrderResponse)
async def create_order(
    order: OrderCreate,
    user_id: str = Depends(get_current_user_id)
):
    store_id = get_user_store_id(user_id)
    
    total_amount = 0.0
    items = []
    
    for item in order.items:
        if item.product_id not in db.products:
            raise HTTPException(status_code=404, detail=f"Product {item.product_id} not found")
        
        product = db.products[item.product_id]
        
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
    
    order_id = db.generate_id()
    new_order = Order(
        id=order_id,
        store_id=store_id,
        customer_name=order.customer_name,
        customer_phone=order.customer_phone,
        customer_email=order.customer_email,
        total_amount=total_amount,
        items=items
    )
    
    db.orders[order_id] = new_order
    
    return OrderResponse(
        id=new_order.id,
        store_id=new_order.store_id,
        customer_name=new_order.customer_name,
        customer_phone=new_order.customer_phone,
        customer_email=new_order.customer_email,
        total_amount=new_order.total_amount,
        status=new_order.status,
        items=new_order.items,
        created_at=new_order.created_at,
        updated_at=new_order.updated_at
    )

@router.post("/{order_id}/confirm")
async def confirm_order(
    order_id: str,
    user_id: str = Depends(get_current_user_id)
):
    store_id = get_user_store_id(user_id)
    
    if order_id not in db.orders:
        raise HTTPException(status_code=404, detail="Order not found")
    
    order = db.orders[order_id]
    
    if order.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if order.status != "pending":
        raise HTTPException(status_code=400, detail="Order already processed")
    
    for item in order.items:
        product_id = item["product_id"]
        quantity = item["quantity"]
        
        if product_id in db.products:
            product = db.products[product_id]
            product.stock -= quantity
            product.updated_at = datetime.utcnow()
    
    order.status = "confirmed"
    order.updated_at = datetime.utcnow()
    
    print(f"Order {order_id} confirmed - WhatsApp notification would be sent here")
    
    return {"message": "Order confirmed", "order_id": order_id}

@router.post("/export")
async def export_orders(user_id: str = Depends(get_current_user_id)):
    store_id = get_user_store_id(user_id)
    
    orders = [o for o in db.orders.values() if o.store_id == store_id]
    
    return {
        "message": "Export ready",
        "total_orders": len(orders)
    }
