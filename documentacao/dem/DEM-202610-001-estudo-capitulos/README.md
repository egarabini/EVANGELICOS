# DEM-202610-001 — Estudo com capítulos próprios e mapa de origem

## Finalidade

Fazer o material aplicável existir como um **estudo** separado da obra, com capítulos
próprios e origem rastreável. Herdado do outcome do intent.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — status **signed** (2026-10-16, `open_questions_open: 0`)
- PRD: [`planner/prd.md`](planner/prd.md) · Spec: [`planner/spec.md`](planner/spec.md)
- ADRs que a regem: 002 (corpus), 003 (Escritura), 005 (modelo Obra→Estudo), 010 (publicação), 011 (aprovação assinada)
- Origem do material: `GSI_EBD/Diagnostico/plano-bibliotecas.md` (v2) e a especificação do ARQUITECT

## Estado

- [x] Intent escrito pelo PLANNER
- [x] **Intent assinado** em 2026-10-16 — `GATE: intent` vencido (5 decisões no §8)
- [x] PRD + spec escritos (10 RF, 6 CA, 3 entidades lógicas)
- [ ] **Spec aprovada pelo ARQUITECT** ← `GATE: spec` — próximo
- [ ] design · plano-testes
- [ ] Briefing + implementação (TLC)
- [ ] EVAL (subagente cego, PASS/FAIL sobre hash, estado limpo)
- [ ] VISION (aceite visual do ARQUITECT)
- [ ] Aceite e fechamento

## Estrutura (ownership por pasta)

```
DEM-202610-001-estudo-capitulos/
├── README.md            ← este índice
├── changelog.md         ← resultado consolidado + veredito dos gates (PLANNER) — nasce no fechamento
└── planner/             ← intent · prd · spec (agora); design · plano-testes (após a spec aprovada)
```

`dev/`, `eval/`, `deploy/` e `vision/` nascem quando cada papel atuar — a ausência de uma
pasta significa que o papel não participou.

## Histórico (data, não relógio — decisão do ARQUITECT)

| Data | Evento |
|---|---|
| 2026-10-16 | Intent criado pelo PLANNER — 5 perguntas abertas |
| 2026-10-16 | ARQUITECT autoriza as recomendações ("segue a sua leitura"); questões fechadas e intent assinado |
| 2026-10-16 | PRD e spec escritos pelo PLANNER — 100% dos RF citam o intent |
