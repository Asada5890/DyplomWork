from datetime import datetime, timedelta, timezone
from typing import Union
import jwt
from models.token import Token
from models.user import User
from repositories.user_repository import select_user_by_email  # Импортируем функцию для выборки пользователя по email
from fastapi import HTTPException, status
import core.settings as settings  # Импортируем настройки

class UserNotFound(Exception):
    """
    Своя ошибка, если пользователь не был найден
    """
    pass


class AuthService:
    """
    Класс для аутентификации пользователей и работы с токенами доступа.
    """

    def create_access_token(self, data: dict, ) -> str:
        """
        Создает JWT токен доступа.

        :param data: Данные, которые будут закодированы в токене (например, email пользователя).
        :param expires_delta: Время жизни токена (timedelta).
        :return: Закодированный JWT токен в виде строки.
        """
        to_encode = data.copy()  # Копируем данные для кодирования
        expire = datetime.now(timezone.utc) + settings.EXPIRES_DELTA  # Устанавливаем время истечения токена
        to_encode.update({"exp": expire})  # Добавляем время истечения в данные токена
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)  # Кодируем токен
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
            raise UserNotFound(
                "Личная ошибка"
            )

        access_token = self.create_access_token(
            data={"email": user.email, "password": user.password},  # Данные для токена
        )
        return Token(access_token=access_token, token_type="bearer", access_token_expires=str(settings.EXPIRES_DELTA))
