-- View: Performance Comercial por País de Destino
CREATE OR REPLACE VIEW v_kpi_performance_pais AS
SELECT 
    c.pais_cliente AS pais,
    COUNT(f.id_venda) AS total_transacoes,
    SUM(f.quantidade) AS total_caixas_despachadas,
    SUM(f.valor_total) AS receita_total_acumulada,
    ROUND(AVG(f.preco_unitario), 2) AS preco_medio_lote
FROM fato_vendas f
JOIN dim_clientes c ON f.id_cliente = c.id_cliente
GROUP BY c.pais_cliente;