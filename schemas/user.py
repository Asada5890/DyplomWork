from pydantic import BaseModel, EmailStr, Field

class UserBase(BaseModel):
    id: int
    email: EmailStr
    name: str
    surname: str


class UserCreate(BaseModel):
    email: EmailStr 
    name: str 
    surname: str 
    password: str 
    phone_number: str 
    role: str = "user"  # Роль по умолчанию - "user"


class UserDTO(BaseModel):
    class Config:
        from_attributes = True
    id: int
    name: str
    surname: str
    email: str
    role: str


class UserLogin(BaseModel):
    email: EmailStr 
    password: str 