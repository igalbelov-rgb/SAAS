# בקובץ הזה אנחנו נחבר את ה-ProductScraper שבנינו קודם, נקבל את הלינק, ונחזיר את המידע המעובד יחד עם Mock AI דמה (בשלב הבא נחבר את ה-AI האמיתי מתוך ai_services)

from fastapi import APIRouter, HTTPException, Depends
from app.schemas import ProductScrapeRequest, ProductScrapeResponse, AICopywriting
from scrapers.product_scraper import ProductScraper
import logging

logger = logging.getLogger(__name__)

# יצירת ה-Router עבור ישויות המוצרים
router = APIRouter(tags=["Products & Automation"])

# אתחול מחלקת הסריקה שבנינו במיילסטון הקודם
scraper = ProductScraper()

@router.post("/scrape", response_model=ProductScrapeResponse)
async def scrape_product_endpoint(payload: ProductScrapeRequest):
    """
    מקבל URL של מוצר, מפעיל את הבוט המגרד, ומייצר קופי ראשוני עבור הרשתות החברתיות.
    """
    logger.info(f"[PRODUCTS_API] Received scrape request for URL: {payload.url}")
    
    # 1. הפעלת מנוע הגירוד האסינכרוני
    scraped_result = await scraper.scrape(payload.url)
    
    # 2. יצירת לוגיקת AI זמנית (Mock AI) עד שנחבר את OpenAI/Anthropic במיילסטון הבא
    # המטרה: שהפרונטאנד יקבל מידע חי ומעוצב על בסיס המוצר האמיתי שנסרק!
    product_title = scraped_result.get("title", "Awesome Product")
    
    mock_ai_copy = AICopywriting(
        telegram=f"🔥 CRAZY DEAL ALERT! 🔥\n\n🎧 {product_title} is now available!\n⚡ Limited time offer, don't miss out.\n\n📌 Link: {payload.url}",
        facebook=f"Looking for the best quality? ✨\n\nWe just analyzed {product_title} and the specs are top-notch. Perfect for daily use and highly recommended by our team.\n\n👇 Check the link in the comments for a special discount!",
        pinterest=f"{product_title} - Full specs, review, and dynamic setup ideas for 2026. Source: {payload.url}"
    )
    
    # 3. החזרת המבנה המלא והמאומת ישירות ל-Frontend
    return ProductScrapeResponse(
        success=scraped_result.get("success", False),
        title=product_title,
        imageUrl=scraped_result.get("imageUrl"),
        specs=scraped_result.get("specs", []),
        sourceUrl=scraped_result.get("sourceUrl", payload.url),
        aiCopy=mock_ai_copy,
        error=scraped_result.get("error")
    )

@router.post("/publish")
async def publish_pipeline_endpoint(payload: dict):
    """
    נקודת קצה זמנית לטיפול בשיגור - תתחבר ישירות ל-n8n בהמשך Milestone B
    """
    logger.info(f"[PRODUCTS_API] Dispatching payload to automation pipeline: {payload}")
    return {"status": "success", "message": "Dispatched to n8n pipeline queue"}