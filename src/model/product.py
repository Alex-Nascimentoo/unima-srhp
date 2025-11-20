from typing import List
from dataclasses import dataclass, field
from datetime import datetime
from .status_product import StatusProduto

@dataclass
class Produto:
    id: str
    nome: str
    preco: float
    descricao: str = ""
    tags: List[str] = field(default_factory=list)
    estoque: int = 0
    status: StatusProduto = StatusProduto.ATIVO
    visualizacoes: int = 0
    vendas: int = 0
    data_cadastro: datetime = field(default_factory=datetime.now)
    
    def calcular_score_relevancia(self) -> float:
        score = (self.visualizacoes * 0.3 + 
                self.vendas * 5.0 + 
                (100 if self.status == StatusProduto.ATIVO else 0))
        return score
    
    def to_dict(self):
        return {
            "id": self.id,
            "nome": self.nome,
            "preco": self.preco,
            "descricao": self.descricao,
            "tags": self.tags,
            "estoque": self.estoque,
            "status": self.status.value,
            "visualizacoes": self.visualizacoes,
            "vendas": self.vendas,
            "score": self.calcular_score_relevancia()
        }