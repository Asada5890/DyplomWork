from pydantic import BaseModel, Field
from typing import List
from uuid import uuid4

class CartItem(BaseModel):
    product_id: str
    quantity: int


class Cart(BaseModel):
    user_id: int
    items: List[CartItem]
    total_price: float = Field(default=0.0)
