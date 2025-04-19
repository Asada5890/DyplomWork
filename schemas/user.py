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


class UserDTO(BaseModel):
    class Config:
        from_attributes = True
    id: int
    name: str
    surname: str
    email: str


class UserLogin(BaseModel):
    email: EmailStr = Field(..., description = "Электронная почта")
    password: str = Field(..., description = "Пароль")  