import logging
from datetime import datetime
from sqlmodel import Session
from fastapi import HTTPException, status
from app.models import Product
from app.schemas import AICopywriting
from scrapers.product_scraper import ProductScraper
from ai_services.open_ai import OpenAIService

logger = logging.getLogger(__name__)

class ProductService:
    def __init__(self):
        self.scraper = ProductScraper()
        self.ai_service = OpenAIService()

    async def scrape_and_prepare(self, url: str, user_id: int, db: Session):
        """מגרד מוצר, מייצר קופי באמצעות AI ושומר בדאטאבייס"""
        scraped_result = await self.scraper.scrape(url)
        product_title = scraped_result.get("title", "Unknown E-Commerce Product")
        is_success = scraped_result.get("success", False)
        
        mock_ai_copy = None
        if is_success:
            try:
                mock_ai_copy = await self.ai_service.generate_product_copy(
                    title=product_title,
                    description=scraped_result.get("description", ""),
                    url=url
                )
            except Exception as ai_err:
                logger.error(f"[PRODUCT_SERVICE] AI Generation failed, using fallback: {ai_err}")
                mock_ai_copy = AICopywriting(
                    telegram=f"🔥 CRAZY DEAL ALERT! 🔥\n\n🎧 {product_title}\n📌 Link: {url}",
                    facebook=f"Check this out! {product_title}",
                    pinterest=f"{product_title} {url}"
                )

        # שמירה בבסיס הנתונים
        product_id = None
        if is_success:
            try:
                db_product = Product(
                    title=product_title,
                    image_url=scraped_result.get("imageUrl"),
                    source_url=scraped_result.get("sourceUrl", url),
                    description=scraped_result.get("description"),
                    ai_generated_review=mock_ai_copy.telegram if mock_ai_copy else None, 
                    user_id=user_id
                )
                db.add(db_product)
                db.commit()
                db.refresh(db_product)
                product_id = db_product.id
            except Exception as db_err:
                db.rollback()
                logger.error(f"[PRODUCT_SERVICE] DB save failed: {str(db_err)}")

        return product_id, is_success, product_title, scraped_result, mock_ai_copy

    def mark_as_published(self, product_id: int, content: str, db: Session) -> Product:
        """עדכון סטטוס המוצר במערכת לאחר פרסום"""
        product = db.get(Product, product_id)
        if not product:
            raise HTTPException(status_code=404, detail="Product not found in database.")
        
        product.ai_generated_review = content
        product.is_published = True
        product.published_at = datetime.utcnow()
        
        db.add(product)
        db.commit()
        db.refresh(product)
        return product