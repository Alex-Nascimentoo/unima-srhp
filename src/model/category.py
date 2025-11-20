from typing import List, Optional
from dataclasses import dataclass, field
from .product import Produto
from .status_product import StatusProduto

@dataclass
class Categoria:
    id: str
    nome: str
    descricao: str = ""
    produtos: List[Produto] = field(default_factory=list)
    nivel: int = 0
    categoria_pai: Optional[str] = None
    total_produtos: int = 0
    
    def adicionar_produto(self, produto: Produto) -> None:
        self.produtos.append(produto)
        self.total_produtos = len(self.produtos)
    
    def remover_produto(self, produto_id: str) -> bool:
        tamanho_inicial = len(self.produtos)
        self.produtos = [p for p in self.produtos if p.id != produto_id]
        self.total_produtos = len(self.produtos)
        return len(self.produtos) < tamanho_inicial
    
    def buscar_produto(self, produto_id: str) -> Optional[Produto]:
        for produto in self.produtos:
            if produto.id == produto_id:
                return produto
        return None
    
    def listar_produtos_ativos(self) -> List[Produto]:
        ativos = [p for p in self.produtos if p.status == StatusProduto.ATIVO]
        return sorted(ativos, key=lambda p: p.calcular_score_relevancia(), reverse=True)