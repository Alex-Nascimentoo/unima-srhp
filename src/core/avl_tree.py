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
    
    def _insert(self, node, key, value):
        """
        Recursively insert a key-value pair into the tree.
        
        Args:
            node: Current node in the recursion
            key: Key to insert
            value: Value to associate with the key
            
        Returns:
            New root of the subtree after insertion and rebalancing
        """
        # Base case: found the insertion point
        if not node:
            return AvlNode(key, value)
        
        # Recursive insertion
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            # Key already exists, update value
            node.value = value
            return node
        
        # Rebalance the tree after insertion
        return self._rebalance(node)
    
    def insert(self, key, value=None):
        """
        Insert a key-value pair into the AVL tree.
        
        If the key already exists, its value is updated.
        
        Args:
            key: Key to insert
            value: Optional value to associate with the key
        """
        self.root = self._insert(self.root, key, value)
    
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