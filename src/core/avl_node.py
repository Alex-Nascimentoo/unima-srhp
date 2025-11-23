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
