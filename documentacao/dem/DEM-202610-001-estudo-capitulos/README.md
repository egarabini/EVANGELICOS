# DEM-202610-001 — Estudo com capítulos próprios e mapa de origem

## Finalidade

Fazer o material aplicável existir como um **estudo** separado da obra, com capítulos
próprios e origem rastreável. Herdado do outcome do intent.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — **signed** (`open_questions_open: 0`)
- PRD: [`planner/prd.md`](planner/prd.md) · Spec: [`planner/spec.md`](planner/spec.md) — **aprovada**
- Design: [`planner/design.md`](planner/design.md) · Plano de testes: [`planner/plano-testes.md`](planner/plano-testes.md)
- Parecer do PLANNER: [`planner/parecer-diff.md`](planner/parecer-diff.md)
- Briefing: [`dev/briefing.md`](dev/briefing.md) · Jornada do DEVS: [`dev/jornada.md`](dev/jornada.md)
- Veredito do EVAL: [`eval/jornada.md`](eval/jornada.md)
- ADRs que a regem: 002, 003, 005, 010, 011

## Estado

- [x] Intent escrito e **assinado** — `GATE: intent` vencido
- [x] PRD + spec escritos e **spec aprovada** — `GATE: spec` vencido
- [x] Design + plano-testes (**28 casos**: 11 F, 4 H, 4 C, 6 N, 1 G)
- [x] Think + **List aprovado** — `GATE: TLC-List` vencido
- [x] **Implementação (TLC)** — 2 commits em `feature/DEM-202610-001-estudo-capitulos`
- [x] Parecer do PLANNER sobre o diff real
- [x] **EVAL cego: PASS** — hash `ac712dd`, estado limpo (C 4/4 · N 6/6 · F 11/11 · H PASS)
- [x] **VISION / aceite do ARQUITECT** — **concedido em 2026-10-17**
- [ ] PR → `develop` · publicação pelo CI — **bloqueados** (Fase A3 / `gh`)
- [ ] Fechamento final — `changelog.md` escrito; conclui após o release

## Implementação (2026-10-16)

| Commit | O que |
|---|---|
| `6defd39` | `fix(obra)`: `select` do SQLModel no importador da obra — defeito de re-execução encontrado no caminho |
| `ac712dd` | `feat(estudo)`: modelos, importador, 6 testes, aba do admin e item de menu |

**Verificação:** 82 testes verdes · autoteste do importador PASS (10 checagens) ·
página admin compila · **C-04** (`git diff` vazio em `lesson.py`, `aluno.py`, `study.py`).

**Operação (design §4):** quem roda `importar_estudo_aplicado --apply` em produção é o
**ARQUITECT**, depois do `pg_dump` e depois do merge. O agente não publica nem escreve
em produção (ADR-010).

## Findings do EVAL — triagem do PLANNER

O EVAL entregou dois itens **fora do contrato**. Nenhum afetou o PASS (não são casos do
plano), e a triagem é minha:

| # | Finding | Decisão |
|---|---|---|
| 1 | A spec §3 (RNF) diz "tela exige ADMIN", mas `/admin` só exige **login**: `check_auth` → `require_login`, e os **loaders** não têm guarda de papel (as guardas `is_admin` estão só nas ações que gravam). Rota **pré-existente**, fora do diff — não é regressão desta DEM. | **Spec corrigida** (RNF marcado como *alvo*, com a pendência e o número da DEM). O buraco vira **DEM-202610-002 (proposta)**: guarda de papel nas rotas `/admin`. Não foi corrigido aqui — mexer nas guardas de *todas* as rotas é fora do escopo desta DEM e é decisão do ARQUITECT. |
| 2 | O commit `c936375` (parecer do PLANNER) varreu os probes do EVAL (`eval/_eval_*.py`) para dentro dele. | **Mantidos de propósito** e documentados em [`eval/README.md`](eval/README.md): são evidência reproduzível em SQLite descartável, nunca produção. Evita que a verificação volte a ser relato. |

## Ajustes do ARQUITECT incorporados

| # | Ajuste | Onde entrou |
|---|---|---|
| 1 | **Quem** roda a carga: o ARQUITECT, após `pg_dump` e após o merge | `design.md` §4 |
| 2 | Obra ausente → importador **aborta sem criar** | `design.md` §3/§4 + caso **F-11** |
| 3 | Prova objetiva de não tocar na lição | caso **C-04** |

## Estrutura (ownership por pasta)

```
DEM-202610-001-estudo-capitulos/
├── README.md            ← este índice
├── changelog.md         ← resultado + veredito dos gates (PLANNER) — nasce no fechamento
├── planner/             ← intent · prd · spec · design · plano-testes · parecer-diff
├── dev/                 ← briefing.md (PLANNER) + jornada.md (DEVS)
└── eval/                ← jornada.md + probes (EVAL)
```

`deploy/` e `vision/` nascem quando cada papel atuar.

## Histórico (data, não relógio)

| Data | Evento |
|---|---|
| 2026-10-16 | Intent criado; ARQUITECT assina ("segue a sua leitura"); PRD e spec escritos |
| 2026-10-16 | Spec **aprovada**; design, plano-testes e briefing escritos |
| 2026-10-16 | ARQUITECT aprova o desenho com 3 ajustes; dois viram casos de teste (F-11, C-04) |
| 2026-10-16 | Think + List do DEVS; **List aprovado** |
| 2026-10-16 | Implementação: 2 commits, 82 testes verdes, C-04 provado |
| 2026-10-16 | Parecer do PLANNER sobre o diff real |
| 2026-10-16 | **EVAL cego: PASS** — verificado com fixture própria, CLI real e sha256 das tabelas |
| 2026-10-16 | Findings do EVAL triados; RNF de segurança corrigido na spec; aberta a proposta de DEM-002 |
