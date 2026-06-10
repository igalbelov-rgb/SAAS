from fastapi import FastAPI
from app.database import init_db
from api.auth import router as auth_router

app = FastAPI(
    title="Affiliate AI SaaS API",
    version="1.0.0",
    docs_url="/docs",
    openapi_url="/openapi.json"
)

@app.on_event("startup")
def on_startup():
    print("🚀 Initializing Database and creating tables...")
    init_db()
    print("✅ Database tables verification complete.")

# חיבור הראוטר של האותנטיקציה
app.include_router(auth_router)

@app.get("/api/health")
def health_check():
    return {"status": "healthy", "message": "Backend is up and running!"}