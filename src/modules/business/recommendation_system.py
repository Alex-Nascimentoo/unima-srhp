from typing import List, Optional
from core.avl_tree import ArvoreAVLCategorias
from core.avl_node import NoAVL
from src.model.product import Produto
from src.model.status_product import StatusProduto

# ==================== SISTEMA DE RECOMENDAÇÃO ====================

class SistemaRecomendacao:
    """
    Motor de recomendação baseado em análise recursiva da árvore
    
    Estratégias de recomendação:
    1. Produtos similares na mesma categoria
    2. Produtos de categorias relacionadas
    3. Produtos baseados em score de relevância
    """
    
    def __init__(self, arvore: ArvoreAVLCategorias):
        self.arvore = arvore
    
    def _coletar_produtos_recursivo(self, no: Optional[NoAVL], produtos: List[Produto], 
                                    max_produtos: int, filtro_tags: Optional[List[str]] = None) -> None:
        """
        Coleta produtos de forma recursiva pela árvore
        Aplica filtros opcionais por tags
        
        Complexidade: O(n * m) onde n = nós e m = produtos por nó
        """
        if not no or len(produtos) >= max_produtos:
            return
        
        # Coletar produtos da categoria atual
        for produto in no.categoria.produtos:
            if len(produtos) >= max_produtos:
                break
            
            if produto.status == StatusProduto.ATIVO:
                if filtro_tags:
                    if any(tag in produto.tags for tag in filtro_tags):
                        produtos.append(produto)
                else:
                    produtos.append(produto)
        
        # Recursão para subárvores
        self._coletar_produtos_recursivo(no.esquerda, produtos, max_produtos, filtro_tags)
        self._coletar_produtos_recursivo(no.direita, produtos, max_produtos, filtro_tags)
    
    def recomendar_produtos_similares(self, produto_id: str, categoria_id: str, 
                                     limite: int = 5) -> List[Produto]:
        """
        Recomenda produtos similares ao produto especificado
        
        Algoritmo:
        1. Busca produto original
        2. Extrai tags do produto
        3. Busca recursiva de produtos com tags similares
        4. Ordena por relevância
        
        Complexidade: O(n log n) - coleta O(n) + ordenação O(n log n)
        """
        categoria = self.arvore.buscar(categoria_id)
        if not categoria:
            return []
        
        produto_original = categoria.buscar_produto(produto_id)
        if not produto_original:
            return []
        
        # Coletar produtos com tags similares
        produtos_similares = []
        self._coletar_produtos_recursivo(
            self.arvore.raiz, 
            produtos_similares, 
            limite * 3,  # Coletar mais para depois filtrar
            produto_original.tags
        )
        
        # Remover produto original e ordenar por relevância
        produtos_similares = [p for p in produtos_similares if p.id != produto_id]
        produtos_similares.sort(key=lambda p: p.calcular_score_relevancia(), reverse=True)
        
        return produtos_similares[:limite]
    
    def recomendar_produtos_categoria(self, categoria_id: str, limite: int = 10) -> List[Produto]:
        """
        Recomenda melhores produtos de uma categoria
        Complexidade: O(n log n)
        """
        categoria = self.arvore.buscar(categoria_id)
        if not categoria:
            return []
        
        produtos_ativos = categoria.listar_produtos_ativos()
        return produtos_ativos[:limite]
    
    def recomendar_produtos_globais(self, limite: int = 20, filtro_tags: Optional[List[str]] = None) -> List[Produto]:
        """
        Recomenda produtos de todo o sistema
        Busca recursiva em toda a árvore
        
        Complexidade: O(n * m * log(n*m)) onde n = categorias, m = produtos
        """
        todos_produtos = []
        self._coletar_produtos_recursivo(self.arvore.raiz, todos_produtos, limite * 2, filtro_tags)
        
        # Ordenar por relevância
        todos_produtos.sort(key=lambda p: p.calcular_score_relevancia(), reverse=True)
        return todos_produtos[:limite]
