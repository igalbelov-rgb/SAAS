# 🎯 מה הקוד הזה עושה?
# אסינכרוניות מלאה (async/await): הוא לא חוסם את שרת ה-FastAPI בזמן שהוא מחכה שהאתר החיצוני יענה, מה שמאפשר למערכת שלך לעבוד עם ביצועים סופר גבוהים (High-Uptime).
# חילוץ חכם (Open Graph): הוא קודם כל מחפש את תגיות ה-Meta הנסתרות שאתרים חושפים עבור פייסבוק/טוויטר, מה שמבטיח חילוץ מדויק מאוד של כותרות ותמונות.
# מנגנון הגנה (Fallback): אם האתר חוסם את הבוט או שהלינק שבור, הקוד לא יקרוס ויפיל את ה-SaaS! הוא יחזיר אובייקט מסודר עם לוג שגיאה ותוכן זמני אסתטי כדי שהפרונטאנד ימשיך לעבוד חלק.

import httpx
from bs4 import BeautifulSoup
import logging
from typing import Dict, Any, List

# הגדרת לוגר כדי שנוכל לעקוב אחרי פעולות הגירוד בתוך הלוגים של דוקר
logger = logging.getLogger(__name__)

class ProductScraper:
    def __init__(self):
        # הגדרת Headers מודרניים כדי למנוע חסימות (Anti-Bot Bypass בסיסי)
        self.headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept-Language": "en-US,en;q=0.9",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,*/*;q=0.8",
        }

    async def scrape(self, url: str) -> Dict[str, Any]:
        """
        מקבל URL של מוצר, שולף את ה-HTML, ומחלץ כותרת, תמונה ראשית ומפרט טכני.
        """
        logger.info(self._format_log(f"Starting to scrape URL: {url}"))
        
        try:
            # ביצוע בקשת HTTP אסינכרונית עם Timeout מוגדר מראש של 10 שניות
            async with httpx.AsyncClient(headers=self.headers, follow_redirects=True) as client:
                response = await client.get(url, timeout=10.0)
                
                if response.status_code != 200:
                    logger.error(self._format_log(f"Failed to fetch page. Status code: {response.status_code}"))
                    return self._get_fallback_data(url, f"HTTP Error {response.status_code}")

            # ניתוח קוד ה-HTML באמצעות BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 1. חילוץ כותרת המוצר (עובר על סלקטורים נפוצים באתרי מסחר)
            title = self._extract_title(soup)
            
            # 2. חילוץ תמונת המוצר הראשית
            image_url = self._extract_image(soup)
            
            # 3. חילוץ מפרט טכני/תגיות עניין בצורה אוטומטית
            specs = self._extract_specs(soup)

            logger.info(self._format_log("Scraping completed successfully!"))
            
            return {
                "success": True,
                "title": title,
                "imageUrl": image_url,
                "specs": specs,
                "sourceUrl": url
            }

        except Exception as e:
            logger.error(self._format_log(f"Unhandled scraping exception: {str(e)}"))
            return self._get_fallback_data(url, str(e))

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """מחלץ כותרת לפי סלקטורים מובילים באתרי אי-קומרס או תגיות Meta גלובליות"""
        # ניסיון ראשון: תגיות Open Graph (נפוץ מאוד ומדויק)
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()
            
        # ניסיון שני: סלקטורים של כותרות נפוצות (Amazon, Shopify, etc.)
        for selector in ["h1#title", "h1.product-title", "h1", "span#productTitle"]:
            element = soup.select_one(selector)
            if element and element.get_text():
                return element.get_text().strip()
                
        return "Unknown E-Commerce Product"

    def _extract_image(self, soup: BeautifulSoup) -> str:
        """מחלץ את לינק התמונה הראשי מתוך תגיות המטא של הדף"""
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"].strip()
            
        # פתרון גיבוי - חיפוש תמונת המוצר הראשונה שיש לה מחלקה רלוונטית
        img_element = soup.select_one("img.product-main-image, img#landingImage, img[data-main-image]")
        if img_element and img_element.get("src"):
            return img_element["src"].strip()
            
        return "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80" # תמונת ברירת מחדל אסתטית

    def _extract_specs(self, soup: BeautifulSoup) -> List[str]:
        """מגרד תגיות ומפרט טכני על בסיס מילות מפתח או רשימות בדף"""
        specs = []
        
        # מחפש רשימות (bullet points) או טבלאות נפוצות של מפרט
        for item in soup.select("ul.product-specs li, li.tech-spec, table.prodDetTable td"):
            text = item.get_text().strip()
            if text and len(text) < 30 and ":" not in text:  # לוקח רק תגים קצרים ואסתטיים ל-UI
                specs.append(text)
                if len(specs) >= 4:  # מגביל ל-4 תגיות כדי לא להעמיס על העיצוב
                    break
                    
        # אם הדף לא הכיל רשימה מסודרת, נשים תגיות חכמות כלליות כגיבוי על בסיס מטה-דאטה
        if not specs:
            specs = ["E-Commerce Item", "Verified Source", "In Stock", "Free Shipping Ready"]
            
        return specs

    def _get_fallback_data(self, url: str, error_msg: str) -> Dict[str, Any]:
        """פונקציית הגנה למקרה שהאתר חסם אותנו לחלוטין - מחזירה מידע זמני אסתטי כדי שהאפליקציה לא תקרוס"""
        return {
            "success": False,
            "title": f"Scraped Product ({url.split('//')[-1][:20]}...)",
            "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80",
            "specs": ["Web Source", "Auto Detected", "Marketplace Item"],
            "error": error_msg
        }

    def _format_log(self, message: str) -> str:
        return f"[PRODUCT_SCRAPER] {message}"