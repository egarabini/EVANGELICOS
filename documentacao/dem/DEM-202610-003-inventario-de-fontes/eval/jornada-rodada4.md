# Jornada EVAL — DEM-202610-003 — rodada 4 (escopo estreito)

- **Agente:** EVAL
- **Data:** 2026-10-17
- **DEM:** DEM-202610-003 / inventario-de-fontes
- **Hash avaliado:** `3018146d3b51dfd5bd54806134e132c50559dbc5`
- **Veredito:** **FAIL** — F PASS · H FAIL · C PASS · N PASS · G N-A

> Escopo: revalidar a F-082 e o endurecimento do verificador, e confirmar que nada
> regrediu. Não li `dev/`, o README da DEM nem as jornadas das rodadas 1–3. Não corrigi
> nada; escrevi apenas em `eval/`. O critério é o de `planner/intent.md`,
> `planner/spec.md` (§4, §6.1, §6.2, §6.3) e `planner/plano-testes.md`.

## 0. Ambiente e método

- O controlador estava em `3018146` no início da rodada. Durante a rodada o HEAD avançou
  para `f99ed97` (commit de docs da DEM-001/ADR-014); `git diff 3018146 HEAD --
  documentacao/fontes/` está **vazio** e o gitlink do `GSI_EBD` é o mesmo (`4ad1e0d`),
  então tudo abaixo vale para o hash despachado, `3018146`.
- Verificador rodado do zero: `C:\Python314\python.exe
  documentacao\fontes\verificar_inventario.py` → `linhas: 86`, **PASS**, exit 0.
- Teste do app: `& .\.venv\Scripts\python.exe -m pytest tests -q` (o launcher
  `pytest.exe` foi bloqueado pelo sandbox local com "Acesso negado"; o `python -m pytest`
  usa o mesmo venv e o mesmo pytest 9.1.0). Resultado: **76 passed**, exit 0.
- Fixtures de teste: o CSV mutado e o export do `ba165d9` foram apagados; restou
  `eval/tmp-gsi/` com um diretório vazio que o sandbox não deixou remover.

## 1. F-082 — corrigida?

Linha atual (`inventario.csv`, linha 83):

| Campo | Valor | Conferência |
|---|---|---|
| `licenca` | `a confirmar` | ok — não afirma licença que não existe |
| `licenca_verificada` | `nao` | coerente com `a confirmar` |
| `regime_exibicao` | `integral_interno` | **§6.1 ok** — não é mais permissivo que `integral_interno` (aceita `nao_exibir`) |
| `decisao` | `depende` | **§6.2 ok** — falta licença |
| `atribuicao_exigida` | `não` | compatível com "nada é exibido" (`depende`); é provisório, não é texto de atribuição |
| `motivo` | "licença dos dados não confirmada registro a registro…" | presente |
| `observacoes` | "… confirmar titular e licença dos dados **junto** aos autores das fontes do atlas (a identificar) **antes de** qualquer exibição ao usuário…" | **§6.3 ok** — o quê (titular/licença) · com quem (autores das fontes) · quando (antes de exibir) |
| `localizacao` | `estudos/atlas-biblico` | caminho existe |
| `adr_referencia` | `ADR-012` | ok |

O defeito da rodada 3 (licença "MIT (código) e dados…", `regime = curto`,
`decisao = depende`) **não existe mais**. `git show 3018146` mostra a troca exata:
`curto` → `integral_interno`, `MIT (código)…` → `a confirmar`, `atribuicao` →
`não`, e o gatilho §6.3 acrescentado.

**F-082: OK.**

## 2. O escape do verificador foi fechado?

Código novo (`documentacao/fontes/verificar_inventario.py`, linhas 119–132): a condição
deixou de ser `licenca == "a confirmar"` e passou a ser

```python
nao_verificada_em_nao_entra = (
    licenca_verificada == "nao" and decisao != "entra"
)
if licenca_txt and ("a confirmar" in licenca_txt or nao_verificada_em_nao_entra) and rid != "F-001":
    if regime not in ("integral_interno", "nao_exibir"):
        falhas.append(...)
```

Testei o escape com o **caso real** e com um caso que **não** contém a string
`a confirmar`:

- **Caso A — F-082 na forma da rodada 3** (licença "MIT (código) e dados…",
  `licenca_verificada = nao`, `decisao = depende`, `regime = curto`):
  `FAIL (1 problema(s))` — "linha 83 (F-082): licenca nao confirmada com decisao
  'nao_entra' exige regime integral_interno ou nao_exibir, nunca curto (spec §6.1)",
  exit 1.
- **Caso B — F-060 com `regime = curto`** (licença `Domínio público`, **não** é
  `a confirmar`, `licenca_verificada = nao`, `decisao = nao_entra`):
  `FAIL (1 problema(s))` — "linha 61 (F-060): … decisao 'entra' …", exit 1.

Nos dois casos o gate **fecha** (exit 1). O escape da rodada 3 está coberto pela
condição nova.

**Ressalva (defeito de mensagem, não de gate):** a f-string usa `decisao` **antes** da
atribuição `decisao = (linha.get("decisao") …)` (linha 135). O valor impresso é o da
**linha anterior**: no Caso A, F-082 é `depende` mas a mensagem diz `nao_entra` (valor
de F-081); no Caso B, F-060 é `nao_entra` mas a mensagem diz `entra` (valor de F-059).
A condição em si usa a linha corrente e está correta; só o texto do erro mente. Se a
**primeira** linha de dados disparasse a regra, haveria `NameError`; hoje a única linha
exceptuada é a primeira (F-001), então isso não é alcançável — mas a exceção está
hardcoded por `rid`, sem verificar que F-001 é o ACF.

**Exceção F-001:** continua justificada. A linha é o **ACF 2007**
(`Sociedade Bíblica Trinitariana do Brasil`), `a confirmar`, `curto`, `entra`; a
ADR-012 **10.10** aceita explicitamente o risco ("citação hoje, confirmação da licença
depois"), e a ADR-012 é a norma superior à regra geral do §6.1. O gatilho da linha está
completo. O único reparo é o hardcode (não valida a identidade ACF/licença).

**Escape fechado? Sim** — com a ressalva de que a mensagem de falha imprime a decisão
da linha anterior.

## 3. Nada regrediu? (estrutura e conteúdo)

- **86 linhas de dados** (87 com cabeçalho; o verificador conta 86).
- **BOM** `EF BB BF` presente.
- **17 colunas** na ordem do §4 (`id` … `revisado_em`), 0 linha com nº de campos ≠ 17.
- **46 ids do Sensus**: reconstruí a lista do `estudos/sensus/DATA_LICENSES.md` §2
  (46 ids) e comparei com os 46 campos `fonte` que começam com `Sensus — `:
  `md=46`, `csv=46`, **faltam = []**, **sobram = []**. São eles:
  `blivre, egw-acts, egw-great-controversy, egw-object-lessons, egw-patriarchs,
  egw-prophets, egw-steps, egw-thoughts, gill, grc-tr, hbo-wlc, kjv, openbible-geo,
  openbible-xref, patristic, smith-daniel, stepbible-tbesg, stepbible-tbesh,
  stepbible-tflsj, stepbible-tipnr, sword-abbott, sword-barnes, sword-burkitt,
  sword-calvincommentaries, sword-catena, sword-clarke, sword-easton, sword-hitchcock,
  sword-isbe, sword-jfb, sword-kd, sword-lightfoot, sword-luther, sword-mhc, sword-nave,
  sword-pnt, sword-rwp, sword-scofield, sword-smith, sword-tfg, sword-torrey, sword-tsk,
  sword-wesley, tagnt, tahot, theographic`.
- **12 exclusões do RF10** presentes como `nao_entra` com motivo: F-011 (código Sensus),
  F-060 (deuterocanônicos), F-068/F-069/F-070/F-071 (lff/lff-en/lffe/sangue), F-072
  (LaTeX), F-073 (código biblia-plataforma), F-076 (skill jesus-cristo), F-077
  (mapas), F-078/F-079 (Jev/Laya). 12/12.
- **Gatilho §6.3** nas 15 linhas com `licenca = a confirmar` (F-001, F-002, F-027,
  F-063, F-068–F-072, F-076, F-078, F-079, F-081, F-082, F-083): todas com "licença/
  titular" + "junto" + "antes de".
- **Motivo** em todas as linhas com `decisao ≠ entra`: 0 sem motivo.
- **`revisado_por`**: vazio em todas as linhas (= pendente da revisão do ARQUITECT,
  §4).
- **Verificador**: PASS, exit 0; os três AVISOs são esperados e não são falha — o de
  `Clark` × `Clarke` é exatamente a desambiguação F-009/F-030; `House` × `Rouse` e
  `Reid` × `Reis` são falsos positivos de nome parecido.

### As 18 correções de identidade — amostra

O commit `c0161ce` alterou 32 linhas e acrescentou 7; 14 titulares mudaram. As seis
amostras pedidas continuam aplicadas no hash:

| id | Antes (`c0161ce^`) | Agora (`3018146`) |
|---|---|---|
| F-009 | "Adam Clarke (1762-1832) / tradução (a identificar)" | **Gordon H. Clark (1902-1985)** / edição a identificar; obs. "NÃO Adam Clarke" |
| F-030 | Adam Clarke, sem desambiguação | Adam Clarke + "NÃO confundir com a F-009 (Gordon H. Clark, calvinista)" |
| F-005 | "Wayne Grudem / Crossway (a confirmar)" | **Wayne Grudem / Zondervan (1994)**; obs. confirma Zondervan |
| F-010 | obra e tradução misturadas, "direito reservado" | **obra** Jonathan Edwards, **Domínio público**; tradução separada na F-080 |
| F-080 | (não existia) | **tradução de 2015, Rodrigo Reis de Faria**, direito reservado |
| F-007 | "James Sire / editora da tradução (a identificar)" | **James W. Sire / Editora Hagnos** |
| F-008 | "Editora da tradução (a identificar)" | **Hawthorne, Martin e Reid / Edições Loyola** |

Observação menor, que não muda titular nem regime: na F-005 (linha **EN**), a cauda
"tradução: Editora Vida Nova" é imprecisa — Vida Nova é a editora da tradução PT, e a
F-005 é o `Systematic Theology` (Zondervan, 1994). A correção de identidade pedida
(Crossway → Zondervan) está feita.

## 4. Plano — F, H, C, N

### 4.1 F-01 a F-10

| ID | Veredito | Evidência |
|---|---|---|
| F-01 | PASS | BOM, `;`, 17 colunas na ordem, 0 linha malformada; verificador PASS |
| F-02 | PASS | 46 linhas `Sensus — `, uma por id; 46/46 do `DATA_LICENSES.md` §2 |
| F-03 | PASS | 15 linhas `a confirmar`, todas com o gatilho completo (§6.3) |
| F-04 | PASS | `regime_exibicao` só `curto`/`integral_interno`/`nao_exibir` |
| F-05 | PASS | `decisao` no conjunto; 0 linha `≠ entra` sem motivo |
| F-06 | PASS | 0 contradições com as 12 decisões da ADR-012 (tabela abaixo) |
| F-07 | PASS | `adequacao_doutrinaria` preenchida; `revisado_por` vazio = revisão pendente |
| F-08 | PASS | 11 linhas internas (`ESTUDOS_BIBLICOS`) e externas no mesmo CSV |
| F-09 | PASS | `documentacao/fontes/README.md` e os caminhos citados existem |
| F-10 | PASS | 12/12 exclusões como `nao_entra` com motivo |

### 4.2 F-06 / H-03 — as 12 decisões da ADR-012

| Decisão | Linha(s) / tratamento | Contradição? |
|---|---|---|
| 10.1 público (coordenador/instrutor) | não é campo do CSV | n/a |
| 10.2 curto com fonte; integral só interno | F-004/005/007/008/009/010/080 `curto` com atribuição; `integral_interno` onde declarado | não |
| 10.3 CC BY-SA | F-012 e F-067 com nota de share-alike | não |
| 10.4 não comercial | F-024 RWP `integral_interno`/`depende`, obs. cita 10.4 | não |
| 10.5 ADR de fontes | n/a (a própria ADR) | n/a |
| 10.6 deuterocanônicos fora | F-060 `nao_entra`/`fora`, motivo 10.6 | não |
| 10.7 lff/lff-en/lffe/sangue fora | F-068–F-071 `nao_entra`/`fora` | não |
| 10.8 mapa | ADR-013; F-086 `depende` | não |
| 10.9 originais entram | F-065/F-066/F-067 `entra` | não |
| 10.10 ACF risco aceito | F-001 `a confirmar`/`curto`/`entra` + gatilho (exceção justificada) | não (ADR aceita) |
| 10.11 resumo por IA | não é fonte do CSV | n/a |
| 10.12 Jev/Laya fora | F-078/F-079 `nao_entra` | não |

**0 contradições.** F-06/H-03 PASS.

### 4.3 H-01 — a suíte

**FAIL.** O hash `3018146` pina `ESTUDOS_BIBLICOS/GSI_EBD` em **`4ad1e0d`** (pré-merge),
não no merge que a própria mensagem do commit diz pinar:

- `git ls-tree 3018146 ESTUDOS_BIBLICOS/GSI_EBD` → `4ad1e0d29a0d…`; `git -C GSI_EBD
  rev-parse HEAD` → o mesmo `4ad1e0d`; working tree limpo.
- `pytest tests -q` nesse checkout → **76 passed** (pytest 9.1.0), exit 0.
- A mensagem de `3018146` diz: "o ponteiro … passa a apontar o merge **ba165d9**
  (develop do GSI_EBD)". `origin/develop` = `ba165d9` (merge do PR #1), que traz
  `tests/test_estudo_aplicado.py` (6 testes novos, 74 `def test_` no total). Exportei
  `ba165d9` com `git archive` para `eval/tmp-gsi` e rodei a mesma suíte: **82 passed**.
- Ou seja: **82 é o merge `ba165d9`, que não está pinado**; o hash avaliado tem 76
  (o merge traria 6 testes a mais; `PAGINAS` tem 9 casos, o que fecha 74 + 8 = 82).

Não é teste vermelho: a suíte passa. É **baseline não cumprido / ponteiro não
atualizado** — H-01 exige 82, o hash entrega 76. O commit `3018146` está internamente
inconsistente (mensagem x gitlink); o HEAD seguinte (`f99ed97`) também não corrigiu o
ponteiro.

### 4.4 H-02, C-01, N-01..N-05

- **H-02 PASS** (com o limite do ambiente): o diff `0c7e005..3018146` não escreve em
  corpus nem em produção (só docs, CSV, verificador, jornada da rodada 3 e o ponteiro do
  submódulo). Não reprovei produção por HTTP — não há rede/credencial nesta sessão; o
  critério que o plano pede ("corpus/produção sem escrita") está satisfeito.
- **C-01 PASS**: no submódulo, `a6c5b80..4ad1e0d` altera só
  `.github/workflows/ci.yml` e `requirements-dev.txt`; **0 arquivo em `gsi_ebd/`**.
  Nesta DEM, nenhum código/banco foi editado.
- **N-01..N-05 PASS**: nenhuma tabela/importador/tela/busca/léxico no diff desta DEM;
  nenhuma licença `a confirmar` foi "resolvida" por suposição (F-082 foi para
  `a confirmar`, não para uma licença inventada; os gatilhos seguem).
- **G-01 N-A** (aceite do ARQUITECT).

## 5. Defeitos e veredito

1. **H-01 (bloqueia):** hash pina `4ad1e0d` (76 testes), não `ba165d9` (82). A
   mensagem do commit afirma o merge; o gitlink não o registra. Correção: apontar o
   gitlink para `ba165d9` (ou corrigir a baseline, se 76 for o novo aceito — mas isso
   reabre o intent, não se ajusta em silêncio).
2. **Verificador (não bloqueia o gate):** a condição nova cobre o escape, mas a
   mensagem usa `decisao` antes da atribuição (linha 130 vs 135) e imprime a decisão
   da linha anterior; na primeira linha disparada haveria `NameError`. O gate fecha
   (exit 1), o diagnóstico engana.
3. **F-005 (menor):** "tradução: Editora Vida Nova" na linha EN; a correção Zondervan
   está feita, a cauda é imprecisa.

```
F: PASS · H: FAIL · C: PASS · N: PASS · G: N-A
agregado: FAIL
```

## 6. Concordância com o verificador

- **Concordo com o PASS no CSV atual**: reproduzi `linhas: 86` e exit 0, e conferi por
  fora (BOM, 17 colunas, 46 ids, 12 exclusões, gatilhos, motivos).
- **Concordo com a regra endurecida**: ela dispara no caso real (F-082 da rodada 3) e
  também em licença não verificada com decisão não-entra que não contém a string
  `a confirmar` (F-060); o escape está fechado.
- **Discordo do texto da falha**: `decisao` é lida antes de ser atribuída e sai o valor
  da linha anterior; corrigir a ordem (ou usar `linha.get("decisao")` na f-string)
  resolve. Não é escape, é diagnóstico.
- **Concordo com a exceção F-001** (ACF + ADR-012 10.10), com a ressalva de que ela é
  hardcoded por `rid` e não valida a identidade/licença da linha.
- **O verificador não cobre H-01**: ele valida o CSV, não o gitlink/testes. O FAIL desta
  rodada vem de fora dele.
