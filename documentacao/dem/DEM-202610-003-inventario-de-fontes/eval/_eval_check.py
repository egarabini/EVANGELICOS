# -*- coding: utf-8 -*-
"""Conferencia independente do EVAL para a DEM-202610-003.

Nao reutiliza a lista de ids do verificador do autor: extrai os ids do
proprio DATA_LICENSES.md (secao 2) e compara com o CSV.
"""
from __future__ import annotations

import csv
import re
import sys
from collections import Counter
from pathlib import Path

ROOT = Path(r"C:\Projetos\EM_ESTUDO\EVANGELICOS")
CSV = ROOT / "documentacao" / "fontes" / "inventario.csv"
DL = ROOT / "estudos" / "sensus" / "DATA_LICENSES.md"

COLUNAS = [
    "id", "fonte", "tipo", "titular", "licenca", "licenca_verificada",
    "regime_exibicao", "atribuicao_exigida", "versao_data",
    "adequacao_doutrinaria", "decisao", "motivo", "localizacao",
    "adr_referencia", "observacoes", "revisado_por", "revisado_em",
]

ENUMS = {
    "tipo": {"corpus", "referencia_cruzada", "obra", "adendo", "fonte_dados",
             "codigo", "conteudo", "ferramenta"},
    "licenca_verificada": {"sim", "nao"},
    "regime_exibicao": {"curto", "integral_interno", "nao_exibir"},
    "adequacao_doutrinaria": {"ok", "atencao", "fora", "a_revisar"},
    "decisao": {"entra", "nao_entra", "depende"},
}

EXCLUSOES = [
    ("F-011", "codigo do Sensus (AGPL-3.0)"),
    ("F-060", "deuterocanonicos (10.6)"),
    ("F-068", "lff (10.7)"),
    ("F-069", "lff-en (10.7)"),
    ("F-070", "lffe (10.7)"),
    ("F-071", "sangue (10.7)"),
    ("F-072", "fluxo LaTeX do estudos-biblicos"),
    ("F-073", "codigo do biblia-plataforma (ADR-001)"),
    ("F-076", "skill jesus-cristo"),
    ("F-077", "mapas-biblicos-e-panorama"),
    ("F-078", "modelo Jev (10.12)"),
    ("F-079", "modelo Laya (10.12)"),
]

print("== F-01 estrutura ==")
raw = CSV.read_bytes()
print("bytes iniciais:", raw[:3].hex(" ").upper())
print("BOM:", raw.startswith(b"\xef\xbb\xbf"))
texto = raw.decode("utf-8-sig", errors="strict")
print("decodifica UTF-8: ok")

# csv.reader sobre o texto inteiro (respeita campos multi-linha)
registros = list(csv.reader(texto.splitlines(), delimiter=";"))
print("registros fisicos (inclui cabecalho):", len(registros))
print("cabecalho:", registros[0])
print("n_colunas_cabecalho:", len(registros[0]))
print("cabecalho_na_ordem:", registros[0] == COLUNAS)
contagem = Counter(len(r) for r in registros[1:])
print("distribuicao de campos por linha de dados:", dict(contagem))
maus = [(i, len(r)) for i, r in enumerate(registros[1:], start=2) if len(r) != 17]
print("linhas com campos != 17:", maus)
# linhas em branco?
brancos = [i for i, r in enumerate(registros[1:], start=2) if not r or (len(r) == 1 and r[0] == "")]
print("linhas de dados vazias:", brancos)
# ponto-e-virgula dentro de campo geraria contagem > 17; checar as linhas cruas
print("linhas fisicas no arquivo:", len(texto.splitlines()))

linhas = list(csv.DictReader(texto.splitlines(), delimiter=";"))
print("linhas de dados (DictReader):", len(linhas))

print("\n== F-02 Sensus: ids extraidos de DATA_LICENSES.md secao 2 ==")
dl = DL.read_text(encoding="utf-8")
sec2 = dl.split("## 2. Fontes", 1)[1].split("## 3.", 1)[0]
ids_dl = re.findall(r"^\|\s*`([^`]+)`\s*\|", sec2, re.M)
print("ids encontrados no DATA_LICENSES:", len(ids_dl))
print("ids:", ", ".join(ids_dl))

linhas_sensus = []
for n, l in enumerate(linhas, start=2):
    fonte = (l.get("fonte") or "").strip()
    if fonte.startswith("Sensus"):
        m = re.match(r"^Sensus \u2014 ([^:]+):", fonte)
        if m:
            linhas_sensus.append((n, m.group(1).strip(), l.get("id")))
        else:
            print(f"  !! linha {n}: fonte com prefixo Sensus mas formato irregular: {fonte!r}")

ids_csv = [sid for _, sid, _ in linhas_sensus]
print("linhas Sensus no CSV:", len(linhas_sensus))
print("ids no CSV:", ", ".join(ids_csv))
dup = [k for k, v in Counter(ids_csv).items() if v > 1]
print("ids Sensus duplicados no CSV:", dup)
faltam = [i for i in ids_dl if i not in ids_csv]
sobram = [i for i in ids_csv if i not in ids_dl]
print("ids do DATA_LICENSES sem linha:", faltam)
print("ids no CSV fora do DATA_LICENSES:", sobram)
print("ids_dl e ids_csv iguais (conjunto):", set(ids_dl) == set(ids_csv))
# ordem de ids no arquivo vs CSV (nao exigida, so evidencia)
print("mesma ordem:", ids_dl == ids_csv)

print("\n== F-04/F-05/F-07 + ids ==")
ids = [(l.get("id") or "").strip() for l in linhas]
print("ids duplicados:", [k for k, v in Counter(ids).items() if v > 1])
print("primeiro/ultimo id:", ids[0], ids[-1])
esperados_ids = [f"F-{i:03d}" for i in range(1, len(ids) + 1)]
print("ids sequenciais F-001..F-0%02d:" % len(ids), ids == esperados_ids)
for coluna, dominio in ENUMS.items():
    fora = [(l.get("id"), l.get(coluna)) for l in linhas if (l.get(coluna) or "").strip() not in dominio]
    print(f"enum {coluna}: fora={fora}")
for l in linhas:
    d = (l.get("decisao") or "").strip()
    m = (l.get("motivo") or "").strip()
    if d != "entra" and not m:
        print(f"  !! {l.get('id')}: decisao={d} sem motivo")
print("toda linha com decisao != entra tem motivo:",
      all((l.get("decisao") or "").strip() == "entra" or (l.get("motivo") or "").strip() for l in linhas))
print("adequacao_doutrinaria preenchida:",
      all((l.get("adequacao_doutrinaria") or "").strip() for l in linhas))
print("revisado_por preenchido em:", sum(1 for l in linhas if (l.get("revisado_por") or "").strip()))
print("revisado_em preenchido em:", sum(1 for l in linhas if (l.get("revisado_em") or "").strip()))

print("\n== F-03 gatilho (licenca == 'a confirmar') ==")
for l in linhas:
    lic = (l.get("licenca") or "").strip().lower()
    if lic == "a confirmar":
        print(f"  {l.get('id')}: obs={l.get('observacoes')!r}")

print("\n== F-08 internas x externas ==")
internas = [l.get("id") for l in linhas if (l.get("localizacao") or "").startswith("ESTUDOS_BIBLICOS")]
print("linhas com localizacao ESTUDOS_BIBLICOS:", internas)
print("total:", len(linhas), "| tipos:", dict(Counter((l.get('tipo') or '').strip() for l in linhas)))

print("\n== F-09 caminhos ==")
for p in ["documentacao/fontes/inventario.csv", "documentacao/fontes/README.md",
          "documentacao/fontes/verificar_inventario.py"]:
    print(f"  {p}: {(ROOT/p).is_file()}")

print("\n== F-10 exclusoes ==")
por_id = {(l.get("id") or "").strip(): l for l in linhas}
for rid, desc in EXCLUSOES:
    l = por_id.get(rid)
    if l is None:
        print(f"  {rid} {desc}: AUSENTE")
        continue
    print(f"  {rid} {desc}: decisao={l.get('decisao')!r} motivo={l.get('motivo')!r}")

print("\n== distribuicao decisao x regime ==")
print(dict(Counter(((l.get('decisao') or '').strip(), (l.get('regime_exibicao') or '').strip()) for l in linhas)))
print("decisoes:", dict(Counter((l.get('decisao') or '').strip() for l in linhas)))
print("licencas 'a confirmar':", sum(1 for l in linhas if (l.get('licenca') or '').strip().lower() == 'a confirmar'))
