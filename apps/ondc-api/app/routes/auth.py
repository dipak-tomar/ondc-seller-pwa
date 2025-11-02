from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from sqlalchemy.orm import Session
from app.schemas.auth import OTPRequest, OTPVerify, Token, UserResponse
from app.db.models import User, Store, OTPStore
from app.db.base import get_db
from app.core.security import create_access_token, generate_otp, verify_token
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

@router.post("/request-otp")
async def request_otp(request: OTPRequest, db: Session = Depends(get_db)):
    if not request.email and not request.phone:
        raise HTTPException(status_code=400, detail="Email or phone required")
    
    otp = generate_otp()
    key = request.email or request.phone
    
    db.query(OTPStore).filter(OTPStore.key == key).delete()
    
    otp_entry = OTPStore(
        key=key,
        otp=otp,
        expires_at=datetime.utcnow() + timedelta(minutes=10)
    )
    db.add(otp_entry)
    db.commit()
    
    print(f"OTP for {key}: {otp}")
    
    return {"message": "OTP sent successfully", "otp": otp}

@router.post("/verify-otp", response_model=Token)
async def verify_otp(request: OTPVerify, db: Session = Depends(get_db)):
    key = request.email or request.phone
    
    otp_entry = db.query(OTPStore).filter(OTPStore.key == key).first()
    
    if not otp_entry:
        raise HTTPException(status_code=400, detail="OTP not found or expired")
    
    if datetime.utcnow() > otp_entry.expires_at:
        db.delete(otp_entry)
        db.commit()
        raise HTTPException(status_code=400, detail="OTP expired")
    
    if otp_entry.otp != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    db.delete(otp_entry)
    db.commit()
    
    user = db.query(User).filter(
        (User.email == request.email) | (User.phone == request.phone)
    ).first()
    
    if not user:
        user = User(
            email=request.email,
            phone=request.phone
        )
        db.add(user)
        db.commit()
        db.refresh(user)
        
        store = Store(
            user_id=user.id,
            name=f"{request.email or request.phone}'s Store"
        )
        db.add(store)
        db.commit()
    
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    access_token = create_access_token(data={"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return UserResponse(
        id=user.id,
        email=user.email,
        phone=user.phone,
        name=user.name,
        plan=user.plan
    )

def get_current_user_id(
    credentials: HTTPAuthorizationCredentials = Depends(security),
    db: Session = Depends(get_db)
) -> str:
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    user = db.query(User).filter(User.id == user_id).first()
    
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_id
