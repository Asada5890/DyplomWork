from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from api import auth, product, admin, cart, profile, orders
from db.session import init



app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
)

app.mount("/frontend", StaticFiles(directory="frontend"), name="frontend")

# Сначала добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:8000"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Затем подключаем роутеры

app.include_router(auth.router, prefix='', tags=["auth"]) # Ауентификация
app.include_router(product.router, prefix='', tags=["products"]) # Продукты
app.include_router(admin.router, prefix='', tags=["admin"]) # Админка
app.include_router(cart.router, prefix='', tags=["cart"]) # Корзина
app.include_router(profile.router, prefix='', tags=["profile"]) # Профиль
app.include_router(orders.router, prefix='', tags=["orders"]) # Заявки



# Инициализация БД
init()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)