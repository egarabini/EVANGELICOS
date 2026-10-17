"""EVAL — F-03 / F-04 / F-07 / F-10 no mapa de origem, lendo a TELA de verdade.

Uso: python _eval_nn.py <dbpath>
Antes de rodar: a carga ja foi executada sobre esse banco.
"""
import sys
from pathlib import Path

_raiz = Path(__file__).resolve().parents[4]
sys.path.insert(0, str(_raiz / "ESTUDOS_BIBLICOS" / "GSI_EBD"))

from sqlalchemy import func  # noqa: E402
from sqlmodel import Session, create_engine, select  # noqa: E402
import rxconfig  # noqa: E402

dbpath = Path(sys.argv[1]).resolve()
rxconfig.config.db_url = f"sqlite:///{dbpath.as_posix()}"
# o engine do rx e cacheado por url: fixar antes de qualquer rx.session()

from gsi_ebd.models import (  # noqa: E402
    Adendo, Estudo, EstudoCapitulo, EstudoCapituloOrigem, ObraCapitulo,
)

engine = create_engine(f"sqlite:///{dbpath.as_posix()}")
with Session(engine) as s:
    estudo = s.exec(select(Estudo)).first()
    cap3 = s.exec(select(ObraCapitulo).where(ObraCapitulo.ordem == 3)).first()
    cap4 = s.exec(select(ObraCapitulo).where(ObraCapitulo.ordem == 4)).first()
    adendo = s.exec(select(Adendo).where(Adendo.codigo == "ADO-01.03")).first()

    # F-04: um SEGUNDO capitulo do estudo bebendo do MESMO capitulo da obra (cap 3),
    # com adendo declarado; e uma segunda origem (cap 4) no MESMO capitulo do estudo.
    cap_a = EstudoCapitulo(estudo_id=estudo.id, ordem=35,
                           titulo="Cap. 35 — Capitulo sintetico do EVAL",
                           conteudo_md="conteudo sintetico", questions_json="[]",
                           status="rascunho")
    s.add(cap_a)
    s.flush()
    s.add(EstudoCapituloOrigem(estudo_capitulo_id=cap_a.id, obra_capitulo_id=cap3.id,
                               adendo_id=adendo.id if adendo else None))
    s.add(EstudoCapituloOrigem(estudo_capitulo_id=cap_a.id, obra_capitulo_id=cap4.id))

    # F-10 / RF10: capitulo SEM origem declarada tem de ser valido
    cap_b = EstudoCapitulo(estudo_id=estudo.id, ordem=36,
                           titulo="Cap. 36 — Sem origem declarada",
                           conteudo_md="material original", questions_json="[]",
                           status="rascunho")
    s.add(cap_b)
    s.commit()

    print("-- F-04: quantas origens apontam para cada capitulo da obra (N:N) --")
    linhas = s.execute(
        select(EstudoCapituloOrigem.obra_capitulo_id,
               func.count(EstudoCapituloOrigem.id))
        .group_by(EstudoCapituloOrigem.obra_capitulo_id)
        .order_by(EstudoCapituloOrigem.obra_capitulo_id)).all()
    for obra_cap_id, n in linhas:
        cap = s.get(ObraCapitulo, obra_cap_id)
        marca = "  <== 2 capitulos do estudo" if n >= 2 else ""
        print(f"  obra cap {cap.ordem:02d}: {n} origem(ns){marca}")

    print("\n-- F-03: origens do capitulo 35 do estudo (obra + adendo opcional) --")
    for o in s.exec(select(EstudoCapituloOrigem)
                    .where(EstudoCapituloOrigem.estudo_capitulo_id == cap_a.id)).all():
        cap = s.get(ObraCapitulo, o.obra_capitulo_id)
        ado = s.get(Adendo, o.adendo_id) if o.adendo_id else None
        print(f"  obra_cap={cap.ordem:02d} adendo={ado.codigo if ado else None}")
    print(f"  origens do capitulo 36 (sem origem) = "
          f"{len(s.exec(select(EstudoCapituloOrigem).where(EstudoCapituloOrigem.estudo_capitulo_id == cap_b.id)).all())}")

    n_caps_antes = s.execute(select(func.count()).select_from(EstudoCapitulo)).scalar_one()
    n_orig_antes = s.execute(select(func.count()).select_from(EstudoCapituloOrigem)).scalar_one()

# ── F-07 / F-10: a TELA (AdminState.load_estudos_aplicados), nao a query ──
from gsi_ebd.states.admin import AdminState  # noqa: E402

st = AdminState(_reflex_internal_init=True)
st.load_estudos_aplicados()

print("\n-- F-07: o que a tela mostra --")
print(f"  estudos_aplicados = {st.estudos_aplicados}")
print(f"  capitulos listados = {len(st.capitulos_estudo)}")
alvo = ("03", "04", "35", "36")
for c in st.capitulos_estudo:
    if c["ordem"] in alvo:
        print(f"  ordem {c['ordem']}: titulo={c['titulo']!r}")
        print(f"            origem_label={c['origem_label']!r}")
        print(f"            conteudo_label={c['conteudo_label']!r} status={c['status']!r}")

cap36 = [c for c in st.capitulos_estudo if c["ordem"] == "36"]
print(f"\n-- F-10: 'sem origem declarada' presente no capitulo 36 -> "
      f"{bool(cap36) and cap36[0]['origem_label'] == 'sem origem declarada'}")
cap35 = [c for c in st.capitulos_estudo if c["ordem"] == "35"]
print(f"-- F-03: adendo exibido na origem do capitulo 35 -> "
      f"{bool(cap35) and str(cap35[0]['origem_label'])}")

with Session(engine) as s:
    n_caps_depois = s.execute(select(func.count()).select_from(EstudoCapitulo)).scalar_one()
    n_orig_depois = s.execute(select(func.count()).select_from(EstudoCapituloOrigem)).scalar_one()
print(f"\n-- F-07 somente leitura: carregar a tela nao gravou nada "
      f"(capitulos {n_caps_antes}->{n_caps_depois}, origens {n_orig_antes}->{n_orig_depois})")
engine.dispose()
