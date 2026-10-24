"""Laboratório local do episódio 1. Usa apenas a biblioteca padrão do Python."""
from __future__ import annotations

import argparse
from pathlib import Path
import sqlite3

ROOT = Path(__file__).resolve().parent
DEFAULT_DB = ROOT / "build" / "select-hill.sqlite3"


def sql_file(name: str) -> str:
    return (ROOT / "sql" / name).read_text(encoding="utf-8")


def iniciar(path: Path) -> bool:
    """Cria um banco novo; preserva qualquer arquivo que já exista."""
    path = path.resolve()
    path.parent.mkdir(parents=True, exist_ok=True)
    # Reserva o nome antes de conectar: nenhum banco existente é sobrescrito.
    try:
        path.touch(exist_ok=False)
    except FileExistsError:
        return False
    connection = None
    try:
        connection = sqlite3.connect(path)
        connection.executescript(
            "BEGIN;\n" + sql_file("01-esquema.sql") + sql_file("02-dados.sql") + "\nCOMMIT;"
        )
    except Exception:
        if connection is not None:
            connection.close()
        path.unlink(missing_ok=True)
        raise
    else:
        connection.close()
    return True


def consultar(path: Path) -> list[tuple[int, str]]:
    # URI local portátil; consultar não cria um arquivo vazio por engano.
    connection = sqlite3.connect(path.resolve().as_uri() + "?mode=ro", uri=True)
    try:
        return connection.execute(sql_file("03-consulta.sql")).fetchall()
    finally:
        connection.close()


def mostrar_rollback() -> list[tuple[str, str]]:
    connection = sqlite3.connect(":memory:", isolation_level=None)
    try:
        connection.execute("CREATE TABLE rotina (situacao TEXT NOT NULL)")
        connection.execute("INSERT INTO rotina VALUES ('pendente')")
        result = [("antes", connection.execute("SELECT situacao FROM rotina").fetchone()[0])]
        connection.execute("BEGIN")
        connection.execute("UPDATE rotina SET situacao = 'em teste'")
        result.append(("provisorio", connection.execute("SELECT situacao FROM rotina").fetchone()[0]))
        connection.execute("ROLLBACK")
        result.append(("apos rollback", connection.execute("SELECT situacao FROM rotina").fetchone()[0]))
        return result
    finally:
        connection.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="SELECT HILL — episódio 1")
    parser.add_argument("acao", choices=["iniciar", "consultar", "rollback"])
    parser.add_argument("--banco", type=Path, default=DEFAULT_DB)
    args = parser.parse_args()
    try:
        if args.acao == "iniciar":
            created = iniciar(args.banco)
            print("Banco criado." if created else "O arquivo já existe e foi preservado.")
            print(args.banco.resolve())
        elif args.acao == "consultar":
            print("id | nome")
            print("---|-------------")
            for identifier, name in consultar(args.banco):
                print(f"{identifier}  | {name}")
        else:
            for etapa, situacao in mostrar_rollback():
                print(f"{etapa}: {situacao}")
    except (sqlite3.Error, OSError) as exc:
        parser.exit(1, f"Não foi possível executar: {exc}\n")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
