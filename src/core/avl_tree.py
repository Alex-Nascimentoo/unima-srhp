"""
AVL Tree Implementation

An AVL tree is a self-balancing binary search tree where the heights of the 
two child subtrees of any node differ by at most one. This ensures O(log n) 
time complexity for insertion, deletion, and search operations.
"""


class AvlNode:
    """
    Node class for AVL Tree.
    
    Attributes:
        key: The key used for ordering nodes in the tree
        value: Optional value associated with the key
        left: Reference to left child node
        right: Reference to right child node
        height: Height of the node (distance to furthest leaf)
    """
    
    def __init__(self, key, value=None):
        """
        Initialize an AVL tree node.
        
        Args:
            key: The key for this node
            value: Optional value to store with the key
        """
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1


class AvlTree:
    """
    AVL Tree implementation with automatic balancing.
    
    The tree maintains balance through rotations after insertions and deletions,
    ensuring that the height difference between left and right subtrees never
    exceeds 1 for any node.
    """
    
    def __init__(self):
        """Initialize an empty AVL tree."""
        self.root = None
    
    # ==================== Height and Balance Methods ====================
    
    def _height(self, node):
        """
        Get the height of a node.
        
        Args:
            node: The node to get height from
            
        Returns:
            Height of the node, or 0 if node is None
        """
        return node.height if node else 0
    
    def _balance(self, node):
        """
        Calculate the balance factor of a node.
        
        Balance factor = height(left subtree) - height(right subtree)
        
        Args:
            node: The node to calculate balance for
            
        Returns:
            Balance factor (positive means left-heavy, negative means right-heavy)
        """
        return self._height(node.left) - self._height(node.right) if node else 0
    
    def _update_height(self, node):
        """
        Update the height of a node based on its children's heights.
        
        Args:
            node: The node to update
        """
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))
    
    # ==================== Rotation Methods ====================
    
    def _rotate_right(self, y):
        """
        Perform a right rotation on the given node.
        
        Used to fix Left-Left case imbalance.
        
        Args:
            y: The root node of the subtree to rotate
            
        Returns:
            New root of the rotated subtree
        """
        x = y.left
        y.left = x.right
        x.right = y
        self._update_height(y)
        self._update_height(x)
        return x
    
    def _rotate_left(self, x):
        """
        Perform a left rotation on the given node.
        
        Used to fix Right-Right case imbalance.
        
        Args:
            x: The root node of the subtree to rotate
            
        Returns:
            New root of the rotated subtree
        """
        y = x.right
        x.right = y.left
        y.left = x
        self._update_height(x)
        self._update_height(y)
        return y
    
    def _rotate_double_right(self, node):
        """
        Perform a double right rotation (Left-Right case).
        
        First rotates left child left, then rotates node right.
        
        Args:
            node: The root node of the subtree to rotate
            
        Returns:
            New root of the rotated subtree
        """
        node.left = self._rotate_left(node.left)
        return self._rotate_right(node)
    
    def _rotate_double_left(self, node):
        """
        Perform a double left rotation (Right-Left case).
        
        First rotates right child right, then rotates node left.
        
        Args:
            node: The root node of the subtree to rotate
            
        Returns:
            New root of the rotated subtree
        """
        node.right = self._rotate_right(node.right)
        return self._rotate_left(node)
    
    # ==================== Rebalancing ====================
    
    def _rebalance(self, node):
        """
        Rebalance a node if necessary after insertion or deletion.
        
        Checks the balance factor and performs appropriate rotations
        to maintain AVL tree property (balance factor of -1, 0, or 1).
        
        Args:
            node: The node to rebalance
            
        Returns:
            The new root of the rebalanced subtree
        """
        if not node:
            return node
        
        self._update_height(node)
        balance = self._balance(node)
        
        # Left-Left case: Right rotation
        if balance > 1 and self._balance(node.left) >= 0:
            return self._rotate_right(node)
        
        # Left-Right case: Double right rotation
        if balance > 1 and self._balance(node.left) < 0:
            return self._rotate_double_right(node)
        
        # Right-Right case: Left rotation
        if balance < -1 and self._balance(node.right) <= 0:
            return self._rotate_left(node)
        
        # Right-Left case: Double left rotation
        if balance < -1 and self._balance(node.right) > 0:
            return self._rotate_double_left(node)
        
        return node
    
    # ==================== Insertion ====================
    
    def _insert(self, node, key, value, inserted):
        """
        Recursively insert a key-value pair into the tree.
        
        Args:
            node: Current node in the recursion
            key: Key to insert
            value: Value to associate with the key
            inserted: List with single boolean to track if insertion occurred
            
        Returns:
            New root of the subtree after insertion and rebalancing
        """
        # Base case: found the insertion point
        if not node:
            inserted[0] = True
            return AvlNode(key, value)
        
        # Recursive insertion
        if key < node.key:
            node.left = self._insert(node.left, key, value, inserted)
        elif key > node.key:
            node.right = self._insert(node.right, key, value, inserted)
        else:
            # Key already exists, don't update - set inserted to False
            inserted[0] = False
            return node
        
        # Rebalance the tree after insertion
        return self._rebalance(node)
    
    def insert(self, key, value=None):
        """
        Insert a key-value pair into the AVL tree.
        
        If the key already exists, returns a message and does not update the value.
        
        Args:
            key: Key to insert
            value: Optional value to associate with the key
            
        Returns:
            Dictionary with 'success' (bool) and 'message' (str) keys
        """
        inserted = [True]  # Use list to allow modification in nested function
        self.root = self._insert(self.root, key, value, inserted)
        
        if inserted[0]:
            return {
                'success': True,
                'message': f'Produto com key {key} inserido com sucesso.'
            }
        else:
            return {
                'success': False,
                'message': f'Produto com key {key} já existe na árvore.'
            }
    
    # ==================== Deletion ====================
    
    def _find_min(self, node):
        """
        Find the node with minimum key in a subtree.
        
        Args:
            node: Root of the subtree
            
        Returns:
            Node with the minimum key
        """
        while node.left:
            node = node.left
        return node
    
    def _delete(self, node, key):
        """
        Recursively delete a key from the tree.
        
        Args:
            node: Current node in the recursion
            key: Key to delete
            
        Returns:
            New root of the subtree after deletion and rebalancing
        """
        if not node:
            return node
        
        # Find the node to delete
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            # Node found - handle deletion cases
            
            # Case 1: Node has only right child or no children
            if not node.left:
                return node.right
            
            # Case 2: Node has only left child
            elif not node.right:
                return node.left
            
            # Case 3: Node has two children
            # Replace with inorder successor (minimum in right subtree)
            temp = self._find_min(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)
        
        # Rebalance the tree after deletion
        return self._rebalance(node)
    
    def delete(self, key):
        """
        Delete a key from the AVL tree.
        
        Args:
            key: Key to delete
        """
        self.root = self._delete(self.root, key)
    
    # ==================== Search ====================
    
    def _search(self, node, key):
        """
        Recursively search for a key in the tree.
        
        Args:
            node: Current node in the recursion
            key: Key to search for
            
        Returns:
            Node containing the key, or None if not found
        """
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)
    
    def search(self, key):
        """
        Search for a key in the AVL tree.
        
        Args:
            key: Key to search for
            
        Returns:
            Value associated with the key, or None if not found
        """
        node = self._search(self.root, key)
        return node.value if node else None
    
    # ==================== Traversal ====================
    
    def _inorder(self, node, result):
        """
        Perform inorder traversal (left-root-right) recursively.
        
        Args:
            node: Current node in the traversal
            result: List to append (key, value) tuples to
        """
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)
    
    def inorder(self):
        """
        Get an inorder traversal of the tree.
        
        Returns:
            List of (key, value) tuples in sorted order by key
        """
        result = []
        self._inorder(self.root, result)
        return result
    
    # ==================== Product Recommendation ====================
    
    def _collect_similar_products(self, node, target_product, result, max_results=10):
        """
        Recursively collect products similar to the target product.
        
        Traverses the entire tree and collects products that match
        either the category or subcategory of the target product.
        
        Args:
            node: Current node in the traversal
            target_product: Dictionary containing the target product info
            result: List to append similar products to
            max_results: Maximum number of results to collect
        """
        if not node or len(result) >= max_results:
            return
        
        # Traverse left subtree
        self._collect_similar_products(node.left, target_product, result, max_results)
        
        # Check if we've reached max results after left traversal
        if len(result) >= max_results:
            return
        
        # Process current node
        if node.value and isinstance(node.value, dict):
            current_product = node.value
            
            # Don't recommend the same product
            if node.key == target_product.get('id'):
                self._collect_similar_products(node.right, target_product, result, max_results)
                return
            
            target_category = target_product.get('category')
            target_subcategory = target_product.get('subcategory')
            current_category = current_product.get('category')
            current_subcategory = current_product.get('subcategory')
            
            # Calculate similarity score
            similarity_score = 0
            
            # Exact subcategory match (highest priority)
            if (target_subcategory and current_subcategory and 
                target_subcategory.lower() == current_subcategory.lower()):
                similarity_score = 2
            
            # Same category match (medium priority)
            elif (target_category and current_category and 
                  target_category.lower() == current_category.lower()):
                similarity_score = 1
            
            # If there's any similarity, add to results
            if similarity_score > 0:
                result.append({
                    'product': current_product,
                    'key': node.key,
                    'similarity_score': similarity_score,
                    'match_type': 'subcategory' if similarity_score == 2 else 'category'
                })
        
        # Traverse right subtree
        self._collect_similar_products(node.right, target_product, result, max_results)
    
    def find_similar_products(self, product_id, max_results=10):
        """
        Find products similar to a given product based on category/subcategory.
        
        This method searches for the target product by ID, then traverses
        the entire tree to find products with matching categories or subcategories.
        Results are sorted by relevance (subcategory matches first, then category matches).
        
        Args:
            product_id: ID (key) of the product to find recommendations for
            max_results: Maximum number of recommendations to return (default: 10)
            
        Returns:
            List of dictionaries containing similar products, sorted by relevance.
            Each dictionary contains:
                - product: The product data
                - key: The product's key in the tree
                - similarity_score: Score indicating match quality (2=subcategory, 1=category)
                - match_type: Type of match ('subcategory' or 'category')
            Returns empty list if product not found or no similar products exist.
            
        Example:
            tree = AvlTree()
            tree.insert(1, {'id': 1, 'name': 'Laptop', 'category': 'Electronics', 'subcategory': 'Computers'})
            tree.insert(2, {'id': 2, 'name': 'Mouse', 'category': 'Electronics', 'subcategory': 'Accessories'})
            tree.insert(3, {'id': 3, 'name': 'Desktop', 'category': 'Electronics', 'subcategory': 'Computers'})
            
            recommendations = tree.find_similar_products(1, max_results=5)
            # Returns Desktop first (same subcategory), then Mouse (same category)
        """
        # Find the target product
        target_node = self._search(self.root, product_id)
        
        if not target_node or not target_node.value:
            return []
        
        target_product = target_node.value
        
        # Ensure product has required fields
        if not isinstance(target_product, dict):
            return []
        
        # Collect similar products
        similar_products = []
        self._collect_similar_products(self.root, target_product, similar_products, max_results)
        
        # Sort by similarity score (subcategory matches first, then category matches)
        similar_products.sort(key=lambda x: x['similarity_score'], reverse=True)
        
        return similar_products
    
    def recommend_by_category(self, category, subcategory=None, max_results=10, exclude_id=None):
        """
        Find products by category and optionally subcategory.
        
        Useful for general category-based browsing or when you want recommendations
        without a specific source product.
        
        Args:
            category: Category to search for
            subcategory: Optional subcategory to filter by
            max_results: Maximum number of results to return
            exclude_id: Optional product ID to exclude from results
            
        Returns:
            List of dictionaries containing matching products with their keys
            
        Example:
            recommendations = tree.recommend_by_category('Electronics', 'Computers', max_results=5)
        """
        results = []
        self._recommend_by_category_helper(self.root, category, subcategory, 
                                          results, max_results, exclude_id)
        return results
    
    def _recommend_by_category_helper(self, node, category, subcategory, 
                                     result, max_results, exclude_id):
        """
        Helper method to recursively find products by category.
        
        Args:
            node: Current node in the traversal
            category: Target category
            subcategory: Optional target subcategory
            result: List to append matching products to
            max_results: Maximum number of results
            exclude_id: Product ID to exclude
        """
        if not node or len(result) >= max_results:
            return
        
        # Traverse left
        self._recommend_by_category_helper(node.left, category, subcategory, 
                                          result, max_results, exclude_id)
        
        if len(result) >= max_results:
            return
        
        # Process current node
        if node.value and isinstance(node.value, dict):
            product = node.value
            
            # Skip excluded product
            if exclude_id and node.key == exclude_id:
                self._recommend_by_category_helper(node.right, category, subcategory, 
                                                  result, max_results, exclude_id)
                return
            
            current_category = product.get('category', '').lower()
            current_subcategory = product.get('subcategory', '').lower()
            
            # Check if product matches criteria
            category_match = current_category == category.lower()
            
            if subcategory:
                subcategory_match = current_subcategory == subcategory.lower()
                if category_match and subcategory_match:
                    result.append({
                        'product': product,
                        'key': node.key
                    })
            elif category_match:
                result.append({
                    'product': product,
                    'key': node.key
                })
        
        # Traverse right
        self._recommend_by_category_helper(node.right, category, subcategory, 
                                          result, max_results, exclude_id)
