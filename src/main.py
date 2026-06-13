import os
from database import init_database
from extract import extract_raw_data
from transform import transform_data
from load import save_to_processed_folder, load_data_to_postgres

def run_pipeline():
    print("=== INICIANDO PIPELINE ANALÍTICO COMPLETO (COMMERCIAL-ALFA) ===")
    
    # Configuração de caminhos locais
    caminho_bruto = "../data/raw/cosmetics_sales_data.csv"
    pasta_processados = "../data/processed/"
    
    try:
        # FASE 0: Inicialização e Reset Estrutural do Banco de Dados
        init_database()
        print("-" * 60)
        
        # FASE 1: Extração (Leitura das 374 linhas brutas reais)
        df_bruto = extract_raw_data(caminho_bruto)
        print("-" * 60)
        
        # FASE 2: Transformação e Modelagem Dimensional (Star Schema)
        clientes, produtos, vendas = transform_data(df_bruto)
        print("-" * 60)
        
        # FASE 3: Carga Física Local (Arquivos de backup .csv)
        save_to_processed_folder(clientes, produtos, vendas, base_path=pasta_processados)
        print("-" * 60)
        
        # FASE 4: Carga Física Relacional (Ingestão Automatizada no PostgreSQL)
        load_data_to_postgres(clientes, produtos, vendas)
        
        print("\n=== PIPELINE DE ENGENHARIA DE DADOS EXECUTADO COM SUCESSO ABSOLUTO! ===")
        print(" -> Arquivos locais gerados em: 'data/processed/'")
        print(" -> Tabelas Star Schema povoadas e indexadas no PostgreSQL.")
        
    except Exception as e:
        print(f"\n[ERRO CRÍTICO NO PIPELINE]: {e}")

if __name__ == "__main__":
    run_pipeline()