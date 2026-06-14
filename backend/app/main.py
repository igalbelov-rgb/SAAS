from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from app.database import init_db
from api.auth import router as auth_router
from api.products import router as products_router

app = FastAPI(
    title="Affiliate AI SaaS API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

# הגדרת CORS - קריטי כדי לאפשר לדפדפן (Frontend) לדבר עם ה-Backend ללא חסימות אבטחה
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.on_event("startup")
def on_startup():
    print("🚀 Initializing Database and creating tables...")
    init_db()
    print("✅ Database tables verification complete.")

# --- חיבור הראוטרים (נתיבי ה-API) ---

# 1. חיבור הראוטר של האותנטיקציה עם הקידומת המלאה שלו
app.include_router(auth_router, prefix="/api/auth", tags=["Authentication"])

# 2. חיבור הראוטר של המוצרים עם הקידומת המלאה שלו
# מכיוון שבתוך api/products.py כבר מוגדר prefix="/products", הוספת /api כאן תיצור בדיוק /api/products
app.include_router(products_router, prefix="/api/products", tags=["Products & Automation"])

# בדיקת תקינות מערכת (Health Check)
@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "Backend is up and running!"}