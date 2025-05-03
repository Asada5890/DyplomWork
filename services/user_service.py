from typing import Union
from fastapi import Depends
from sqlalchemy.orm import Session

from core.security import get_password_hash, verify_password
from db.session import get_db
from models.user import User
from services.auth_service import AuthService
from schemas.user import UserDTO, UserLogin


class UniqueViolation(Exception):
    pass

class UserDoesNotExist(Exception):
    pass

class UserService:  # Общий класс пользователей
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db

    def create_user(self, user_data) -> UserDTO:
        """
         Создает пользователя,
           принимает параметр user_data:
           логин, пароль, итд 
        """

        # Проверка существующего пользователя
        existing_user = self.db.query(User).filter(
            (User.email == user_data.email)
        ).first()

        if existing_user:
            raise UniqueViolation("User with this email or phone already exists")
        data_to_orm = user_data.dict()
        data_to_orm['password'] = get_password_hash(data_to_orm['password'])
        # Создаем нового пользователя
        db_user = User(**data_to_orm)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return UserDTO.from_orm(db_user)

    def get_all_users(self):
        """
        Отдает всех пользователей
        """
        users = self.db.query(User).all()
        return [UserDTO.from_orm(user) for user in users]
        
    def get_users_count(self):
        """
        Возвращает количество пользователей
        """
        return self.db.query(User).count()
    def get_user_by_id(self, user_id):
        """
        Возвращает пользователя по id 
        """
        return self.db.query(User).filter(User.id == user_id).first()
        

    def update_user_by_user(self, user_id, user_data):
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
    def get_user(self, user_data:UserLogin):
        """
        аунтефикация пользователя 
        """
        existing_user = self.db.query(User).filter(
            User.email == user_data.email).first()
        if existing_user and verify_password(user_data.password, existing_user.password):
            return UserDTO.from_orm(existing_user)
        else:
            raise UserDoesNotExist

    # Взаимодействие админа с пользователями
    def admin_change_user_data(self, user_id, username, surname, email, password=None):
        """
        Изменение данных пользователя админом.
        Если пароль не передан, он не будет обновлен.
        """
        try:
            # Создаем словарь с обновленными данными
            user_data = {"name": username, "surname": surname, "email": email}
            
            # Если передан новый пароль, добавляем его в данные для обновления
            if password:
                user_data["password"] = password

            # Выполняем обновление в базе данных
            result = self.db.query(User).filter(User.id == user_id).update(user_data)
            
            # Сохраняем изменения
            self.db.commit()

            return True
        except Exception as e:
            print("Ошибка обновления пользователя: " + str(e))
            self.db.rollback()  # Откат транзакции в случае ошибки
            return False



    def admin_delete_user(self, user_id):
        """
        Удаление пользователя админом
        """
        try:
            result = self.db.query(User).filter(User.id == user_id).delete()

            self.db.commit()  

            if result:
                return True
            else:
                return False
        except Exception as e:
            self.db.rollback()  
            print("Ошибка удаления пользователя: " + str(e))
            return False
        
   


    # def validate_user(self, email: str, password: str) -> Union[User, bool]:
    #     """
    #     Проверяет, существует ли пользователь с указанными учетными данными.
    #
    #     :param email: Электронная почта пользователя.
    #     :param password: Пароль пользователя.
    #     :return: Объект User, если учетные данные верны, иначе False.
    #     """
    #     user: User = select_user_by_email(email)  # Используем функцию из user_repository для получения пользователя
    #     if user and user.password == password:  # Проверяем, совпадают ли пароль и email
    #         return user  # Возвращаем пользователя, если учетные данные верны
    #     else:
    #         return False  # Возвращаем False, если учетные данные неверны

    # def login_history(self):

    # def select_user_by_email(db: Session, email: str) -> User:
    #     """
    #     поиск пользователя по почте
    #     """
    #     return db.query(User).filter(User.email == email).first()
