import pandas as pd

def transform_data(df_raw):
    """
    Normaliza as colunas reais de cosméticos, gera IDs estruturais
    e divide os dados no modelo Star Schema.
    """
    print("[TRANSFORMAÇÃO] Iniciando tratamento dos dados brutos...")
    
    # 1. Limpeza inicial de registros nulos nas colunas essenciais
    df_clean = df_raw.dropna(subset=['Sales Person', 'Product']).drop_duplicates().copy()
    
    # 2. Padronização e criação dos IDs por mapeamento categórico
    # Criamos IDs numéricos baseados nos nomes únicos de Clientes (Sales Person) e Produtos
    df_clean['id_cliente'] = df_clean['Sales Person'].astype('category').cat.codes + 1
    df_clean['id_produto'] = df_clean['Product'].astype('category').cat.codes + 1
    df_clean['id_venda'] = range(1, len(df_clean) + 1) # Cria uma chave sequencial para cada venda
    
    # 3. Engenharia de Atributos (Cálculos Matemáticos)
    # Convertemos a data para o formato padrão ISO (AAAA-MM-DD)
    df_clean['data_venda'] = pd.to_datetime(df_clean['Date']).dt.strftime('%Y-%m-%d')
    
    # Renomeamos e isolamos as métricas de negócio
    df_clean['quantidade'] = df_clean['Boxes Shipped'].astype(int)
    
    # Como o arquivo bruto já traz o valor total da transação em 'Amount ($)', 
    # calculamos o preço unitário aproximado para manter a granularidade do modelo
    df_clean['valor_total'] = df_clean['Amount ($)'].astype(float)
    df_clean['preco_unitario'] = (df_clean['valor_total'] / df_clean['quantidade']).round(2)
    
    # 4. Modelagem: Estruturação da Dimensão Clientes
    dim_clientes = df_clean[['id_cliente', 'Sales Person', 'Country']].copy()
    dim_clientes.columns = ['id_cliente', 'nome_cliente', 'pais_cliente']
    dim_clientes = dim_clientes.drop_duplicates(subset=['id_cliente'])
    
    # 5. Modelagem: Estruturação da Dimensão Produtos
    # Como não há categoria no bruto, mapeamos temporariamente como 'Cosmetics'
    dim_produtos = df_clean[['id_produto', 'Product']].copy()
    dim_produtos.columns = ['id_produto', 'nome_produto']
    dim_produtos['categoria_produto'] = 'Cosmetics'
    dim_produtos = dim_produtos.drop_duplicates(subset=['id_produto'])
    
    # 6. Modelagem: Estruturação da Tabela Fato Vendas
    fato_vendas = df_clean[['id_venda', 'id_cliente', 'id_produto', 'data_venda', 'quantidade', 'preco_unitario', 'valor_total']]
    
    print(f"[TRANSFORMAÇÃO] Transformação concluída com sucesso.")
    print(f" -> Clientes mapeados (Vendedores): {len(dim_clientes)}")
    print(f" -> Produtos mapeados: {len(dim_produtos)}")
    print(f" -> Registros de Fato estruturados: {len(fato_vendas)}")
    
    return dim_clientes, dim_produtos, fato_vendas

if __name__ == "__main__":
    print("[TESTE] Componente de transformação pronto para ser orquestrado.")
