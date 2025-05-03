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
    def get_all_categories(self):
        """
        Возвращает все категории
        """
        return self.collection.distinct("category")
    
    def get_products_by_category(self, category_name):
        """
        Возвращает все продукты по категории
        """
        return list(self.collection.find({"category": category_name}))

    def sort_products(self):
        """
        сортировка 
        """
    def get_product_by_articul(self, prodict_id):
        """
        Поиск продукта по артиклу
        """
    
