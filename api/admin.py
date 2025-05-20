from fastapi import APIRouter, Request, Form, Depends, HTTPException
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from jose import JWTError
import jwt
import json
from sqlalchemy.orm import joinedload
from bson import ObjectId
from services.product_service import ProductService
from requests import Session
from streamlit import status
from core.security import get_current_user
from db.mongo import products
from db.session import get_db
from models.order import Order
from schemas.product import Product
from services.product_service import ProductService
from services.user_service import UserService
from core.settings import settings

router = APIRouter()
templates = Jinja2Templates(directory="frontend")

@router.get("/admin/", response_class=HTMLResponse)
def admin_page(request: Request):
    token = request.cookies.get("access_token")
    if not token:
        # Если нет токена - редирект на логин
        return RedirectResponse(url="/login", status_code=303)
    
    try:
        # Декодируем токен
        payload = jwt.decode(
            token.replace("Bearer ", ""),
            settings.SECRET_KEY,
            algorithms=[settings.JWT_ALGORITHM]
        )
        
        # Проверяем роль пользователя
        if payload.get("role") != "admin":
            raise HTTPException(status_code=403, detail="Forbidden")
            
    except (JWTError, KeyError):
        # Если ошибка валидации или нет роли - удаляем куку и редиректим
        response = RedirectResponse(url="/login", status_code=303)
        response.delete_cookie("access_token")
        return response
    
    except HTTPException as he:
        # Для обычных пользователей показываем страницу с запретом доступа
        return templates.TemplateResponse(
            "login.html",  # Или специальную страницу access_denied.html
            {
                "request": request,
                "error": "Доступ запрещен. Требуются права администратора"
            },
            status_code=403
        )
    
    return templates.TemplateResponse("admin.html", {"request": request})

#Работа с продуктами

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


@router.get("/admin/products", response_class=HTMLResponse)
def get_products(request: Request):
    all_products = list(products.find({})) #TODO: закинуть в сервисы 
    return templates.TemplateResponse("admin_products.html", {"request": request, "products": all_products})

@router.post("/admin/products/{product_id}", response_class=HTMLResponse)
def delete_product(request: Request, product_id: str, product_service: ProductService = Depends()):
    try:
        is_deleted = product_service.delete_product_by_id(product_id)
        
        if not is_deleted:
            message = "Товар не найден или уже удален."
        else:
            message = "Товар успешно удален!"
    except Exception as e:
        message = f"Ошибка: {str(e)}"
    
    all_products = product_service.get_all_products()
    return templates.TemplateResponse("admin_products.html", {"request": request, "products": all_products, "message": message})

@router.get("/admin/products/edit/{product_id}", response_class=HTMLResponse)
def edit_product(request: Request, product_id: str, product_service: ProductService = Depends()):
    try:
        product = product_service.get_product_by_id(product_id)
        if not product:
            message = "Товар не найден."
            return templates.TemplateResponse("admin_products.html", {"request": request, "message": message})
    except Exception as e:
        message = f"Ошибка: {str(e)}"
        return templates.TemplateResponse("admin_products.html", {"request": request, "message": message})

    return templates.TemplateResponse("edit_product.html", {"request": request, "product": product})


@router.post("/admin/products/edit/{product_id}", response_class=HTMLResponse)
def update_product(request: Request, product_id: str, product_service: ProductService = Depends(),
                   name: str = Form(...), category: str = Form(...), price: float = Form(...), description: str = Form(...)):
    try:

        product = product_service.get_product_by_id(product_id)
        if not product:
            message = "Товар не найден."
            return templates.TemplateResponse("admin_products.html", {"request": request, "message": message})
        
        updated_product = product_service.update_product(product_id, name, category, price, description)
        
        message = "Товар успешно обновлен!"
        return templates.TemplateResponse("edit_product.html", {"request": request, "product": updated_product, "message": message})
    except Exception as e:
        message = f"Ошибка: {str(e)}"
        return templates.TemplateResponse("edit_product.html", {"request": request, "product": product, "message": message})


#Работа с пользователями

@router.get("/admin/users", response_class=HTMLResponse)
def get_users(request: Request, user_service: UserService = Depends()):
    users_count = user_service.get_users_count()  
    try:
        all_users = user_service.get_all_users()  
    except Exception as e:
        message = f"Ошибка: {str(e)}"
        return templates.TemplateResponse("admin_users.html", {"request": request, "message": message, "users_count": users_count})
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": all_users, "users_count": users_count})

@router.post("/admin/users/{user_id}", response_class=HTMLResponse)
def change_user_data(request: Request, user_id: str, user_service: UserService = Depends()):
    try:
        is_deleted = user_service.admin_delete_user(user_id)
        
        if not is_deleted:
            message = "Пользователь не найден или уже удален."
        else:
            message = "Пользователь успешно удален!"
    except Exception as e:
        message = f"Ошибка: {str(e)}"
    
    all_users = user_service.get_all_users()
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": all_users, "message": message})
@router.get("/admin/users/edit/{user_id}", response_class=HTMLResponse)
def edit_user(request: Request, user_id: str, user_service: UserService = Depends()):
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            message = "Пользователь не найден."
            return templates.TemplateResponse("admin_users.html", {"request": request, "message": message})
    except Exception as e:
        message = f"Ошибка: {str(e)}"
        return templates.TemplateResponse("admin_users.html", {"request": request, "message": message})
    return templates.TemplateResponse("edit_user.html", {"request": request, "user": user})

@router.post("/admin/users/edit/{user_id}", response_class=HTMLResponse)
def update_user(
    request: Request,
    user_id: int,  # ID — это int, как в модели
    user_service: UserService = Depends(),
    name: str = Form(...),
    surname: str = Form(...),
    email: str = Form(...),
    password: str = Form(...)
):
    try:
        user = user_service.get_user_by_id(user_id)
        if not user:
            message = "Пользователь не найден."
            return templates.TemplateResponse("admin_users.html", {"request": request, "message": message})
        
        updated_user = user_service.admin_change_user_data(
            user_id, name, surname, email, password
        )
        
        message = "Данные пользователя успешно обновлены!"
        return templates.TemplateResponse("edit_user.html", {"request": request, "user": updated_user, "message": message})
    except Exception as e:
        message = f"Ошибка: {str(e)}"
        return templates.TemplateResponse("edit_user.html", {"request": request, "user": user, "message": message})
    
@router.post("/admin/users/delete/{user_id}", response_class=HTMLResponse)
def delete_user(request: Request, user_id: str, user_service: UserService = Depends()):
    try:
        is_deleted = user_service.admin_delete_user(user_id)
        
        if not is_deleted:
            message = "Пользователь не найден или уже удален."
        else:
            message = "Пользователь успешно удален!"
    except Exception as e:
        message = f"Ошибка: {str(e)}"
    
    all_users = user_service.get_all_users()
    return templates.TemplateResponse("admin_users.html", {"request": request, "users": all_users, "message": message})



@router.get("/admin/orders")
async def admin_orders(
    request: Request,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user is None:
        raise HTTPException(status_code=401, detail="User not authenticated")

    if current_user["role"] != "admin":
        raise HTTPException(status_code=403, detail="You do not have permission to access this resource.")
    

    orders = db.query(Order).options(joinedload(Order.user)).all()

    
    for order in orders:
        print(f"Order {order.id} items: {order.items}")  

    orders_data = []
    for order in orders:
        user_email = order.user.email if order.user else "N/A"
        

        if isinstance(order.items, str):
            order.items = json.loads(order.items)
        

        if isinstance(order.items, list):
            product_ids = [item["product_id"] for item in order.items]

            object_ids = [ObjectId(pid) for pid in product_ids]
            

            product_service = ProductService()
            products = product_service.collection.find({"_id": {"$in": object_ids}})
            print(f"Products found: {list(products)}")  

            product_map = {str(product["_id"]): product["name"] for product in products}
            

            product_names = [
                f'{product_map.get(str(item["product_id"]), "Неизвестный продукт")} (×{item["quantity"]})'
                for item in order.items
            ]
        else:
            product_names = []  
        
        # Формируем данные для шаблона
        products = list(product_service.collection.find({"_id": {"$in": object_ids}}))
        orders_data.append({
            "id": order.id,
            "user_email": user_email,
            "products": product_names,
            "created_at": order.created_at,
            "status": order.status,
            "phone": order.phone,
            "address": order.address,
        })

    # Отправляем данные в шаблон
    return templates.TemplateResponse("admin_orders.html", {
        "request": request,
        "orders": orders_data
    })


@router.get("/admin/orders/{order_id}/update-status")
async def show_update_status_page(
    request: Request,
    order_id: int,
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    # Проверка прав администратора
    if current_user["role"] != "admin":
        raise HTTPException(status_code=403)
    
    # Получаем заказ из базы данных
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(status_code=404)
    
    # Передаем полный объект заказа в шаблон
    return templates.TemplateResponse(
        "admin_order_change_status.html",
        { 
            "request": request,
            "order": order  # Передаем весь объект заказа
        }
    )


@router.post("/admin/orders/{order_id}/update-status")
async def update_order_status(
    order_id: int,
    new_status: str = Form(...),
    db: Session = Depends(get_db),
    current_user: dict = Depends(get_current_user)
):
    if current_user["role"] != "admin":
        raise HTTPException(403)
    if not current_user:
        raise HTTPException(403)
    
    order = db.query(Order).filter(Order.id == order_id).first()
    if not order:
        raise HTTPException(404)
    
    order.status = new_status
    db.commit()
    
    return RedirectResponse(url="/admin/orders", status_code=303)