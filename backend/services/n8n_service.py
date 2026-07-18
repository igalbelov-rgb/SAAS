import httpx
import logging
from fastapi import HTTPException, status
from app.config import settings

logger = logging.getLogger(__name__)

class N8NAutomationService:
    def __init__(self):
        # אנחנו קוראים ישירות מה-settings המעודכן. 
        # ה-getattr שומר עלינו כפלסטלינה למקרה שהמשתנה לא מוגדר מסיבה כלשהי ב-settings
        self.default_url = getattr(
            settings, 
            "N8N_WEBHOOK_URL", 
            "http://saas_n8n_automation:5678/webhook/v1/publish-product"
        )

    async def send_to_pipeline(self, payload: dict, custom_url: str = None) -> bool:
        """משגר payload בצורה אסינכרונית ל-n8n"""
        url = custom_url or self.default_url
        logger.info(f"[N8N_SERVICE] Dispatching payload to n8n Webhook: {url}")
        
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(url, json=payload, timeout=10.0)
                if response.status_code in [200, 201]:
                    return True
                
                logger.error(f"[N8N_SERVICE] n8n returned error status: {response.status_code} - {response.text}")
                raise HTTPException(
                    status_code=status.HTTP_502_BAD_GATEWAY, 
                    detail="Automation engine failed to process request"
                )
            except httpx.RequestError as exc:
                logger.error(f"[N8N_SERVICE] Connection to n8n failed: {exc}")
                raise HTTPException(
                    status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
                    detail="Automation engine (n8n) is unreachable"
                )