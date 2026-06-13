-- View: Ranking de Produtos por Faturamento Absoluto
CREATE OR REPLACE VIEW v_kpi_ranking_produtos AS
SELECT 
    p.nome_produto,
    p.categoria_produto,
    SUM(f.quantidade) AS unidades_caixas_voldidas,
    SUM(f.valor_total) AS receita_gerada,
    DENSE_RANK() OVER (ORDER BY SUM(f.valor_total) DESC) AS posicao_ranking
FROM fato_vendas f
JOIN dim_produtos p ON f.id_produto = p.id_produto
GROUP BY p.nome_produto, p.categoria_produto;