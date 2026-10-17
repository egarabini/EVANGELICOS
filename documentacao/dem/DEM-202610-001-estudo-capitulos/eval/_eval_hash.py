"""EVAL — impressao digital das tabelas que nao podem mudar (F-09 / H-04, parte local).

Uso: python _eval_hash.py <dbpath>
"""
import hashlib
import sys
from pathlib import Path

_raiz = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_raiz / "ESTUDOS_BIBLICOS" / "GSI_EBD"))

from sqlalchemy import text  # noqa: E402
from sqlmodel import Session, create_engine  # noqa: E402

TABELAS = ["study", "studyversion", "studyassignment", "progress", "userresponse",
           "obra", "obracapitulo", "referenciacruzada"]

dbpath = Path(sys.argv[1]).resolve()
engine = create_engine(f"sqlite:///{dbpath.as_posix()}")
with Session(engine) as s:
    for tabela in TABELAS:
        linhas = s.execute(text(f"select * from {tabela}")).all()
        blob = repr([tuple(r) for r in linhas]).encode()
        print(f"  {tabela:<18} linhas={len(linhas):<4} sha256={hashlib.sha256(blob).hexdigest()[:32]}")
engine.dispose()
