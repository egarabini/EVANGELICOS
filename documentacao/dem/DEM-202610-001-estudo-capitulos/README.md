# DEM-202610-001 — Estudo com capítulos próprios e mapa de origem

## Finalidade

Fazer o material aplicável existir como um **estudo** separado da obra, com capítulos
próprios e origem rastreável. Herdado do outcome do intent.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — **signed** (2026-10-16, `open_questions_open: 0`)
- PRD: [`planner/prd.md`](planner/prd.md) · Spec: [`planner/spec.md`](planner/spec.md) — **aprovada**
- Design: [`planner/design.md`](planner/design.md) · Plano de testes: [`planner/plano-testes.md`](planner/plano-testes.md)
- Briefing do DEVS: [`dev/briefing.md`](dev/briefing.md)
- ADRs que a regem: 002, 003, 005, 010, 011
- Origem do material: `GSI_EBD/Diagnostico/plano-bibliotecas.md` (v2)

## Estado

- [x] Intent escrito e **assinado** — `GATE: intent` vencido (5 decisões no §8)
- [x] PRD + spec escritos
- [x] **Spec aprovada pelo ARQUITECT** — `GATE: spec` vencido
- [x] Design + plano-testes (26 casos: 10 F, 4 H, 3 C, 6 N, 1 G)
- [ ] **List do TLC aprovado** ← `GATE: TLC-List` — próximo
- [ ] Implementação (TLC) na branch `feature/DEM-202610-001-estudo-capitulos`
- [ ] EVAL (subagente cego, PASS/FAIL sobre hash, estado limpo)
- [ ] VISION / aceite do ARQUITECT
- [ ] Publicação pelo CI + fechamento (`changelog.md`)

## Estrutura (ownership por pasta)

```
DEM-202610-001-estudo-capitulos/
├── README.md            ← este índice
├── changelog.md         ← resultado + veredito dos gates (PLANNER) — nasce no fechamento
├── planner/             ← intent · prd · spec · design · plano-testes
└── dev/                 ← briefing.md (PLANNER) + jornada.md (DEVS, a partir da Tarefa 1)
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
