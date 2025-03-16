from fastapi import APIRouter, Depends, HTTPException, status
from models.token import Token
from models.login import UserLogin
from services.auth_service import UserAuth

router = APIRouter(tags=["Authentication"])

@router.post("/token", response_model=Token)
async def login_for_access_token(
    form_data: UserLogin,
    auth_service: UserAuth = Depends()
):
    try:
        return auth_service.login_for_access_token(
            email=form_data.email,
            password=form_data.password
        )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail=str(e),
            headers={"WWW-Authenticate": "Bearer"},
        )