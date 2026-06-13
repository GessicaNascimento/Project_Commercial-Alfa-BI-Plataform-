import os
import pandas as pd
import psycopg2
from psycopg2.extras import execute_values
from configparser import ConfigParser

def load_db_config(filename="database.ini", section="postgresql"):
    """Lê as credenciais do arquivo buscando dinamicamente na raiz do projeto."""
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raiz_projeto = os.path.abspath(os.path.join(script_dir, "..", ".."))
    caminho_absoluto_ini = os.path.join(raiz_projeto, filename)
    
    if not os.path.exists(caminho_absoluto_ini):
        caminho_absoluto_ini = os.path.join(script_dir, filename)

    if not os.path.exists(caminho_absoluto_ini):
        raise FileNotFoundError(f"Erro Crítico: O arquivo '{filename}' não foi encontrado na raiz ({raiz_projeto}) nem em ({script_dir}).")
    
    parser = ConfigParser()
    parser.read(caminho_absoluto_ini)
    db_params = {}
    if parser.has_section(section):
        for param in parser.items(section):
            db_params[param[0]] = param[1]
    else:
        raise FileNotFoundError(f"Configuração [{section}] não encontrada em {caminho_absoluto_ini}")
    return db_params

def run_etl():
    print("=== INICIANDO ETL DE PRODUÇÃO (STAR SCHEMA) ===")
    
    # Mapeamento de caminhos relativos ao script para ler dados brutos e salvar processados
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raiz_projeto = os.path.abspath(os.path.join(script_dir, "..", ".."))
    
    caminho_bruto = os.path.join(raiz_projeto, "data", "raw", "cosmetics_sales_data.csv")
    pasta_processados = os.path.join(raiz_projeto, "data", "processed")
    
    # 1. Extração
    print(f"[ETL] Lendo arquivo bruto: {caminho_bruto}")
    df_raw = pd.read_csv(caminho_bruto)
    
    # 2. Transformação e Modelagem Dimensional
    print("[ETL] Tratando e normalizando dimensões...")
    df_clean = df_raw.dropna(subset=['Sales Person', 'Product']).drop_duplicates().copy()
    
    df_clean['id_cliente'] = df_clean['Sales Person'].astype('category').cat.codes + 1
    df_clean['id_produto'] = df_clean['Product'].astype('category').cat.codes + 1
    df_clean['id_venda'] = range(1, len(df_clean) + 1)
    df_clean['data_venda'] = pd.to_datetime(df_clean['Date']).dt.strftime('%Y-%m-%d')
    df_clean['quantidade'] = df_clean['Boxes Shipped'].astype(int)
    df_clean['valor_total'] = df_clean['Amount ($)'].astype(float)
    df_clean['preco_unitario'] = (df_clean['valor_total'] / df_clean['quantidade']).round(2)
    
    # Estruturação das tabelas dimensionais e fato
    dim_clientes = df_clean[['id_cliente', 'Sales Person', 'Country']].copy()
    dim_clientes.columns = ['id_cliente', 'nome_cliente', 'pais_cliente']
    dim_clientes = dim_clientes.drop_duplicates(subset=['id_cliente'])
    
    dim_produtos = df_clean[['id_produto', 'Product']].copy()
    dim_produtos.columns = ['id_produto', 'nome_produto']
    dim_produtos['categoria_produto'] = 'Cosmetics'
    dim_produtos = dim_produtos.drop_duplicates(subset=['id_produto'])
    
    fato_vendas = df_clean[['id_venda', 'id_cliente', 'id_produto', 'data_venda', 'quantidade', 'preco_unitario', 'valor_total']]
    
    # 3. Carga Local (Backup em processed/)
    print(f"[ETL] Salvando backups locais em: {pasta_processados}")
    os.makedirs(pasta_processados, exist_ok=True)
    dim_clientes.to_csv(os.path.join(pasta_processados, "dim_clientes_processed.csv"), index=False)
    dim_produtos.to_csv(os.path.join(pasta_processados, "dim_produtos_processed.csv"), index=False)
    fato_vendas.to_csv(os.path.join(pasta_processados, "fato_vendas_processed.csv"), index=False)
    
    # 4. Ingestão Massiva no PostgreSQL
    print("[ETL] Conectando ao banco de dados...")
    db_params = load_db_config()
    conn = psycopg2.connect(**db_params)
    cursor = conn.cursor()
    
    try:
        # Limpeza prévia para re-carga atômica
        cursor.execute("TRUNCATE TABLE fato_vendas CASCADE;")
        cursor.execute("TRUNCATE TABLE dim_clientes CASCADE;")
        cursor.execute("TRUNCATE TABLE dim_produtos CASCADE;")
        
        # Carga síncrona
        print("[ETL] Injetando dim_clientes...")
        execute_values(cursor, "INSERT INTO dim_clientes VALUES %s", list(dim_clientes.itertuples(index=False, name=None)))
        
        print("[ETL] Injetando dim_produtos...")
        execute_values(cursor, "INSERT INTO dim_produtos VALUES %s", list(dim_produtos.itertuples(index=False, name=None)))
        
        print("[ETL] Injetando fato_vendas...")
        execute_values(cursor, "INSERT INTO fato_vendas VALUES %s", list(fato_vendas.itertuples(index=False, name=None)))
        
        conn.commit()
        print(f"=== ETL CONCLUÍDO COM SUCESSO! {len(fato_vendas)} LINHAS NA FATO ===")
    except Exception as e:
        conn.rollback()
        raise Exception(f"Falha na execução do DML de Carga: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    run_etl()