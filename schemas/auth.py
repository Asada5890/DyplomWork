from pydantic import BaseModel


class AuthSub(BaseModel):
    id: int


class Token(BaseModel):
    access_token: str
    refresh_token: str
    token_type: str


class UserResponse(BaseModel):
    access_token: str
    refresh_token: str
