from pydantic import BaseModel

class Token(BaseModel):
    access_token: str
    token_type: str
    access_token_expires: str