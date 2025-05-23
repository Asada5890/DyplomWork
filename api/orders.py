from fastapi import APIRouter, Depends, HTTPException, Query, Request, Form, logger
from fastapi.responses import RedirectResponse, HTMLResponse
from fastapi.templating import Jinja2Templates
from db.redis import redis_client
from core.security import get_current_user
from models.order import Order
from db.session import get_db
from sqlalchemy.orm import Session
from bson import ObjectId
from services.product_service import ProductService
templates = Jinja2Templates(directory="frontend")


router = APIRouter()


@router.get("/checkout", response_class=HTMLResponse)
async def checkout_page(
    request: Request,
    current_user: dict = Depends(get_current_user)
):
    if not current_user:
        return RedirectResponse(url="/login")
    
    user_id = current_user["id"]
    cart_key = f"cart:{user_id}"
    cart_items = redis_client.hgetall(cart_key)
    
    if not cart_items:
        return RedirectResponse(url="/view_cart")

    total_price = 0
    product_service = ProductService()
    items = []
    
    for product_id_str, quantity in cart_items.items():
        product_id = ObjectId(product_id_str)
        product = product_service.get_product_by_id(product_id)
        
        if product:
            item_total = int(quantity) * product["price"]
            total_price += item_total
            
            items.append({
                "product_id": product_id_str,
                "product_name": product["name"],
                "quantity": int(quantity),
                "price": product["price"]
            })

    return templates.TemplateResponse("checkout.html", {
        "request": request,
        "cart_items": items,
        "user": current_user,
        "total_price": total_price  
    })

@router.post("/create_order")
async def create_order(
    request: Request,
    phone: str = Form(...),
    address: str = Form(...),
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(get_db)
):
    if not current_user:
        return RedirectResponse(url="/login", status_code=303)  # 303 для корректной переадресации после POST
    
    user_id = current_user["id"]
    cart_key = f"cart:{user_id}"
    cart_items = redis_client.hgetall(cart_key)
    
    if not cart_items:
        return RedirectResponse(url="/view_cart", status_code=303)
    
    product_service = ProductService()
    valid_items = []
    for product_id, quantity in cart_items.items():
        if product_service.product_exists(ObjectId(product_id)):
            valid_items.append({
                "product_id": product_id,
                "quantity": int(quantity)
            })
    
    if not valid_items:
        return RedirectResponse(url="/view_cart", status_code=303)
    
    try:
        new_order = Order(
            user_id=user_id,
            items=valid_items,
            phone=phone,
            address=address
        )
        db.add(new_order)
        db.commit()
        redis_client.delete(cart_key)
        return RedirectResponse(url="/success_checkout", status_code=303)
    except Exception as e:
        db.rollback()
        logger.error(f"Ошибка: {e}")
        return RedirectResponse(url="/error", status_code=303)
    

@router.get('/success_checkout', response_class=HTMLResponse)
def view_success_checkout(
    request: Request,
):

    return templates.TemplateResponse(
        "success_checkout.html",
        {
            "request": request
        }
    )