from fastapi import FastAPI, Request, HTTPException
from fastapi.staticfiles import StaticFiles
from bson.errors import InvalidId
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse
from api import auth,product, admin,cart
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
app.include_router(cart.router, prefix='', tags=["cart"]) # корзина



# Инициализация БД
init()


if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)