"""Sonda dos HANDLERS reais (DEM-202610-002), sem tocar no banco.

Cria instancias de verdade dos estados (substates do AuthState), injeta o papel
no estado pai e chama cada evento publico dos 3 estados administrativos.

- `reflex.session` e substituido por uma sentinela que LEVANTA: se o corpo do
  handler comecar a consultar, a sonda registra "DELEGOU" sem abrir sessao.
- Para handlers que nao usam sessao, a sonda olha o efeito no estado.

Roda do diretorio do app. Nao escreve nada.
"""
import os
import sys

APP = r"C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD"
os.chdir(APP)
sys.path.insert(0, APP)

from unittest.mock import patch  # noqa: E402

import reflex  # noqa: E402

from gsi_ebd.models.user import Role  # noqa: E402
from gsi_ebd.states.admin import AdminState  # noqa: E402
from gsi_ebd.states.auth import AuthState  # noqa: E402
from gsi_ebd.states.coordenador import CoordenadorState  # noqa: E402
from gsi_ebd.states.revisao import RevisaoState  # noqa: E402
from gsi_ebd.utils import rbac  # noqa: E402


class Delegou(Exception):
    """O corpo do handler chegou a abrir sessao: o @exige liberou."""


def sessao_sentinela(*args, **kwargs):
    raise Delegou()


FALHAS = []


def instancia(estado_cls, papel):
    auth = AuthState(_reflex_internal_init=True)
    auth.is_authenticated = True
    auth.current_user_role = papel
    sub = auth.substates[estado_cls.get_name()]
    return sub


def snapshot(sub):
    """Todos os vars (frontend e backend) do estado, para detectar efeito."""
    return {nome: repr(getattr(sub, nome, None)) for nome in sub.vars}


def chama(sub, nome, args=()):
    """Chama o handler; devolve ('delegou'|'barrado'|'efeito'|'retorno', estado)."""
    handler = sub.event_handlers[nome]
    fn = handler.fn
    antes = snapshot(sub)
    try:
        with patch.object(reflex, "session", sessao_sentinela):
            retorno = fn(sub, *args)
    except Delegou:
        return "delegou", sub
    depois = snapshot(sub)
    if depois != antes:
        return "efeito", sub
    if retorno is None:
        return "barrado", sub
    return "retorno", sub


# (estado, handler, args, setup antes de chamar, acao esperada)
CASOS = [
    # ── AdminState ────────────────────────────────────────────────────────
    (AdminState, "load_coordenadores", (), {}, "banco"),
    (AdminState, "load_leads", (), {}, "banco"),
    (AdminState, "load_estudos_pendentes", (), {}, "banco"),
    (AdminState, "load_obras", (), {}, "banco"),
    (AdminState, "load_estudos_aplicados", (), {}, "banco"),
    (AdminState, "create_gestor", (), {}, "banco"),
    (AdminState, "activate_user", (1,), {}, "banco"),
    (AdminState, "suspend_user", (1,), {}, "banco"),
    (AdminState, "cancel_user", (1,), {}, "banco"),
    (AdminState, "update_lead_status", (1, "novo"), {}, "banco"),
    (AdminState, "aprovar_estudo", (1,), {}, "banco"),
    (AdminState, "aprovar_todos", (), {}, "banco"),
    (AdminState, "rejeitar_estudo", (1,), {"reject_motivo": "motivo"}, "banco"),
    # ── CoordenadorState ─────────────────────────────────────────────────
    (CoordenadorState, "load_all", (), {}, "banco"),
    (CoordenadorState, "load_alunos", (), {}, "banco"),
    (CoordenadorState, "load_estudos", (), {}, "banco"),
    (CoordenadorState, "load_turmas", (), {}, "banco"),
    (CoordenadorState, "toggle_aluno", ("7",), {"selected_aluno_ids": []}, "efeito"),
    (CoordenadorState, "select_all_alunos", (), {"alunos": [{"id": "7"}]}, "efeito"),
    (CoordenadorState, "clear_selection", (), {"selected_aluno_ids": [7], "message": "x"}, "efeito"),
    (CoordenadorState, "assign_study", (), {"selected_study_option": "1:x",
                                            "selected_aluno_ids": [1]}, "banco"),
    # ── RevisaoState ─────────────────────────────────────────────────────
    (RevisaoState, "load_fila", (), {}, "banco"),
    (RevisaoState, "abrir_resposta", ("9",), {"resposta_aberta_id": "1"}, "efeito"),
    (RevisaoState, "fechar_resposta", (), {"resposta_aberta_id": "9",
                                           "parecer_texto": "x"}, "efeito"),
    (RevisaoState, "pedir_sugestao", (), {"resposta_aberta_id": "1"}, "banco"),
    (RevisaoState, "usar_sugestao", (), {"sugestao_comentario": "x"}, "efeito"),
    (RevisaoState, "descartar_sugestao", (), {"sugestao_disponivel": True}, "efeito"),
    (RevisaoState, "salvar_parecer", (), {"resposta_aberta_id": "1",
                                          "parecer_texto": "x"}, "banco"),
]

print("=" * 100)
print("SONDA: handler real x papel (barrado nao abre sessao; permitido delega)")
print("=" * 100)
print(f"{'estado.handler':42s} {'chave':24s} " + " ".join(f"{p.name:12s}" for p in Role))
for estado_cls, nome, args, setup, tipo in CASOS:
    chave = getattr(estado_cls.event_handlers[nome].fn, "__exige__", None)
    linha = []
    for papel in Role:
        sub = instancia(estado_cls, papel)
        for k, v in setup.items():
            setattr(sub, k, v)
        try:
            resultado, _ = chama(sub, nome, args)
        except Exception as e:  # corpo estourou por falta de banco: tambem delegou
            resultado = "delegou" if type(e) is not Delegou else "delegou"
        permitido = rbac.pode(chave, papel)
        if permitido:
            ok = resultado in ("delegou", "efeito", "retorno")
        else:
            ok = resultado == "barrado"
        linha.append(("OK " if ok else "FURO") + f":{resultado[:8]:8s}")
        if not ok:
            FALHAS.append(f"{estado_cls.__name__}.{nome} papel={papel.name} "
                          f"permitido={permitido} resultado={resultado}")
    print(f"{estado_cls.__name__ + '.' + nome:42s} {str(chave):24s} " + " ".join(linha))

print()
print("=" * 100)
print("RESUMO: %d furo(s)" % len(FALHAS))
for f in FALHAS:
    print("  - " + f)
print("=" * 100)
sys.exit(1 if FALHAS else 0)
