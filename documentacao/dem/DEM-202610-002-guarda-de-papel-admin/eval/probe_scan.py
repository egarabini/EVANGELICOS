"""EVAL DEM-202610-002 - sonda 1: o scan do teste enxerga os handlers? (memoria)

Roda do diretorio do app. Nao edita nada.
"""
import inspect
import os
import sys

sys.path.insert(0, os.getcwd())  # roda do diretorio do app

from gsi_ebd.states.admin import AdminState
from gsi_ebd.states.coordenador import CoordenadorState
from gsi_ebd.states.revisao import RevisaoState


def scan_do_teste(estado):
    """Copia literal da logica de tests/test_rbac.py::test_todo_evento_tem_marcador_exige."""
    sem_marcador = []
    vistos = []
    for nome, fn in vars(estado).items():
        if nome.startswith("_") or nome == "setvar" or not inspect.isfunction(fn):
            continue
        if nome.startswith("set_"):
            continue
        vistos.append((nome, type(fn).__name__, hasattr(fn, "__exige__")))
        if not hasattr(fn, "__exige__"):
            sem_marcador.append(nome)
    return vistos, sem_marcador


for E in (AdminState, CoordenadorState, RevisaoState):
    vistos, sem = scan_do_teste(E)
    print("==", E.__name__, "| event_handlers:", len(E.event_handlers))
    print("   entradas que o scan olha:", len(vistos), "->", [v[0] for v in vistos])
    print("   tipos:", sorted({v[1] for v in vistos}))
    print("   sem marcador:", sem)
    print()

print("vars(AdminState)['load_leads'] =", type(vars(AdminState)["load_leads"]).__name__)
print("inspect.isfunction(vars(AdminState)['load_leads']) =",
      inspect.isfunction(vars(AdminState)["load_leads"]))
