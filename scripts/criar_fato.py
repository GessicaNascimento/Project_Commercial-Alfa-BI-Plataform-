import sqlite3

def criar_tabelas_dimensao_completo():
    try:
        db_name = "commercial_alfa_ltda.db"
        conexao = sqlite3.connect(db_name)
        cursor = conexao.cursor()
        
        # 1. Tabela Dimensão Clientes
        query_clientes = """
        CREATE TABLE IF NOT EXISTS dim_clientes (
            id_cliente INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_cliente TEXT NOT NULL,
            pais_cliente TEXT NOT NULL
        );
        """
        
        # 2. Tabela Dimensão Produtos
        query_produtos = """
        CREATE TABLE IF NOT EXISTS dim_produtos (
            id_produto INTEGER PRIMARY KEY AUTOINCREMENT,
            nome_produto TEXT NOT NULL,
            categoria_produto TEXT NOT NULL
        );
        """
        
        # 3. Tabela Dimensão Tempo (Calendário)
        query_tempo = """
        CREATE TABLE IF NOT EXISTS dim_tempo (
            id_tempo TEXT PRIMARY KEY,
            ano INTEGER NOT NULL,
            mes INTEGER NOT NULL,
            dia INTEGER NOT NULL,
            dia_da_semana TEXT NOT NULL
        );
        """
        
        # Executa todos os comandos
        cursor.execute(query_clientes)
        cursor.execute(query_produtos)
        cursor.execute(query_tempo)
        
        conexao.commit()
        print(f"-> Sucesso: As 3 dimensões (clientes, produtos, tempo) foram criadas no banco '{db_name}'.")
        
    except sqlite3.Error as e:
        print(f"-> Erro crítico no Passo 2: {e}")
    finally:
        if conexao:
            conexao.close()

if __name__ == "__main__":
    criar_tabelas_dimensao_completo()
