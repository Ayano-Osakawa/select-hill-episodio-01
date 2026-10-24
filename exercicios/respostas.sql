-- 1. Somente os nomes, respeitando a ordem do cadastro.
SELECT nome FROM locais ORDER BY ordem;

-- 2. Um lugar específico.
SELECT id, nome FROM locais WHERE id = 2;

-- 3. Outra apresentação dos mesmos registros.
SELECT id, nome, regiao, ordem FROM locais ORDER BY nome;
-- Não: Café 5to2 continua com id 1; Beco inicial continua com id 2.
-- ORDER BY altera a apresentação, não o identificador armazenado.

-- 4. Pessoas em ordem alfabética.
SELECT nome FROM pessoas ORDER BY nome;

-- 5. Não. Locais guarda id, nome, regiao e ordem.
-- Pessoas guarda id e nome. Nenhuma dessas tabelas registra encontros.
-- Não podemos inventar uma presença a partir desses cadastros.
