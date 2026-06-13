-- Criação do Schema Dimensional para o projeto Commercial-Alfa

-- 1. Dimensão Clientes
CREATE TABLE IF NOT EXISTS dim_clientes (
    id_cliente INT PRIMARY KEY,
    nome_cliente VARCHAR(255) NOT NULL,
    pais_cliente VARCHAR(100) NOT NULL
);

-- 2. Dimensão Produtos
CREATE TABLE IF NOT EXISTS dim_produtos (
    id_produto INT PRIMARY KEY,
    nome_produto VARCHAR(255) NOT NULL,
    categoria_produto VARCHAR(100) NOT NULL
);

-- 3. Tabela Fato Vendas (Estrutura Base)
CREATE TABLE IF NOT EXISTS fato_vendas (
    id_venda INT PRIMARY KEY,
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    data_venda DATE NOT NULL,
    quantidade INT NOT NULL,
    preco_unitario NUMERIC(10, 2) NOT NULL,
    valor_total NUMERIC(10, 2) NOT NULL
);