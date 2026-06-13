import os
import pandas as pd

def extract_raw_data(file_path):
    """
    Localiza e carrega o arquivo de dados brutos para o pipeline.
    """
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"Erro Estrutural: O arquivo bruto não foi encontrado em: {file_path}")
        
    print(f"[EXTRAÇÃO] Arquivo bruto localizado com sucesso em: {file_path}")
    
    df_raw = pd.read_csv(file_path)
    print(f"[EXTRAÇÃO] Total de linhas brutas importadas: {len(df_raw)}")
    
    # Linha de diagnóstico para identificarmos o cabeçalho original
    print(f"[DIAGNÓSTICO] Colunas encontradas no arquivo real: {list(df_raw.columns)}")
    
    return df_raw
