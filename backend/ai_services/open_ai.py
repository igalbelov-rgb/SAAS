import json
import logging
from openai import AsyncOpenAI
from app.config import settings
from app.schemas import AICopywriting

logger = logging.getLogger(__name__)

class OpenAIService:
    def __init__(self):
        # אנחנו משתמשים ב-SDK של OpenAI, אבל מנתבים אותו לשרתים החינמיים של Groq!
        self.client = AsyncOpenAI(
            api_key=settings.GROQ_API_KEY, # ודא שאתה מגדיר את זה ב-config וב-env
            base_url="https://api.groq.com/openai/v1" # נקודת הקצה של Groq שתואמת ל-OpenAI
        )
        # משתמשים במודל Llama 3 החזק של Meta, שזמין בחינם ומבין עברית מעולה
        self.model = "llama3-8b-8192"

    async def generate_product_copy(self, title: str, description: str, url: str) -> AICopywriting:
        """
        שולח את פרטי המוצר ל-Groq (תואם OpenAI) ומייצר קופי שיווקי בחינם לחלוטין.
        """
        logger.info("[AI_SERVICE] Sending product to Groq (Free Tier) for copywriting...")
        
        prompt = f"""
        You are an expert social media copywriter for an affiliate marketing SaaS platform.
        Analyze the following product details and generate highly engaging, high-converting marketing copy for Telegram, Facebook, and Pinterest.
        
        Product Title: {title}
        Product Description: {description}
        Product URL: {url}

        Requirements:
        1. 1. Write the content 100% in English (US). Tone should be natural, enthusiastic, catchy, and professional. Emojis are highly recommended.
        2. For Telegram: Short, punchy, bold headline, clear call to action, and include the URL.
        3. For Facebook: Engaging hook, brief mention of top features/specs, and a clear call to action.
        4. For Pinterest: Aesthetic description, keywords focused, clean format.
        
        You must respond ONLY with a raw, valid JSON object matching this structure:
        {{"telegram": "...", "facebook": "...", "pinterest": "..."}}
        """

        try:
            response = await self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": "You are a professional marketing copywriter. You must respond ONLY with a raw, valid JSON object. Do not include any markdown formatting like ```json or intro text."},
                    {"role": "user", "content": prompt}
                ],
                # חלק ממודלי Groq לא תומכים ב-response_format קשיח, אז נבקש JSON ישירות בטקסט
                temperature=0.6
            )

            raw_content = response.choices[0].message.content.strip()
            
            # ניקוי תגיות markdown אם המודל בטעות הוסיף אותן
            if raw_content.startswith("```"):
                raw_content = raw_content.split("\n", 1)[1].rsplit("\n", 1)[0].strip()
                if raw_content.startswith("json"):
                    raw_content = raw_content[4:].strip()

            data = json.loads(raw_content)

            return AICopywriting(
                telegram=data.get("telegram", f"🔥 מבצע מטורף! {title}\nלינק: {url}"),
                facebook=data.get("facebook", f"תראו מה מצאנו עבורכם! ✨\n{title}"),
                pinterest=data.get("pinterest", f"{title} - השראה ועיצוב. מקור: {url}")
            )

        except Exception as e:
            logger.error(f"[AI_SERVICE] Failed to generate free AI copy: {str(e)}")
            # מנגנון הגנה (Fallback) אסתטי בעברית
            return AICopywriting(
                telegram=f"🔥 מבצע חם שאסור לפספס! 🔥\n\n🎧 {title}\n⚡ המלאי מוגבל, מהרו לתפוס.\n\n📌 לינק ישיר לרכישה: {url}",
                facebook=f"מחפשים את השדרוג הבא שלכם? ✨\n\nהמוצר {title} עכשיו זמין ובדקנו את המפרט שלו לעומק – פשוט שווה כל שקל.\n\n👇 כנסו ללינק בתגובות לקבלת הנחה מיוחדת!",
                pinterest=f"{title} - כל הפרטים, הסקירה והמפרט הטכני המלא לשנת 2026. מקור: {url}"
            )