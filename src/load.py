import os
import psycopg2
from psycopg2.extras import execute_values
from database import load_db_config
import logging

def save_to_processed_folder(dim_clientes, dim_produtos, fato_vendas, base_path="../data/processed/"):
    """
    Salva os arquivos locais na pasta 'processed'.
    """
    logging.info("Gravando arquivos de backup locais na pasta 'processed'...")
    os.makedirs(base_path, exist_ok=True)
    
    dim_clientes.to_csv(os.path.join(base_path, "dim_clientes_processed.csv"), index=False)
    dim_produtos.to_csv(os.path.join(base_path, "dim_produtos_processed.csv"), index=False)
    fato_vendas.to_csv(os.path.join(base_path, "fato_vendas_processed.csv"), index=False)
    
    logging.info("Backups locais em formato CSV gerados com sucesso.")

def load_data_to_postgres(dim_clientes, dim_produtos, fato_vendas):
    """
    Injeta os DataFrames tratados diretamente no PostgreSQL respeitando a integridade referencial.
    """
    logging.info("Iniciando conexão com o PostgreSQL para inserção de dados...")
    params = load_db_config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    
    try:
        # 1. Inserção massiva na Dimensão Clientes
        logging.info("Injetando registros na tabela 'dim_clientes'...")
        valores_clientes = list(dim_clientes.itertuples(index=False, name=None))
        query_clientes = "INSERT INTO dim_clientes (id_cliente, nome_cliente, pais_cliente) VALUES %s"
        execute_values(cursor, query_clientes, valores_clientes)
        
        # 2. Inserção massiva na Dimensão Produtos
        logging.info("Injetando registros na tabela 'dim_produtos'...")
        valores_produtos = list(dim_produtos.itertuples(index=False, name=None))
        query_produtos = "INSERT INTO dim_produtos (id_produto, nome_produto, categoria_produto) VALUES %s"
        execute_values(cursor, query_produtos, valores_produtos)
        
        # 3. Inserção massiva na Tabela Fato
        logging.info("Injetando registros na tabela fato 'fato_vendas'...")
        valores_vendas = list(fato_vendas.itertuples(index=False, name=None))
        query_vendas = """
            INSERT INTO fato_vendas 
            (id_venda, id_cliente, id_produto, data_venda, quantidade, preco_unitario, valor_total) 
            VALUES %s
        """
        execute_values(cursor, query_vendas, valores_vendas)
        
        conn.commit()
        logging.info(f"Sucesso! Banco de dados PostgreSQL atualizado com {len(valores_vendas)} transações comerciais.")
        
    except Exception as e:
        conn.rollback()
        error_msg = f"Falha crítica na carga dos dados para o PostgreSQL: {e}"
        logging.error(error_msg)
        raise Exception(error_msg)
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    logging.info("Componente de carga atualizado pronto para orquestração.")