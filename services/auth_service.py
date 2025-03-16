from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from models.token import Token
from models.user import User
from repositories.user_repository import select_user_by_email  # Импортируем функцию для выборки пользователя по email
from fastapi import HTTPException, status
import settings  # Импортируем настройки

class UserAuth:
    """
    Класс для аутентификации пользователей и работы с токенами доступа.
    """

    def create_access_token(self, data: dict, expires_delta: timedelta) -> str:
        """
        Создает JWT токен доступа.

        :param data: Данные, которые будут закодированы в токене (например, email пользователя).
        :param expires_delta: Время жизни токена (timedelta).
        :return: Закодированный JWT токен в виде строки.
        """
        to_encode = data.copy()  # Копируем данные для кодирования
        expire = datetime.now(timezone.utc) + expires_delta  # Устанавливаем время истечения токена
        to_encode.update({"exp": expire})  # Добавляем время истечения в данные токена
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm="HS256")  # Кодируем токен
        return encoded_jwt

    def decode_token(self, token: str):
        """
        Декодирует JWT токен и возвращает его содержимое.

        :param token: JWT токен в виде строки.
        :return: Декодированные данные токена.
        """
        # TODO: Реализовать декодирование токена
        pass

    def login_for_access_token(self, email: str, password: str) -> Token:
        """
        Проверяет учетные данные пользователя и создает токен доступа.

        :param email: Электронная почта пользователя.
        :param password: Пароль пользователя.
        :return: Объект Token с токеном доступа и его типом.
        :raises HTTPException: Если учетные данные неверны.
        """
        user: User = self.validate_user(email, password)  # Проверка введенных данных
      
        if not user:
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Incorrect username or password",  # Сообщение об ошибке
                headers={"WWW-Authenticate": "Bearer"},  # Заголовок для аутентификации
            )
      
        access_token_expires = timedelta(minutes=15)  # Устанавливаем время действия токена
        access_token = self.create_access_token(
            data={"email": user.email, "password": user.password},  # Данные для токена
            expires_delta=access_token_expires  # Время жизни токена
        )
        return Token(access_token=access_token, token_type="bearer", access_token_expires=str(access_token_expires))

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