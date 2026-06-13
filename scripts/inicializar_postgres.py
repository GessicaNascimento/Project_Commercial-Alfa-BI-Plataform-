import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def configurar_postgres():
    # Configurações de conexão padrão do Homebrew (geralmente usuário é o seu nome do sistema)
    # Por padrão, o Homebrew cria o superusuário com o mesmo nome do seu usuário do Mac
    usuario_mac = "Ruca" 
    
    conexao = None
    try:
        # 1. Conecta ao banco padrão 'postgres' para poder criar o nosso banco de dados
        conexao = psycopg2.connect(
            dbname="postgres",
            user=usuario_mac,
            host="localhost"
        )
        conexao.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
        cursor = conexao.cursor()
        
        # Cria o banco de dados oficial se ele não existir
        cursor.execute("SELECT 1 FROM pg_catalog.pg_database WHERE datname = 'commercial_alfa_ltda';")
        exists = cursor.fetchone()
        if not exists:
            cursor.execute("CREATE DATABASE commercial_alfa_ltda;")
            print("-> Banco 'commercial_alfa_ltda' criado com sucesso.")
        else:
            print("-> Banco 'commercial_alfa_ltda' já existe.")
            
        cursor.close()
        conexao.close()
        
        # 2. Conecta diretamente ao novo banco para criar o Schema com as Constraints
        conexao = psycopg2.connect(
            dbname="commercial_alfa_ltda",
            user=usuario_mac,
            host="localhost"
        )
        cursor = conexao.cursor()
        
        # DDL - Criação das Dimensões primeiro (necessárias para as Foreign Keys da Fato)
        query_dim_clientes = """
        CREATE TABLE IF NOT EXISTS dim_clientes (
            id_cliente SERIAL PRIMARY KEY,
            nome_cliente VARCHAR(255) NOT NULL,
            pais_cliente VARCHAR(100) NOT NULL
        );
        """
        
        query_dim_produtos = """
        CREATE TABLE IF NOT EXISTS dim_produtos (
            id_produto SERIAL PRIMARY KEY,
            nome_produto VARCHAR(255) NOT NULL,
            categoria_produto VARCHAR(100) NOT NULL
        );
        """
        
        query_dim_tempo = """
        CREATE TABLE IF NOT EXISTS dim_tempo (
            id_tempo DATE PRIMARY KEY,
            ano INT NOT NULL,
            mes INT NOT NULL,
            dia INT NOT NULL,
            dia_da_semana VARCHAR(50) NOT NULL
        );
        """
        
        # DDL - Criação da Fato com Restrições de Integridade (Foreign Keys)
        query_fato_vendas = """
        CREATE TABLE IF NOT EXISTS fato_vendas (
            id_venda SERIAL PRIMARY KEY,
            data_venda DATE NOT NULL,
            id_cliente INT NOT NULL,
            id_produto INT NOT NULL,
            quantidade INT NOT NULL CHECK (quantidade > 0),
            valor_total NUMERIC(12,2) NOT NULL CHECK (valor_total >= 0),
            
            -- Restrições de Integridade Referencial (Constraints)
            CONSTRAINT fk_tempo FOREIGN KEY (data_venda) REFERENCES dim_tempo(id_tempo) ON DELETE CASCADE,
            CONSTRAINT fk_cliente FOREIGN KEY (id_cliente) REFERENCES dim_clientes(id_cliente) ON DELETE CASCADE,
            CONSTRAINT fk_produto FOREIGN KEY (id_produto) REFERENCES dim_produtos(id_produto) ON DELETE CASCADE
        );
        """
        
        # Execução sequencial dos DDLs
        cursor.execute(query_dim_clientes)
        cursor.execute(query_dim_produtos)
        cursor.execute(query_dim_tempo)
        cursor.execute(query_fato_vendas)
        
        conexao.commit()
        print("-> Sucesso: Schema Star Schema e Restrições de Integridade aplicados no PostgreSQL!")
        
    except Exception as e:
        print(f"-> Erro crítico no Passo 2: {e}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    configurar_postgres()
