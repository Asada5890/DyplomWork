# from fastapi import FastAPI
# from fastapi.middleware.cors import CORSMiddleware
# from fastapi.responses import ORJSONResponse

# from api import auth
# from db.session import init





# app = FastAPI(default_response_class=ORJSONResponse,
#               docs_url='/api/openapi',
#               openapi_url='/api/openapi.json',
#               )
# app.include_router(auth.router, prefix='/auth')
# init()

# app.add_middleware(
#     CORSMiddleware,
#     allow_origins=["*"],  # Укажите домен вашего фронтенда
#     allow_credentials=True,
#     allow_methods=["GET", "POST", "PUT", "DELETE"],
#     allow_headers=["*"],)


# if __name__ == "__main__":
#     import uvicorn

#     uvicorn.run(app, host="0.0.0.0", port=8000)


from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api import auth
from db.session import init

app = FastAPI(
    default_response_class=ORJSONResponse,
    docs_url='/api/openapi',
    openapi_url='/api/openapi.json',
)

# Сначала добавляем CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["GET", "POST", "PUT", "DELETE"],
    allow_headers=["*"],
)

# Затем подключаем роутеры
app.include_router(auth.router, prefix='/auth')

# Инициализация БД
init()

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)