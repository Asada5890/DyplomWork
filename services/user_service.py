from typing import Union
from fastapi import Depends
from sqlalchemy.orm import Session
from models.user import User
from models.create_user import CreateUser
from models.userdto import UserDTO
from database import get_db
from auth_service import AuthService
from repositories.user_repository import select_user_by_email


class UserService: # Общий класс пользователей 
    def __init__(self, db : Session = Depends(get_db), auth_service : AuthService = Depends()):
        self.db = db 
        self.auth_service = auth_service

    def create_user(self, user_data):
        """
         Создает пользователя,
           принимает параметр user_data:
           логин, пароль, итд 
        """

        # Проверка существующего пользователя
        existing_user = self.db.query(User).filter(
            (User.email == user_data.email) | 
            (User.phone_number == user_data.phone_number)
        ).first()
        
        if existing_user:
            raise ValueError("User with this email or phone already exists")
        
        # Создаем нового пользователя
        db_user = User(**user_data.dict())
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        
        return UserDTO(
            id=db_user.id,
            name=db_user.name,
            surname=db_user.surname,
            last_name=db_user.last_name,
            email=db_user.email,
            phone_number=db_user.phone_number
        )

    def get_users(self):
        """
        Отдает всех пользователей
        """
        pass

    def get_user_by_id(self):
        """
        Возвращает пользователя по id 
        """
        pass

    def update_user(self, user_id, user_data):
        """
        Изменяет данные пользователя 
        user_id - принимает id пользователя для которого хотим применить изменения 
        user_data - логин, пароль, итд 
        """
        pass

    def change_password(self, user_id, uesr_data):
        """
        user_id - принимает id пользователя для которого хотим применить изменения пароля 
        user_data - логин, пароль, итд. Чтобы понять что за пользователей и проверить чтобы новый пароль не совпадал с новым 
        """
        pass

    def register_user(self):
        """
        регистрация пользователя 
        """
        pass
    
    def login_user(self):
        """
        аунтефикация пользователя 
        """
        pass



    def validate_user(self, email: str, password: str) -> Union[User , bool]:
        """
        Проверяет, существует ли пользователь с указанными учетными данными.

        :param email: Электронная почта пользователя.
        :param password: Пароль пользователя.
        :return: Объект User, если учетные данные верны, иначе False.
        """
        user: User = select_user_by_email(email)  # Используем функцию из user_repository для получения пользователя
        if user and user.password == password:  # Проверяем, совпадают ли пароль и email
            return user  # Возвращаем пользователя, если учетные данные верны
        else:
            return False  # Возвращаем False, если учетные данные неверны
    # def login_history(self):

    def select_user_by_email(db: Session, email: str) -> User:
        """
        поиск пользователя по почте
        """
        return db.query(User).filter(User.email == email).first()
