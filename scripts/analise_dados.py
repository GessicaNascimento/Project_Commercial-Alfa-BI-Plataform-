import os
import pandas as pd
import psycopg2
import matplotlib.pyplot as plt
import seaborn as sns
from carga_dados import load_db_config

# Configuração estética dos plots (Estilo Dark/Clean Acadêmico)
sns.set_theme(style="whitegrid")
plt.rcParams.update({'font.size': 10, 'axes.labelsize': 12, 'axes.titlesize': 14})

def gerar_dashboards_macos():
    print("=== INICIANDO RENDERIZAÇÃO DOS DASHBOARDS HISTOGRAMA/BARRA (macOS) ===")
    
    params = load_db_config()
    conn = psycopg2.connect(**params)
    
    # Definição das pastas de destino oficiais da sua árvore
    script_dir = os.path.dirname(os.path.abspath(__file__))
    raiz_projeto = os.path.abspath(os.path.join(script_dir, ".."))
    pasta_screenshots_dash = os.path.join(raiz_projeto, "dashboards", "screenshots")
    pasta_screenshots_docs = os.path.join(raiz_projeto, "docs", "screenshots")
    
    os.makedirs(pasta_screenshots_dash, exist_ok=True)
    os.makedirs(pasta_screenshots_docs, exist_ok=True)
    
    try:
        # ----------------------------------------------------
        # GRÁFICO 1: TOP 5 PRODUTOS (Operational View)
        # ----------------------------------------------------
        df_prod = pd.read_sql_query("SELECT * FROM v_kpi_ranking_produtos LIMIT 5;", conn)
        
        plt.figure(figsize=(10, 5))
        ax1 = sns.barplot(x="receita_generated", y="nome_produto", data=df_prod.rename(columns={"receita_gerada": "receita_generated"}), palette="Blues_r")
        plt.title("Executive View: Top 5 Produtos por Faturamento Acumulado")
        plt.xlabel("Receita em Dólar ($)")
        plt.ylabel("Produto")
        plt.tight_layout()
        
        # Salva o print nas duas pastas requisitadas na sua árvore
        path_prod_dash = os.path.join(pasta_screenshots_dash, "operational_dashboard.png")
        plt.savefig(path_prod_dash, dpi=300)
        plt.savefig(os.path.join(pasta_screenshots_docs, "operational_dashboard.png"), dpi=300)
        plt.close()
        print(f"[PLOT] Operational Dashboard gerado em: {path_prod_dash}")
        
        # ----------------------------------------------------
        # GRÁFICO 2: PERFORMANCE POR PAÍS (Executive View)
        # ----------------------------------------------------
        df_pais = pd.read_sql_query("SELECT * FROM v_kpi_performance_pais;", conn)
        
        plt.figure(figsize=(10, 5))
        ax2 = sns.barplot(x="pais", y="receita_total_acumulada", data=df_pais, palette="viridis")
        plt.title("Strategic View: Performance de Faturamento por País")
        plt.xlabel("País de Destino")
        plt.ylabel("Receita Acumulada ($)")
        plt.tight_layout()
        
        path_pais_dash = os.path.join(pasta_screenshots_dash, "executive_dashboard.png")
        plt.savefig(path_pais_dash, dpi=300)
        plt.savefig(os.path.join(pasta_screenshots_docs, "executive_dashboard.png"), dpi=300)
        plt.close()
        print(f"[PLOT] Executive Dashboard gerado em: {path_pais_dash}")
        
        print("\n=== PIPELINE VISUAL FINALIZADO COM SUCESSO ABSOLUTO! ===")
        print("Os prints dos dashboards estão salvos e prontos para o README.md.")
        
    except Exception as e:
        print(f"Erro na geração dos gráficos: {e}")
    finally:
        conn.close()

if __name__ == "__main__":
    gerar_dashboards_macos()
