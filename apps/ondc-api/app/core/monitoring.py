import sentry_sdk
from sentry_sdk.integrations.fastapi import FastApiIntegration
from app.core.config import settings

def init_monitoring():
    if settings.SENTRY_DSN:
        sentry_sdk.init(
            dsn=settings.SENTRY_DSN,
            integrations=[FastApiIntegration()],
            traces_sample_rate=1.0,
            environment="production" if not settings.DEBUG else "development"
        )
        print("Sentry monitoring initialized")
    else:
        print("Sentry monitoring not configured (SENTRY_DSN not set)")
