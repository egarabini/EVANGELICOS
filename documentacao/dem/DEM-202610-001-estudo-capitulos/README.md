# DEM-202610-001 — Estudo com capítulos próprios e mapa de origem

## Finalidade

Fazer o material aplicável existir como um **estudo** separado da obra, com capítulos
próprios e origem rastreável. Herdado do outcome do intent.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — status **draft**
- ADRs que a regem: 002 (corpus), 003 (Escritura), 005 (modelo Obra→Estudo), 010 (publicação), 011 (aprovação assinada)
- Origem do material: `GSI_EBD/Diagnostico/plano-bibliotecas.md` (v2) e a especificação do ARQUITECT

## Estado

- [x] Intent escrito pelo PLANNER
- [ ] **Intent assinado** ← `GATE: intent`. Nenhuma spec abre antes disto.
- [ ] PRD · spec · design · plano-testes
- [ ] Briefing + implementação (TLC)
- [ ] EVAL (subagente cego, sobre hash)
- [ ] VISION (aceite visual do ARQUITECT)
- [ ] Aceite e fechamento

## Estrutura (ownership por pasta)

```
DEM-202610-001-estudo-capitulos/
├── README.md            ← este índice
├── changelog.md         ← resultado consolidado + veredito dos gates (PLANNER) — nasce no fechamento
└── planner/             ← intent (agora); prd · spec · design · plano-testes (depois da assinatura)
```

`dev/`, `eval/`, `deploy/` e `vision/` nascem quando cada papel atuar — a ausência de uma
pasta significa que o papel não participou.

## Histórico (data, não relógio — decisão do ARQUITECT)

| Data | Evento |
|---|---|
| 2026-10-16 | Intent criado pelo PLANNER — 5 perguntas abertas para o ARQUITECT |
