
from pydantic import BaseSettings, Field
from typing import ClassVar

class Settings(BaseSettings):
    # MongoDB
    MONGODB_URL: str = Field(default="mongodb://localhost:27017", env="MONGODB_URL")
    MONGODB_DB_NAME: str = Field(default="my_database", env="MONGODB_DB_NAME")
    
    # SQLite (если нужно)
    SQLITE_DB_URL: ClassVar[str] = "sqlite:///./sql_app.db"
    
    class Config:
        env_file = ".env"
        case_sensitive = False

settings = Settings()