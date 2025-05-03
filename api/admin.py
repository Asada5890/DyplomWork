from fastapi import APIRouter, Request, Form, Depends
from fastapi.responses import HTMLResponse, RedirectResponse
from fastapi.templating import Jinja2Templates
from db.mongo import products
from schemas.product import Product
from services.product_service import ProductService
from services.user_service import UserService

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


@router.get("/admin/products", response_class=HTMLResponse)
def get_products(request: Request):
    all_products = list(products.find({}))
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
