from pymongo import ReturnDocument
from bson import ObjectId
from fastapi import HTTPException, status, Depends
from decimal import Decimal
from schemas.cart import Cart, CartItem
from models.user import User
from db import session, mongo

class CartService:
    def __init__(self, mongo_db, session):
        self.carts = mongo_db.carts
        self.products = mongo_db.products
        self.session = session

    def _get_user(self, user_id: int):
        user = self.session.query(User).get(user_id)
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Пользователь не найден"
            )
        return user

    def _get_product(self, product_id: str):
        product = self.products.find_one({"_id": ObjectId(product_id)})
        if not product:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден"
            )
        return product

    def get_cart(self, user_id: int) -> Cart:
        user = self._get_user(user_id)
        cart = self.carts.find_one({"user_id": user.id})
        
        if not cart:
            return Cart(user_id=user.id, items=[])
            
        # Конвертация MongoDB document в Pydantic модель
        return Cart(**cart)

    def add_to_cart(self, user_id: int, product_id: str, quantity: int = 1) -> Cart:
        user = self._get_user(user_id)
        product = self._get_product(product_id)
        
        # Обновление корзины с атомарной операцией
        updated_cart = self.carts.find_one_and_update(
            {"user_id": user.id},
            {
                "$push": {
                    "items": {
                        "product_id": product_id,
                        "quantity": quantity
                    }
                },
                "$inc": {"total_price": product["price"] * quantity}
            },
            upsert=True,
            return_document=ReturnDocument.AFTER
        )
        
        return Cart(**updated_cart)

    def update_item(self, user_id: int, product_id: str, new_quantity: int) -> Cart:
        user = self._get_user(user_id)
        product = self._get_product(product_id)
        
        # Находим текущее количество
        cart = self.get_cart(user.id)
        current_item = next((i for i in cart.items if i.product_id == product_id), None)
        
        if not current_item:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден в корзине"
            )
        
        # Вычисляем разницу для обновления общей суммы
        price_diff = (new_quantity - current_item.quantity) * product["price"]
        
        updated_cart = self.carts.find_one_and_update(
            {"user_id": user.id, "items.product_id": product_id},
            {
                "$set": {"items.$.quantity": new_quantity},
                "$inc": {"total_price": price_diff}
            },
            return_document=ReturnDocument.AFTER
        )
        
        return Cart(**updated_cart)

    def remove_item(self, user_id: int, product_id: str) -> Cart:
        user = self._get_user(user_id)
        product = self._get_product(product_id)
        
        # Получаем текущую корзину для расчета
        cart = self.get_cart(user.id)
        item_to_remove = next((i for i in cart.items if i.product_id == product_id), None)
        
        if not item_to_remove:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="Товар не найден в корзине"
            )
        
        # Обновляем корзину
        updated_cart = self.carts.find_one_and_update(
            {"user_id": user.id},
            {
                "$pull": {"items": {"product_id": product_id}},
                "$inc": {"total_price": -item_to_remove.quantity * product["price"]}
            },
            return_document=ReturnDocument.AFTER
        )
        
        return Cart(**updated_cart) if updated_cart else Cart(user_id=user.id)

    def clear_cart(self, user_id: int) -> None:
        user = self._get_user(user_id)
        self.carts.delete_one({"user_id": user.id})




def get_cart_service(mongo_db=Depends(mongo), session=Depends(session)):
    return CartService(mongo_db=mongo_db, session=session)
