from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
from fastapi.middleware.cors import CORSMiddleware
from api import user, auth  # Импортируем роутеры

# Создаем экземпляр приложения
app = FastAPI()

# Настраиваем CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Подключаем роутеры
app.include_router(user.router, prefix="/api/users")
app.include_router(auth.router, prefix="/api/auth")

# Настраиваем статические файлы
app.mount("/static", StaticFiles(directory="static"), name="static")