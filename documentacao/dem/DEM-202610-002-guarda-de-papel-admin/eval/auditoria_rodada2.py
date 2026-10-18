"""Auditoria cega da rodada 2 (DEM-202610-002).

Roda SEMPRE do diretorio do app (o Reflex descobre o rxconfig pelo CWD).
Nao altera nada: so le a matriz, os eventos, os on_load e os guardas.
"""
import os
import sys
import inspect

APP = r"C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD"
os.chdir(APP)
sys.path.insert(0, APP)

from gsi_ebd.models.user import Role  # noqa: E402
from gsi_ebd.utils import rbac  # noqa: E402
from gsi_ebd.states.auth import AuthState  # noqa: E402
from gsi_ebd.states.admin import AdminState  # noqa: E402
from gsi_ebd.states.aluno import AlunoState  # noqa: E402
from gsi_ebd.states.common import CommonState  # noqa: E402
from gsi_ebd.states.coordenador import CoordenadorState  # noqa: E402
from gsi_ebd.states.perfil import PerfilState  # noqa: E402
from gsi_ebd.states.revisao import RevisaoState  # noqa: E402

ESTADOS = (AuthState, AdminState, CoordenadorState, RevisaoState, AlunoState, PerfilState, CommonState)
GUARDADOS = (AdminState, CoordenadorState, RevisaoState)

FALHAS = []


def ok(cond, msg):
    print(("OK   " if cond else "FALHA") + "  " + msg)
    if not cond:
        FALHAS.append(msg)


def destino(ev):
    """Path do EventSpec de rx.redirect, ou None quando o guarda libera."""
    if ev is None:
        return None
    for var, lit in getattr(ev, "args", ()) or ():
        if getattr(var, "_js_expr", "") == "path":
            return getattr(lit, "_var_value", "?")
    return "?"


print("=" * 78)
print("1. MATRIZ (rotas e acoes)")
print("=" * 78)
for rota in ("/admin", "/coordenador", "/revisao"):
    linha = {p.name: rbac.pode("rota:" + rota, p) for p in Role}
    print(f"  rota:{rota:15s} {linha}")
print("  acoes:")
for acao in sorted(k for k in rbac.PERMISSOES if k.startswith("acao:")):
    linha = {p.name: rbac.pode(acao, p) for p in Role}
    print(f"    {acao:26s} {linha}")

print()
print("=" * 78)
print("2. F-06 rotas publicas (pode=True para todo papel; anonimo nao e papel)")
print("=" * 78)
PUBLICAS = ("/", "/login", "/confirmar/[token]", "/homenagens",
            "/aluno", "/aluno/licao", "/aluno/pareceres", "/perfil/alterar-senha")
for rota in PUBLICAS:
    ok(all(rbac.pode("rota:" + rota, p) for p in Role), f"rota publica {rota} para os 5 papeis")
print(f"  pode(rota:/ , -1) = {rbac.pode('rota:/', -1)}  (anonimo nao tem assento na matriz)")

print()
print("=" * 78)
print("3. F-08 casa do papel: AuthService x rbac (fonte unica)")
print("=" * 78)
from gsi_ebd.services.auth_service import AuthService  # noqa: E402
for p in Role:
    casa = rbac.home_do_papel(p)
    svc = AuthService.redirect_for_role(p)
    ok(casa == svc and rbac.pode("rota:" + casa, p),
       f"{p.name:12s} home={casa:14s} AuthService={svc:14s} pode={rbac.pode('rota:' + casa, p)}")
print(f"  papel invalido (99): home={rbac.home_do_papel(99)} AuthService={AuthService.redirect_for_role(99)}")

print()
print("=" * 78)
print("4. IDENTIDADE: setters proibidos nos 7 estados + alcance do setvar")
print("=" * 78)
PROIBIDOS = ("set_current_user_id", "set_current_user_name", "set_current_user_role",
             "set_current_user_status", "set_current_user_ambiente",
             "set_is_authenticated", "set_must_change_password")
for estado in ESTADOS:
    achados_attr = [n for n in PROIBIDOS if getattr(estado, n, None) is not None]
    achados_ev = [n for n in estado.event_handlers
                  if n.startswith("set_current_user") or n in ("set_is_authenticated", "set_must_change_password")]
    ok(not achados_attr and not achados_ev,
       f"{estado.__name__:18s} setters identidade attr={achados_attr} eventos={achados_ev}")

print("  setvar tentando alcancar identidade:")
for var, valor in (("current_user_role", 1), ("current_user_id", 999),
                   ("is_authenticated", True), ("must_change_password", False)):
    alvo = AuthState.setvar
    try:
        alvo(var, valor)
        print(f"    setvar({var!r}) -> NAO lancou (FURO)")
        FALHAS.append("setvar alcancou " + var)
    except Exception as e:
        print(f"    setvar({var!r}) -> {type(e).__name__}: {e}")
    try:
        alvo = AdminState.setvar
        alvo(var, valor)
        print(f"    AdminState.setvar({var!r}) -> NAO lancou (FURO)")
        FALHAS.append("AdminState.setvar alcancou " + var)
    except Exception as e:
        print(f"    AdminState.setvar({var!r}) -> {type(e).__name__}: {e}")

print()
print("=" * 78)
print("5. ROTA: on_load real das 3 rotas guardadas")
print("=" * 78)
from gsi_ebd.gsi_ebd import app  # noqa: E402
for rota in ("/admin", "/coordenador", "/revisao"):
    pagina = app._unevaluated_pages[rota.lstrip("/")]
    on_load = list(pagina.on_load or [])
    guarda = {"admin": AuthState.guarda_admin,
              "coordenador": AuthState.guarda_coordenador,
              "revisao": AuthState.guarda_revisao}[rota.lstrip("/")]
    funcoes = [getattr(h, "fn", None) for h in on_load]
    print(f"  {rota:14s} on_load={[getattr(f, '__qualname__', f) for f in funcoes]}")
    ok(guarda.fn in funcoes, f"{rota} tem {guarda.fn.__qualname__} no on_load")

print("  guarda_rota usado por (marcador __guarda_rota__):")
for rota, handler in (("/admin", AuthState.guarda_admin),
                      ("/coordenador", AuthState.guarda_coordenador),
                      ("/revisao", AuthState.guarda_revisao)):
    print(f"    {handler.fn.__qualname__:28s} __guarda_rota__={getattr(handler.fn, '__guarda_rota__', None)}")
print(f"  AuthState.check_auth ainda existe e NAO e guarda de papel: {AuthState.check_auth is not None}")

print()
print("=" * 78)
print("6. EVENTO: 28 @exige nos 3 estados (e o que a varredura examina)")
print("=" * 78)
total = 0
for estado in GUARDADOS:
    nomes = sorted(n for n, h in estado.event_handlers.items()
                   if hasattr(getattr(h, "fn", None), "__exige__"))
    total += len(nomes)
    sem = sorted(n for n, h in estado.event_handlers.items()
                 if not hasattr(getattr(h, "fn", None), "__exige__"))
    print(f"  {estado.__name__:18s} eventos={len(estado.event_handlers):2d} "
          f"com_marcador={len(nomes):2d} sem_marcador={sem}")
    print(f"    {nomes}")
ok(total == 28, f"total de @exige nos 3 estados = {total} (esperado 28)")

print("  varredura F-12: quantos eventos ela realmente examina?")
examinados = []
for estado in GUARDADOS:
    for nome, handler in estado.event_handlers.items():
        if nome == "setvar" or nome.startswith("set_"):
            continue
        examinados.append((estado.__name__, nome))
print(f"    examina {len(examinados)} eventos (nao-zero; a lista inteira esta acima)")

print()
print("=" * 78)
print("7. GUARDAS reais: destino do redirect por papel x rota")
print("=" * 78)
for rota, handler in (("/admin", AuthState.guarda_admin),
                      ("/coordenador", AuthState.guarda_coordenador),
                      ("/revisao", AuthState.guarda_revisao)):
    fn = handler.fn
    print(f"  {rota}")
    for autenticado in (False, True):
        for p in Role:
            ev = fn(type("S", (), {"is_authenticated": autenticado, "current_user_role": p})())
            d = destino(ev)
            if autenticado:
                esperado = None if rbac.pode("rota:" + rota, p) else rbac.home_do_papel(p)
            else:
                esperado = "/login"
            marca = "OK " if d == esperado else "DIF"
            print(f"    auth={str(autenticado):5s} {p.name:12s} destino={str(d):14s} esperado={str(esperado):14s} {marca}")
            if d != esperado:
                FALHAS.append(f"{rota} {p.name} auth={autenticado} destino={d} esperado={esperado}")

print()
print("=" * 78)
print("8. F-19/F-25: catalogo_aprovar (positivo ADMIN, negativo REVISOR)")
print("=" * 78)
print(f"  pode(catalogo_aprovar, ADMIN)   = {rbac.pode('acao:catalogo_aprovar', Role.ADMIN)}")
print(f"  pode(catalogo_aprovar, REVISOR) = {rbac.pode('acao:catalogo_aprovar', Role.REVISOR)}")
for nome in ("aprovar_estudo", "aprovar_todos", "rejeitar_estudo"):
    h = AdminState.event_handlers[nome]
    print(f"  {nome:16s} __exige__={getattr(h.fn, '__exige__', None)}")
print("  (nao ha teste que EXECUTE o handler com ADMIN; ver jornada)")

print()
print("=" * 78)
print("9. Eventos que recebem id (pertenca nao conferida no estado)")
print("=" * 78)
for estado in (AdminState, CoordenadorState, RevisaoState, AlunoState):
    for nome, h in estado.event_handlers.items():
        fn = getattr(h, "fn", None)
        try:
            assinatura = inspect.signature(fn)
        except (TypeError, ValueError):
            continue
        params = list(assinatura.parameters.values())[1:]
        if any(p.name.endswith("_id") or p.name in ("aluno_id", "response_id", "user_id", "lead_id", "study_id")
               for p in params):
            print(f"  {estado.__name__}.{nome}{assinatura}  marker={getattr(fn, '__exige__', None)}")

print()
print("=" * 78)
print("RESUMO: %d falha(s)" % len(FALHAS))
for f in FALHAS:
    print("  - " + f)
print("=" * 78)
sys.exit(1 if FALHAS else 0)
