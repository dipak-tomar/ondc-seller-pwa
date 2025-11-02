from fastapi import APIRouter, HTTPException, Depends
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.schemas.auth import OTPRequest, OTPVerify, Token, UserResponse
from app.models.database import db, User, Store
from app.core.security import create_access_token, generate_otp, verify_token
from datetime import datetime, timedelta

router = APIRouter(prefix="/auth", tags=["auth"])
security = HTTPBearer()

@router.post("/request-otp")
async def request_otp(request: OTPRequest):
    if not request.email and not request.phone:
        raise HTTPException(status_code=400, detail="Email or phone required")
    
    otp = generate_otp()
    key = request.email or request.phone
    
    db.otp_store[key] = {
        "otp": otp,
        "expires_at": datetime.utcnow() + timedelta(minutes=10)
    }
    
    print(f"OTP for {key}: {otp}")
    
    return {"message": "OTP sent successfully", "otp": otp}

@router.post("/verify-otp", response_model=Token)
async def verify_otp(request: OTPVerify):
    key = request.email or request.phone
    
    if key not in db.otp_store:
        raise HTTPException(status_code=400, detail="OTP not found or expired")
    
    stored_otp = db.otp_store[key]
    
    if datetime.utcnow() > stored_otp["expires_at"]:
        del db.otp_store[key]
        raise HTTPException(status_code=400, detail="OTP expired")
    
    if stored_otp["otp"] != request.otp:
        raise HTTPException(status_code=400, detail="Invalid OTP")
    
    del db.otp_store[key]
    
    user = None
    for u in db.users.values():
        if u.email == request.email or u.phone == request.phone:
            user = u
            break
    
    if not user:
        user_id = db.generate_id()
        user = User(
            id=user_id,
            email=request.email,
            phone=request.phone
        )
        db.users[user_id] = user
        
        store_id = db.generate_id()
        store = Store(
            id=store_id,
            user_id=user_id,
            name=f"{request.email or request.phone}'s Store"
        )
        db.stores[store_id] = store
    
    access_token = create_access_token(data={"sub": user.id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/refresh", response_model=Token)
async def refresh_token(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if user_id not in db.users:
        raise HTTPException(status_code=404, detail="User not found")
    
    access_token = create_access_token(data={"sub": user_id})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/logout")
async def logout():
    return {"message": "Logged out successfully"}

@router.get("/me", response_model=UserResponse)
async def get_current_user(credentials: HTTPAuthorizationCredentials = Depends(security)):
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if user_id not in db.users:
        raise HTTPException(status_code=404, detail="User not found")
    
    user = db.users[user_id]
    return UserResponse(
        id=user.id,
        email=user.email,
        phone=user.phone,
        name=user.name,
        plan=user.plan
    )

def get_current_user_id(credentials: HTTPAuthorizationCredentials = Depends(security)) -> str:
    payload = verify_token(credentials.credentials)
    if not payload:
        raise HTTPException(status_code=401, detail="Invalid token")
    
    user_id = payload.get("sub")
    if user_id not in db.users:
        raise HTTPException(status_code=404, detail="User not found")
    
    return user_id
