import jwt
from fastapi import APIRouter, HTTPException, Request
from fastapi.responses import JSONResponse
from pymongo import MongoClient
from core.settings import settings
from bson.objectid import ObjectId

router = APIRouter()

# Подключение к базе данных MongoDB
server = MongoClient(settings.MONGODB_URL, settings.MONGODB_PORT)
products_db = server[settings.MONGODB_DB_NAME]

# Коллекции
products = products_db[settings.MONGODB_COLLECTION_PRODUCTS]
cart = products_db[settings.MONGODB_COLLECTION_СARTS]

# Функция для получения user_id из JWT токена
def get_user_id_from_cookie(request: Request):
    token = request.cookies.get('access_token')  # Получаем токен из cookies
    
    if not token:
        print("Токен не найден в cookies")  # Лог, если токен отсутствует
        return None
    
    try:
        # Декодируем JWT токен
        payload = jwt.decode(token, settings.SECRET_KEY, algorithms=["HS256"])
        print(f"Декодированный payload: {payload}")  # Лог, чтобы увидеть payload токена
        return payload.get("user_id")  # Предполагаем, что user_id хранится в payload
    except jwt.ExpiredSignatureError:
        print("Токен истек")
        raise HTTPException(status_code=401, detail="Token has expired")
    except jwt.InvalidTokenError:
        print("Неверный токен")
        raise HTTPException(status_code=401, detail="Invalid token")

@router.get("/protected")
async def protected_route(request: Request):
    user_id = get_user_id_from_cookie(request)  # Получаем user_id из токена
    
    if not user_id:
        return {"message": "Hello, user None!"}
    
    # Делаем что-то с user_id, например, показываем информацию о пользователе
    return {"message": f"Hello, user {user_id}!"}
