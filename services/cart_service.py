from db.mongo import carts
from bson import ObjectId
from schemas.cart import Cart, CartItem
from services.product_service import ProductService

class CartService:
    def __init__(self):
        self.collection = carts
        self.product_service = ProductService()

    def get_user_cart(self, user_id: int):
        """
        Получает корзину пользователя по user_id.
        """
        user_id_str = str(user_id)  # Преобразуем user_id из SQLite (целое число) в строку
        cart = self.collection.find_one({"user_id": user_id_str})
        if not cart:
            return None
        return Cart(**cart)  # Преобразуем результат в объект Cart

    def add_to_cart(self, user_id: int, product_id: str, quantity: int):
        """
        Добавляет товар в корзину или обновляет его количество, если товар уже есть в корзине.
        """
        user_id_str = str(user_id)  # Преобразуем user_id в строку для MongoDB
        # Получаем продукт по идентификатору
        product = self.product_service.get_product_by_id(product_id)
        if not product:
            raise Exception("Продукт не найден")

        # Получаем корзину пользователя
        cart = self.get_user_cart(user_id_str)
        if not cart:
            # Если корзины нет, создаем новую
            cart = Cart(user_id=user_id_str, items=[], total_price=0.0)

        # Проверяем, есть ли товар уже в корзине
        existing_item = next((item for item in cart.items if item.product_id == product_id), None)

        if existing_item:
            # Если товар уже есть в корзине, увеличиваем количество
            existing_item.quantity += quantity
        else:
            # Если товара нет в корзине, добавляем новый товар
            cart.items.append(CartItem(product_id=product_id, quantity=quantity))

        # Обновляем общую цену корзины
        self._update_total_price(cart)

        # Сохраняем корзину в базу данных
        self.collection.update_one(
            {"user_id": user_id_str},
            {"$set": cart.dict()},
            upsert=True  # Если корзины нет, создаем новую
        )

        return cart

    def remove_from_cart(self, user_id: int, product_id: str):
        """
        Удаляет товар из корзины.
        """
        user_id_str = str(user_id)  # Преобразуем user_id в строку для MongoDB
        cart = self.get_user_cart(user_id_str)
        if not cart:
            raise Exception("Корзина не найдена")

        # Удаляем товар из корзины
        cart.items = [item for item in cart.items if item.product_id != product_id]
        
        # Обновляем общую цену корзины
        self._update_total_price(cart)

        # Сохраняем изменения в базу данных
        self.collection.update_one({"user_id": user_id_str}, {"$set": cart.dict()})
        return cart

    def update_total_price(self, cart: Cart):
        """
        Обновляет общую цену корзины.
        """
        total = 0.0
        for item in cart.items:
            product = self.product_service.get_product_by_id(item.product_id)
            total += product["price"] * item.quantity
        cart.total_price = total

    def clear_cart(self, user_id: int):
        """
        Очищает корзину пользователя.
        """
        user_id_str = str(user_id)  # Преобразуем user_id в строку для MongoDB
        self.collection.delete_one({"user_id": user_id_str})
