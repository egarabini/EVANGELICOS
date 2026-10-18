"""EVAL DEM-202610-002 - sonda 2: o flag state_auto_setters e load-bearing? (contrafactual)

Em memoria: liga o flag ANTES de importar os estados e mede. Nao edita o rxconfig.
Roda do diretorio do app.
"""
import os
import sys

sys.path.insert(0, os.getcwd())

from reflex.config import get_config

get_config().state_auto_setters = True  # contrafactual, so neste processo

from gsi_ebd.states.auth import AuthState  # noqa: E402
from gsi_ebd.models.user import Role  # noqa: E402

print("state_auto_setters (contrafactual) =", get_config().state_auto_setters)
ident = sorted(
    h for h in AuthState.event_handlers
    if h.startswith("set_current_user") or h in ("set_is_authenticated", "set_must_change_password")
)
print("handlers de AuthState:", len(AuthState.event_handlers))
print("setters de identidade recriados:", ident)

st = AuthState(_reflex_internal_init=True, init_substates=False)
print("antes: current_user_role =", int(st.current_user_role), "| is_authenticated =", st.is_authenticated)
AuthState.event_handlers["setvar"].fn(st, "current_user_role", 1)
AuthState.event_handlers["setvar"].fn(st, "is_authenticated", True)
print("depois de setvar('current_user_role',1)+setvar('is_authenticated',True):")
print("   current_user_role =", int(st.current_user_role), "| is_authenticated =", st.is_authenticated)
print("   -> com o flag ligado, o cliente vira ADMIN pelo setvar (o furo do RF09)")

print()
print("-- o teste de identidade reprova nesse cenario?")
import tests.test_rbac as t  # noqa: E402

for nome in ("test_state_auto_setters_desligado", "test_nenhum_setter_de_identidade"):
    try:
        getattr(t, nome)()
        print(f"   !! {nome} PASSOU (nao pega o furo)")
    except AssertionError as e:
        print(f"   ok {nome} REPROVOU (AssertionError, msg={str(e)!r})")
