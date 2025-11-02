from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.routes.auth import get_current_user_id

router = APIRouter(prefix="/notify", tags=["notifications"])

class WhatsAppNotification(BaseModel):
    phone: str
    message: str

class EmailNotification(BaseModel):
    email: str
    subject: str
    body: str

@router.post("/whatsapp/order")
async def send_whatsapp_notification(
    notification: WhatsAppNotification,
    user_id: str = Depends(get_current_user_id)
):
    print(f"WhatsApp notification to {notification.phone}: {notification.message}")
    
    return {
        "message": "WhatsApp notification sent (stub)",
        "phone": notification.phone
    }

@router.post("/email/order")
async def send_email_notification(
    notification: EmailNotification,
    user_id: str = Depends(get_current_user_id)
):
    print(f"Email notification to {notification.email}: {notification.subject}")
    
    return {
        "message": "Email notification sent (stub)",
        "email": notification.email
    }
