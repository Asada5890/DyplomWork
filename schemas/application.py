from typing import List, Optional
from pydantic import BaseModel

class ApplicationCreate(BaseModel):
    user_id: int
    status: str
    description: Optional[str] = None
    product_ids: List[str]  # Список ID товаров из MongoDB

class ApplicationResponse(ApplicationCreate):
    id: int
    created_at: str
    updated_at: Optional[str]