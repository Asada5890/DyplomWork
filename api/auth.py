from fastapi import APIRouter, HTTPException, Depends
from schemas.auth import Token
from schemas.user import UserCreate
from services.auth_service import AuthService
from services.user_service import UserService, UniqueViolation

router = APIRouter()


@router.post("/register", response_model=Token)
def register(user_data: UserCreate,
             auth_service: AuthService = Depends(),
             user_service: UserService = Depends()) -> Token:
    try:
        user = user_service.create_user(user_data)
        return auth_service.register(user)
    except (UniqueViolation,) as error:
        raise HTTPException(detail=str(error), status_code=400)

# TODO:
# @router.post("/login", response_model=UserResponse)
# @router.post("/logout", response_model=UserResponse)
# @router.post("/me", response_model=UserResponse)
