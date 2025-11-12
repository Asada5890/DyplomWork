from fastapi import APIRouter, HTTPException, Depends, Request, Form
from jose import JWTError
import jwt
from requests import Session
from models.order import Order
from db import session
from core.settings import settings
from core.security import get_current_user
from fastapi.templating import Jinja2Templates
from fastapi.responses import HTMLResponse, RedirectResponse
router = APIRouter()


templates = Jinja2Templates(directory="frontend")

@router.get("/profile", response_class=HTMLResponse)
def profile_page(request: Request):
    # Проверяем наличие токена в куках
    token = request.cookies.get("access_token")
    if not token:
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Декодируем токен
        payload = jwt.decode(
            token.replace("Bearer ", ""),
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Извлекаем данные пользователя из payload
        user_email = payload.get("email")  
        user_role = payload.get("role")


        
    except (JWTError, KeyError):
        # Обработка невалидного токена
        response = RedirectResponse(url="/login", status_code=303)
        response.delete_cookie("access_token")
        return response
    
    # Передаем данные в шаблон профиля
    return templates.TemplateResponse(
        "profile.html",
        {
            "request": request,
            "user_email": user_email,
            "user_role": user_role
        }
    )



@router.get("/profile/orders", response_class=HTMLResponse)
async def user_orders(
    request: Request,
    current_user: dict = Depends(get_current_user),
    db: Session = Depends(session.get_db)
):
    if not current_user:
        return RedirectResponse(url="/login")
    
    orders = db.query(Order).filter(
        Order.user_id == current_user["id"]
    ).order_by(Order.created_at.desc()).all()
    
    return templates.TemplateResponse("user_orders.html", {
        "request": request,
        "orders": orders
    })