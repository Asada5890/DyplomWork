from pydantic import BaseModel, EmailStr

class CreateUser(BaseModel):
    name: str
    surname: str
    last_name: str
    email: EmailStr
    phone_number: str
    password: str