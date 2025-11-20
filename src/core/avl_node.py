from typing import Optional
from model.category import Categoria


class NoAVL:
    """Nó da árvore AVL contendo uma categoria"""
    
    def __init__(self, categoria: Categoria):
        self.categoria = categoria
        self.esquerda: Optional['NoAVL'] = None
        self.direita: Optional['NoAVL'] = None
        self.altura = 1
        self.fator_balanceamento = 0