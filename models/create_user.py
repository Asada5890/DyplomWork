from pydantic import BaseModel

class CreateUser(BaseModel):
    name: str
    surname: str
    last_name: str
    email: str
    phone_number: str
    password: str