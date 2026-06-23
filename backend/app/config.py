import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# טעינת קובץ ה-.env.production שנמצא בתיקיית האם של app
load_dotenv(dotenv_path=os.path.join(os.path.dirname(__file__), '..', '.env.production'))

class Settings(BaseSettings):
    DATABASE_URL: str = os.getenv("DATABASE_URL")
    JWT_SECRET_KEY: str = os.getenv("JWT_SECRET_KEY")
    JWT_ALGORITHM: str = os.getenv("JWT_ALGORITHM", "HS256")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES", 60))
    GROQ_API_KEY: str = os.getenv("GROQ_API_KEY")
    TELEGRAM_TOKEN: str = os.getenv("TELEGRAM_TOKEN")
    TELEGRAM_CHAT_ID: str = os.getenv("TELEGRAM_CHAT_ID")
    # הכתובת הפנימית של n8n בתוך ה-Docker Network 🔌
    N8N_WEBHOOK_URL: str = os.getenv("N8N_WEBHOOK_URL", "http://saas_n8n_automation:5678/webhook/v1/publish-product")
    
settings = Settings()