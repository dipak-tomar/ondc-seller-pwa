from fastapi import APIRouter, HTTPException, Depends
from pydantic import BaseModel
from app.routes.auth import get_current_user_id
from app.models.database import db

router = APIRouter(prefix="/billing", tags=["billing"])

class SubscriptionRequest(BaseModel):
    plan: str

@router.post("/subscribe")
async def subscribe_to_plan(
    request: SubscriptionRequest,
    user_id: str = Depends(get_current_user_id)
):
    if request.plan not in ["free", "basic", "premium"]:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    user = db.users[user_id]
    user.plan = request.plan
    
    return {
        "message": "Subscription updated (Razorpay stub)",
        "plan": request.plan,
        "payment_link": "https://razorpay.com/payment/stub"
    }

@router.get("/status")
async def get_billing_status(user_id: str = Depends(get_current_user_id)):
    user = db.users[user_id]
    
    return {
        "plan": user.plan,
        "status": "active"
    }
