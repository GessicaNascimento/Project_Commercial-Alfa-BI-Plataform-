import os
import psycopg2
from configparser import ConfigParser

def load_db_config(filename="database.ini", section="postgresql"):
    """Busca dinamicamente o arquivo de configuração na raiz do projeto."""
    # Descobre o caminho absoluto da pasta onde este script (carga_dados.py) está salvo
    script_dir = os.path.dirname(os.path.abspath(__file__))
    
    # Sobe apenas um nível para chegar na raiz do repositório
    raiz_projeto = os.path.abspath(os.path.join(script_dir, ".."))
    
    # Define o caminho absoluto final apontando para a raiz
    caminho_absoluto_ini = os.path.join(raiz_projeto, filename)
    
    # Caso o arquivo esteja por engano dentro da própria pasta scripts/
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

def implantar_views():
    print("=== IMPLANTANDO VIEWS ANALÍTICAS NO POSTGRESQL ===")
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raiz_projeto = os.path.abspath(os.path.join(script_dir, ".."))
    pasta_views = os.path.join(raiz_projeto, "database", "views")
    
    # Lista oficial de views mapeadas na sua árvore de diretórios
    arquivos_views = [
        "v_kpi_performance_pais.sql",
        "v_kpi_receita_mensal.sql",
        "v_kpi_ranking_produtos.sql"
    ]
    
    # Conexão com o Banco
    params = load_db_config()
    conn = psycopg2.connect(**params)
    cursor = conn.cursor()
    
    try:
        for arquivo in arquivos_views:
            caminho_sql = os.path.join(pasta_views, arquivo)
            print(f"[VIEWS] Aplicando estrutura: {arquivo}")
            
            with open(caminho_sql, "r") as f:
                cursor.execute(f.read())
                
        conn.commit()
        print("=== VIEWS ANALÍTICAS IMPLANTADAS COM SUCESSO ABSOLUTO! ===")
        
    except Exception as e:
        conn.rollback()
        raise Exception(f"Falha na implantação das Views: {e}")
    finally:
        cursor.close()
        conn.close()

if __name__ == "__main__":
    implantar_views()