from pymongo import MongoClient
from core.settings import settings

server = MongoClient(settings.MONGODB_URL, settings.MONGODB_PORT)

products_db = server[settings.MONGODB_DB_NAME]

products = products_db[settings.MONGODB_COLLECTION_PRODUCTS]

cart = products_db[settings.MONGODB_COLLECTION_СARTS]


data = products.find({})
cart = cart.find({})
