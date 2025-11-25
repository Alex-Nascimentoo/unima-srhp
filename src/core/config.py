from src.modules.product.routes import products_tree
from src.modules.category.routes import category_tree
from src.model.category import Category
from src.core.__init__ import CATEGORIES
from src.model.product import Product
from src.core.__init__ import PRODUCTS_DB

def start_local_db():
    for product in PRODUCTS_DB:
        new_product = Product(product["id"], product["name"], product["price"], product["id_category"])
        products_tree.insert(product["name"], new_product)

    for category in CATEGORIES:
        new_category = Category(category["id"], category["name"])
        category_tree.insert(category["name"], new_category)

