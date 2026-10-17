"""EVAL — leitura pos-carga (F-01, F-02, F-05, F-06, F-09, N-06, C-02).

Uso: python _eval_after.py <dbpath>
"""
import sys
from pathlib import Path

_raiz = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_raiz / "ESTUDOS_BIBLICOS" / "GSI_EBD"))

from sqlalchemy import func, text  # noqa: E402
from sqlmodel import Session, create_engine, select  # noqa: E402

from gsi_ebd.models import (  # noqa: E402
    Estudo, EstudoCapitulo, EstudoCapituloOrigem, Obra, ObraCapitulo,
    Progress, Study, StudyAssignment, StudyVersion, UserResponse,
)

dbpath = Path(sys.argv[1]).resolve()
engine = create_engine(f"sqlite:///{dbpath.as_posix()}")

TABELAS = [
    ("study", Study), ("studyversion", StudyVersion), ("studyassignment", StudyAssignment),
    ("progress", Progress), ("userresponse", UserResponse), ("obra", Obra),
    ("obracapitulo", ObraCapitulo), ("estudo", Estudo),
    ("estudocapitulo", EstudoCapitulo), ("estudocapituloorigem", EstudoCapituloOrigem),
]

with Session(engine) as s:
    print("TABELA                  CONTAGEM")
    for nome, modelo in TABELAS:
        n = s.execute(select(func.count()).select_from(modelo)).scalar_one()
        print(f"  {nome:<22} {n}")

    print("\n-- F-01: o Estudo --")
    for e in s.exec(select(Estudo)).all():
        obra = s.get(Obra, e.obra_id)
        print(f"  id={e.id} obra_id={e.obra_id} obra={obra.titulo!r} titulo={e.titulo!r}")
        print(f"  descricao={e.descricao!r} doutrina_id={e.doutrina_id} status={e.status!r}"
              f" is_active={e.is_active} created_at={e.created_at}")

    print("\n-- F-02: ordem dos capitulos --")
    caps = s.exec(select(EstudoCapitulo).order_by(EstudoCapitulo.ordem)).all()
    ordens = [c.ordem for c in caps]
    print(f"  capitulos={len(caps)} ordens_min={min(ordens)} ordens_max={max(ordens)}")
    print(f"  distintas={len(set(ordens))} continua_1_a_34={ordens == list(range(1, 35))}")
    print(f"  estudo_ids={sorted({c.estudo_id for c in caps})}")

    print("\n-- F-05: estudo/capitulos/origens --")
    print(f"  estudos={s.execute(select(func.count()).select_from(Estudo)).scalar_one()}"
          f" capitulos={s.execute(select(func.count()).select_from(EstudoCapitulo)).scalar_one()}"
          f" origens={s.execute(select(func.count()).select_from(EstudoCapituloOrigem)).scalar_one()}")

    print("\n-- F-06 / C-02: status dos capitulos criados --")
    dist = s.execute(
        text("select status, count(*) from estudocapitulo group by status")).all()
    print(f"  por_status={[(r[0], r[1]) for r in dist]}")
    fora = s.exec(select(EstudoCapitulo).where(
        EstudoCapitulo.status != "rascunho")).all()
    print(f"  fora_de_rascunho={len(fora)}")

    print("\n-- conteudo propagado da origem real (StudyVersion) --")
    estudo = s.exec(select(Study).where(Study.title.like("Cap. 01%"))).first()
    versao = s.exec(select(StudyVersion).where(StudyVersion.study_id == estudo.id)).first()
    cap1 = s.exec(select(EstudoCapitulo).where(EstudoCapitulo.ordem == 1)).first()
    print(f"  cap1.titulo={cap1.titulo!r} == study.title={estudo.title!r} -> {cap1.titulo == estudo.title}")
    print(f"  cap1.conteudo_md == studyversion.content_md -> {cap1.conteudo_md == versao.content_md}"
          f" (len={len(cap1.conteudo_md)})")
    print(f"  cap1.questions_json == studyversion.questions_json -> "
          f"{cap1.questions_json == versao.questions_json} ({cap1.questions_json})")

    print("\n-- N-06: os 5 exemplos nao viraram estudo --")
    titulos = [c.titulo for c in caps]
    print(f"  algum titulo 'Exemplo' entre os capitulos do estudo: "
          f"{[t for t in titulos if t.lower().startswith('exemplo')]}")
    print(f"  estudos no banco (deve ser 1) = "
          f"{s.execute(select(func.count()).select_from(Estudo)).scalar_one()}")
    print(f"  capitulos do estudo que nao sao 'Cap. NN' = "
          f"{[t for t in titulos if not t.startswith('Cap. ')]}")

engine.dispose()
