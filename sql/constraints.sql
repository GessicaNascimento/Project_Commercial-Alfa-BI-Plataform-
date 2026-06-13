-- Aplicação de Restrições e Chaves Estrangeiras (Constraints)

-- 1. Vincula o id_cliente da Fato com a Dimensão Clientes
ALTER TABLE fato_vendas
ADD CONSTRAINT fk_vendas_clientes
FOREIGN KEY (id_cliente) REFERENCES dim_clientes(id_cliente);

-- 2. Vincula o id_produto da Fato com a Dimensão Produtos
ALTER TABLE fato_vendas
ADD CONSTRAINT fk_vendas_produtos
FOREIGN KEY (id_produto) REFERENCES dim_produtos(id_produto);