-- =========================================================================
-- 1. DATA DEFINITION LANGUAGE (DDL) - SCHEMA CREATION
-- =========================================================================

CREATE TABLE dim_clientes (
    id_cliente SERIAL PRIMARY KEY,
    nome_cliente VARCHAR(255) NOT NULL,
    pais_cliente VARCHAR(100) NOT NULL
);

CREATE TABLE dim_produtos (
    id_produto SERIAL PRIMARY KEY,
    nome_produto VARCHAR(255) NOT NULL,
    categoria_produto VARCHAR(100) NOT NULL
);

CREATE TABLE dim_tempo (
    id_tempo DATE PRIMARY KEY,
    ano INT NOT NULL,
    mes INT NOT NULL,
    dia INT NOT NULL,
    dia_da_semana VARCHAR(50) NOT NULL
);

CREATE TABLE fato_vendas (
    id_venda SERIAL PRIMARY KEY,
    data_venda DATE NOT NULL,
    id_cliente INT NOT NULL,
    id_produto INT NOT NULL,
    quantidade INT NOT NULL,
    valor_total NUMERIC(12,2) NOT NULL,
    CONSTRAINT fk_vendas_tempo FOREIGN KEY (data_venda) REFERENCES dim_tempo(id_tempo) ON DELETE CASCADE,
    CONSTRAINT fk_vendas_cliente FOREIGN KEY (id_cliente) REFERENCES dim_clientes(id_cliente) ON DELETE CASCADE,
    CONSTRAINT fk_vendas_produto FOREIGN KEY (id_produto) REFERENCES dim_produtos(id_produto) ON DELETE CASCADE,
    CONSTRAINT chk_quantidade_positiva CHECK (quantidade > 0),
    CONSTRAINT chk_valor_positivo CHECK (valor_total >= 0)
);

-- PERFORMANCE TUNING: B-TREE INDEXES
CREATE INDEX idx_fato_data ON fato_vendas(data_venda);
CREATE INDEX idx_fato_cliente ON fato_vendas(id_cliente);
CREATE INDEX idx_fato_produto ON fato_vendas(id_produto);
CREATE INDEX idx_clientes_pais ON dim_clientes(pais_cliente);

-- =========================================================================
-- 2. SEMANTIC LAYER - ANALYTICAL VIEWS
-- =========================================================================

-- VIEW 01: HISTORICAL MONTHLY REVENUE (v_monthly_revenue)
CREATE OR REPLACE VIEW v_monthly_revenue AS
SELECT 
    t.ano AS sales_year,
    t.mes AS sales_month,
    SUM(f.valor_total) AS gross_revenue,
    COUNT(f.id_venda) AS transaction_count
FROM fato_vendas f
JOIN dim_tempo t ON f.data_venda = t.id_tempo
GROUP BY t.ano, t.mes;

-- VIEW 02: CUSTOMER PERFORMANCE & MONETARY SCALE (v_customer_performance)
CREATE OR REPLACE VIEW v_customer_performance AS
SELECT 
    c.id_cliente,
    c.nome_cliente,
    c.pais_cliente,
    SUM(f.valor_total) AS total_spent,
    AVG(f.valor_total) AS average_ticket,
    COUNT(f.id_venda) AS total_contracts,
    CASE 
        WHEN SUM(f.valor_total) >= 70000 THEN 'VIP Account'
        WHEN SUM(f.valor_total) BETWEEN 40000 AND 69999 THEN 'Regular Account'
        ELSE 'Iniciant Account'
    END AS customer_segment
FROM fato_vendas f
JOIN dim_clientes c ON f.id_cliente = c.id_cliente
GROUP BY c.id_cliente, c.nome_cliente, c.pais_cliente;

-- VIEW 03: PRODUCT RANKING BY MARKET SHARE (v_product_ranking)
CREATE OR REPLACE VIEW v_product_ranking AS
SELECT 
    p.id_produto,
    p.nome_produto,
    p.categoria_produto,
    SUM(f.quantidade) AS total_units_sold,
    SUM(f.valor_total) AS total_revenue_generated,
    RANK() OVER (ORDER BY SUM(f.valor_total) DESC) AS market_position
FROM fato_vendas f
JOIN dim_produtos p ON f.id_produto = p.id_produto
GROUP BY p.id_produto, p.nome_produto, p.categoria_produto;