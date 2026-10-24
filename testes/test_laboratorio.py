from pathlib import Path
import sqlite3
import subprocess
import sys
import tempfile
import unittest

from backup import criar_backup
from laboratorio import ROOT, consultar, iniciar, mostrar_rollback


class LaboratorioTest(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory()
        self.addCleanup(self.temp.cleanup)
        self.db = Path(self.temp.name) / "episodio.sqlite3"
        iniciar(self.db)

    def test_consulta_do_video_e_campos_do_cadastro(self):
        self.assertEqual(consultar(self.db), [(1, "Café 5to2"), (2, "Beco inicial")])
        with sqlite3.connect(self.db) as con:
            self.assertEqual([c[1] for c in con.execute("PRAGMA table_info(locais)")],
                             ["id", "nome", "regiao", "ordem"])
            self.assertEqual(con.execute("SELECT COUNT(*) FROM pessoas").fetchone()[0], 3)

    def test_persistencia_em_outro_processo(self):
        completed = subprocess.run(
            [sys.executable, str(ROOT / "laboratorio.py"), "consultar", "--banco", str(self.db)],
            check=True, capture_output=True, text=True, encoding="utf-8")
        self.assertIn("1  | Café 5to2", completed.stdout)
        self.assertIn("2  | Beco inicial", completed.stdout)

    def test_iniciar_novamente_preserva_edicoes(self):
        with sqlite3.connect(self.db) as con:
            con.execute("UPDATE locais SET nome = 'Nome do exercício' WHERE id = 1")
        self.assertFalse(iniciar(self.db))
        self.assertEqual(consultar(self.db)[0][1], "Nome do exercício")

    def test_rollback_real_e_exemplo_sql(self):
        self.assertEqual(mostrar_rollback(), [("antes", "pendente"),
                         ("provisorio", "em teste"), ("apos rollback", "pendente")])
        with sqlite3.connect(self.db) as con:
            con.executescript((ROOT / "extras/rollback.sql").read_text(encoding="utf-8"))
            self.assertEqual(con.execute("SELECT COUNT(*) FROM locais").fetchone()[0], 2)

    def test_backup_pode_ser_consultado_sem_alterar_origem(self):
        before = self.db.read_bytes()
        target = Path(self.temp.name) / "backup.sqlite3"
        criar_backup(self.db, target)
        self.assertEqual(consultar(target), consultar(self.db))
        self.assertEqual(self.db.read_bytes(), before)
        with sqlite3.connect(self.db) as a, sqlite3.connect(target) as b:
            self.assertEqual(a.execute("SELECT * FROM pessoas ORDER BY id").fetchall(),
                             b.execute("SELECT * FROM pessoas ORDER BY id").fetchall())
        backup_before = target.read_bytes()
        with self.assertRaises(FileExistsError):
            criar_backup(self.db, target)
        self.assertEqual(target.read_bytes(), backup_before)

    def test_consulta_nao_cria_banco_ausente(self):
        missing = Path(self.temp.name) / "ausente.sqlite3"
        with self.assertRaises(sqlite3.OperationalError):
            consultar(missing)
        self.assertFalse(missing.exists())


if __name__ == "__main__":
    unittest.main()
