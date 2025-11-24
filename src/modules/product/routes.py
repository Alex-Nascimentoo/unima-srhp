from flask import Blueprint, request, jsonify
from src.model.product import Product
from src.core.avl_tree import AvlTree

product_bp = Blueprint('product', __name__, url_prefix='/business/product')

products_tree = AvlTree()
product_id_counter = 1


@product_bp.route('/', methods=['GET'])
def get_all_products():
    products = [value for key, value in products_tree.inorder()]
    return jsonify(products), 200


@product_bp.route('/find', methods=['GET'])
def find_product():
    product_key = request.args.get('key', type=str)
    product = products_tree.search(product_key)
    if product:
        return jsonify(product), 200
    return jsonify({'error': 'Product not found'}), 404


@product_bp.route('/recommend', methods=['GET'])
def recommend_products():
    product_key = request.args.get('key', type=str)
    product = products_tree.search(product_key)
    print(f'product is: {product}')
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    recommendations = [value for key, value in products_tree.inorder() 
                      if value['id_category'] == product['id_category'] and value.id != product['id']]
    # recommendations = products_tree.recommend_by_category(product['id_category'], product_key)
    # product_list = [value for key, value in products_tree.inorder()]
    # print(f'Product List: {product_list}')
    recommendations = []
    return jsonify(recommendations), 200


@product_bp.route('/add', methods=['POST'])
def add_product():
    global product_id_counter
    data = request.get_json()
    product = Product(product_id_counter, data['name'], data['price'], data['id_category'])
    products_tree.insert(product_id_counter, product)
    product_id_counter += 1
    return jsonify(product.to_dict()), 201


@product_bp.route('/update/<int:product_id>', methods=['PUT'])
def update_product(product_id):
    product = products_tree.search(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    data = request.get_json()
    product.name = data.get('name', product.name)
    product.price = data.get('price', product.price)
    product.id_category = data.get('id_category', product.id_category)
    return jsonify(product.to_dict()), 200


@product_bp.route('/delete/<int:product_id>', methods=['DELETE'])
def delete_product(product_id):
    product = products_tree.search(product_id)
    if not product:
        return jsonify({'error': 'Product not found'}), 404
    
    products_tree.delete(product_id)
    return jsonify({'message': 'Product deleted'}), 200
