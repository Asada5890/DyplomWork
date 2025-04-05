from pydantic import BaseModel

from pydantic import BaseModel, EmailStr

class UserBase(BaseModel):
    email: EmailStr
    name: str
    sur_name: str
    last_name: str | None = None
    phone_number: str | None = None

class UserCreate(UserBase):
    password: str

class UserResponse(UserBase):
    id: str
    is_active: bool

    class Config:
        orm_mode = True
