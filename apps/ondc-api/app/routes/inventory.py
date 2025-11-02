from fastapi import APIRouter, HTTPException, Depends
from typing import List
from sqlalchemy.orm import Session
from app.schemas.inventory import InventoryAdjustment, InventoryResponse
from app.db.models import Product, Store, InventoryEvent
from app.db.base import get_db
from app.routes.auth import get_current_user_id
from datetime import datetime

router = APIRouter(prefix="/inventory", tags=["inventory"])

def get_user_store_id(user_id: str, db: Session) -> str:
    store = db.query(Store).filter(Store.user_id == user_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store.id

@router.get("", response_model=List[InventoryResponse])
async def get_inventory(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    products = db.query(Product).filter(Product.store_id == store_id).all()
    
    return [InventoryResponse(
        product_id=p.id,
        product_name=p.name,
        current_stock=p.stock,
        sku=p.sku
    ) for p in products]

@router.post("/adjust")
async def adjust_inventory(
    adjustment: InventoryAdjustment,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    product = db.query(Product).filter(Product.id == adjustment.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_stock = product.stock + adjustment.quantity_change
    
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")
    
    product.stock = new_stock
    product.updated_at = datetime.utcnow()
    
    event = InventoryEvent(
        product_id=adjustment.product_id,
        quantity_change=adjustment.quantity_change,
        reason=adjustment.reason
    )
    db.add(event)
    
    db.commit()
    
    return {
        "message": "Inventory adjusted",
        "product_id": adjustment.product_id,
        "new_stock": new_stock
    }
