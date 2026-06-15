import pandas as pd
import numpy as np
import logging

def generate_revenue_forecast(fato_vendas: pd.DataFrame):
    """
    Aplica conceitos analíticos de série temporal (Média Móvel e Tendência)
    sobre o DataFrame de Fato Vendas para fornecer projeções de receita.
    """
    logging.info("Iniciando processamento da camada de Forecasting Preditivo...")
    
    # Garante a tipagem correta de data e valores
    df = fato_vendas.copy()
    df['data_venda'] = pd.to_datetime(df['data_venda'])
    
    # 1. Agrupamento Temporal Discreto (Receita Mensal)
    df_mensal = df.groupby(df['data_venda'].dt.to_period('M'))['valor_total'].sum().reset_index()
    df_mensal['data_venda'] = df_mensal['data_venda'].dt.to_timestamp()
    
    # 2. Cálculo da Média Móvel de 3 Períodos (Suavização de ruído de mercado)
    df_mensal['media_movel_3m'] = df_mensal['valor_total'].rolling(window=3, min_periods=1).mean().round(2)
    
    # 3. Análise de Tendência (Taxa de Variação Percentual Média)
    taxa_crescimento = df_mensal['valor_total'].pct_change().mean()
    
    if np.isnan(taxa_crescimento) or np.isinf(taxa_crescimento):
        taxa_crescimento = 0.0
        
    # 4. Projeção Matemática para o Próximo Mês
    ultima_receita = df_mensal['valor_total'].iloc[-1]
    previsao_proximo_mes = round(ultima_receita * (1 + taxa_crescimento), 2)
    
    logging.info("Cálculos de Forecast concluídos.")
    logging.info(f" -> Taxa de Crescimento Mensal Média Estimada: {taxa_crescimento:.2%}")
    logging.info(f" -> Última Receita Histórica: $ {ultima_receita:,.2f}")
    logging.info(f" -> Receita Projetada para o Próximo Período: $ {previsao_proximo_mes:,.2f}")
    
    return df_mensal, previsao_proximo_mes