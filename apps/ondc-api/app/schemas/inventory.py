from pydantic import BaseModel
from typing import Optional

class InventoryAdjustment(BaseModel):
    product_id: str
    quantity_change: int
    reason: str

class InventoryResponse(BaseModel):
    product_id: str
    product_name: str
    current_stock: int
    sku: Optional[str] = None
