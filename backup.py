"""Cópia consistente de um arquivo SQLite, usando a API de backup do SQLite."""
from __future__ import annotations

import argparse
from pathlib import Path
import sqlite3


def criar_backup(origem: Path, destino: Path) -> None:
    origem, destino = origem.resolve(), destino.resolve()
    if origem == destino:
        raise ValueError("Origem e destino precisam ser arquivos diferentes.")
    source = sqlite3.connect(origem.as_uri() + "?mode=ro", uri=True)
    reserved = False
    target = None
    try:
        destino.parent.mkdir(parents=True, exist_ok=True)
        destino.touch(exist_ok=False)
        reserved = True
        target = sqlite3.connect(destino)
        source.backup(target)
        if target.execute("PRAGMA integrity_check").fetchone()[0] != "ok":
            raise RuntimeError("A integridade da cópia não foi confirmada.")
    except Exception:
        if target is not None:
            target.close()
        if reserved:
            destino.unlink(missing_ok=True)
        raise
    else:
        target.close()
    finally:
        source.close()


def main() -> int:
    parser = argparse.ArgumentParser(description="Backup do arquivo didático de SELECT HILL")
    parser.add_argument("origem", type=Path)
    parser.add_argument("destino", type=Path)
    args = parser.parse_args()
    try:
        criar_backup(args.origem, args.destino)
    except (sqlite3.Error, OSError, ValueError, RuntimeError) as exc:
        parser.exit(1, f"Backup não concluído: {exc}\n")
    print("Cópia criada; integridade do arquivo conferida.")
    print("Confira também os dados usando a consulta do episódio.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
