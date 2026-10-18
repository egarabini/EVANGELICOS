"""EVAL DEM-202610-002 (guarda de papel) - sonda de verificacao (memoria, sem editar).

Roda do diretorio do app:
    cd ESTUDOS_BIBLICOS/GSI_EBD
    .venv\\Scripts\\python.exe <este_script>
"""
import inspect
import os
import sys

sys.path.insert(0, os.getcwd())  # o Reflex descobre o rxconfig pelo CWD

import reflex as rx
from reflex.config import get_config
from reflex.state import EventHandler

from gsi_ebd.models.user import Role
from gsi_ebd.services.auth_service import AuthService
from gsi_ebd.states.admin import AdminState
from gsi_ebd.states.aluno import AlunoState
from gsi_ebd.states.auth import AuthState
from gsi_ebd.states.common import CommonState
from gsi_ebd.states.coordenador import CoordenadorState
from gsi_ebd.states.perfil import PerfilState
from gsi_ebd.states.revisao import RevisaoState
from gsi_ebd.utils import rbac

ESTADOS = (AuthState, AdminState, CoordenadorState, RevisaoState, AlunoState, PerfilState, CommonState)
GUARDADOS = (AdminState, CoordenadorState, RevisaoState)
IDENTIDADE = (
    "current_user_id", "current_user_name", "current_user_role", "current_user_status",
    "current_user_ambiente", "is_authenticated", "must_change_password",
)


def inst(E):
    """Instancia um estado em memoria. Vars herdadas vivem no estado pai."""
    if E is AuthState:
        return E(_reflex_internal_init=True, init_substates=False)
    pai = AuthState(_reflex_internal_init=True, init_substates=False)
    return E(parent_state=pai, _reflex_internal_init=True, init_substates=False)


def rota_do_retorno(resultado):
    """Extrai a rota de um rx.redirect() (EventSpec) sem browser."""
    if resultado is None:
        return None
    try:
        return resultado.args[0][1]._var_value
    except Exception:
        return f"<{type(resultado).__name__}>"


print("=" * 78)
print("1. CONFIG / IDENTIDADE / SETVAR")
print("=" * 78)
print("get_config().state_auto_setters =", get_config().state_auto_setters)
print()
for E in ESTADOS:
    handlers = sorted(E.event_handlers)
    ident = [h for h in handlers if h.startswith("set_current_user") or h in ("set_is_authenticated", "set_must_change_password")]
    attrs = sorted(a for a in dir(E) if a.startswith("set_current_user") or a in ("set_is_authenticated", "set_must_change_password"))
    print(f"{E.__name__:18s} handlers={len(handlers):2d} identidade_em_handlers={ident} attrs_identidade={attrs}")
    print(f"{'':18s} {handlers}")
print()

print("-- setvar alcanca a identidade? (chamada direta do handler registrado)")
for E in ESTADOS:
    st = inst(E)
    fn = E.event_handlers["setvar"].fn
    for campo in ("current_user_role", "is_authenticated", "must_change_password"):
        try:
            fn(st, campo, 1)
            print(f"   !! {E.__name__}.setvar({campo!r}) SETOU (FURO)")
        except AttributeError as e:
            print(f"   ok {E.__name__}.setvar({campo!r}) -> AttributeError: {e}")
            break
print()

print("=" * 78)
print("2. ROTAS: matriz, guarda real, casa do papel")
print("=" * 78)
print("PERMISSOES =", {k: tuple(int(r) for r in v) for k, v in rbac.PERMISSOES.items()})
print()
for rota in ("/admin", "/coordenador", "/revisao"):
    print(f"rota {rota:14s} ->", {r.name: rbac.pode("rota:" + rota, r) for r in Role})
print()

print("-- guarda real (AuthState.guarda_*) por papel")
for rota, handler in (("/admin", AuthState.guarda_admin), ("/coordenador", AuthState.guarda_coordenador), ("/revisao", AuthState.guarda_revisao)):
    linha = []
    for r in Role:
        st = inst(AuthState)
        st.is_authenticated = True
        st.current_user_role = int(r)
        linha.append(f"{r.name}->{rota_do_retorno(handler.fn(st))}")
    st = inst(AuthState)
    linha.append(f"ANONIMO->{rota_do_retorno(handler.fn(st))}")
    print(f"{rota:14s} " + " | ".join(linha))
print()

print("-- invariante: casa do papel == redirect_for_role e a casa e permitida")
for r in Role:
    casa_rbac = rbac.home_do_papel(int(r))
    casa_login = AuthService.redirect_for_role(int(r))
    permitida = rbac.pode("rota:" + casa_login, r) if ("rota:" + casa_login) in rbac.PERMISSOES else "rota sem guarda"
    print(f"   {r.name:12s} rbac={casa_rbac:14s} login={casa_login:14s} permitida={permitida}")
print()

print("-- rotas publicas na funcao pura (F-06)")
for rota in ("/", "/login", "/confirmar/[token]", "/homenagens"):
    print(f"   pode('rota:{rota}', ALUNO) = {rbac.pode('rota:' + rota, Role.ALUNO)}  "
          f"(pode('rota:{rota}', ADMIN) = {rbac.pode('rota:' + rota, Role.ADMIN)})")
print()

print("-- on_load real do app (gsi_ebd/gsi_ebd.py)")
import gsi_ebd.gsi_ebd as appmod

for chave in ("admin", "coordenador", "revisao"):
    page = appmod.app._unevaluated_pages.get(chave)
    events = getattr(page, "on_load", None)
    nomes = [getattr(e.fn, "__qualname__", repr(e)) for e in (events if isinstance(events, list) else [events])]
    print(f"   {chave:14s} on_load = {nomes}")
print()

print("=" * 78)
print("3. EVENTOS DOS 3 ESTADOS ADMINISTRATIVOS")
print("=" * 78)
total = 0
for E in GUARDADOS:
    print(f"== {E.__name__} ({len(E.event_handlers)} handlers no barramento)")
    for nome in sorted(E.event_handlers):
        if nome == "setvar":
            print(f"   {nome:32s} setvar (nao decorado; so setter explicito)")
            continue
        handler = E.event_handlers[nome]
        chave = getattr(getattr(handler, "fn", None), "__exige__", None)
        if chave is None and nome.startswith("set_"):
            print(f"   {nome:32s} SETTER (sem __exige__; coberto pela lista congelada)")
        else:
            total += 1
            print(f"   {nome:32s} __exige__ = {chave!r}")
print(f"\n   eventos NAO-setter com marcador: {total} (alegado: 28)")
print()

print("-- scan do teste F-12 sobre vars(estado)")
for E in GUARDADOS:
    vistos = []
    for nome, fn in vars(E).items():
        if nome.startswith("_") or nome == "setvar" or not inspect.isfunction(fn):
            continue
        if nome.startswith("set_"):
            continue
        vistos.append(nome)
    print(f"   {E.__name__:18s} entradas que o scan do teste examina: {len(vistos)} -> {vistos}")
print("   (todos os atributos publicos da classe sao EventHandler, nao function)")
print()

print("-- decorador barra de verdade? (handlers reais, sem tocar no banco)")
original_session = rx.session


def _boom(*a, **k):
    raise RuntimeError("ABRIU SESSAO - NAO DEVERIA")


rx.session = _boom
try:
    casos = [
        (AdminState.load_coordenadores, AdminState, Role.ALUNO),
        (AdminState.load_leads, AdminState, Role.REVISOR),
        (AdminState.update_lead_status, AdminState, Role.COORDENADOR),
        (AdminState.aprovar_estudo, AdminState, Role.REVISOR),
        (AdminState.aprovar_estudo, AdminState, Role.COORDENADOR),
        (CoordenadorState.assign_study, CoordenadorState, Role.ALUNO),
        (CoordenadorState.assign_study, CoordenadorState, Role.REVISOR),
        (RevisaoState.abrir_resposta, RevisaoState, Role.COORDENADOR),
        (RevisaoState.salvar_parecer, RevisaoState, Role.ALUNO),
    ]
    for handler, E, papel in casos:
        st = inst(E)
        st.is_authenticated = True
        st.current_user_role = int(papel)
        try:
            r = handler.fn(st, 1) if handler.fn.__code__.co_argcount >= 2 else handler.fn(st)
            print(f"   {E.__name__}.{handler.fn.__name__}({papel.name}) -> {r!r} (barrado, nao abriu sessao)")
        except RuntimeError as e:
            print(f"   !! {E.__name__}.{handler.fn.__name__}({papel.name}) -> {e} (FURO)")
finally:
    rx.session = original_session
print()

print("-- assinatura preservada (F-27)")
for handler in (AdminState.aprovar_estudo, CoordenadorState.assign_study, RevisaoState.abrir_resposta):
    fn = handler.fn
    print(f"   {fn.__qualname__:40s} iscoroutine={inspect.iscoroutinefunction(fn)} "
          f"signature={inspect.signature(fn)} wrapped={hasattr(fn, '__wrapped__')}")
print()

print("=" * 78)
print("4. ADVERSARIAL")
print("=" * 78)
print("-- AlunoState: eventos publicos sem guarda de papel/autenticacao/posse")
for nome in sorted(AlunoState.event_handlers):
    h = AlunoState.event_handlers[nome]
    print(f"   {nome:26s} __exige__={getattr(getattr(h,'fn',None),'__exige__',None)!r} "
          f"assinatura={inspect.signature(h.fn) if nome!='setvar' else 'n/a'}")
print("   select_study/start_study/submit_answer nao conferem is_authenticated nem posse do estudo.")
print()

print("-- CoordenadorState.toggle_aluno: aceita qualquer id de aluno? (COORDENADOR)")
st = inst(CoordenadorState)
st.is_authenticated = True
st.current_user_role = int(Role.COORDENADOR)
st.selected_aluno_ids = []
CoordenadorState.toggle_aluno.fn(st, "999999")
print(f"   selected_aluno_ids apos toggle_aluno('999999') = {st.selected_aluno_ids}")
print("   assign_study grava StudyAssignment para esses ids sem conferir o ambiente do aluno.")
print()

print("-- onde current_user_role e escrito no codigo do app")
print("   auth.py:138  self.current_user_role = user.role   (login, do banco)")
print("   auth.py:190  self.current_user_role = Role.ALUNO  (logout)")
print("   nenhum setter, nenhum getattr('set_'+...), nenhum add_var no app")
print()

print("-- RevisaoState.abrir_resposta: id arbitrário, mas a escrita confere posse no service")
print("   ReviewService.registrar_parecer: 'Voce nao acompanha este aluno' (lido no service)")
print()
print("FIM")
