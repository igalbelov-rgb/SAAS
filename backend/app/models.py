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
    original_price: float = Field(nullable=False)
    affiliate_url: str = Field(nullable=False) # הקישור שממנו מרוויחים כסף
    image_url: Optional[str] = Field(default=None)
    
    # שדות קריטיים עבור ה-AI והאוטומציה
    category: Optional[str] = Field(default="General", index=True)
    ai_generated_review: Optional[str] = Field(default=None) # התוכן האוטומטי שהבוט ייצר
    is_published: bool = Field(default=True)
    
    created_at: datetime = Field(default_factory=datetime.utcnow)
    
    # מפתח זר המקשר למשתמש שהוסיף את המוצר (או שהבוט הוסיף עבורו)
    owner_id: Optional[int] = Field(default=None, foreign_key="user.id")
    owner: Optional[User] = Relationship(back_populates="products")