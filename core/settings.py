from datetime import timedelta

from pydantic_settings import BaseSettings
from pathlib import Path


class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///example.db"
    SECRET_KEY: str = "secret-key-123"
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRES_DAYS: int = 30
    EXPIRES_DELTA: int = 15
    SQLALCHEMY_DATABASE_URL: str = "sqlite:///./example.db"  # or "sqlite:///:memory:"

    class Config:
        env_file = Path(__file__).parent.parent / ".env"


settings = Settings()
