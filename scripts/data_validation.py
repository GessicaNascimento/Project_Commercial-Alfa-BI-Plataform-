import pandas as pd
import logging

def run_pipeline_validation(df: pd.DataFrame, expected_columns: list, stage_name: str) -> bool:
    """
    Executa a validação estrutural de dados (Data Quality Check).
    Se encontrar anomalias críticas, levanta uma exceção travando o pipeline.
    """
    logging.info(f"Iniciando barreira de validação para: {stage_name}")

    # Trava 1: Verificação de Colunas Ausentes (Estrutural)
    missing_columns = set(expected_columns) - set(df.columns)
    if missing_columns:
        error_msg = f"VALIDATION FAILURE: Colunas ausentes em {stage_name}: {missing_columns}"
        logging.error(error_msg)
        raise ValueError(error_msg)

    # Trava 2: Verificação de Registros Nulos (Nulls) em campos críticos
    null_counts = df.isnull().sum().sum()
    if null_counts > 0:
        logging.warning(f"VALIDATION WARNING: Detectados {null_counts} valores nulos em {stage_name}.")

    # Trava 3: Verificação de Duplicidade Absoluta
    duplicate_count = df.duplicated().sum()
    if duplicate_count > 0:
        logging.warning(f"VALIDATION WARNING: {duplicate_count} linhas duplicadas encontradas em {stage_name}.")

    logging.info(f"VALIDATION SUCCESS: {stage_name} aprovado nos testes de qualidade.")
    return True
