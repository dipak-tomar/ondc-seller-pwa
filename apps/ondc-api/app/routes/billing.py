from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.orm import Session
from pydantic import BaseModel
from app.routes.auth import get_current_user_id
from app.db.models import User
from app.db.base import get_db

router = APIRouter(prefix="/billing", tags=["billing"])

class SubscriptionRequest(BaseModel):
    plan: str

@router.post("/subscribe")
async def subscribe_to_plan(
    request: SubscriptionRequest,
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    if request.plan not in ["free", "basic", "premium"]:
        raise HTTPException(status_code=400, detail="Invalid plan")
    
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    user.plan = request.plan
    db.commit()
    
    return {
        "message": "Subscription updated (Razorpay stub)",
        "plan": request.plan,
        "payment_link": "https://razorpay.com/payment/stub"
    }

@router.get("/status")
async def get_billing_status(
    user_id: str = Depends(get_current_user_id),
    db: Session = Depends(get_db)
):
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return {
        "plan": user.plan,
        "status": "active"
    }
