from fastapi import APIRouter, HTTPException, Request
from sqlalchemy.orm import Session
from app.db.models import WebhookEvent
from app.db.base import get_db
from fastapi import Depends
from datetime import datetime
import json

router = APIRouter(prefix="/webhooks", tags=["webhooks"])

@router.post("/ondc/order")
async def handle_ondc_order_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        payload = await request.json()
        
        webhook_event = WebhookEvent(
            source="ondc",
            event_type="order",
            payload=payload,
            processed=False
        )
        db.add(webhook_event)
        db.commit()
        
        print(f"[WEBHOOK] ONDC order webhook received: {json.dumps(payload)[:200]}")
        
        return {"status": "received", "event_id": webhook_event.id}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Error processing webhook")

@router.post("/ondc/catalog")
async def handle_ondc_catalog_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        payload = await request.json()
        
        webhook_event = WebhookEvent(
            source="ondc",
            event_type="catalog",
            payload=payload,
            processed=False
        )
        db.add(webhook_event)
        db.commit()
        
        print(f"[WEBHOOK] ONDC catalog webhook received: {json.dumps(payload)[:200]}")
        
        return {"status": "received", "event_id": webhook_event.id}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Error processing webhook")

@router.post("/payment/razorpay")
async def handle_razorpay_webhook(
    request: Request,
    db: Session = Depends(get_db)
):
    try:
        payload = await request.json()
        
        webhook_event = WebhookEvent(
            source="razorpay",
            event_type="payment",
            payload=payload,
            processed=False
        )
        db.add(webhook_event)
        db.commit()
        
        print(f"[WEBHOOK] Razorpay webhook received: {json.dumps(payload)[:200]}")
        
        return {"status": "received", "event_id": webhook_event.id}
    except Exception as e:
        print(f"Error processing webhook: {e}")
        raise HTTPException(status_code=500, detail="Error processing webhook")
