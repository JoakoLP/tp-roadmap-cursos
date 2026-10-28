import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    ENVIRONMENT: str = os.getenv("ENVIRONMENT", "development")
    BACKEND_PORT: int = int(os.getenv("BACKEND_PORT", "8000"))
    DATABASE_URL: str = os.getenv("DATABASE_URL", "postgresql+psycopg://postgres:postgres@localhost:5432/roadmap_db")
    SECRET_KEY: str = os.getenv("SECRET_KEY", "dev-insecure-secret-key-32-chars-min!!")

    class Config:
        env_file = ".env"
        extra = "ignore"

settings = Settings()
