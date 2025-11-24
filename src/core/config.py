from src.core.avl_tree import AvlTree
from src.modules.product.routes import products_tree
from src.modules.category.routes import category_tree

PRODUCTS_DB = {
    "shirt": [
        {"id": 1, "id_category": 1, "name": "Blue Polo Shirt", "price": 89.90},
        {"id": 2, "id_category": 1, "name": "White Dress Shirt", "price": 129.90},
        {"id": 3, "id_category": 1, "name": "Floral Print Shirt", "price": 79.90}
    ],
    "pants": [
        {"id": 4, "id_category": 2, "name": "Skinny Jeans", "price": 159.90},
        {"id": 5, "id_category": 2, "name": "Black Dress Pants", "price": 189.90},
        {"id": 6, "id_category": 2, "name": "Beige Cargo Pants", "price": 139.90}
    ],
    "shorts": [
        {"id": 7, "id_category": 3, "name": "Ripped Denim Shorts", "price": 89.90},
        {"id": 8, "id_category": 3, "name": "Gray Sweat Shorts", "price": 69.90},
        {"id": 9, "id_category": 3, "name": "Black Sport Shorts", "price": 59.90}
    ],
    "jacket": [
        {"id": 10, "id_category": 4, "name": "Leather Jacket", "price": 299.90},
        {"id": 11, "id_category": 4, "name": "Hoodie Sweatshirt", "price": 149.90},
        {"id": 12, "id_category": 4, "name": "Green Bomber Jacket", "price": 199.90}
    ],
    "sneakers": [
        {"id": 13, "id_category": 5, "name": "Nike Sport Sneakers", "price": 349.90},
        {"id": 14, "id_category": 5, "name": "Adidas Casual Sneakers", "price": 299.90},
        {"id": 15, "id_category": 5, "name": "Black All Star", "price": 219.90}
    ]
}

CATEGORIES = [
    {"id": 1, "name" : "shirt"},
    {"id": 2, "name" : "pants"},
    {"id": 3, "name" : "shorts"},
    {"id": 4, "name" : "jacket"},
    {"id": 5, "name" : "sneakers"}
]

def start_local_db():
    for category, products in PRODUCTS_DB.items():
        for product in products:
            products_tree.insert(product["id"], product["name"], product)
    for category in CATEGORIES:
        category_tree.insert(category["name"], category)
        print(category)
