class AvlNode:
    def __init__(self, key, value=None):
        self.key = key
        self.value = value
        self.left = None
        self.right = None
        self.height = 1

class AvlTree:
    def __init__(self):
        self.root = None
    
    def _height(self, node):
        return node.height if node else 0
    
    def _balance(self, node):
        return self._height(node.left) - self._height(node.right) if node else 0
    
    def _update_height(self, node):
        if node:
            node.height = 1 + max(self._height(node.left), self._height(node.right))
    
    # Rotação simples a direita
    def _rotate_right(self, y):
        x = y.left
        y.left = x.right
        x.right = y
        self._update_height(y)
        self._update_height(x)
        return x
    
    # Rotação simples a esquerda
    def _rotate_left(self, x):
        y = x.right
        x.right = y.left
        y.left = x
        self._update_height(x)
        self._update_height(y)
        return y
    
    # Rotação dupla a direita (Left-Right)
    def _rotate_double_right(self, node):
        node.left = self._rotate_left(node.left)
        return self._rotate_right(node)
    
    # Rotação dupla a esquerda (Right-Left)
    def _rotate_double_left(self, node):
        node.right = self._rotate_right(node.right)
        return self._rotate_left(node)
    
    def _rebalance(self, node):
        """Rebalanceia o nó se necessário após inserção ou remoção"""
        if not node:
            return node
        
        self._update_height(node)
        balance = self._balance(node)
        
        # Caso Left-Left
        if balance > 1 and self._balance(node.left) >= 0:
            return self._rotate_right(node)
        
        # Caso Left-Right
        if balance > 1 and self._balance(node.left) < 0:
            return self._rotate_double_right(node)
        
        # Caso Right-Right
        if balance < -1 and self._balance(node.right) <= 0:
            return self._rotate_left(node)
        
        # Caso Right-Left
        if balance < -1 and self._balance(node.right) > 0:
            return self._rotate_double_left(node)
        
        return node
    
    def _insert(self, node, key, value):
        if not node:
            return AvlNode(key, value)
        
        if key < node.key:
            node.left = self._insert(node.left, key, value)
        elif key > node.key:
            node.right = self._insert(node.right, key, value)
        else:
            node.value = value
            return node
        
        return self._rebalance(node)
    
    def insert(self, key, value=None):
        self.root = self._insert(self.root, key, value)
    
    def _find_min(self, node):
        while node.left:
            node = node.left
        return node
    
    def _delete(self, node, key):
        if not node:
            return node
        
        if key < node.key:
            node.left = self._delete(node.left, key)
        elif key > node.key:
            node.right = self._delete(node.right, key)
        else:
            if not node.left:
                return node.right
            elif not node.right:
                return node.left
            
            temp = self._find_min(node.right)
            node.key = temp.key
            node.value = temp.value
            node.right = self._delete(node.right, temp.key)
        
        return self._rebalance(node)
    
    def delete(self, key):
        self.root = self._delete(self.root, key)
    
    def _search(self, node, key):
        if not node or node.key == key:
            return node
        if key < node.key:
            return self._search(node.left, key)
        return self._search(node.right, key)
    
    def search(self, key):
        node = self._search(self.root, key)
        return node.value if node else None
    
    def _inorder(self, node, result):
        if node:
            self._inorder(node.left, result)
            result.append((node.key, node.value))
            self._inorder(node.right, result)
    
    def inorder(self):
        result = []
        self._inorder(self.root, result)
        return result