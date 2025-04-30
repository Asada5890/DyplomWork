from pydantic import BaseModel

class Product(BaseModel): # Валидация данных для продукта 
    id: int 
    name: str
    description: str
    price: float
    category_id: int

    class Config:
        orm_mode = True
