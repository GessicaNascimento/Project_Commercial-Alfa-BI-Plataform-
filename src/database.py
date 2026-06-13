import os
import psycopg2
from configparser import ConfigParser

def load_db_config(filename="../config/database.ini", section="postgresql"):
    """
    Lê o arquivo INI de configuração e extrai as credenciais de acesso de forma segura.
    """
    if not os.path.exists(filename):
        raise FileNotFoundError(f"Erro de Configuração: O arquivo {filename} não foi encontrado.")
        
    parser = ConfigParser()
    parser.read(filename)
    
    db_params = {}
    if parser.has_section(section):
        params = parser.items(section)
        for param in params:
            db_params[param[0]] = param[1]
    else:
        raise Exception(f"Seção [{section}] não foi encontrada no arquivo {filename}")
        
    return db_params

def init_database():
    """
    Conecta ao PostgreSQL e executa os scripts DDL (schema e constraints) 
    para resetar/criar o esqueleto das tabelas.
    """
    print("[BANCO] Iniciando conexão com o PostgreSQL...")
    
    # Carrega os parâmetros de conexão isolados
    params = load_db_config()
    
    # Estabelece a conexão física com o banco
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    
    print("[BANCO] Conexão estabelecida com sucesso.")
    
    try:
        # Como estamos desenvolvendo e testando estruturalmente, 
        # vamos limpar tabelas antigas para evitar conflitos de ID
        print("[BANCO] Resetando estruturas antigas (Drop Tables se existirem)...")
        cursor.execute("DROP TABLE IF EXISTS fato_vendas CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS dim_clientes CASCADE;")
        cursor.execute("DROP TABLE IF EXISTS dim_produtos CASCADE;")
        
        # 1. Executa o Schema Base
        print("[BANCO] Executando schema.sql...")
        with open("../sql/schema.sql", "r") as f:
            cursor.execute(f.read())
            
        # 2. Executa as Restrições (Constraints)
        print("[BANCO] Executando constraints.sql...")
        with open("../sql/constraints.sql", "r") as f:
            cursor.execute(f.read())
            
        # Confirma as alterações de forma atômica no banco de dados
        conn.commit()
        print("[BANCO] Estrutura Star Schema inicializada no PostgreSQL com sucesso absoluto!")
        
    except Exception as e:
        conn.rollback() # Cancela a operação em caso de falha estrutural
        raise Exception(f"Erro ao inicializar o banco de dados: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    # Teste isolado do componente de banco de dados
    print("[TESTE] Executando inicialização do banco de forma isolada...")
    try:
        init_database()
    except Exception as e:
        print(f"\n[TESTE - ERRO CRÍTICO]: {e}")
        print("DICA: Certifique-se de que o seu aplicativo PostgreSQL (pgAdmin/Postgres App) está rodando no Mac.")