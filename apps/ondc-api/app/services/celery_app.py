from celery import Celery
from app.core.config import settings

celery_app = Celery(
    'ondc_seller',
    broker=settings.REDIS_URL,
    backend=settings.REDIS_URL
)

celery_app.conf.update(
    task_serializer='json',
    accept_content=['json'],
    result_serializer='json',
    timezone='UTC',
    enable_utc=True,
)

@celery_app.task(name='sync_products_to_ondc')
def sync_products_to_ondc(store_id: str, product_ids: list):
    print(f"[CELERY TASK] Syncing {len(product_ids)} products from store {store_id} to ONDC")
    return {"status": "completed", "synced": len(product_ids)}

@celery_app.task(name='process_bulk_upload')
def process_bulk_upload(store_id: str, file_path: str):
    print(f"[CELERY TASK] Processing bulk upload for store {store_id}: {file_path}")
    return {"status": "completed"}

@celery_app.task(name='send_order_notification')
def send_order_notification(order_id: str, notification_type: str):
    print(f"[CELERY TASK] Sending {notification_type} notification for order {order_id}")
    return {"status": "sent"}
