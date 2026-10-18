"""EVAL DEM-202610-002 - sonda 3: os testes reprovam quando a guarda some? (memoria)

Nao edita arquivo nenhum. Roda do diretorio do app.
"""
import inspect
import os
import sys

sys.path.insert(0, os.getcwd())

import pytest

from gsi_ebd.states.admin import AdminState
from gsi_ebd.states.auth import AuthState
from gsi_ebd.states.coordenador import CoordenadorState
from gsi_ebd.states.revisao import RevisaoState

import tests.test_rbac as t

print("=" * 78)
print("A. o teste do marcador examina alguma coisa?")
print("=" * 78)
print("   entradas de vars() que passam no filtro isfunction:", end=" ")
import inspect
n = 0
for E in (AdminState,):
    for nome, fn in vars(E).items():
        if nome.startswith("_") or nome == "setvar" or not inspect.isfunction(fn):
            continue
        if nome.startswith("set_"):
            continue
        n += 1
print(n)
print("   -> test_todo_evento_tem_marcador_exige() roda sobre ZERO metodos")
t.test_todo_evento_tem_marcador_exige()
print("   -> teste PASSA (verde) mesmo sem examinar nada")

print()
print("=" * 78)
print("B. removendo __exige__ de TODOS os 28 eventos (em memoria): o teste reprova?")
print("=" * 78)
salvos = {}
for E in (AdminState, CoordenadorState, RevisaoState):
    for nome, h in list(E.event_handlers.items()):
        fn = getattr(h, "fn", None)
        if fn is not None and hasattr(fn, "__exige__"):
            salvos[(E, nome)] = fn.__exige__
            del fn.__exige__
print("   marcadores removidos:", len(salvos), "(esperado: 28)")
t.test_todo_evento_tem_marcador_exige()
print("   -> test_todo_evento_tem_marcador_exige() CONTINUA PASSANDO (falso verde)")
for (E, nome), chave in salvos.items():
    getattr(E.event_handlers[nome], "fn").__exige__ = chave

print()
print("=" * 78)
print("C. evento novo sem classificacao: a lista congelada reprova?")
print("=" * 78)
antes = dict(AdminState.event_handlers)
AdminState._add_event_handler("evento_novo_de_prova", lambda self: None)
print("   event_handlers de AdminState agora tem", len(AdminState.event_handlers), "entradas")
try:
    t.test_lista_de_eventos_congelada("AdminState")
    print("   !! lista congelada NAO reprovou")
except AssertionError as e:
    print("   ok lista congelada REPROVOU (AssertionError:", repr(str(e)), ")")
finally:
    AdminState.event_handlers = antes
    if hasattr(AdminState, "evento_novo_de_prova"):
        delattr(AdminState, "evento_novo_de_prova")

print()
print("=" * 78)
print("D. guarda de rota neutrada (em memoria): a suite reprova?")
print("=" * 78)
AuthState._guarda = lambda self, rota: None
print("   AuthState._guarda = lambda self, rota: None  (guarda real vira no-op)")
codigo = pytest.main(["tests", "-q", "-p", "no:cacheprovider"])
print("   pytest exit code com a guarda neutrada:", codigo)
print("   0 = suite inteira passou (a guarda de rota NAO e coberta por teste)")

print()
print("=" * 78)
print("E. algum teste toca o on_load de gsi_ebd/gsi_ebd.py?")
print("=" * 78)
import subprocess
out = subprocess.run(
    ["git", "grep", "-n", "-E", r"on_load|gsi_ebd\.gsi_ebd|guarda_admin\(", "--", "tests"],
    capture_output=True, text=True, encoding="utf-8", errors="replace",
)
print("   git grep em tests/ ->", out.stdout.strip() or "(so o teste sintetico de test_rbac.py, que NAO usa AuthState.guarda_*)")
