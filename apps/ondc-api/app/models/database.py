from typing import Dict, List, Optional
from datetime import datetime
from dataclasses import dataclass, field
import uuid

@dataclass
class User:
    id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True
    plan: str = "free"

@dataclass
class Store:
    id: str
    user_id: str
    name: str
    description: Optional[str] = None
    created_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class Product:
    id: str
    store_id: str
    name: str
    price: float
    mrp: float
    description: Optional[str] = None
    sku: Optional[str] = None
    hsn_code: Optional[str] = None
    stock: int = 0
    category: Optional[str] = None
    images: List[str] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)
    is_active: bool = True

@dataclass
class Order:
    id: str
    store_id: str
    customer_name: Optional[str] = None
    customer_phone: Optional[str] = None
    customer_email: Optional[str] = None
    total_amount: float = 0.0
    status: str = "pending"
    items: List[dict] = field(default_factory=list)
    created_at: datetime = field(default_factory=datetime.utcnow)
    updated_at: datetime = field(default_factory=datetime.utcnow)

@dataclass
class InventoryEvent:
    id: str
    product_id: str
    quantity_change: int
    reason: str
    created_at: datetime = field(default_factory=datetime.utcnow)

class InMemoryDB:
    def __init__(self):
        self.users: Dict[str, User] = {}
        self.stores: Dict[str, Store] = {}
        self.products: Dict[str, Product] = {}
        self.orders: Dict[str, Order] = {}
        self.inventory_events: Dict[str, InventoryEvent] = {}
        self.otp_store: Dict[str, dict] = {}
        
    def generate_id(self) -> str:
        return str(uuid.uuid4())

db = InMemoryDB()
