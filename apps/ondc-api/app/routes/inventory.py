from fastapi import APIRouter, HTTPException, Depends
from typing import List
from app.schemas.inventory import InventoryAdjustment, InventoryResponse
from app.models.database import db, InventoryEvent
from app.routes.auth import get_current_user_id
from datetime import datetime

router = APIRouter(prefix="/inventory", tags=["inventory"])

def get_user_store_id(user_id: str) -> str:
    for store in db.stores.values():
        if store.user_id == user_id:
            return store.id
    raise HTTPException(status_code=404, detail="Store not found")

@router.get("", response_model=List[InventoryResponse])
async def get_inventory(user_id: str = Depends(get_current_user_id)):
    store_id = get_user_store_id(user_id)
    
    inventory = []
    for product in db.products.values():
        if product.store_id == store_id:
            inventory.append(InventoryResponse(
                product_id=product.id,
                product_name=product.name,
                current_stock=product.stock,
                sku=product.sku
            ))
    
    return inventory

@router.post("/adjust")
async def adjust_inventory(
    adjustment: InventoryAdjustment,
    user_id: str = Depends(get_current_user_id)
):
    store_id = get_user_store_id(user_id)
    
    if adjustment.product_id not in db.products:
        raise HTTPException(status_code=404, detail="Product not found")
    
    product = db.products[adjustment.product_id]
    
    if product.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    new_stock = product.stock + adjustment.quantity_change
    
    if new_stock < 0:
        raise HTTPException(status_code=400, detail="Stock cannot be negative")
    
    product.stock = new_stock
    product.updated_at = datetime.utcnow()
    
    event_id = db.generate_id()
    event = InventoryEvent(
        id=event_id,
        product_id=adjustment.product_id,
        quantity_change=adjustment.quantity_change,
        reason=adjustment.reason
    )
    db.inventory_events[event_id] = event
    
    return {
        "message": "Inventory adjusted",
        "product_id": adjustment.product_id,
        "new_stock": new_stock
    }
