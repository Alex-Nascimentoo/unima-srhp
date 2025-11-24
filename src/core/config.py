from src.core.avl_tree import AvlTree
from src.modules.product.routes import products_tree
from src.modules.category.routes import category_tree
from src.model.product import Product
from src.core.__init__ import PRODUCTS_DB

CATEGORIES = [
    {"id": 1, "name" : "shirt"},
    {"id": 2, "name" : "pants"},
    {"id": 3, "name" : "shorts"},
    {"id": 4, "name" : "jacket"},
    {"id": 5, "name" : "sneakers"}
]

def start_local_db():
    for product in PRODUCTS_DB:
        new_product = Product(product["id"], product["name"], product["price"], product["id_category"])
        products_tree.insert(product["name"], new_product)

    for category in CATEGORIES:
        category_tree.insert(category["name"], category)
