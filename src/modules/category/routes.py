from flask import Blueprint, request, jsonify
from model import Category

category_bp = Blueprint("category", __name__)

@category_bp.post("/")
def create_category():
    data = request.get_json()
    category = Category(name=data["name"])
    
    return jsonify({"message": "Created category!", "id": category.id})

@category_bp.get("/")
def list_categories():
    categories = Category.query.all()
    return jsonify([
        {"id": c.id, "name": c.name} for c in categories
    ])
