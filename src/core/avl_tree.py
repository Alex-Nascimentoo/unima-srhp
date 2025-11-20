from typing import Optional, List, Tuple, Dict, Any
from core.avl_node import NoAVL
from model.category import Categoria


class ArvoreAVLCategorias:
    """
    Árvore AVL especializada para gerenciamento hierárquico de categorias
    
    Principais características:
    - Balanceamento automático após inserções/remoções
    - Operações garantidas em O(log n)
    - Suporte a busca eficiente por ID de categoria
    - Navegação hierárquica recursiva
    """
    
    def __init__(self):
        self.raiz: Optional[NoAVL] = None
        self.total_categorias = 0
        self.total_produtos_sistema = 0
        self.estatisticas = {
            "insercoes": 0,
            "remocoes": 0,
            "buscas": 0,
            "rotacoes": 0
        }
    
    # ========== MÉTODOS AUXILIARES ==========
    
    def _obter_altura(self, no: Optional[NoAVL]) -> int:
        """Retorna altura do nó ou 0 se None. Complexidade: O(1)"""
        return no.altura if no else 0
    
    def _calcular_fator_balanceamento(self, no: Optional[NoAVL]) -> int:
        """Calcula fator de balanceamento (altura_esq - altura_dir). Complexidade: O(1)"""
        if not no:
            return 0
        return self._obter_altura(no.esquerda) - self._obter_altura(no.direita)
    
    def _atualizar_altura(self, no: NoAVL) -> None:
        """Atualiza altura do nó baseado nos filhos. Complexidade: O(1)"""
        no.altura = 1 + max(
            self._obter_altura(no.esquerda),
            self._obter_altura(no.direita)
        )
        no.fator_balanceamento = self._calcular_fator_balanceamento(no)
    
    # ========== ROTAÇÕES AVL ==========
    
    def _rotacao_direita(self, y: NoAVL) -> NoAVL:
        """Rotação simples à direita. Complexidade: O(1)"""
        self.estatisticas["rotacoes"] += 1
        
        x = y.esquerda
        B = x.direita
        
        # Realizar rotação
        x.direita = y
        y.esquerda = B
        
        # Atualizar alturas
        self._atualizar_altura(y)
        self._atualizar_altura(x)
        
        return x
    
    def _rotacao_esquerda(self, x: NoAVL) -> NoAVL:
        """Rotação simples à esquerda. Complexidade: O(1)"""
        self.estatisticas["rotacoes"] += 1
        
        y = x.direita
        B = y.esquerda
        
        # Realizar rotação
        y.esquerda = x
        x.direita = B
        
        # Atualizar alturas
        self._atualizar_altura(x)
        self._atualizar_altura(y)
        
        return y
    
    def _balancear(self, no: NoAVL) -> NoAVL:
        """
        Balanceia o nó aplicando rotações necessárias
        
        Casos de balanceamento AVL:
        1. Esquerda-Esquerda (LL): Rotação direita
        2. Direita-Direita (RR): Rotação esquerda
        3. Esquerda-Direita (LR): Rotação esquerda + direita
        4. Direita-Esquerda (RL): Rotação direita + esquerda
        
        Complexidade: O(1)
        """
        self._atualizar_altura(no)
        fator = no.fator_balanceamento
        
        # Caso Esquerda-Esquerda
        if fator > 1 and self._calcular_fator_balanceamento(no.esquerda) >= 0:
            return self._rotacao_direita(no)
        
        # Caso Direita-Direita
        if fator < -1 and self._calcular_fator_balanceamento(no.direita) <= 0:
            return self._rotacao_esquerda(no)
        
        # Caso Esquerda-Direita
        if fator > 1 and self._calcular_fator_balanceamento(no.esquerda) < 0:
            no.esquerda = self._rotacao_esquerda(no.esquerda)
            return self._rotacao_direita(no)
        
        # Caso Direita-Esquerda
        if fator < -1 and self._calcular_fator_balanceamento(no.direita) > 0:
            no.direita = self._rotacao_direita(no.direita)
            return self._rotacao_esquerda(no)
        
        return no
    
    # ========== OPERAÇÕES PRINCIPAIS (RECURSIVAS) ==========
    
    def _inserir_recursivo(self, no: Optional[NoAVL], categoria: Categoria) -> NoAVL:
        """
        Insere categoria na árvore de forma recursiva
        Complexidade: O(log n) - altura da árvore balanceada
        """
        # Caso base: posição vazia
        if not no:
            self.total_categorias += 1
            return NoAVL(categoria)
        
        # Recursão baseada em comparação de IDs
        if categoria.id < no.categoria.id:
            no.esquerda = self._inserir_recursivo(no.esquerda, categoria)
        elif categoria.id > no.categoria.id:
            no.direita = self._inserir_recursivo(no.direita, categoria)
        else:
            # Categoria já existe - atualiza dados
            no.categoria = categoria
            return no
        
        # Balancear após inserção
        return self._balancear(no)
    
    def _buscar_recursivo(self, no: Optional[NoAVL], categoria_id: str) -> Optional[Categoria]:
        """
        Busca categoria por ID de forma recursiva
        Complexidade: O(log n)
        """
        # Caso base
        if not no or no.categoria.id == categoria_id:
            return no.categoria if no else None
        
        # Recursão binária
        if categoria_id < no.categoria.id:
            return self._buscar_recursivo(no.esquerda, categoria_id)
        return self._buscar_recursivo(no.direita, categoria_id)
    
    def _encontrar_minimo(self, no: NoAVL) -> NoAVL:
        """
        Encontra nó com menor chave na subárvore
        Usado na remoção para encontrar sucessor
        Complexidade: O(log n)
        """
        atual = no
        while atual.esquerda:
            atual = atual.esquerda
        return atual
    
    def _remover_recursivo(self, no: Optional[NoAVL], categoria_id: str) -> Optional[NoAVL]:
        """
        Remove categoria da árvore de forma recursiva
        Complexidade: O(log n)
        """
        # Caso base
        if not no:
            return None
        
        # Recursão para encontrar nó
        if categoria_id < no.categoria.id:
            no.esquerda = self._remover_recursivo(no.esquerda, categoria_id)
        elif categoria_id > no.categoria.id:
            no.direita = self._remover_recursivo(no.direita, categoria_id)
        else:
            # Nó encontrado - executar remoção
            
            # Caso 1: Nó com um filho ou folha
            if not no.esquerda:
                self.total_categorias -= 1
                return no.direita
            if not no.direita:
                self.total_categorias -= 1
                return no.esquerda
            
            # Caso 2: Nó com dois filhos
            # Encontrar sucessor (menor da subárvore direita)
            sucessor = self._encontrar_minimo(no.direita)
            no.categoria = sucessor.categoria
            no.direita = self._remover_recursivo(no.direita, sucessor.categoria.id)
        
        # Balancear após remoção
        return self._balancear(no)
    
    def _percorrer_inorder(self, no: Optional[NoAVL], resultado: List[Categoria]) -> None:
        """
        Percorre árvore em ordem (in-order traversal) recursivamente
        Visita: esquerda -> raiz -> direita
        Produz lista ordenada de categorias por ID
        Complexidade: O(n) - visita todos os nós
        """
        if no:
            self._percorrer_inorder(no.esquerda, resultado)
            resultado.append(no.categoria)
            self._percorrer_inorder(no.direita, resultado)
    
    def _percorrer_hierarquico(self, no: Optional[NoAVL], nivel: int, resultado: List[Tuple[int, Categoria]]) -> None:
        """
        Percorre árvore mantendo informação de nível hierárquico
        Usado para impressão visual da estrutura
        Complexidade: O(n)
        """
        if no:
            resultado.append((nivel, no.categoria))
            self._percorrer_hierarquico(no.esquerda, nivel + 1, resultado)
            self._percorrer_hierarquico(no.direita, nivel + 1, resultado)
    
    # ========== API PÚBLICA ==========
    
    def inserir(self, categoria: Categoria) -> None:
        """Insere nova categoria no sistema. Complexidade: O(log n)"""
        self.estatisticas["insercoes"] += 1
        self.raiz = self._inserir_recursivo(self.raiz, categoria)
        self.total_produtos_sistema += categoria.total_produtos
    
    def buscar(self, categoria_id: str) -> Optional[Categoria]:
        """Busca categoria por ID. Complexidade: O(log n)"""
        self.estatisticas["buscas"] += 1
        return self._buscar_recursivo(self.raiz, categoria_id)
    
    def remover(self, categoria_id: str) -> bool:
        """Remove categoria do sistema. Complexidade: O(log n)"""
        categoria = self.buscar(categoria_id)
        if categoria:
            self.estatisticas["remocoes"] += 1
            self.total_produtos_sistema -= categoria.total_produtos
            self.raiz = self._remover_recursivo(self.raiz, categoria_id)
            return True
        return False
    
    def listar_categorias_ordenadas(self) -> List[Categoria]:
        """Lista todas as categorias em ordem alfabética. Complexidade: O(n)"""
        resultado = []
        self._percorrer_inorder(self.raiz, resultado)
        return resultado
    
    def obter_estrutura_hierarquica(self) -> List[Tuple[int, Categoria]]:
        """Retorna estrutura com níveis de hierarquia. Complexidade: O(n)"""
        resultado = []
        self._percorrer_hierarquico(self.raiz, 0, resultado)
        return resultado
    
    def obter_estatisticas(self) -> Dict[str, Any]:
        """Retorna estatísticas de uso da árvore"""
        return {
            **self.estatisticas,
            "total_categorias": self.total_categorias,
            "total_produtos": self.total_produtos_sistema,
            "altura_arvore": self._obter_altura(self.raiz),
            "fator_balanceamento_raiz": self._calcular_fator_balanceamento(self.raiz)
        }