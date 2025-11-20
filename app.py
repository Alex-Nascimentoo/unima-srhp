"""
Sistema de Recomendação Hierárquica de Produtos (SRHP)
Aplicação Principal - Demonstração Completa
"""

from src.core.avl_tree import ArvoreAVLCategorias
from src.model.category import Categoria
from src.model.product import Produto
from src.model.status_product import StatusProduto
from modules.business.recommendation_system import SistemaRecomendacao
from modules.business.performance_analyzer import AnalisadorPerformance


class SistemaRecomendacaoHierarquicaProdutos:
    """
    Classe principal do sistema SRHP
    Gerencia todas as operações e módulos do sistema
    """
    
    def __init__(self):
        self.arvore = ArvoreAVLCategorias()
        self.recomendador = SistemaRecomendacao(self.arvore)
        self.analisador = AnalisadorPerformance()
        print("=" * 60)
        print("SISTEMA DE RECOMENDAÇÃO HIERÁRQUICA DE PRODUTOS (SRHP)")
        print("Versão 1.0.0 | Estrutura: AVL Tree")
        print("=" * 60)
    
    def popular_dados_exemplo(self):
        """Popula sistema com dados de exemplo para demonstração"""
        print("\n📦 Populando sistema com dados de exemplo...")
        
        # Categoria: Eletrônicos
        cat_eletronicos = Categoria(
            id="eletronicos",
            nome="Eletrônicos",
            descricao="Produtos eletrônicos e tecnologia",
            nivel=0
        )
        
        produtos_eletronicos = [
            Produto("ELEC001", "Smartphone Galaxy S23", 3499.90, 
                   "Smartphone premium com câmera de 50MP", 
                   ["smartphone", "samsung", "android"], 45, StatusProduto.ATIVO, 1250, 89),
            Produto("ELEC002", "Notebook Dell Inspiron", 4299.00,
                   "Notebook i7 16GB RAM", 
                   ["notebook", "dell", "computador"], 23, StatusProduto.ATIVO, 890, 45),
            Produto("ELEC003", "Fone Bluetooth JBL", 299.90,
                   "Fone sem fio com cancelamento de ruído",
                   ["fone", "audio", "bluetooth"], 120, StatusProduto.ATIVO, 2100, 156)
        ]
        
        for prod in produtos_eletronicos:
            cat_eletronicos.adicionar_produto(prod)
        
        # Categoria: Livros
        cat_livros = Categoria(
            id="livros",
            nome="Livros",
            descricao="Livros e publicações",
            nivel=0
        )
        
        produtos_livros = [
            Produto("LIV001", "Clean Code", 89.90,
                   "Boas práticas de programação",
                   ["programacao", "tecnologia", "desenvolvimento"], 67, StatusProduto.ATIVO, 450, 78),
            Produto("LIV002", "Algoritmos e Estruturas de Dados", 125.00,
                   "Fundamentos de algoritmos",
                   ["programacao", "algoritmos", "educacao"], 34, StatusProduto.ATIVO, 320, 45)
        ]
        
        for prod in produtos_livros:
            cat_livros.adicionar_produto(prod)
        
        # Categoria: Moda
        cat_moda = Categoria(
            id="moda",
            nome="Moda e Vestuário",
            descricao="Roupas e acessórios",
            nivel=0
        )
        
        produtos_moda = [
            Produto("MOD001", "Camiseta Nike Dry-Fit", 129.90,
                   "Camiseta esportiva respirável",
                   ["roupa", "esporte", "nike"], 200, StatusProduto.ATIVO, 980, 123),
            Produto("MOD002", "Tênis Adidas Ultraboost", 699.90,
                   "Tênis para corrida de alta performance",
                   ["tenis", "esporte", "adidas"], 45, StatusProduto.ATIVO, 1450, 67)
        ]
        
        for prod in produtos_moda:
            cat_moda.adicionar_produto(prod)
        
        # Inserir categorias na árvore
        self.arvore.inserir(cat_eletronicos)
        self.arvore.inserir(cat_livros)
        self.arvore.inserir(cat_moda)
        
        print(f"✅ Sistema populado com {self.arvore.total_categorias} categorias")
        print(f"✅ Total de {self.arvore.total_produtos_sistema} produtos cadastrados")
    
    def exibir_estrutura_hierarquica(self):
        """Exibe estrutura da árvore de forma hierárquica"""
        print("\n" + "=" * 60)
        print("📊 ESTRUTURA HIERÁRQUICA DE CATEGORIAS")
        print("=" * 60)
        
        estrutura = self.arvore.obter_estrutura_hierarquica()
        
        for nivel, categoria in estrutura:
            indentacao = "  " * nivel
            simbolo = "└─" if nivel > 0 else "●"
            print(f"{indentacao}{simbolo} {categoria.nome} (ID: {categoria.id})")
            print(f"{indentacao}   └─ Produtos: {categoria.total_produtos}")
    
    def exibir_estatisticas(self):
        """Exibe estatísticas da árvore AVL"""
        print("\n" + "=" * 60)
        print("📈 ESTATÍSTICAS DA ÁRVORE AVL")
        print("=" * 60)
        
        stats = self.arvore.obter_estatisticas()
        
        print(f"\n🌳 Estrutura da Árvore:")
        print(f"  • Total de categorias: {stats['total_categorias']}")
        print(f"  • Altura da árvore: {stats['altura_arvore']}")
        print(f"  • Fator de balanceamento (raiz): {stats['fator_balanceamento_raiz']}")
        
        print(f"\n📦 Produtos:")
        print(f"  • Total no sistema: {stats['total_produtos']}")
        
        print(f"\n⚡ Operações Realizadas:")
        print(f"  • Inserções: {stats['insercoes']}")
        print(f"  • Buscas: {stats['buscas']}")
        print(f"  • Remoções: {stats['remocoes']}")
        print(f"  • Rotações AVL: {stats['rotacoes']}")
    
    def demonstrar_recomendacoes(self):
        """Demonstra sistema de recomendações"""
        print("\n" + "=" * 60)
        print("🎯 SISTEMA DE RECOMENDAÇÕES")
        print("=" * 60)
        
        # 1. Recomendações por Categoria
        print("\n📱 Top 3 Produtos de Eletrônicos:")
        produtos = self.recomendador.recomendar_produtos_categoria("eletronicos", limite=3)
        for i, p in enumerate(produtos, 1):
            score = p.calcular_score_relevancia()
            print(f"  {i}. {p.nome}")
            print(f"     💰 R$ {p.preco:.2f} | ⭐ Score: {score:.0f} | 👁 Views: {p.visualizacoes} | 🛒 Vendas: {p.vendas}")
        
        # 2. Recomendações Globais
        print("\n🌟 Top 5 Produtos do Sistema (Global):")
        produtos = self.recomendador.recomendar_produtos_globais(limite=5)
        for i, p in enumerate(produtos, 1):
            score = p.calcular_score_relevancia()
            print(f"  {i}. {p.nome}")
            print(f"     💰 R$ {p.preco:.2f} | ⭐ Score: {score:.0f}")
        
        # 3. Produtos Similares (exemplo com Fone JBL)
        print("\n🔍 Produtos Similares ao 'Fone Bluetooth JBL':")
        similares = self.recomendador.recomendar_produtos_similares(
            "ELEC003", "eletronicos", limite=3
        )
        if similares:
            for i, p in enumerate(similares, 1):
                print(f"  {i}. {p.nome} - R$ {p.preco:.2f}")
                print(f"     Tags: {', '.join(p.tags)}")
        else:
            print("  ℹ️  Nenhum produto similar encontrado na base atual")
        
        # 4. Recomendações com Filtro de Tags
        print("\n🏷️  Produtos com Tag 'programacao':")
        produtos = self.recomendador.recomendar_produtos_globais(
            limite=5, filtro_tags=["programacao"]
        )
        for i, p in enumerate(produtos, 1):
            print(f"  {i}. {p.nome} - R$ {p.preco:.2f}")
    
    def demonstrar_analise_performance(self):
        """Demonstra análise de performance comparativa"""
        print("\n" + "=" * 60)
        print("⚡ ANÁLISE DE PERFORMANCE")
        print("=" * 60)
        
        categorias = self.arvore.listar_categorias_ordenadas()
        
        if categorias:
            analise = self.analisador.analise_comparativa_busca(self.arvore, categorias)
            
            print(f"\n🔍 Comparação: Busca AVL vs Busca Linear")
            print(f"  • Total de categorias: {analise['total_categorias']}")
            print(f"\n  ⏱️  Tempo AVL: {analise['tempo_avl_ms']:.4f} ms")
            print(f"     Complexidade: {analise['complexidade_avl']}")
            print(f"\n  ⏱️  Tempo Linear: {analise['tempo_linear_ms']:.4f} ms")
            print(f"     Complexidade: {analise['complexidade_linear']}")
            print(f"\n  📊 Ganho de Performance: {analise['ganho_percentual']:.2f}%")
            
            # Explicação teórica
            print(f"\n💡 Interpretação:")
            if analise['ganho_percentual'] > 0:
                print(f"     A árvore AVL é {analise['ganho_percentual']:.1f}% mais rápida!")
            print(f"     Com mais categorias, a vantagem do O(log n) aumenta exponencialmente.")
    
    def demonstrar_operacoes_crud(self):
        """Demonstra operações CRUD na árvore"""
        print("\n" + "=" * 60)
        print("🔧 OPERAÇÕES CRUD")
        print("=" * 60)
        
        # Buscar categoria
        print("\n🔍 Buscando categoria 'livros':")
        cat = self.arvore.buscar("livros")
        if cat:
            print(f"  ✅ Categoria encontrada: {cat.nome}")
            print(f"     Total de produtos: {cat.total_produtos}")
        
        # Adicionar nova categoria
        print("\n➕ Adicionando nova categoria 'games':")
        cat_games = Categoria(
            id="games",
            nome="Games",
            descricao="Jogos e consoles",
            nivel=0
        )
        
        # Adicionar produtos à categoria
        produto_game = Produto(
            "GAME001", "PlayStation 5", 4499.00,
            "Console de nova geração",
            ["console", "playstation", "games"],
            15, StatusProduto.ATIVO, 3500, 120
        )
        cat_games.adicionar_produto(produto_game)
        
        self.arvore.inserir(cat_games)
        print(f"  ✅ Categoria 'games' adicionada com sucesso!")
        print(f"  📊 Total de categorias agora: {self.arvore.total_categorias}")
        
        # Listar todas as categorias
        print("\n📋 Listando todas as categorias (ordenadas):")
        todas = self.arvore.listar_categorias_ordenadas()
        for i, cat in enumerate(todas, 1):
            print(f"  {i}. {cat.nome} (ID: {cat.id}) - {cat.total_produtos} produtos")
        
        # Remover categoria
        print("\n❌ Removendo categoria 'games':")
        removido = self.arvore.remover("games")
        if removido:
            print(f"  ✅ Categoria removida com sucesso!")
            print(f"  📊 Total de categorias agora: {self.arvore.total_categorias}")
    
    def exibir_detalhes_categoria(self, categoria_id: str):
        """Exibe detalhes completos de uma categoria"""
        print(f"\n" + "=" * 60)
        print(f"📂 DETALHES DA CATEGORIA: {categoria_id.upper()}")
        print("=" * 60)
        
        cat = self.arvore.buscar(categoria_id)
        
        if not cat:
            print(f"  ❌ Categoria '{categoria_id}' não encontrada!")
            return
        
        print(f"\n🏷️  Nome: {cat.nome}")
        print(f"📝 Descrição: {cat.descricao}")
        print(f"📊 Total de produtos: {cat.total_produtos}")
        print(f"📈 Nível hierárquico: {cat.nivel}")
        
        if cat.produtos:
            print(f"\n📦 Produtos da categoria:")
            for i, prod in enumerate(cat.produtos, 1):
                print(f"\n  {i}. {prod.nome}")
                print(f"     • ID: {prod.id}")
                print(f"     • Preço: R$ {prod.preco:.2f}")
                print(f"     • Status: {prod.status.value}")
                print(f"     • Estoque: {prod.estoque} unidades")
                print(f"     • Visualizações: {prod.visualizacoes}")
                print(f"     • Vendas: {prod.vendas}")
                print(f"     • Score: {prod.calcular_score_relevancia():.0f}")
                print(f"     • Tags: {', '.join(prod.tags)}")
    
    def executar_demonstracao_completa(self):
        """Executa demonstração completa de todas as funcionalidades"""
        
        # 1. Popular dados
        self.popular_dados_exemplo()
        
        # 2. Exibir estrutura
        self.exibir_estrutura_hierarquica()
        
        # 3. Exibir estatísticas
        self.exibir_estatisticas()
        
        # 4. Demonstrar recomendações
        self.demonstrar_recomendacoes()
        
        # 5. Análise de performance
        self.demonstrar_analise_performance()
        
        # 6. Operações CRUD
        self.demonstrar_operacoes_crud()
        
        # 7. Detalhes de categorias específicas
        self.exibir_detalhes_categoria("eletronicos")
        
        # 8. Estatísticas finais
        print("\n" + "=" * 60)
        print("📊 ESTATÍSTICAS FINAIS DO SISTEMA")
        print("=" * 60)
        stats = self.arvore.obter_estatisticas()
        print(f"\n  • Total de operações de busca: {stats['buscas']}")
        print(f"  • Total de inserções: {stats['insercoes']}")
        print(f"  • Total de remoções: {stats['remocoes']}")
        print(f"  • Total de rotações AVL: {stats['rotacoes']}")
        print(f"  • Altura da árvore: {stats['altura_arvore']}")
        print(f"  • Categorias ativas: {stats['total_categorias']}")
        print(f"  • Produtos no sistema: {stats['total_produtos']}")
        
        print("\n" + "=" * 60)
        print("✅ DEMONSTRAÇÃO CONCLUÍDA COM SUCESSO!")
        print("=" * 60)


# ==================== EXECUÇÃO PRINCIPAL ====================

if __name__ == "__main__":
    sistema = SistemaRecomendacaoHierarquicaProdutos()
    sistema.executar_demonstracao_completa()