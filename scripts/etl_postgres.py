import csv
import psycopg2
from datetime import datetime

def executar_etl_postgres():
    usuario_mac = "Ruca"
    db_name = "commercial_alfa_ltda"
    caminho_csv = '../cosmetics_sales_data.csv'
    
    conexao = None
    try:
        conexao = psycopg2.connect(
            dbname=db_name,
            user=usuario_mac,
            host="localhost"
        )
        cursor = conexao.cursor()
        
        print("-> Iniciando a carga de dados no PostgreSQL...")
        
        with open(caminho_csv, mode='r', encoding='utf-8') as arquivo:
            leitor = csv.DictReader(arquivo)
            cont_linhas = 0
            
            for linha in leitor:
                vendedor_cliente = linha['Sales Person'].strip()
                pais = linha['Country'].strip()
                produto = linha['Product'].strip()
                data_str = inline_date if (inline_date := linha['Date'].strip()) else data_str
                valor_total = float(linha['Amount ($)'])
                quantidade = int(linha['Boxes Shipped'])
                
                # 1. POPULAR DIM_CLIENTES
                cursor.execute(
                    "SELECT id_cliente FROM dim_clientes WHERE nome_cliente = %s AND pais_cliente = %s;", 
                    (vendedor_cliente, pais)
                )
                resultado_cliente = cursor.fetchone()
                if resultado_cliente:
                    id_cliente = resultado_cliente[0]
                else:
                    cursor.execute(
                        "INSERT INTO dim_clientes (nome_cliente, pais_cliente) VALUES (%s, %s) RETURNING id_cliente;", 
                        (vendedor_cliente, pais)
                    )
                    id_cliente = cursor.fetchone()[0]
                
                # 2. POPULAR DIM_PRODUTOS
                cursor.execute("SELECT id_produto FROM dim_produtos WHERE nome_produto = %s;", (produto,))
                resultado_produto = cursor.fetchone()
                if resultado_produto:
                    id_produto = resultado_produto[0]
                else:
                    cursor.execute(
                        "INSERT INTO dim_produtos (nome_produto, categoria_produto) VALUES (%s, %s) RETURNING id_produto;", 
                        (produto, 'Cosméticos')
                    )
                    id_produto = cursor.fetchone()[0]
                
                # 3. POPULAR DIM_TEMPO
                dt = datetime.strptime(data_str, "%Y-%m-%d")
                dias_semana_pt = ["Segunda", "Terça", "Quarta", "Quinta", "Sexta", "Sábado", "Domingo"]
                dia_da_semana = dias_semana_pt[dt.weekday()]
                
                cursor.execute("SELECT id_tempo FROM dim_tempo WHERE id_tempo = %s;", (data_str,))
                if not cursor.fetchone():
                    cursor.execute(
                        "INSERT INTO dim_tempo (id_tempo, ano, mes, dia, dia_da_semana) VALUES (%s, %s, %s, %s, %s);",
                        (data_str, dt.year, dt.month, dt.day, dia_da_semana)
                    )
                
                # 4. POPULAR FATO_VENDAS (Correção da coluna para 'quantidade')
                cursor.execute("""
                    INSERT INTO fato_vendas (data_venda, id_cliente, id_produto, quantidade, valor_total) 
                    VALUES (%s, %s, %s, %s, %s);
                """, (data_str, id_cliente, id_produto, quantidade, valor_total))
                
                cont_linhas += 1
        
        # 5. OTIMIZAÇÃO E INDEXAÇÃO
        print("-> Criando índices de otimização no banco de dados...")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fato_data ON fato_vendas(data_venda);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fato_cliente ON fato_vendas(id_cliente);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_fato_produto ON fato_vendas(id_produto);")
        cursor.execute("CREATE INDEX IF NOT EXISTS idx_clientes_pais ON dim_clientes(pais_cliente);")
        
        conexao.commit()
        print(f"-> Sucesso: ETL concluído! {cont_linhas} registros armazenados e índices gerados.")
        
    except Exception as e:
        if conexao:
            conexao.rollback()
        print(f"-> Erro crítico no Passo 3: {e}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    executar_etl_postgres()
