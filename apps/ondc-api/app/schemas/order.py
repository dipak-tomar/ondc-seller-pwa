from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

class OrderItem(BaseModel):
    product_id: str
    quantity: int
    price: float

class OrderCreate(BaseModel):
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    items: List[OrderItem]

class OrderResponse(BaseModel):
    id: str
    store_id: str
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: float
    status: str
    items: List[dict]
    created_at: datetime
    updated_at: datetime

class OrderStatusUpdate(BaseModel):
    status: str
