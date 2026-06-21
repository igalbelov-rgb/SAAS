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
    OPENAI_API_KEY: str = os.getenv("OPENAI_API_KEY")

settings = Settings()