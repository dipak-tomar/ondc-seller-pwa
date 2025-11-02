from app.core.config import settings
from typing import Optional

class NotificationService:
    def __init__(self):
        self.twilio_configured = bool(settings.TWILIO_ACCOUNT_SID and settings.TWILIO_AUTH_TOKEN)
        self.postmark_configured = bool(settings.POSTMARK_API_KEY)
    
    async def send_whatsapp(self, to: str, message: str) -> bool:
        if not self.twilio_configured:
            print(f"[STUB] WhatsApp to {to}: {message}")
            return True
        
        try:
            from twilio.rest import Client
            client = Client(settings.TWILIO_ACCOUNT_SID, settings.TWILIO_AUTH_TOKEN)
            
            message = client.messages.create(
                from_=f'whatsapp:{settings.TWILIO_WHATSAPP_FROM}',
                body=message,
                to=f'whatsapp:{to}'
            )
            
            return message.sid is not None
        except Exception as e:
            print(f"Error sending WhatsApp: {e}")
            return False
    
    async def send_email(self, to: str, subject: str, body: str) -> bool:
        if not self.postmark_configured:
            print(f"[STUB] Email to {to}: {subject}")
            return True
        
        try:
            import httpx
            
            response = await httpx.AsyncClient().post(
                'https://api.postmarkapp.com/email',
                headers={
                    'X-Postmark-Server-Token': settings.POSTMARK_API_KEY,
                    'Content-Type': 'application/json'
                },
                json={
                    'From': settings.POSTMARK_FROM_EMAIL,
                    'To': to,
                    'Subject': subject,
                    'TextBody': body
                }
            )
            
            return response.status_code == 200
        except Exception as e:
            print(f"Error sending email: {e}")
            return False

notification_service = NotificationService()
