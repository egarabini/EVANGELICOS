# DEM-202610-001 — Estudo com capítulos próprios e mapa de origem

## Finalidade

Fazer o material aplicável existir como um **estudo** separado da obra, com capítulos
próprios e origem rastreável. Herdado do outcome do intent.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — **signed** (2026-10-16, `open_questions_open: 0`)
- PRD: [`planner/prd.md`](planner/prd.md) · Spec: [`planner/spec.md`](planner/spec.md) — **aprovada**
- Design: [`planner/design.md`](planner/design.md) · Plano de testes: [`planner/plano-testes.md`](planner/plano-testes.md)
- Briefing do DEVS: [`dev/briefing.md`](dev/briefing.md) · Jornada do DEVS: [`dev/jornada.md`](dev/jornada.md)
- ADRs que a regem: 002, 003, 005, 010, 011
- Origem do material: `GSI_EBD/Diagnostico/plano-bibliotecas.md` (v2)

## Estado

- [x] Intent escrito e **assinado** — `GATE: intent` vencido (5 decisões no §8)
- [x] PRD + spec escritos
- [x] **Spec aprovada pelo ARQUITECT** — `GATE: spec` vencido
- [x] Design + plano-testes (**28 casos**: 11 F, 4 H, 4 C, 6 N, 1 G)
- [x] Briefing e Think/List do DEVS — `dev/jornada.md`
- [ ] **List aprovado pelo ARQUITECT** ← `GATE: TLC-List` — aguardando
- [ ] Implementação (TLC) na branch `feature/DEM-202610-001-estudo-capitulos`
- [ ] EVAL (subagente cego, PASS/FAIL sobre hash, estado limpo)
- [ ] VISION / aceite do ARQUITECT
- [ ] Publicação pelo CI + fechamento (`changelog.md`)

## Ajustes do ARQUITECT incorporados (2026-10-16)

| # | Ajuste | Onde entrou |
|---|---|---|
| 1 | **Quem** roda a carga em produção: o ARQUITECT, após `pg_dump` e após o merge | `design.md` §4 |
| 2 | Obra ausente no banco → importador **aborta sem criar** | `design.md` §3/§4 + caso **F-11** |
| 3 | Prova objetiva de não tocar na lição | caso **C-04** (`git diff` vazio em `lesson.py`, `aluno.py`, `study.py`) |

## Estrutura (ownership por pasta)

```
DEM-202610-001-estudo-capitulos/
├── README.md            ← este índice
├── changelog.md         ← resultado + veredito dos gates (PLANNER) — nasce no fechamento
├── planner/             ← intent · prd · spec · design · plano-testes
└── dev/                 ← briefing.md (PLANNER) + jornada.md (DEVS)
```

`eval/`, `deploy/` e `vision/` nascem quando cada papel atuar.

## Histórico (data, não relógio)

| Data | Evento |
|---|---|
| 2026-10-16 | Intent criado pelo PLANNER — 5 perguntas abertas |
| 2026-10-16 | ARQUITECT autoriza as recomendações ("segue a sua leitura") e assina |
| 2026-10-16 | PRD e spec escritos — 100% dos RF citam o intent |
| 2026-10-16 | Spec **aprovada** pelo ARQUITECT |
| 2026-10-16 | Design, plano-testes e briefing do DEVS escritos |
| 2026-10-16 | ARQUITECT aprova o desenho com 3 ajustes; design e plano-testes corrigidos |
| 2026-10-16 | Think + List do DEVS em `dev/jornada.md` — aguardando aprovação |
