from fastapi import APIRouter, HTTPException, Depends
from schemas.auth import Token, UserResponse
from schemas.user import UserCreate, UserLogin
from services.auth_service import AuthService
from services.user_service import UserDoesNotExist, UserService, UniqueViolation

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

@router.post("/login", response_model=Token)
def login(user_data: UserLogin,
          user_service: UserService = Depends(),
          auth_service:AuthService  = Depends()) -> Token:
    try:
        user = user_service.get_user(user_data)
        return auth_service.login(user)
    except UserDoesNotExist:
        raise HTTPException(status_code=401, detail="Не правильный логин или пароль") 

# TODO:
# @router.post("/logout", response_model=UserResponse)
# @router.post("/me", response_model=UserResponse)
