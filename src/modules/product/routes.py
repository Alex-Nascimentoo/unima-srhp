from flask import Blueprint, request, jsonify
from src.model.product import Product

product_bp = Blueprint('product', __name__, url_prefix='/business/product')

products_db = []
product_id_counter = 1


@product_bp.route('/', methods=['GET'])
def get_all_products():
    return jsonify([p.to_dict() for p in products_db]), 200


@product_bp.route('/find', methods=['GET'])
def find_product():
    product_id = request.args.get('id', type=int)
    product = next((p for p in products_db if p.id == product_id), None)
    if product:
        return jsonify(product.to_dict()), 200
    return jsonify({'error': 'Product not found'}), 404


@product_bp.route('/recommend', methods=['GET'])
def recommend_products():
    product_id = request.args.get('id', type=int)
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    recommendations = [p.to_dict() for p in products_db if p.id_category == product.id_category and p.id != product_id]
    return jsonify(recommendations), 200


@product_bp.route('/add', methods=['POST'])
def add_product():
    global product_id_counter
    data = request.get_json()
    product = Product(product_id_counter, data['name'], data['price'], data['id_category'])
    products_db.append(product)
    product_id_counter += 1
    return jsonify(product.to_dict()), 201


@product_bp.route('/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.id_category = data.get('id_category', product.id_category)
    return jsonify(product.to_dict()), 200


@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    global products_db
    product = next((p for p in products_db if p.id == product_id), None)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    products_db = [p for p in products_db if p.id != product_id]
    return jsonify({'message': 'Product deleted'}), 200
