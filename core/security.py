from passlib.context import CryptContext
from jose import JWTError, jwt
from datetime import datetime, timedelta
from datetime import datetime, timedelta
from typing import Optional
from fastapi import Depends, HTTPException, status, Request
from fastapi.security import OAuth2PasswordBearer
from jose import JWTError, jwt
from pydantic import BaseModel
from .settings import settings


pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")


def verify_password(plain_password: str, hashed_password: str) -> bool:
    return pwd_context.verify(plain_password, hashed_password)


def get_password_hash(password: str) -> str:
    return pwd_context.hash(password)





oauth2_scheme = OAuth2PasswordBearer(tokenUrl="auth/login")

class TokenData(BaseModel):
    email: Optional[str] = None

async def get_current_user(request: Request):
    token = request.cookies.get("access_token")
    
    if not token:
        return None
    
    try:
        payload = jwt.decode(
            token.split()[1],  # Удаляем 'Bearer '
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        return payload
    except (JWTError, AttributeError):
        return None