from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from database import get_db
from models.create_user import CreateUser
from models.userdto import UserDTO
from services.user_service import UserService

router = APIRouter()


@router.post('/', response_model=UserDTO)
def create_user(
        user_data: CreateUser,
        db: Session = Depends(get_db),
        user_service: UserService = Depends()
):
    try:
        return user_service.create_user(user_data, db)
    except Exception as error:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=str(error)
        )
