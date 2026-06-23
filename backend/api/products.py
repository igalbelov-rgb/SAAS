# בקובץ הזה אנחנו נחבר את ה-ProductScraper שבנינו קודם, נקבל את הלינק, ונחזיר את המידע המעובד יחד עם Mock AI דמה (בשלב הבא נחבר את ה-AI האמיתי מתוך ai_services)
import requests
from datetime import datetime
from sqlmodel import Session, select
from fastapi import APIRouter, HTTPException, Depends, status
from fastapi.security import OAuth2PasswordBearer
from app.schemas import ProductScrapeRequest, ProductScrapeResponse, AICopywriting, ProductPublishRequest, ProductPublishResponse
from app.database import get_session
from app.models import Product, User
from app.config import settings
from scrapers.product_scraper import ProductScraper
from app.crypto import verify_access_token 
import logging
import httpx  # 🔥 חובה להוסיף httpx ל-requirements.txt אם אין לך (ספריה לקריאות HTTP אסינכרוניות)

logger = logging.getLogger(__name__)

# יצירת ה-Router עבור ישויות המוצרים
router = APIRouter(tags=["Products & Automation"])
scraper = ProductScraper()  # אתחול מחלקת הסריקה שבנינו במיילסטון הקודם
oauth2_scheme = OAuth2PasswordBearer(tokenUrl="/api/auth/login")  # נקודת קצה לדמיוננו עבור אימות משתמשים (לא בשימוש כרגע)

async def get_current_user(token: str = Depends(oauth2_scheme)):
    """
    מנגנון האבטחה (Middleware/Dependency): 
    מוודא שהמשתמש שולח JWT תקין לפני גישה לנתיבי המוצרים.
    """
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    payload = verify_access_token(token) # הפונקציה שלך מ-crypto.py
    if payload is None:
        raise credentials_exception
    return payload # מחזיר את ה-payload (למשל: user_id, email)

@router.post("/scrape", response_model=ProductScrapeResponse)
async def scrape_product_endpoint(
    payload: ProductScrapeRequest, 
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_session) # 🔥 1. הזרקת ה-Database Session
):
    """
    מקבל URL של מוצר, מפעיל את הבוט המגרד, שומר ב-DB ומייצר קופי ראשוני עבור הרשתות החברתיות.
    """
    logger.info(f"[PRODUCTS_API] Received scrape request for URL: {payload.url}")
    
    # 1. הפעלת מנוע הגירוד האסינכרוני
    scraped_result = await scraper.scrape(payload.url)
    
    product_title = scraped_result.get("title", "Unknown E-Commerce Product")
    is_success = scraped_result.get("success", False)
    
    # 2. יצירת לוגיקת AI זמנית (Mock AI)
    if is_success:
        mock_ai_copy = AICopywriting(
            telegram=f"🔥 CRAZY DEAL ALERT! 🔥\n\n🎧 {product_title} is now available!\n⚡ Limited time offer, don't miss out.\n\n📌 Link: {payload.url}",
            facebook=f"Looking for the best quality? ✨\n\nWe just analyzed {product_title} and the specs are top-notch. Perfect for daily use and highly recommended by our team.\n\n👇 Check the link in the comments for a special discount!",
            pinterest=f"{product_title} - Full specs, review, and dynamic setup ideas for 2026. Source: {payload.url}"
        )
    else:
        mock_ai_copy = AICopywriting(
            telegram=f"⚠️ OOPS! We couldn't scrape the product details from the provided URL. Please check the link and try again.\n\n📌 Link: {payload.url}",
            facebook=f"Unfortunately, we couldn't retrieve the product information from the URL you provided. Please ensure it's a valid e-commerce product page and try again.",
            pinterest=f"Unable to fetch product details from the provided URL. Please verify the link and try again."
        )
    
    # 🔥 3. שמירת המוצר בדאטאבייס כדי שייווצר לו ID אמיתי
    product_id = None
    if is_success:
        try:
            db_product = Product(
                title=product_title,
                image_url=scraped_result.get("imageUrl"),
                source_url=scraped_result.get("sourceUrl", payload.url),
                description=scraped_result.get("description"),
                # שומרים את הקופי של טלגרם כברירת מחדל בשדה ה-Review ב-DB
                ai_generated_review=mock_ai_copy.telegram, 
                user_id=current_user.get("id") # אם יש קשר בין מוצר למשתמש
            )
            db.add(db_product)
            db.commit()
            db.refresh(db_product) # מביא את ה-ID האוטומטי מ-Postgres
            product_id = db_product.id
            logger.info(f"[PRODUCTS_API] Product saved successfully with ID: {product_id}")
        except Exception as db_err:
            db.rollback()
            logger.error(f"[PRODUCTS_API] Database save failed: {str(db_err)}")
            # ממשיכים ולא קורסים, כדי שהמשתמש לפחות יראה את התצוגה המקדימה
    
    # 4. החזרת המבנה המלא והמאומת ישירות ל-Frontend (כולל ה-ID החדש!)
    return ProductScrapeResponse(
        id=product_id, # 🔥 4. הוספת ה-ID ל-Response
        success=is_success,
        title=product_title,
        imageUrl=scraped_result.get("imageUrl"),
        description=scraped_result.get("description"),
        specs=scraped_result.get("specs", ["web source"]),
        sourceUrl=scraped_result.get("sourceUrl", payload.url),
        aiCopy=mock_ai_copy,
        error=scraped_result.get("error")
    )


@router.post("/publish")
async def publish_pipeline_endpoint(payload: dict, current_user: dict = Depends(get_current_user)):
    """
    מקבל את הקופי שנבחר ומזרים אותו ישירות ל-Webhook הפנימי של קונטיינר n8n
    """
    logger.info(f"[PRODUCTS_API] User triggered publish. Payload: {payload}")
    
    # הכתובת הלבנה של n8n בתוך הרשת של דוקר (משתמשת בשם השירות כ-Host ובפורט הפנימי)
    n8n_webhook_url = "http://saas_n8n_automation:5678/webhook/v1/publish-product"
    
    async with httpx.AsyncClient() as client:
        try:
            response = await client.post(n8n_webhook_url, json=payload, timeout=10.0)
            
            if response.status_code >= 400:
                logger.error(f"[PRODUCTS_API] n8n returned an error: {response.status_code} - {response.text}")
                raise HTTPException(status_code=500, detail="Automation engine failed to process request")
                
            return {"status": "success", "message": "Successfully dispatched to social media channels via n8n!"}
            
        except httpx.RequestError as exc:
            logger.error(f"[PRODUCTS_API] Connection to n8n failed: {exc}")
            raise HTTPException(status_code=503, detail="Automation engine (n8n) is unreachable")
        
@router.post("/publish/telegram")
def publish_to_telegram(payload: ProductPublishRequest, db: Session = Depends(get_session)):
    # חיפוש ישיר ומהיר לפי ה-ID שקיבלנו מהפרונט!
    product = db.get(Product, payload.product_id)
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found in database. ")    
    
    product.ai_generated_review = payload.content
        
    if not product.ai_generated_review:
        # גיבוי: אם ה-review הגיע ישירות מהפרונט בתוך payload.content, נשתמש בו במקום להכשיל
        if payload.content:
            product.ai_generated_review = payload.content
        else:
            raise HTTPException(
                status_code=400, 
                detail="Product does not have an AI generated review yet. Generate it first."
            )

    # 3. בניית ה-Payload שנשלח ל-n8n 
    n8n_payload = {
        "productId": product.id,
        "title": product.title,
        "affiliate_url": product.affiliate_url,
        "image_url": product.image_url,
        "body": {
            "aiCopy": {
                "telegram": product.ai_generated_review
            }
        }
    }

    # 3. יריית ה-Webhook לכיוון n8n
    try:
        response = requests.post(settings.N8N_WEBHOOK_URL, json=n8n_payload, timeout=10)
        
        # אם ה-Workflow ב-n8n מוגדר להחזיר תגובה מיידית (נקרא Respond to Webhook)
        # נוכל אפילו לתפוס את ה-message_id שטלגרם מחזיר. 
        # כרגע נניח שהוא פשוט קיבל את זה בצלחה (סטטוס 200/201).
        if response.status_code not in [200, 201]:
            raise HTTPException(
                status_code=status.HTTP_502_BAD_GATEWAY, 
                detail=f"n8n automation responded with error: {response.text}"
            )
            
    except requests.exceptions.RequestException as e:
        raise HTTPException(
            status_code=status.HTTP_503_SERVICE_UNAVAILABLE, 
            detail=f"Failed to connect to n8n automation: {str(e)}"
        )

    # 4. עדכון המוצר בדאטאבייס כ"פורסם"
    product.is_published = True
    product.published_at = datetime.utcnow()
    
    db.add(product)
    db.commit()
    db.refresh(product)

    return {
        "status": "success",
        "message": "Product successfully passed to n8n pipeline and published.",
        "product_id": product.id
    }