from pydantic import BaseModel, HttpUrl, Field
from typing import Optional
from uuid import uuid4

class Product(BaseModel): # Валидация данных для продуктов
    sku: str = Field(default_factory=lambda: str(uuid4()))  # Генерация уникального SKU
    name: str
    articul: str
    price: float
    category: str
    brand: str | None  
    img: Optional[str] = None
    description: Optional[str] = ""