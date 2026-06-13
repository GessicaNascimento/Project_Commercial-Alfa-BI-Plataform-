import psycopg2

def criar_views_analiticas():
    usuario_mac = "Ruca"
    db_name = "commercial_alfa_ltda"
    
    conexao = None
    try:
        conexao = psycopg2.connect(
            dbname=db_name,
            user=usuario_mac,
            host="localhost"
        )
        cursor = conexao.cursor()
        
        print("-> Construindo a camada semântica de SQL Views no PostgreSQL...")
        
        # View 1: Resumo Comercial por País (KPIs Geográficos)
        view_pais = """
        CREATE OR REPLACE VIEW v_kpi_performance_pais AS
        SELECT 
            c.pais_cliente AS pais,
            COUNT(f.id_venda) AS total_transacoes,
            SUM(f.quantidade) AS total_caixas,
            SUM(f.valor_total) AS receita_total,
            ROUND(AVG(f.valor_total), 2) AS ticket_medio
        FROM fato_vendas f
        JOIN dim_clientes c ON f.id_cliente = c.id_cliente
        GROUP BY c.pais_cliente;
        """
        
        # View 2: Faturamento Mensal Histórico (KPIs de Tendência Temporal)
        view_mensal = """
        CREATE OR REPLACE VIEW v_kpi_receita_mensal AS
        SELECT 
            t.ano,
            t.mes,
            SUM(f.valor_total) AS receita_mensal,
            SUM(f.quantidade) AS caixas_mensais
        FROM fato_vendas f
        JOIN dim_tempo t ON f.data_venda = t.id_tempo
        GROUP BY t.ano, t.mes
        ORDER BY t.ano ASC, t.mes ASC;
        """
        
        # View 3: Curva de Performance de Produtos (Análise de Pareto/Portfólio)
        view_produtos = """
        CREATE OR REPLACE VIEW v_kpi_ranking_produtos AS
        SELECT 
            p.nome_produto AS produto,
            SUM(f.quantidade) AS caixas_vendidas,
            SUM(f.valor_total) AS receita_gerada,
            ROUND((SUM(f.valor_total) / SUM(f.quantidade)), 2) AS preco_medio_caixa
        FROM fato_vendas f
        JOIN dim_produtos p ON f.id_produto = p.id_produto
        GROUP BY p.nome_produto;
        """
        
        # Execução das queries DDL de criação das Views
        cursor.execute(view_pais)
        cursor.execute(view_mensal)
        cursor.execute(view_produtos)
        
        conexao.commit()
        print("-> Sucesso: SQL Views analíticas (v_kpi_performance_pais, v_kpi_receita_mensal, v_kpi_ranking_produtos) criadas com sucesso!")
        
    except Exception as e:
        if conexao:
            conexao.rollback()
        print(f"-> Erro crítico no Passo 4: {e}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    criar_views_analiticas()
