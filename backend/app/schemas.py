# ימנע שגיאות של טיפוסי נתונים ויאבטח את ה-API
from pydantic import BaseModel, HttpUrl
from typing import List, Optional, Dict

# --- בקשה שמתקבלת מה-Frontend ---
class ProductScrapeRequest(BaseModel):
    url: str  # הלינק שהמשתמש הזין בתיבת הטקסט

# --- מבנה הקופי של ה-AI שיחזור לפרונט ---
class AICopywriting(BaseModel):
    telegram: str
    facebook: str
    pinterest: str

# --- תשובה שחוזרת ל-Frontend לאחר סריקה והפקת AI ---
class ProductScrapeResponse(BaseModel):
    id: Optional[int] = None  # 🔥 הוסף את השורה הזו בראש המודל!
    success: bool
    title: str
    imageUrl: Optional[str] = None
    description: Optional[str] = None
    specs: List[str] = []
    sourceUrl: str
    aiCopy: AICopywriting
    error: Optional[str] = None

    class Config:
        from_attributes = True # מאפשר ל-Pydantic לקרוא מודלים של SQLAlchemy בצורה חלקה
    
class ProductPublishSchema(BaseModel):
    product_id: int
    custom_message: Optional[str] = None
    
class ProductPublishRequest(BaseModel):
    product_id: int  # 🔥 זה מה שהפרונטאנד שולח כעת
    title: str
    imageUrl: str
    content: str
    
class ProductPublishResponse(BaseModel):
    status: str
    message: str
    product_id: int