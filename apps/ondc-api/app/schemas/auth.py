from pydantic import BaseModel, EmailStr
from typing import Optional

class OTPRequest(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None

class OTPVerify(BaseModel):
    email: Optional[EmailStr] = None
    phone: Optional[str] = None
    otp: str

class Token(BaseModel):
    access_token: str
    token_type: str = "bearer"

class UserResponse(BaseModel):
    id: str
    email: Optional[str] = None
    phone: Optional[str] = None
    name: Optional[str] = None
    plan: str
