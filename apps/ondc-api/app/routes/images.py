from fastapi import APIRouter, HTTPException, Depends, UploadFile, File
from sqlalchemy.orm import Session
from app.db.models import Product, ProductImage, Store
from app.db.base import get_db
from app.routes.auth import get_current_user_id
from app.services.s3 import s3_service
from app.services.image import image_service
from pydantic import BaseModel

router = APIRouter(prefix="/images", tags=["images"])

def get_user_store_id(user_id: str, db: Session) -> str:
    store = db.query(Store).filter(Store.user_id == user_id).first()
    if not store:
        raise HTTPException(status_code=404, detail="Store not found")
    return store.id

class PresignedUrlRequest(BaseModel):
    product_id: str
    filename: str

class PresignedUrlResponse(BaseModel):
    upload_url: str
    object_key: str
    image_url: str

@router.post("/presign", response_model=PresignedUrlResponse)
async def get_presigned_url(
    request: PresignedUrlRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    product = db.query(Product).filter(Product.id == request.product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    object_key = s3_service.generate_unique_key(request.filename, prefix=f"products/{request.product_id}")
    
    upload_url = s3_service.generate_presigned_url(object_key, expiration=3600, http_method='PUT')
    
    if s3_service.s3_client._endpoint.host:
        image_url = f"{s3_service.s3_client._endpoint.host}/{s3_service.bucket_name}/{object_key}"
    else:
        image_url = f"https://{s3_service.bucket_name}.s3.{s3_service.s3_client.meta.region_name}.amazonaws.com/{object_key}"
    
    return PresignedUrlResponse(
        upload_url=upload_url,
        object_key=object_key,
        image_url=image_url
    )

@router.post("/products/{product_id}/upload")
async def upload_product_image(
    product_id: str,
    file: UploadFile = File(...),
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    file_content = await file.read()
    
    is_valid, message = image_service.validate_image(file_content)
    if not is_valid:
        raise HTTPException(status_code=400, detail=message)
    
    optimized_content = image_service.resize_image(file_content)
    
    object_key = s3_service.generate_unique_key(file.filename, prefix=f"products/{product_id}")
    
    image_url = s3_service.upload_file(optimized_content, object_key, content_type=file.content_type)
    
    product_image = ProductImage(
        product_id=product_id,
        url=image_url,
        is_primary=len(product.images) == 0
    )
    db.add(product_image)
    db.commit()
    
    return {
        "message": "Image uploaded successfully",
        "image_url": image_url,
        "product_id": product_id
    }

@router.delete("/products/{product_id}/images/{image_id}")
async def delete_product_image(
    product_id: str,
    image_id: str,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    store_id = get_user_store_id(user_id, db)
    
    product = db.query(Product).filter(Product.id == product_id).first()
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    if product.store_id != store_id:
        raise HTTPException(status_code=403, detail="Not authorized")
    
    image = db.query(ProductImage).filter(ProductImage.id == image_id).first()
    
    if not image or image.product_id != product_id:
        raise HTTPException(status_code=404, detail="Image not found")
    
    object_key = image.url.split('/')[-1]
    s3_service.delete_file(f"products/{product_id}/{object_key}")
    
    db.delete(image)
    db.commit()
    
    return {"message": "Image deleted successfully"}
