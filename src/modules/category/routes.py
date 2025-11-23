from flask import Blueprint, request, jsonify
from model import Category

category_bp = Blueprint("category", __name__, url_prefix='/category')

@category_bp.route('/', methods=['GET'])
def get_all_categories():
    categories = Category.get_all()
    return jsonify(categories), 200

@category_bp.route('/find', methods=['GET'])
def find_category():
    category_id = request.args.get('id')
    if not category_id:
        return jsonify({"error": "Missing id parameter"}), 400
    
    category = Category.get_by_id(int(category_id))
    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    return jsonify(category), 200

@category_bp.route('/add', methods=['POST'])
def add_category():
    data = request.get_json()
    category = Category.create(data)
    return jsonify(category), 201

@category_bp.route('/update/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    data = request.get_json()
    category = Category.update(category_id, data)
    if not category:
        return jsonify({"error": "Category not found"}), 404
    
    return jsonify(category), 200

@category_bp.route('/delete/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    success = Category.delete(category_id)
    if not success:
        return jsonify({"error": "Category not found"}), 404
    
    return jsonify({"message": "Category deleted successfully"}), 200
