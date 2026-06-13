-- View: Evolução da Receita e Volume de Vendas Mensal
CREATE OR REPLACE VIEW v_kpi_receita_mensal AS
SELECT 
    TO_CHAR(f.data_venda, 'YYYY-MM') AS ano_mes,
    COUNT(f.id_venda) AS volume_vendas,
    SUM(f.quantidade) AS caixas_vendidas,
    SUM(f.valor_total) AS faturamento_mensal
FROM fato_vendas f
GROUP BY TO_CHAR(f.data_venda, 'YYYY-MM')
ORDER BY ano_mes;