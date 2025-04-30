from db.mongo import products


class CollectionService:
    def __init__(self):
        self.collection = products

class ProductService:
    def __init__(self):
        self.collection = products

    def get_all_products(self):
        """
        Возвращает все продукты
        """
        return list(self.collection.find({}))
    def get_one_product(self, query: dict):
        """
        Возвращает один продукт по id
        """
        return self.collection.find_one(query)
    
    def get_product_by_id(self, product_id):
        """
        Поиск продукта по ID
        """

    
