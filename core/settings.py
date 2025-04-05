# settings.py
import os
from datetime import timedelta

SECRET_KEY = os.getenv("ae028ebe724e67e4979c2c19acb1f75a11e6ed9bd4ba0411d111b9238ed657f6", "your-default-secret-key")
EXPIRES_DELTA = timedelta(15)
ALGORITHM = "HS256"

from pydantic_settings import BaseSettings
from pathlib import Path

class Settings(BaseSettings):
    DATABASE_URL: str = "sqlite:///./example.db"
    SECRET_KEY: str = "secret-key-123"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30

    class Config:
        env_file = Path(__file__).parent.parent / ".env"

settings = Settings()