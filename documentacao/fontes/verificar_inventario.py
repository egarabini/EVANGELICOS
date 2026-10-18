"""Verifica o inventario.csv contra a spec da DEM-202610-003.

Instrumento do EVAL: le o CSV, nao o codigo que o gerou. Cobre CA01-CA07 e a
cobertura do Anexo A da spec.

    python documentacao/fontes/verificar_inventario.py
"""
from __future__ import annotations

import csv
import re
import sys
from pathlib import Path

AQUI = Path(__file__).resolve().parent
CSV = AQUI / "inventario.csv"

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

# Anexo A da spec: os 46 ids declarados em estudos/sensus/DATA_LICENSES.md
SENSUS_IDS = {
    "theographic",
    "tagnt", "grc-tr", "tahot", "hbo-wlc",
    "stepbible-tbesg", "stepbible-tbesh", "stepbible-tflsj", "stepbible-tipnr",
    "openbible-geo", "openbible-xref",
    "blivre", "sword-rwp", "kjv",
    "gill", "patristic", "sword-barnes", "sword-calvincommentaries", "sword-clarke",
    "sword-jfb", "sword-kd", "sword-mhc", "sword-scofield", "sword-wesley",
    "sword-abbott", "sword-burkitt", "sword-catena", "sword-lightfoot",
    "sword-luther", "sword-pnt", "sword-tfg",
    "egw-great-controversy", "egw-patriarchs", "egw-prophets", "egw-acts",
    "egw-object-lessons", "egw-steps", "egw-thoughts", "smith-daniel",
    "sword-easton", "sword-hitchcock", "sword-isbe", "sword-smith",
    "sword-nave", "sword-torrey", "sword-tsk",
}

# RF10: as 12 exclusoes que precisam existir como linha com motivo
EXCLUSOES = {
    "F-011": "codigo do Sensus (AGPL)",
    "F-060": "deuterocanonicos",
    "F-068": "caderno lff",
    "F-069": "caderno lff-en",
    "F-070": "caderno lffe",
    "F-071": "caderno sangue",
    "F-072": "fluxo LaTeX",
    "F-073": "codigo biblia-plataforma (Expo/TS)",
    "F-076": "skill jesus-cristo",
    "F-077": "mapas-biblicos-e-panorama",
    "F-078": "modelo Jev",
    "F-079": "modelo Laya",
}


def main() -> int:
    falhas: list[str] = []
    avisos: list[str] = []

    bruto = CSV.read_bytes()
    if not bruto.startswith(b"\xef\xbb\xbf"):
        falhas.append("CA01: arquivo sem BOM UTF-8 (Excel PT-BR corrompe acentos)")
    texto = bruto.decode("utf-8-sig")

    linhas = list(csv.DictReader(texto.splitlines(), delimiter=";"))
    if not linhas:
        falhas.append("CA01: CSV vazio")
        return relatar(falhas, avisos, 0)

    # CA01: colunas na ordem
    cabecalho = list(linhas[0].keys())
    if cabecalho != COLUNAS:
        falhas.append(f"CA01: colunas fora da ordem. Esperado {COLUNAS}. Achado {cabecalho}")

    ids = set()
    sensus_vistos = set()
    for n, linha in enumerate(linhas, start=2):
        rid = (linha.get("id") or "").strip()
        rotulo = f"linha {n} ({rid or 'sem id'})"

        if not rid:
            falhas.append(f"{rotulo}: id vazio")
        elif rid in ids:
            falhas.append(f"{rotulo}: id duplicado")
        ids.add(rid)

        # campos com numero errado de separadores aparecem como None no DictReader
        if None in linha:
            falhas.append(f"{rotulo}: numero de campos diferente de 17")

        # CA06: enums
        for coluna, dominio in ENUMS.items():
            valor = (linha.get(coluna) or "").strip()
            if valor not in dominio:
                falhas.append(f"{rotulo}: {coluna}='{valor}' fora do dominio {sorted(dominio)}")

        # CA01: campos obrigatorios preenchidos (spec §4)
        obrigatorios = [
            "id", "fonte", "tipo", "titular", "licenca", "licenca_verificada",
            "regime_exibicao", "atribuicao_exigida", "versao_data",
            "adequacao_doutrinaria", "decisao", "localizacao",
        ]
        vazios = [c for c in obrigatorios if not (linha.get(c) or "").strip()]
        if vazios:
            falhas.append(f"{rotulo}: campos obrigatorios vazios {vazios} (CA01)")

        # spec §6.1: licenca a confirmar, OU licenca nao verificada com decisao nao-entra,
        # exige regime NAO MAIS PERMISSIVO que integral_interno (aceita nao_exibir).
        # Excecao unica: F-001 (ACF), cujo risco a ADR-012 10.10 aceita explicitamente.
        licenca_txt = (linha.get("licenca") or "").strip().lower()
        nao_verificada_em_nao_entra = (
            (linha.get("licenca_verificada") or "").strip() == "nao"
            and (linha.get("decisao") or "").strip() != "entra"
        )
        if licenca_txt and ("a confirmar" in licenca_txt or nao_verificada_em_nao_entra) and rid != "F-001":
            if (linha.get("regime_exibicao") or "").strip() not in ("integral_interno", "nao_exibir"):
                falhas.append(
                    f"{rotulo}: licenca nao confirmada com decisao '{decisao}' exige regime "
                    f"integral_interno ou nao_exibir, nunca curto (spec §6.1)"
                )

        # CA03: motivo obrigatorio quando nao entra
        decisao = (linha.get("decisao") or "").strip()
        motivo = (linha.get("motivo") or "").strip()
        if decisao in ("nao_entra", "depende") and not motivo:
            falhas.append(f"{rotulo}: decisao={decisao} sem motivo (CA03)")

        # CA07: gatilho completo quando licenca a confirmar
        licenca = (linha.get("licenca") or "").strip().lower()
        if licenca == "a confirmar":
            obs = (linha.get("observacoes") or "").lower()
            faltando = [
                parte for parte, marca in (
                    ("o que", "licen" in obs or "titular" in obs),
                    ("com quem", "junto" in obs),
                    ("quando", "antes de" in obs),
                ) if not marca
            ]
            if faltando:
                falhas.append(f"{rotulo}: licenca 'a confirmar' sem {faltando} no gatilho (CA07)")

        # cobertura do Sensus: o id vai no campo fonte, apos 'Sensus — '
        fonte = (linha.get("fonte") or "").strip()
        if fonte.startswith("Sensus — "):
            sid = fonte.split("Sensus — ", 1)[1].split(":", 1)[0].strip()
            sensus_vistos.add(sid)

    # CA02: cobertura dos 46 ids do Sensus
    faltam_sensus = SENSUS_IDS - sensus_vistos
    sobram_sensus = sensus_vistos - SENSUS_IDS
    if faltam_sensus:
        falhas.append(f"CA02: fontes do Sensus sem linha: {sorted(faltam_sensus)}")
    if sobram_sensus:
        avisos.append(f"ids do Sensus no CSV fora do Anexo A: {sorted(sobram_sensus)}")

    # RF10: exclusoes presentes, com decisao nao_entra e motivo
    por_id = {l["id"].strip(): l for l in linhas if l.get("id")}
    for rid, descricao in EXCLUSOES.items():
        linha = por_id.get(rid)
        if linha is None:
            falhas.append(f"RF10: exclusao '{descricao}' ({rid}) ausente")
            continue
        if linha.get("decisao", "").strip() != "nao_entra":
            falhas.append(f"RF10: '{descricao}' ({rid}) deveria ser nao_entra")
        if not linha.get("motivo", "").strip():
            falhas.append(f"RF10: '{descricao}' ({rid}) sem motivo")

    # CA05: internas e externas no mesmo arquivo (trivial, mas registra)
    internas = [l for l in linhas if "ESTUDOS_BIBLICOS" in (l.get("localizacao") or "")]
    avisos.append(f"fontes internas na mesma tabela: {len(internas)} linha(s)")

    # ── checagens de IDENTIDADE (sugeridas pelo AUXILIAR-ARCHITECT, 17/10) ───
    # Nao verificam verdade; reduzem onde o erro se esconde.
    raiz = AQUI.parents[1]  # .../EVANGELICOS  (AQUI = documentacao/fontes)
    padrao_caminho = re.compile(r"((?:ESTUDOS_BIBLICOS|estudos|documentacao)/[A-Za-z0-9_./\-]+)")
    caminhos = set()

    # 1. existencia do caminho citado na localizacao
    for linha in linhas:
        rid = (linha.get("id") or "").strip()
        loc = (linha.get("localizacao") or "").strip()
        if not loc or "não identificado" in loc:
            continue
        for achado in padrao_caminho.findall(loc):
            caminho = achado.rstrip("/")
            caminhos.add(caminho)
            candidatos = (raiz / caminho, raiz / "ESTUDOS_BIBLICOS" / caminho)
            if not any(c.exists() for c in candidatos):
                falhas.append(f"{rid}: caminho da localizacao nao existe: {caminho}")
        if "a confirmar" in loc.lower() and "fora do git" not in loc.lower():
            avisos.append(f"{rid}: localizacao com 'a confirmar' - usar o caminho real se o material esta no git")

    # 2. autores com nome parecido: Clark x Clarke ja enganou uma linha uma vez
    def _ed(a: str, b: str) -> int:
        if abs(len(a) - len(b)) > 1:
            return 9
        anterior = list(range(len(b) + 1))
        for i, ca in enumerate(a, 1):
            atual = [i]
            for j, cb in enumerate(b, 1):
                atual.append(min(anterior[j] + 1, atual[j - 1] + 1, anterior[j - 1] + (ca != cb)))
            anterior = atual
        return anterior[-1]

    tokens: dict[str, set[str]] = {}
    for linha in linhas:
        rid = (linha.get("id") or "").strip()
        for palavra in re.findall(r"\b[A-ZÁÉÍÓÚÂÊÔÃÕÇ][a-záéíóúâêôãõç]{3,}\b", linha.get("titular") or ""):
            tokens.setdefault(palavra, set()).add(rid)
    nomes = sorted(tokens)
    for i, a in enumerate(nomes):
        for b in nomes[i + 1:]:
            if tokens[a] == tokens[b]:
                continue
            if _ed(a.lower(), b.lower()) == 1:
                avisos.append(
                    f"autores com nome parecido: '{a}' {sorted(tokens[a])} x '{b}' "
                    f"{sorted(tokens[b])} - conferir identidade"
                )

    # 3. cobertura inversa: diretorio de primeiro nivel sem nenhuma linha citada.
    # Excluidos os que NAO sao fonte de conteudo (codigo, planejamento, template).
    nao_fonte = {"GSI_EBD", "Diagnostico", "PASTOR_IA", "TEMPLATE_ESTUDO", "conteudo"}
    for pasta, rotulo in ((raiz / "estudos", "estudos/"), (raiz / "ESTUDOS_BIBLICOS", "ESTUDOS_BIBLICOS/")):
        if not pasta.is_dir():
            continue
        for d in sorted(p for p in pasta.iterdir() if p.is_dir()):
            if d.name.startswith(".") or d.name in ("__pycache__",) or d.name in nao_fonte:
                continue
            if not any(d.name in c for c in caminhos):
                avisos.append(f"cobertura inversa: nenhum caminho cita {rotulo}{d.name}/")

    return relatar(falhas, avisos, len(linhas))


def relatar(falhas: list[str], avisos: list[str], total: int) -> int:
    print(f"linhas: {total}")
    for aviso in avisos:
        print(f"AVISO {aviso}")
    if falhas:
        print(f"\nFAIL ({len(falhas)} problema(s)):")
        for falha in falhas:
            print(f"  - {falha}")
        return 1
    print("\nPASS — estrutura, enums, motivo, gatilho e cobertura do Anexo A")
    return 0


if __name__ == "__main__":
    sys.exit(main())
