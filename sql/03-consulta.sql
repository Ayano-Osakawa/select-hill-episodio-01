-- A mesma consulta executada no episódio.
SELECT id, nome
FROM locais
WHERE ordem <= 2
ORDER BY ordem;
