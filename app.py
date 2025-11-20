# from src.config import app

# if __name__ == "__main__":
#     app.run(debug=True)

from src.core.avl_tree import AvlTree

# Exemplo de uso
if __name__ == "__main__":
    tree = AvlTree()
    
    # Inserindo produtos
    result1 = tree.insert(1, {'id': 1, 'name': 'Laptop', 'category': 'Electronics', 'subcategory': 'Computers'})
    print(result1)  # {'success': True, 'message': 'Produto com key 1 inserido com sucesso.'}
    
    result2 = tree.insert(1, {'id': 1, 'name': 'Outro Laptop', 'category': 'Electronics', 'subcategory': 'Computers'})
    print(result2)  # {'success': False, 'message': 'Produto com key 1 já existe na árvore.'}


# # Exemplo de uso
# if __name__ == "__main__":
#     # Criar uma instância da árvore
#     tree = AvlTree()
    
#     # Inserir produtos
#     tree.insert(1, {
#         'id': 1, 
#         'name': 'Laptop Dell', 
#         'category': 'Electronics', 
#         'subcategory': 'Computers'
#     })
    
#     tree.insert(2, {
#         'id': 2, 
#         'name': 'Mouse Logitech', 
#         'category': 'Electronics', 
#         'subcategory': 'Accessories'
#     })
    
#     tree.insert(3, {
#         'id': 3, 
#         'name': 'Desktop HP', 
#         'category': 'Electronics', 
#         'subcategory': 'Computers'
#     })
    
#     # Buscar produtos similares ao Laptop (id=1)
#     recommendations = tree.find_similar_products(1, max_results=5)
#     print("Recomendações para Laptop Dell:")
#     for rec in recommendations:
#         print(f"  - {rec['product']['name']} (match: {rec['match_type']})")
    
#     # Buscar por categoria
#     electronics = tree.recommend_by_category('Electronics', max_results=10)
#     print(f"\nTotal de produtos em Electronics: {len(electronics)}")