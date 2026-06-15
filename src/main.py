import os
import sys
import logging
from extract import extract_raw_data
from transform import transform_data
from load import save_to_processed_folder, load_data_to_postgres

# Habilita a importação dinâmica de módulos da pasta 'scripts'
sys.path.append(os.path.join(os.path.dirname(__file__), '..'))
from scripts.data_validation import run_pipeline_validation
from scripts.analytics_forecast import generate_revenue_forecast

# Configuração de Segurança e Infraestrutura de Observabilidade
os.makedirs("logs", exist_ok=True)

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s [%(levelname)s] %(message)s',
    handlers=[
        logging.FileHandler("logs/etl_log.txt", encoding="utf-8"),
        logging.StreamHandler()
    ]
)

def run_pipeline():
    """
    Orquestra o fluxo ponta a ponta (End-to-End) com Validação e Forecasting ativos.
    """
    logging.info("==================================================")
    logging.info("INICIANDO EXECUÇÃO DO PIPELINE COMERCIAL ALFA BI")
    logging.info("==================================================")
    
    raw_data_path = "scripts/cosmetics_sales_data.csv"
    
    try:
        # 1. Extração de Dados Brutos
        df_raw = extract_raw_data(raw_data_path)
        
        # 2. Transformação e Modelagem Star Schema
        dim_clientes, dim_produtos, fato_vendas = transform_data(df_raw)
        
        # 3. Camada de Validação Estrutural (Data Quality Check)
        cols_clientes = ['id_cliente', 'nome_cliente', 'pais_cliente']
        cols_produtos = ['id_produto', 'nome_produto', 'categoria_produto']
        cols_fato = ['id_venda', 'id_cliente', 'id_produto', 'data_venda', 'quantidade', 'preco_unitario', 'valor_total']
        
        run_pipeline_validation(dim_clientes, cols_clientes, "Dimensão Clientes")
        run_pipeline_validation(dim_produtos, cols_produtos, "Dimensão Produtos")
        run_pipeline_validation(fato_vendas, cols_fato, "Tabela Fato Vendas")
        
        # 4. Camada de Inteligência de Negócio: Forecasting Preditivo
        df_mensal, previsao_proximo_mes = generate_revenue_forecast(fato_vendas)
        
        # 5. Carga Atômica e Backups Locais
        save_to_processed_folder(dim_clientes, dim_produtos, fato_vendas)
        load_data_to_postgres(dim_clientes, dim_produtos, fato_vendas)
        
        logging.info("==================================================")
        logging.info("PIPELINE EXECUTADO E CONCLUÍDO COM SUCESSO COMPLETO")
        logging.info("==================================================")
        
    except Exception as e:
        logging.critical(f"EXECUÇÃO ABORTADA: Falha catastrófica no orquestrador: {e}")

if __name__ == "__main__":
    run_pipeline()