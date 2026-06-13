import sqlite3

def gerar_relatorio_gerencial():
    db_name = "commercial_alfa_ltda.db"
    
    try:
        conexao = sqlite3.connect(db_name)
        cursor = conexao.cursor()
        
        # 1. Métrica Global
        query_global = """
        SELECT 
            COUNT(id_venda) AS total_transacoes,
            SUM(quantidade) AS total_caixas,
            ROUND(SUM(valor_total), 2) AS faturamento_global,
            ROUND(AVG(valor_total), 2) AS ticket_medio_global
        FROM fato_vendas;
        """
        cursor.execute(query_global)
        transacoes, caixas, faturamento, ticket = cursor.fetchone()
        
        # 2. Ranking de Produtos mais vendidos
        query_produtos = """
        SELECT 
            p.nome_produto,
            SUM(f.quantidade) AS total_unidades,
            ROUND(SUM(f.valor_total), 2) AS receita_produto
        FROM fato_vendas f
        JOIN dim_produtos p ON f.id_produto = p.id_produto
        GROUP BY p.nome_produto
        ORDER BY receita_produto DESC;
        """
        cursor.execute(query_produtos)
        produtos = cursor.fetchall()
        
        # Impressão do Relatório Executivo Final
        print("\n" + "="*20 + " COMMERCIAL ALFA LTDA - RELATÓRIO EXECUTIVO " + "="*20)
        print(f"Faturamento Global Bruto:  ${faturamento:,.2f}")
        print(f"Volume Total de Transações: {transacoes} contratos")
        print(f"Volume de Caixas Despachadas: {caixas} unidades")
        print(f"Ticket Médio por Contrato:  ${ticket:,.2f}")
        print("-" * 74)
        
        print("RANKING DE PERFORMANCE POR PRODUTO:")
        print(f"{'Produto':<25} | {'Caixas Despachadas':<20} | {'Receita Gerada':<15}")
        print("-" * 74)
        for prod in produtos:
            nome, qtd, rec = prod
            print(f"{nome:<25} | {qtd:<20} | ${rec:,.2f}")
        print("="*74 + "\n")
        
    except sqlite3.Error as e:
        print(f"-> Erro ao gerar relatório executivo: {e}")
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    gerar_relatorio_gerencial()
