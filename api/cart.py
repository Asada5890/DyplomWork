from fastapi import APIRouter, HTTPException, Request, Depends, Form
from fastapi.responses import HTMLResponse, JSONResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.redis import redis_client  # Работа с Redis
from core.security import get_current_user  # Для получения текущего пользователя
from services.product_service import ProductService  # Сервис для работы с продуктами
from bson import ObjectId  # Для работы с ObjectId в MongoDB

router = APIRouter()


templates = Jinja2Templates(directory="frontend")
# Роут для добавления товара в корзину
@router.post("/add_to_cart")
async def add_to_cart(
    request: Request,
    product_id: str = Form(...),
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        user_id = current_user["id"]
        cart_key = f"cart:{user_id}"
        redis_client.hincrby(cart_key, product_id, 1)
        
        # Редирект с параметром
        return RedirectResponse(url="/?added_to_cart=true", status_code=303)
    
    except Exception as e:
        return RedirectResponse(url="/error", status_code=500)
# Отображение товаров в корзине
@router.get("/view_cart", response_class=HTMLResponse)
async def view_cart(request: Request, current_user: dict = Depends(get_current_user)):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)

    user_id = current_user.get("id")
    cart_key = f"cart:{user_id}"

    cart_items = redis_client.hgetall(cart_key)

    if not cart_items:
        return templates.TemplateResponse(
            "cart.html", 
            {"request": request, "cart_items": [], "total_price": 0}
        )

    product_service = ProductService()
    items = []
    total_price = 0

    for product_id_str, quantity in cart_items.items():
        product_id = ObjectId(product_id_str)
        product = product_service.get_product_by_id(product_id)
        
        if product:
            items.append({
                "product_id": product_id_str,
                "product_name": product["name"],
                "quantity": int(quantity),
                "price": product["price"]
            })
            total_price += int(quantity) * product["price"]
    
    return templates.TemplateResponse(
        "cart.html", 
        {
            "request": request, 
            "cart_items": items, 
            "total_price": total_price
        }
    )


@router.post("/increase_quantity/{product_id}")
async def increase_quantity(
    product_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        user_id = current_user["id"]
        cart_key = f"cart:{user_id}"
        
        redis_client.hincrby(cart_key, product_id, 1)
        
        return RedirectResponse(url="/view_cart", status_code=303)
    
    except Exception as e:
        return RedirectResponse(url="/error", status_code=500)

@router.post("/decrease_quantity/{product_id}")
async def decrease_quantity(
    product_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        user_id = current_user["id"]
        cart_key = f"cart:{user_id}"
        
        # Получаем текущее количество
        current_quantity = int(redis_client.hget(cart_key, product_id) or 0)
        
        if current_quantity > 1:
            # Уменьшаем количество на 1
            redis_client.hincrby(cart_key, product_id, -1)
        else:
            # Если количество 1 - удаляем товар
            redis_client.hdel(cart_key, product_id)
        
        return RedirectResponse(url="/view_cart", status_code=303)
    
    except Exception as e:
        return RedirectResponse(url="/error", status_code=500)

@router.post("/remove_item/{product_id}")
async def remove_item(
    product_id: str,
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        user_id = current_user["id"]
        cart_key = f"cart:{user_id}"
        
        redis_client.hdel(cart_key, product_id)
        
        return RedirectResponse(url="/view_cart", status_code=303)
    
    except Exception as e:
        return RedirectResponse(url="/error", status_code=500)