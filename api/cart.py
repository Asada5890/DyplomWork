# from fastapi import FastAPI, Request, Depends
# from fastapi.templating import Jinja2Templates
# from fastapi.responses import HTMLResponse

# from pydantic import BaseModel
# from typing import List

# router = FastAPI()

# # Настройка Jinja2
# templates = Jinja2Templates(directory="frontend")





# # Модели для товаров и корзины

# class CartItem(BaseModel):
#     product_name: str
#     product_description: str
#     price: float
#     quantity: int
#     product_img: str


# # Данные для корзины (пример)
# cart_items = [
#     CartItem(
#         product_name="Товар 1",
#         product_description="Описание товара 1",
#         price=1500,
#         quantity=2,
#         product_img="/static/img/product1.jpg"
#     ),
#     CartItem(
#         product_name="Товар 2",
#         product_description="Описание товара 2",
#         price=3000,
#         quantity=1,
#         product_img="/static/img/product2.jpg"
#     ),
# ]


# # Страница корзины
# @router.get("/cart", response_class=HTMLResponse)
# async def cart(request: Request):
#     total_count = sum(item.quantity for item in cart_items)
#     total_price = sum(item.price * item.quantity for item in cart_items)
#     total_with_delivery = total_price  # Бесплатная доставка

#     return templates.TemplateResponse(
#         "cart.html",
#         {
#             "request": request,
#             "cart_items": cart_items,
#             "total_count": total_count,
#             "total_price": total_price,
#             "total_with_delivery": total_with_delivery
#         }
#     )
