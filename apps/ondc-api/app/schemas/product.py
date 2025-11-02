from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime

class ProductBase(BaseModel):
    name: str
    description: Optional[str] = None
    sku: Optional[str] = None
    hsn_code: Optional[str] = None
    price: float = Field(gt=0)
    mrp: float = Field(gt=0)
    stock: int = Field(ge=0)
    category: Optional[str] = None
    images: List[str] = []

class ProductCreate(ProductBase):
    pass

class ProductUpdate(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    price: Optional[float] = Field(None, gt=0)
    mrp: Optional[float] = Field(None, gt=0)
    stock: Optional[int] = Field(None, ge=0)
    category: Optional[str] = None
    is_active: Optional[bool] = None

class ProductResponse(ProductBase):
    id: str
    store_id: str
    is_active: bool
    created_at: datetime
    updated_at: datetime

class BulkProductUpload(BaseModel):
    products: List[ProductCreate]

class ProductFilter(BaseModel):
    category: Optional[str] = None
    min_price: Optional[float] = None
    max_price: Optional[float] = None
    in_stock: Optional[bool] = None
    search: Optional[str] = None
