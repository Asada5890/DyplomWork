from pydantic import BaseModel, EmailStr


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
