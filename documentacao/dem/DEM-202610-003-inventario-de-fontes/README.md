# DEM-202610-003 — Inventário de fontes e licenças

## Finalidade

Um **registro único e estruturado** de todas as fontes do acervo — licença, regime de
exibição, atribuição e decisão — para que ninguém precise redescobrir o que pode ser
exibido ao aluno. É a **DEM-A** da OLPF da frente de base de conhecimento.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — **signed** (2026-10-17, `open_questions_open: 0`)
- PRD: [`planner/prd.md`](planner/prd.md)
- Spec: [`planner/spec.md`](planner/spec.md) — **aprovada com 3 ajustes** (2026-10-17)
- **ADR-012** governa cada linha; **OLPF** define a frente
- Depende de: DEM-202610-001 (entregue — libera a frente)

## Estado

- [x] Intent escrito e **assinado** (3 decisões no §8)
- [x] PRD escrito
- [x] **Spec aprovada** — `GATE: spec` vencido, com três ajustes incorporados
- [x] Design + plano-testes (enxutos: esta DEM produz **dado e documento**)
- [x] **Artefato entregue**: `documentacao/fontes/inventario.csv` (79 linhas) + `README.md` + `verificar_inventario.py`
- [x] **EVAL rodada 1: FAIL** — 2 defeitos reais + 3 observações (`eval/jornada.md`)
- [x] Correções: artefato **e instrumento** (o verificador não testava CA01 nem a regra do §6.1)
- [x] **EVAL rodada 2: PASS** — `eval/jornada-rodada2.md`, hash `17fc665`
- [ ] **Aceite do ARQUITECT** ← próximo

> **Registro pós-veredito:** uma correção documental entrou **depois** do PASS (o corpo do caso F-10 ainda dizia "13 exclusões"). Não altera o CSV, portanto o veredito segue valendo para o artefato no hash `17fc665`.

## Os três ajustes do ARQUITECT (incorporados em 2026-10-17)

| # | Ajuste | O que mudou |
|---|---|---|
| 1 | **Granularidade do Sensus** | RF02 agora exige **uma linha por fonte de dados** (~46 ids do `DATA_LICENSES.md`), não uma por projeto. É o que a DEM-C vai ingerir. |
| 2 | **RF10 incompleta** | Entraram como `nao_entra`: **código do Sensus (AGPL-3.0)**, **código do `biblia-plataforma` (Expo/TS)**, fluxo LaTeX e **modelos Jev e Laya**. |
| 3 | **CA02 não verificável** | Criado o **Anexo A — lista de referência fechada**, item a item. Somados **CA06** (enums) e **CA07** (gatilho com o quê/com quem/quando), e criado o **§6** com os critérios de classificação que tornam RF04/05/07 objetivos. |

**Detalhe menor aceito:** o CSV é gravado em **UTF-8 com BOM** (`utf-8-sig`) para abrir no
Excel em português sem perder acento.

## Uma consequência que o levantamento revelou

O acervo do Sensus traz **7 fontes de Ellen G. White** (linha adventista) e clássicos de
várias tradições (`sword-scofield`, `sword-torrey`, `sword-calvincommentaries`,
`sword-wesley`, `sword-luther`…). Com a granularidade por fonte, a **adequação doutrinária
passa a ser decidida por fonte** — não dá mais para dizer "o Sensus entra" ou "não entra".
É o primeiro caso em que o inventário **força uma decisão doutrinária** que antes ficaria
escondida dentro de um projeto.

## Histórico (data, não relógio)

| Data | Evento |
|---|---|
| 2026-10-17 | Intent criado (proposta da OLPF); ARQUITECT fecha as 3 questões e assina |
| 2026-10-17 | PRD e spec escritos |
| 2026-10-17 | Spec **aprovada com 3 ajustes**; ajustes incorporados (RF02, RF10, Anexo A, §6, CA06/CA07, BOM) |
| 2026-10-17 | Implementação; EVAL rodada 1 **FAIL** (2 defeitos de forma) → corrigido; rodada 2 **PASS** |
| 2026-10-18 | Auditoria do AUXILIAR-ARCHITECT **contra o disco**: 18 erros de identidade + 7 artefatos sem linha aplicados (`c0161ce`) |
| 2026-10-18 | EVAL rodada 3 **FAIL** (F-082 fora da §6.1) → corrigido + verificador endurecido (`3018146`) |
| 2026-10-18 | EVAL rodada 4 **FAIL** (H-01: ponteiro no commit pré-merge) → apontado para `ba165d9` (`6d9d1cc`) |
| 2026-10-18 | **EVAL rodada 5: PASS** (82 testes no hash pinado; verificador PASS, 86 linhas) — **aguarda aceite do ARQUITECT** |
