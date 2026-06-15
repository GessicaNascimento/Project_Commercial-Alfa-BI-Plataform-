import os
import pandas as pd
import logging

def extract_raw_data(file_path):
    """
    Localiza e carrega o arquivo de dados brutos para o pipeline.
    """
    if not os.path.exists(file_path):
        error_msg = f"Erro Estrutural: O arquivo bruto não foi encontrado em: {file_path}"
        logging.error(error_msg)
        raise FileNotFoundError(error_msg)
        
    logging.info("Iniciando a etapa de extração de dados do pipeline ETL.")
    
    df_raw = pd.read_csv(file_path)
    
    logging.info(f"Total de linhas brutas importadas: {len(df_raw)}")
    logging.info(f"Colunas encontradas no arquivo real: {list(df_raw.columns)}")
    
    return df_raw