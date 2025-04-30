# Импорты FastAPI 
from fastapi import FastAPI, Request, HTTPException, APIRouter
from bson.errors import InvalidId
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
from bson import ObjectId
# Локальные импорты 
from db.mongo import products
from services.product_service import ProductService
import frontend
# Определение шаблонов
templates = Jinja2Templates(directory="frontend")

router = APIRouter()

collection = products

@router.get("/", response_class=HTMLResponse, tags="")
def read_products(request: Request):
    products = ProductService().get_all_products()
    for product in products:
        product["_id"] = str(product["_id"])

    return templates.TemplateResponse("index.html", {
        "request": request,
        "products": products,
    })


@router.get("/product/{product_id}", response_class=HTMLResponse)
def product_detail(request: Request, product_id: str):
    try:
        # Конвертируем строку в ObjectId
        obj_id = ObjectId(product_id)
    except InvalidId:
        raise HTTPException(status_code=400, detail="Invalid product ID format")
    
    # Ищем продукт
    product = ProductService().get_one_product({"_id": obj_id})
    
    if not product:
        raise HTTPException(status_code=404, detail="Product not found")
    
    # Конвертируем ObjectId в строку
    product["_id"] = str(product["_id"])
    
    return templates.TemplateResponse(
        "product.html",
        {"request": request, "product": product}
    )
