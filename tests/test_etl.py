import os
import pandas as pd

def test_raw_data_integrity():
    """Valida se o arquivo original de cosméticos contém a volumetria correta."""
    caminho = "data/raw/cosmetics_sales_data.csv"
    if not os.path.exists(caminho):
        caminho = os.path.join("..", caminho)
        
    df = pd.read_csv(caminho)
    assert len(df) == 374, "A volumetria do arquivo bruto mudou!"
    assert 'Sales Person' in df.columns, "A coluna Sales Person sumiu!"
