from flask import Blueprint, request, jsonify
from src.db.config import db
from model import Product

product_bp = Blueprint("product", __name__)

@product_bp.post("/")
def create_product():
    data = request.get_json()
    product = Product(
        name=data["name"],
        price=data["price"],
        category_id=data.get("category_id")
    )
    db.session.add(product)
    db.session.commit()

    return jsonify({"message": "Produto criado!", "id": product.id})

@product_bp.get("/")
def list_products():
    products = Product.query.all()
    return jsonify([
        {
            "id": p.id,
            "name": p.name,
            "price": p.price,
            "category_id": p.category_id
        }
        for p in products
    ])
