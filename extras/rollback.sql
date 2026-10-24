-- Demonstração isolada da manutenção mencionada na abertura.
-- TEMP mantém este exemplo separado do cadastro principal.
CREATE TEMP TABLE rotina_backup (
    id INTEGER PRIMARY KEY,
    situacao TEXT NOT NULL
);
INSERT INTO rotina_backup VALUES (1, 'pendente');

SELECT 'antes' AS etapa, situacao FROM rotina_backup;

BEGIN;
UPDATE rotina_backup SET situacao = 'em teste' WHERE id = 1;
SELECT 'provisorio' AS etapa, situacao FROM rotina_backup;
ROLLBACK;

SELECT 'apos rollback' AS etapa, situacao FROM rotina_backup;
-- Resultado: pendente. ROLLBACK não desfaz ações físicas nem fecha portais.
DROP TABLE rotina_backup;
