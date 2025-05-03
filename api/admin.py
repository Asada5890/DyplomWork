from fastapi import APIRouter, Request, Form
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.mongo import products
from schemas.product import Product

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

@router.get("/admin/", response_class=HTMLResponse)
def admin_page(request: Request):
    return templates.TemplateResponse("admin.html", {"request": request})

@router.post("/admin/add-product", response_class=HTMLResponse)
def add_product(
    request: Request,
    name: str = Form(...),
    articul: str = Form(...),
    price: float = Form(...),
    category: str = Form(...),
    img: str = Form(""),
    description: str = Form("")
):
    product_data = {
        "name": name,
        "articul": articul,
        "price": price,
        "category": category,
        "img": img,
        "description": description,
    }

    # Валидация через Pydantic
    try:
        product = Product(**product_data)
        products.insert_one(product.dict())
        message = "Товар успешно добавлен!"
    except Exception as e:
        message = f"Ошибка: {str(e)}"

    return templates.TemplateResponse("admin.html", {"request": request, "message": message})
