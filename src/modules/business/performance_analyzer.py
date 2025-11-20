from typing import Tuple, Any, Dict, List
import time
from core.avl_tree import ArvoreAVLCategorias
from src.model.category import Categoria

# ==================== ANÁLISE DE PERFORMANCE ====================

class AnalisadorPerformance:
    """
    Módulo de análise e medição de performance
    Compara complexidades teóricas vs práticas
    """
    
    @staticmethod
    def medir_tempo_operacao(funcao, *args, **kwargs) -> Tuple[Any, float]:
        """
        Mede tempo de execução de uma operação
        Retorna: (resultado, tempo_em_ms)
        """
        inicio = time.perf_counter()
        resultado = funcao(*args, **kwargs)
        fim = time.perf_counter()
        tempo_ms = (fim - inicio) * 1000
        return resultado, tempo_ms
    
    @staticmethod
    def analise_comparativa_busca(arvore: ArvoreAVLCategorias, categorias: List[Categoria]) -> Dict:
        """
        Compara performance de busca em árvore AVL vs busca linear
        Demonstra ganho de O(log n) vs O(n)
        """
        if not categorias:
            return {}
        
        # Buscar categoria do meio
        categoria_alvo = categorias[len(categorias) // 2]
        
        # Busca AVL (O(log n))
        _, tempo_avl = AnalisadorPerformance.medir_tempo_operacao(
            arvore.buscar, categoria_alvo.id
        )
        
        # Busca linear simulada (O(n))
        def busca_linear(lista, id_alvo):
            for cat in lista:
                if cat.id == id_alvo:
                    return cat
            return None
        
        _, tempo_linear = AnalisadorPerformance.medir_tempo_operacao(
            busca_linear, categorias, categoria_alvo.id
        )
        
        return {
            "total_categorias": len(categorias),
            "tempo_avl_ms": round(tempo_avl, 4),
            "tempo_linear_ms": round(tempo_linear, 4),
            "ganho_percentual": round(((tempo_linear - tempo_avl) / tempo_linear * 100), 2) if tempo_linear > 0 else 0,
            "complexidade_avl": "O(log n)",
            "complexidade_linear": "O(n)"
        }
