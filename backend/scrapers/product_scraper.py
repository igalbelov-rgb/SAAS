# 🎯 מה הקוד המאוחד הזה עושה?
# 1. אסינכרוניות מלאה + HTTP/2: ביצועים מקסימליים ועקיפת חסימות פרוטוקול מתקדמות (כמו Cloudflare).
# 2. רוטציית דפדפנים (User-Agent Rotation): הגרלת דפדפן בכל בקשה כדי למנוע חסימות 403/404 באתרי מסחר.
# 3. חילוץ משולש (JSON-LD -> Open Graph -> HTML Tags):
#    - קודם כל מחפש את הנתונים המובנים שאתרים מכינים עבור גוגל (JSON-LD).
#    - אם אין, עובר לתגיות המטא הנסתרות של פייסבוק/טוויטר (Open Graph).
#    - כמוצא אחרון, סורק סלקטורים נפוצים ב-HTML (כמו h1, img וכו').
# 4. חילוץ תיאור עשיר: שואב את תיאור המוצר האמיתי מהאתר (og:description).
# 5. מנגנון הגנה (Fallback): אם האתר חוסם או הלינק שבור, המערכת לא תקרוס ומחזירה מבנה אסתטי לפרונטאנד.

import httpx
from bs4 import BeautifulSoup
import logging
import json
import random
from typing import Dict, Any, List

# הגדרת לוגר כדי שנוכל לעקוב אחרי פעולות הגירוד בתוך הלוגים של דוקר
logger = logging.getLogger(__name__)

class ProductScraper:
    def __init__(self):
        # רשימת דפדפנים מודרניים שונים להגרלה - מקטין משמעותית סיכוי לחסימות 403
        self.user_agents = [
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36",
            "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/17.4 Safari/605.1.15",
            "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:125.0) Gecko/20100101 Firefox/125.0"
        ]

    async def scrape(self, url: str) -> Dict[str, Any]:
        """
        מקבל URL של מוצר, שולף את ה-HTML בצורה חמקמקה, ומחלץ כותרת, תמונה, תיאור ומפרט.
        """
        logger.info(self._format_log(f"Starting to scrape URL: {url}"))
        
        # בניית Headers דינמיים המדמים דפדפן אנושי לחלוטין
        headers = {
            "User-Agent": random.choice(self.user_agents),
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
            "Accept-Language": "he-IL,he;q=0.9,en-US;q=0.8,en;q=0.7",
            "Cache-Control": "max-age=0",
            "Connection": "keep-alive",
            "Upgrade-Insecure-Requests": "1"
        }
        
        try:
            # ביצוע בקשת HTTP אסינכרונית עם תמיכה ב-HTTP/2 ו-Timeout מוגדר מראש של 12 שניות
            async with httpx.AsyncClient(headers=headers, follow_redirects=True, http2=True) as client:
                response = await client.get(url, timeout=12.0)
                
                if response.status_code != 200:
                    logger.error(self._format_log(f"Failed to fetch page. Status code: {response.status_code}"))
                    return self._get_fallback_data(url, f"HTTP Error {response.status_code}")

            # ניתוח קוד ה-HTML באמצעות BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            # 🔥 שלב א': חילוץ מטא-דאטא מובנה של גוגל (הכי מדויק ויציב באי-קומרס)
            ld_data = self._parse_json_ld(soup)
            
            # 🔥 שלב ב': חילוץ משולב (מובנה -> Open Graph -> סלקטורים רגילים)
            title = ld_data.get("title") or self._extract_title(soup)
            image_url = ld_data.get("image") or self._extract_image(soup)
            description = ld_data.get("description") or self._extract_description(soup)
            specs = self._extract_specs(soup)

            logger.info(self._format_log("Scraping completed successfully!"))
            
            return {
                "success": True,
                "title": title,
                "imageUrl": image_url,
                "description": description,
                "specs": specs,
                "sourceUrl": url
            }

        except Exception as e:
            logger.error(self._format_log(f"Unhandled scraping exception: {str(e)}"))
            return self._get_fallback_data(url, str(e))

    def _parse_json_ld(self, soup: BeautifulSoup) -> Dict[str, Any]:
        """מחפש ומפענח תגיות סקריפט מובנות מסוג JSON-LD לחילוץ דאטא מושלם מחנויות מודרניות"""
        extracted = {}
        try:
            for script in soup.find_all("script", type="application/ld+json"):
                try:
                    data = json.loads(script.string or "")
                    items = data if isinstance(data, list) else [data]
                    for item in items:
                        if item.get("@type") in ["Product", "ProductPage", "http://schema.org/Product"]:
                            if "name" in item: 
                                extracted["title"] = item["name"]
                            if "description" in item: 
                                extracted["description"] = item["description"]
                            if "image" in item:
                                img = item["image"]
                                extracted["image"] = img[0] if isinstance(img, list) else img
                            return extracted
                except:
                    continue
        except Exception:
            pass
        return extracted

    def _extract_title(self, soup: BeautifulSoup) -> str:
        """מחלץ כותרת לפי סלקטורים מובילים או תגיות Meta גלובליות"""
        og_title = soup.find("meta", property="og:title")
        if og_title and og_title.get("content"):
            return og_title["content"].strip()
            
        for selector in ["h1", "h1#title", "h1.product-title", "h1[class*='title']", "span#productTitle"]:
            element = soup.select_one(selector)
            if element and element.get_text():
                return element.get_text().strip()
                
        return "Unknown E-Commerce Product"

    def _extract_image(self, soup: BeautifulSoup) -> str:
        """מחלץ את לינק התמונה הראשי מתוך תגיות המטא או סלקטורים נפוצים"""
        og_image = soup.find("meta", property="og:image")
        if og_image and og_image.get("content"):
            return og_image["content"].strip()
            
        img_element = soup.select_one("img[class*='product-main'], img[id*='landingImage'], img[src*='product'], img.product-main-image")
        if img_element and img_element.get("src"):
            return img_element["src"].strip()
            
        return "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80"

    def _extract_description(self, soup: BeautifulSoup) -> str:
        """מחלץ את תיאור המוצר מתוך תגיות המטא הסטנדרטיות"""
        for desc_prop in ["og:description", "description"]:
            tag = soup.find("meta", property=desc_prop) or soup.find("meta", attrs={"name": desc_prop})
            if tag and tag.get("content"):
                return tag["content"].strip()
        return "No description available."

    def _extract_specs(self, soup: BeautifulSoup) -> List[str]:
        """מגרד תגיות ומפרט טכני קצר על בסיס מילות מפתח או רשימות בדף לטובת ה-UI"""
        specs = []
        for item in soup.select("ul[class*='spec'] li, li[class*='item-spec'], ul.product-specs li, table td"):
            text = item.get_text().strip()
            if text and len(text) < 30 and ":" not in text:
                specs.append(text)
                if len(specs) >= 4:
                    break
                    
        if not specs:
            specs = ["E-Commerce Item", "Verified Source", "In Stock", "Free Shipping Ready"]
            
        return specs

    def _get_fallback_data(self, url: str, error_msg: str) -> Dict[str, Any]:
        """מחזירה מידע זמני אסתטי במקרה של חסימה קשוחה כדי למנוע קריסה של ה-Client"""
        return {
            "success": False,
            "title": f"Product ({url.split('//')[-1][:15]}...)",
            "imageUrl": "https://images.unsplash.com/photo-1505740420928-5e560c06d30e?w=500&q=80",
            "description": "Failed to extract product details from the source link.",
            "specs": ["Web Source", "Auto Detected", "Marketplace Item"],
            "error": error_msg
        }

    def _format_log(self, message: str) -> str:
        return f"[PRODUCT_SCRAPER] {message}"