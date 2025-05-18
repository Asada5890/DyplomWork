from db.mongo import products
from bson import ObjectId

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
        if isinstance(product_id, str):
            product_id = ObjectId(product_id)
    
        return self.collection.find_one({"_id": product_id})
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
    def get_product_by_articul(self, articul: str):
        """
        Поиск продукта по артиклу
        """
        return self.collection.find_one({"articul": articul})
    
    
    def update_product(self, product_id: str, name: str, category: str, price: float, description: str):
        """
        Обновление данных товара в базе данных.
        """
        product_id = ObjectId(product_id)
        
        updated_product = self.collection.update_one(
            {"_id": product_id},
            {"$set": {"name": name, "category": category, "price": price, "description": description}}
        )

        if updated_product.modified_count == 0:
            raise Exception(f"Ошибка при обновлении товара. Возможно, данные не изменились.")

        return self.collection.find_one({"_id": product_id})
    
    def delete_product_by_id(self, product_id: str):
        """
        Удаление продукта по ID
        """
        result = self.collection.delete_one({"_id": ObjectId(product_id)})
        return result.deleted_count > 0  # Возвращаем True, если удален хотя бы один продукт
