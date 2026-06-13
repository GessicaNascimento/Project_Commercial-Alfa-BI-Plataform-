import psycopg2
import csv
import os

def exportar_camada_semantica():
    usuario_mac = "Ruca"
    db_name = "commercial_alfa_ltda"
    diretorio_saida = "../camada_bi"
    
    # Cria a pasta de saída se não existir
    if not os.path.exists(diretorio_saida):
        os.makedirs(diretorio_saida)
        
    views = [
        ("v_kpi_performance_pais", "bi_performance_pais.csv"),
        ("v_kpi_receita_mensal", "bi_receita_mensal.csv"),
        ("v_kpi_ranking_produtos", "bi_ranking_produtos.csv")
    ]
    
    conexao = None
    try:
        conexao = psycopg2.connect(dbname=db_name, user=usuario_mac, host="localhost")
        cursor = conexao.cursor()
        
        print("-> Exportando Views analíticas para a carga no Power BI...")
        
        for view_name, file_name in views:
            caminho_final = os.path.join(diretorio_saida, file_name)
            
            # Executa a query de leitura da View
            cursor.execute(f"SELECT * FROM {view_name};")
            colunas = [desc[0] for desc in cursor.description]
            linhas = cursor.fetchall()
            
            # Grava o CSV otimizado para BI
            with open(caminho_final, mode='w', encoding='utf-8', newline='') as f:
                escritor = csv.writer(f)
                escritor.writerow(colunas) # Cabeçalho
                escritor.writerows(linhas) # Dados
                
            print(f"   [OK] {view_name} -> {caminho_final}")
            
        print("\n-> Sucesso: Camada de dados para o Power BI provisionada com integridade!")
        
    except Exception as e:
        print(f"-> Erro crítico no Passo 6: {e}")
    finally:
        if conexao:
            cursor.close()
            conexao.close()

if __name__ == "__main__":
    exportar_camada_semantica()
