from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from sqlmodel import Session

from app.database import get_session
from app.crypto import verify_access_token
from app.schemas import ProductScrapeRequest, ProductScrapeResponse, ProductPublishRequest
from app.models import Product

# ייבוא השירותים החדשים
from services.product_service import ProductService
from services.n8n_service import N8NAutomationService

router = APIRouter(tags=["Products & Automation"])
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")

# אתחול השירותים
product_service = ProductService()
n8n_service = N8NAutomationService()

async def get_current_user(token: str = Depends(oauth2_scheme)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token)
    if payload is None:
        raise credentials_exception
    return payload

@router.post("/scrape", response_model=ProductScrapeResponse)
async def scrape_product_endpoint(
    payload: ProductScrapeRequest, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    product_id, is_success, title, scraped_result, ai_copy = await product_service.scrape_and_prepare(
        url=payload.url, 
        user_id=current_user.get("id"), 
        db=db
    )
    
    return ProductScrapeResponse(
        id=product_id,
        success=is_success,
        title=title,
        imageUrl=scraped_result.get("imageUrl"),
        description=scraped_result.get("description"),
        specs=scraped_result.get("specs", ["web source"]),
        sourceUrl=scraped_result.get("sourceUrl", payload.url),
        aiCopy=ai_copy,
        error=scraped_result.get("error")
    )

@router.post("/publish")
async def publish_pipeline_endpoint(payload: dict, current_user: dict = Depends(get_current_user)):
    """מזרים קופי כללי ל-n8n"""
    # כאן השתמשנו בכתובת הספציפית שהגדרת לקונטיינר בדוקר
    container_url = "http://saas_n8n_automation:5678/webhook/v1/publish-product"
    await n8n_service.send_to_pipeline(payload=payload, custom_url=container_url)
    return {"status": "success", "message": "Successfully dispatched via n8n!"}

@router.post("/publish/telegram")
async def publish_to_telegram(
    payload: ProductPublishRequest, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session)
):
    """טוען מוצר, מעדכן לוגיקה, ומשגר לטלגרם דרך n8n (בצורה אסינכרונית)"""
    # 1. שליפת המוצר מה-DB לצורך בניית ה-Payload (מבוצע בתוך ה-Service בשלב הבא)
    product = db.get(Product, payload.product_id)
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in database.")

    # 2. בניית ה-Payload השטוח עבור n8n
    n8n_payload = {
        "productId": product.id,
        "title": product.title,
        "affiliate_url": product.affiliate_url,
        "image_url": product.image_url,
        "aiCopy": {
            "telegram": payload.content or product.ai_generated_review
        }
    }

    # 3. שליחה אסינכרונית ל-n8n (מונע חסימת Threads של השרת)
    await n8n_service.send_to_pipeline(payload=n8n_payload)

    # 4. עדכון סטטוס המוצר בדאטאבייס כ"פורסם"
    product_service.mark_as_published(product_id=product.id, content=payload.content, db=db)

    return {
        "status": "success",
        "message": "Product successfully passed to n8n pipeline and published.",
        "product_id": product.id
    }