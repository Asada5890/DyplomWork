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
from fastapi import FastAPI, Request, HTTPException
from bson.errors import InvalidId
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import ORJSONResponse

from api import auth
from db.session import init
from motor.motor_asyncio import AsyncIOMotorClient
from pymongo import MongoClient
from core.settings import settings
from bson import ObjectId


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

templates = Jinja2Templates(directory="frontend")
client = MongoClient(settings.MONGODB_URL, port=settings.MONGODB_PORT)
db = client[settings.MONGODB_DB_NAME]
collection = db[settings.MONGODB_COLLECTION_NAME]

@app.get("/", response_class=HTMLResponse)
def read_products(request: Request):
    products = list(collection.find())
    for product in products:
        product["_id"] = str(product["_id"])
    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products
    })


@app.get("/product/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: str):
    try:
        # Конвертируем строку в ObjectId
        obj_id = ObjectId(product_id.strip())
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    # Ищем продукт
    product = collection.find_one({"_id": obj_id})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Конвертируем ObjectId в строку
    product["_id"] = str(product["_id"])
    
    return templates.TemplateResponse(
        "product.html",
        {"request": request, "product": product}
    )

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)