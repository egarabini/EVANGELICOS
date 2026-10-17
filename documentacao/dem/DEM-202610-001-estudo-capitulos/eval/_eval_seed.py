"""EVAL — fixture descartavel para executar a carga fora de producao.

Uso:
    python _eval_seed.py <dbpath>          # obra + 34 estudos "Cap. NN" + 5 exemplos
    python _eval_seed.py <dbpath> --no-obra  # so os estudos (para F-11)

Nada aqui e do autor: e fixture do EVAL, montada a partir do que o plano descreve
(34 capitulos do livro + 5 exemplos de §8.2 e a obra da Fase 1).
"""
import sys
from datetime import datetime
from pathlib import Path

_raiz = Path(__file__).resolve().parents[4]  # ...\EVANGELICOS
sys.path.insert(0, str(_raiz / "ESTUDOS_BIBLICOS" / "GSI_EBD"))

from sqlmodel import Session, SQLModel, create_engine, select  # noqa: E402

from gsi_ebd.models import (  # noqa: E402
    Adendo, Obra, ObraCapitulo, Progress, Study, StudyAssignment,
    StudyVersion, User, UserResponse,
)


def main() -> int:
    dbpath = Path(sys.argv[1]).resolve()
    if dbpath.exists():
        dbpath.unlink()
    com_obra = "--no-obra" not in sys.argv
    engine = create_engine(f"sqlite:///{dbpath.as_posix()}")
    SQLModel.metadata.create_all(engine)

    with Session(engine) as s:
        u = User(nome_completo="Aluno EVAL", nome_base="Aluno", email="eval@teste.invalid",
                 role=4, status="ativo", created_at=datetime.utcnow())
        s.add(u)
        s.flush()

        for ordem in range(1, 35):
            st = Study(title=f"Cap. {ordem:02d} — Estudo {ordem}", category="doutrina",
                       status="aprovado", created_at=datetime.utcnow())
            s.add(st)
            s.flush()
            sv = StudyVersion(study_id=st.id, version=1,
                              content_md=f"# Conteudo do capitulo {ordem}\n\n"
                                         + ("paragrafo de estudo " * (ordem * 10)),
                              questions_json=f'[{{"q": "pergunta {ordem}"}}]',
                              created_at=datetime.utcnow())
            s.add(sv)
            s.flush()
            s.add(StudyAssignment(user_id=u.id, study_id=st.id, study_version_id=sv.id,
                                  created_at=datetime.utcnow()))
            s.add(Progress(user_id=u.id, study_id=st.id, score=float(ordem)))
            s.add(UserResponse(user_id=u.id, study_version_id=sv.id,
                               question_key=f"q{ordem}", question_type=3,
                               answer="resposta", created_at=datetime.utcnow()))

        for i in range(1, 6):
            st = Study(title=f"Exemplo {i}", category="exemplo", status="aprovado",
                       created_at=datetime.utcnow())
            s.add(st)
            s.flush()
            sv = StudyVersion(study_id=st.id, version=1, content_md=f"exemplo {i}",
                              created_at=datetime.utcnow())
            s.add(sv)
            s.flush()
            s.add(StudyAssignment(user_id=u.id, study_id=st.id, study_version_id=sv.id,
                                  created_at=datetime.utcnow()))
            s.add(Progress(user_id=u.id, study_id=st.id))
            s.add(UserResponse(user_id=u.id, study_version_id=sv.id,
                               question_key="qe", question_type=3, answer="x",
                               created_at=datetime.utcnow()))

        if com_obra:
            obra = Obra(titulo="Doutrinas Cristãs", tipo="livro",
                        descricao="fixture EVAL", origem="fixture",
                        created_at=datetime.utcnow())
            s.add(obra)
            s.flush()
            for ordem in range(1, 35):
                s.add(ObraCapitulo(obra_id=obra.id, ordem=ordem,
                                   titulo=f"Cap. {ordem:02d} — Obra {ordem}",
                                   conteudo_md=f"texto da obra {ordem}"))
            s.flush()
            cap3 = s.exec(select(ObraCapitulo).where(ObraCapitulo.ordem == 3)).first()
            s.add(Adendo(obra_id=obra.id, obra_capitulo_id=cap3.id, codigo="ADO-01.03",
                         titulo="Nota do revisor", texto="ressalva",
                         created_at=datetime.utcnow()))
        s.commit()

        print(f"SEED OK db={dbpath} com_obra={com_obra}")
        print(f"  study={len(s.exec(select(Study)).all())}"
              f" studyversion={len(s.exec(select(StudyVersion)).all())}"
              f" studyassignment={len(s.exec(select(StudyAssignment)).all())}"
              f" progress={len(s.exec(select(Progress)).all())}"
              f" userresponse={len(s.exec(select(UserResponse)).all())}"
              f" obra={len(s.exec(select(Obra)).all())}"
              f" obracapitulo={len(s.exec(select(ObraCapitulo)).all())}")
    engine.dispose()
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
