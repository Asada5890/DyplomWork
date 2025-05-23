from pymongo import MongoClient
from uuid import uuid4
import random

# Подключение к MongoDB
client = MongoClient("mongodb://localhost:27017/")  # Замени URI, если у тебя другой
db = client["laminate_store"]  # Название БД
collection = db["products"]  # Коллекция товаров

# Примерные данные
categories = ["Сухие смеси", "Краски", "Гипсокартон", "Инструменты", "Изоляция"]
brands = ["Knauf", "Ceresit", "Tikkurila", "Makita", "URSA"]
product_names = [
    "Штукатурка гипсовая Volma Слой 30 кг",
    "Краска фасадная Dufa Expert 10 л",
    "Гипсокартон влагостойкий Lafarge 12.5 мм",
    "Перфоратор Bosch GBH 2-26 DRE",
    "Утеплитель Rockwool Лайт Баттс 100 мм",
]

images = [
    "https://example.com/images/shtukaturka.jpg",
    "https://example.com/images/kraska2.jpg",
    "https://example.com/images/gipsokarton.jpg",
    "https://example.com/images/perforator.jpg",
    "https://example.com/images/uteplitel.jpg",
]

descriptions = [
    "Легко наносится, не требует армирующей сетки.",
    "Износостойкая и атмосферостойкая фасадная краска.",
    "Идеален для ванных комнат и кухонь.",
    "Мощный и надёжный перфоратор для бетона и кирпича.",
    "Эффективный теплоизоляционный материал для стен и перекрытий.",
]

# Генерация и вставка товаров
products = []

for i in range(len(product_names)):
    product = {
        "sku": str(uuid4()),
        "name": product_names[i],
        "articul": f"ART-{random.randint(10000, 99999)}",
        "price": round(random.uniform(600, 6000), 2),
        "category": categories[i],
        "brand": brands[i],
        "img": images[i],
        "description": descriptions[i],
    }
    products.append(product)

# Вставка новых товаров (без очистки)
collection.insert_many(products)

print(f"Успешно добавлено {len(products)} дополнительных товаров.")
