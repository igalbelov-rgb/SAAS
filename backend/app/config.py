import os
from pydantic import BaseModel
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# טעינה מוקדמת כדי לוודא שהקובץ נגיש
env_path = os.path.join(os.path.dirname(__file__), '..', '.env.production')
load_dotenv(dotenv_path=env_path)

class Settings(BaseSettings):
    DATABASE_URL: str
    JWT_SECRET_KEY: str
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    GROQ_API_KEY: str
    TELEGRAM_TOKEN: str
    TELEGRAM_CHAT_ID: str
    N8N_WEBHOOK_URL: str = "http://saas_n8n_automation:5678/webhook/v1/publish-product"
    
    class Config:
        env_file = ".env.production"
        extra = "ignore" # מתעלם ממשתנים עודפים בקובץ ה-env אם יש
        env_file_encoding = "utf-8" # 🔥 שומר עליך משגיאות קידוד ותומך בתווים מיוחדים
settings = Settings()