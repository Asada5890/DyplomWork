from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker, declarative_base
from core.settings import settings

# Для SQLite
engine = create_async_engine(
    settings.DATABASE_URL,
    future=True,
    connect_args={"check_same_thread": False}
)

# Для PostgreSQL
# engine = create_async_engine(settings.DATABASE_URL)

AsyncSessionLocal = sessionmaker(
    engine,
    class_=AsyncSession,
    expire_on_commit=False
)

Base = declarative_base()

async def get_db():
    async with AsyncSessionLocal() as session:
        yield session