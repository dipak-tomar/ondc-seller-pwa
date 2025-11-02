from pydantic_settings import BaseSettings
from typing import Optional

class Settings(BaseSettings):
    PROJECT_NAME: str = "ONDC Seller Booster API"
    VERSION: str = "1.0.0"
    API_V1_STR: str = "/api/v1"
    
    SECRET_KEY: str = "your-secret-key-change-in-production"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24 * 7  # 7 days
    
    DATABASE_URL: str = "postgresql+psycopg://ondc:ondc_dev_password@localhost:5432/ondc_seller"
    
    REDIS_HOST: str = "localhost"
    REDIS_PORT: int = 6379
    REDIS_URL: str = "redis://localhost:6379/0"
    
    S3_ENDPOINT_URL: Optional[str] = "http://localhost:9000"
    S3_ACCESS_KEY: str = "minioadmin"
    S3_SECRET_KEY: str = "minioadmin123"
    S3_BUCKET_NAME: str = "ondc-products"
    S3_REGION: str = "us-east-1"
    
    TWILIO_ACCOUNT_SID: Optional[str] = None
    TWILIO_AUTH_TOKEN: Optional[str] = None
    TWILIO_WHATSAPP_FROM: Optional[str] = None
    
    POSTMARK_API_KEY: Optional[str] = None
    POSTMARK_FROM_EMAIL: str = "noreply@ondcseller.com"
    
    RAZORPAY_KEY_ID: Optional[str] = None
    RAZORPAY_KEY_SECRET: Optional[str] = None
    
    ONDC_SELLER_APP_URL: Optional[str] = None
    ONDC_SELLER_APP_KEY: Optional[str] = None
    
    SENTRY_DSN: Optional[str] = None
    ENABLE_TELEMETRY: bool = False
    
    class Config:
        case_sensitive = True
        env_file = ".env"

settings = Settings()
