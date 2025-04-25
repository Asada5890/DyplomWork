from pymongo import MongoClient
from core import settings

server = MongoClient(settings.MONGODB_URL , port=settings.MONGODB_PORT)

products_db = server[settings.DATABASE_NAME]

products = products_db[settings.MONGODB_COLLECTION_NAME]


data = products.find({})



