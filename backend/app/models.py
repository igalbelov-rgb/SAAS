from datetime import datetime
from typing import Optional, List
from sqlmodel import SQLModel, Field, Relationship

# --- 1. מודל משתמש (User) ---
class User(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    email: str = Field(unique=True, index=True, nullable=False)
    hashed_password: str = Field(nullable=False)
    full_name: Optional[str] = Field(default=None)
    is_active: bool = Field(default=True)
    is_admin: bool = Field(default=False)
    created_at: datetime = Field(default_factory=datetime.utcnow)

    # קשר חנות: למשתמש יכולים להיות הרבה מוצרים בחנות שלו
    products: List["Product"] = Relationship(back_populates="owner")


# --- 2. מודל מוצר (Product) ---
class Product(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    title: str = Field(index=True, nullable=False)
    description: Optional[str] = Field(default=None)
    
    # 🔥 התיקון כאן: משתמשים בסינטקס הטבעי של SQLModel ומאפשרים None (שזה Null ב-DB)
    original_price: Optional[float] = Field(default=None, nullable=True)
    affiliate_url: Optional[str] = Field(default=None, nullable=True) # הקישור שממנו מרוויחים כסף
    
    image_url: Optional[str] = Field(default=None)
    
    # שדות קריטיים עבור ה-AI והאוטומציה
    category: Optional[str] = Field(default="General", index=True)
    ai_generated_review: Optional[str] = Field(default=None) # התוכן האוטומטי שהבוט ייצר
    
    # השדות המעודכנים והחדשים עבור טלגרם 🤖
    is_published: bool = Field(default=False) 
    published_at: Optional[datetime] = Field(default=None)
    telegram_message_id: Optional[str] = Field(default=None) 
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # מפתח זר המקשר למשתמש שהוסיף את המוצר
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="products")