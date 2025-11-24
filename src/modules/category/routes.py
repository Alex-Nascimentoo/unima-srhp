from flask import Blueprint, request, jsonify
from src.model.category import Category
from src.core.avl_tree import AvlTree
from src.core.__init__ import CATEGORIES
import json

category_bp = Blueprint('category', __name__, url_prefix='/category')

category_tree = AvlTree()
category_id_counter = len(CATEGORIES) + 1


@category_bp.route('/', methods=['GET'])
def get_all_categories():
    categories = [value.to_dict() for key, value in category_tree.inorder()]
    return jsonify(categories), 200


@category_bp.route('/find', methods=['GET'])
def find_category():
    category_key = request.args.get('key', type=str)
    category = category_tree.search(category_key)
    if category:
        return jsonify(category.to_dict()), 200
    return jsonify({'error': 'Category not found'}), 404


@category_bp.route('/add', methods=['POST'])
def add_category():
    global category_id_counter
    data = request.get_json()
    category = Category(category_id_counter, data['name'])
    category_tree.insert(data["name"], category)
    category_id_counter += 1
    return jsonify(category.to_dict()), 201


@category_bp.route('/update/<category_key>', methods=['PUT'])
def update_category(category_key):
    category = category_tree.search(category_key)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    data = request.get_json()
    category.name = data.get('name', category.name)
    return jsonify(category.to_dict()), 200


@category_bp.route('/delete/<category_key>', methods=['DELETE'])
def delete_category(category_key):
    category = category_tree.search(category_key)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    category_tree.delete(category_key)
    return jsonify({'message': 'Category deleted'}), 200
