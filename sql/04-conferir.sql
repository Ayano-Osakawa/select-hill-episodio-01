-- Quais propriedades descrevem cada lugar?
PRAGMA table_info(locais);

-- Conferência do cadastro, incluindo os campos não pedidos na primeira consulta.
SELECT id, nome, regiao, ordem
FROM locais
ORDER BY ordem;

-- O cadastro de pessoas é separado do cadastro de lugares.
SELECT id, nome
FROM pessoas
ORDER BY id;
