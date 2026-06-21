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
    success: bool
    title: str
    imageUrl: str
    description: Optional[str] = None  # 🔥 תוספת קריטית כדי לתמוך בשדה התיאור שחילצנו
    specs: List[str]
    sourceUrl: str
    aiCopy: AICopywriting  # אובייקט מקונן המכיל את שלוש הפלטפורמות
    error: Optional[str] = None