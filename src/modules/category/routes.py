from flask import Blueprint, request, jsonify
from src.model.category import Category
from src.core.avl_tree import AvlTree

category_bp = Blueprint('category', __name__, url_prefix='/category')

category_tree = AvlTree()
category_id_counter = 1


@category_bp.route('/', methods=['GET'])
def get_all_categories():
    categories = [value for key, value in category_tree.inorder()]
    return jsonify(categories), 200


@category_bp.route('/find', methods=['GET'])
def find_category():
    category_key = request.args.get('key', type=int)
    category = category_tree.search(category_key)
    if category:
        return jsonify(category.to_dict()), 200
    return jsonify({'error': 'Category not found'}), 404


@category_bp.route('/add', methods=['POST'])
def add_category():
    global category_id_counter
    data = request.get_json()
    category = Category(data['name'], {'id': category_id_counter, 'name': data['name']})
    category_tree.insert(data["name"], category)
    category_id_counter += 1
    return jsonify(category.to_dict()), 201


@category_bp.route('/update/<int:category_id>', methods=['PUT'])
def update_category(category_id):
    category = category_tree.search(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    data = request.get_json()
    category.name = data.get('name', category.name)
    return jsonify(category.to_dict()), 200


@category_bp.route('/delete/<int:category_id>', methods=['DELETE'])
def delete_category(category_id):
    category = category_tree.search(category_id)
    if not category:
        return jsonify({'error': 'Category not found'}), 404
    
    category_tree.delete(category_id)
    return jsonify({'message': 'Category deleted'}), 200
