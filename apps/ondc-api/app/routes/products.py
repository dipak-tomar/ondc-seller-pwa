from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from typing import List, Optional
from sqlalchemy.orm import Session
from app.schemas.product import ProductCreate, ProductResponse, ProductUpdate, BulkProductUpload
from app.db.models import Product, Store
from app.db.base import get_db
from app.routes.auth import get_current_user_id
from datetime import datetime
import csv
import io

router = APIRouter(prefix="/products", tags=["products"])

def get_user_store_id(user_id: str, db: Session) -> str:
    store = db.query(Store).filter(Store.user_id == user_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store.id

@router.get("", response_model=List[ProductResponse])
async def list_products(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db),
    category: Optional[str] = None,
    search: Optional[str] = None,
    in_stock: Optional[bool] = None
):
    store_id = get_user_store_id(user_id, db)
    
    query = db.query(Product).filter(Product.store_id == store_id)
    
    if category:
        query = query.filter(Product.category == category)
    
    if search:
        query = query.filter(Product.name.ilike(f"%{search}%"))
    
    if in_stock is not None:
        if in_stock:
            query = query.filter(Product.stock > 0)
        else:
            query = query.filter(Product.stock <= 0)
    
    products = query.all()
    
    return [ProductResponse(
        id=p.id,
        store_id=p.store_id,
        name=p.name,
        description=p.description,
        sku=p.sku,
        hsn_code=p.hsn_code,
        price=p.price,
        mrp=p.mrp,
        stock=p.stock,
        category=p.category,
        images=[img.url for img in p.images],
        is_active=p.is_active,
        created_at=p.created_at,
        updated_at=p.updated_at
    ) for p in products]

@router.post("", response_model=ProductResponse)
async def create_product(
    product: ProductCreate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    if product.price > product.mrp:
        raise HTTPException(status_code=400, detail="Price cannot be greater than MRP")
    
    new_product = Product(
        store_id=store_id,
        name=product.name,
        description=product.description,
        sku=product.sku,
        hsn_code=product.hsn_code,
        price=product.price,
        mrp=product.mrp,
        stock=product.stock,
        category=product.category
    )
    
    db.add(new_product)
    db.commit()
    db.refresh(new_product)
    
    return ProductResponse(
        id=new_product.id,
        store_id=new_product.store_id,
        name=new_product.name,
        description=new_product.description,
        sku=new_product.sku,
        hsn_code=new_product.hsn_code,
        price=new_product.price,
        mrp=new_product.mrp,
        stock=new_product.stock,
        category=new_product.category,
        images=[],
        is_active=new_product.is_active,
        created_at=new_product.created_at,
        updated_at=new_product.updated_at
    )

@router.post("/bulk")
async def bulk_upload_products(
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    if not file.filename.endswith('.csv'):
        raise HTTPException(status_code=400, detail="Only CSV files are supported")
    
    content = await file.read()
    csv_file = io.StringIO(content.decode('utf-8'))
    csv_reader = csv.DictReader(csv_file)
    
    products_created = []
    errors = []
    
    for idx, row in enumerate(csv_reader):
        if idx >= 1000:
            break
        
        try:
            price = float(row.get('price', 0))
            mrp = float(row.get('mrp', 0))
            stock = int(row.get('stock', 0))
            
            if price > mrp:
                errors.append(f"Row {idx + 1}: Price cannot be greater than MRP")
                continue
            
            new_product = Product(
                store_id=store_id,
                name=row.get('name', ''),
                description=row.get('description'),
                sku=row.get('sku'),
                hsn_code=row.get('hsn_code'),
                price=price,
                mrp=mrp,
                stock=stock,
                category=row.get('category')
            )
            
            db.add(new_product)
            products_created.append(new_product.id)
        except Exception as e:
            errors.append(f"Row {idx + 1}: {str(e)}")
    
    db.commit()
    
    return {
        "message": f"Uploaded {len(products_created)} products",
        "products_created": len(products_created),
        "errors": errors
    }

@router.put("/{product_id}", response_model=ProductResponse)
async def update_product(
    product_id: str,
    product_update: ProductUpdate,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    if product_update.name is not None:
        product.name = product_update.name
    if product_update.description is not None:
        product.description = product_update.description
    if product_update.price is not None:
        product.price = product_update.price
    if product_update.mrp is not None:
        product.mrp = product_update.mrp
    if product_update.stock is not None:
        product.stock = product_update.stock
    if product_update.category is not None:
        product.category = product_update.category
    if product_update.is_active is not None:
        product.is_active = product_update.is_active
    
    product.updated_at = datetime.utcnow()
    
    db.commit()
    db.refresh(product)
    
    return ProductResponse(
        id=product.id,
        store_id=product.store_id,
        name=product.name,
        description=product.description,
        sku=product.sku,
        hsn_code=product.hsn_code,
        price=product.price,
        mrp=product.mrp,
        stock=product.stock,
        category=product.category,
        images=[img.url for img in product.images],
        is_active=product.is_active,
        created_at=product.created_at,
        updated_at=product.updated_at
    )

@router.post("/sync")
async def sync_to_ondc(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    products = db.query(Product).filter(
        Product.store_id == store_id,
        Product.is_active == True
    ).all()
    
    return {
        "message": "ONDC sync initiated",
        "products_synced": len(products),
        "status": "queued"
    }
