from pydantic import BaseModel

class UserDTO(BaseModel):
    id: int
    name: str
    surname: str
    last_name: str
    email: str
    phone_number: str