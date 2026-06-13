import psycopg2

def executar_analytics_preditivo():
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
        
        print("-> Executando algoritmos de Customer Analytics (RFM) e Financial Forecast...")
        
        # 1. Query de Segmentação de Clientes (Frequência e Monetário adaptados para o Atacado)
        query_rfm = """
        SELECT 
            nome_cliente,
            pais_cliente,
            total_vendas AS frequencia,
            receita_total AS monetario,
            CASE 
                WHEN receita_total >= 70000 THEN 'Cliente VIP (Alta Receita)'
                WHEN receita_total BETWEEN 40000 AND 69999 THEN 'Cliente Regular (Médio Impacto)'
                ELSE 'Cliente Iniciante / Baixo Volume'
            END AS segmento_cliente
        FROM (
            SELECT 
                c.nome_cliente,
                c.pais_cliente,
                COUNT(f.id_venda) AS total_vendas,
                SUM(f.valor_total) AS receita_total
            FROM fato_vendas f
            JOIN dim_clientes c ON f.id_cliente = c.id_cliente
            GROUP BY c.nome_cliente, c.pais_cliente
        ) sub
        ORDER BY monetario DESC
        LIMIT 5;
        """
        
        # 2. Query de Forecast - Projeção de Faturamento para os Próximos 12 meses
        query_forecast = """
        SELECT 
            SUM(valor_total) AS faturamento_atual,
            ROUND(SUM(valor_total) * 1.05, 2) AS c_conservador,
            ROUND(SUM(valor_total) * 1.15, 2) AS c_otimista,
            ROUND(SUM(valor_total) * 1.25, 2) AS c_agressivo
        FROM fato_vendas;
        """
        
        # Executar e exibir Customer Analytics
        cursor.execute(query_rfm)
        top_clientes = cursor.fetchall()
        
        print("\n" + "="*20 + " CUSTOMER ANALYTICS: TOP 5 CLIENTES & SEGMENTAÇÃO " + "="*20)
        print(f"{'Cliente':<20} | {'País':<15} | {'Frequência':<10} | {'Monetário':<15} | {'Categoria':<25}")
        print("-" * 90)
        for clie in top_clientes:
            nome, pais, freq, mon, seg = clie
            print(f"{nome:<20} | {pais:<15} | {freq:<10} | ${mon:<14,.2f} | {seg:<25}")
            
        # Executar e exibir Forecast
        cursor.execute(query_forecast)
        atual, cons, otim, agres = cursor.fetchone()
        
        print("\n" + "="*25 + " FINANCIAL FORECAST (PRÓXIMO ANO) " + "="*25)
        print(f"Faturamento Base Atual : ${atual:,.2f}")
        print(f"Cenário Conservador (+5%): ${cons:,.2f} (Ganho de: ${cons-atual:,.2f})")
        print(f"Cenário Otimista   (+15%): ${otim:,.2f} (Ganho de: ${otim-atual:,.2f})")
        print(f"Cenário Agressivo  (+25%): ${agres:,.2f} (Ganho de: ${agres-atual:,.2f})")
        print("=" * 84 + "\n")
        
    except Exception as e:
        print(f"-> Erro crítico no Passo 5: {e}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    executar_analytics_preditivo()
