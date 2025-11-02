from pydantic import BaseModel
from typing import List
from datetime import date

class SalesDataPoint(BaseModel):
    date: str
    sales: float
    orders: int

class TopProduct(BaseModel):
    product_id: str
    product_name: str
    total_sales: float
    units_sold: int

class SalesAnalytics(BaseModel):
    data: List[SalesDataPoint]

class TopProductsAnalytics(BaseModel):
    products: List[TopProduct]
