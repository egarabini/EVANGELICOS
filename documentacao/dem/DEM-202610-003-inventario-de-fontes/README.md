# DEM-202610-003 — Inventário de fontes e licenças

## Finalidade

Um **registro único e estruturado** de todas as fontes do acervo — licença, regime de
exibição, atribuição e decisão — para que ninguém precise redescobrir o que pode ser
exibido ao aluno. É a **DEM-A** da OLPF da frente de base de conhecimento.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — **signed** (2026-10-17, `open_questions_open: 0`)
- PRD: [`planner/prd.md`](planner/prd.md) · Spec: [`planner/spec.md`](planner/spec.md)
- **ADR-012** governa cada linha do inventário; **OLPF** define a frente
- Depende de: DEM-202610-001 (entregue — libera a frente)

## Estado

- [x] Intent escrito e **assinado** (3 decisões no §8)
- [x] PRD + spec escritos
- [ ] **Spec aprovada pelo ARQUITECT** ← próximo
- [ ] Design + plano-testes (enxutos: esta DEM produz **dado e documento**, não código)
- [ ] Artefato: `documentacao/fontes/inventario.csv` + `README.md`
- [ ] List + implementação (TLC)
- [ ] EVAL + aceite

## O que o artifacto vai ser

Um CSV com **uma linha por artefato** (código e dados são linhas separadas quando as
licenças diferem), colunas conforme a spec §4: `id`, `fonte`, `tipo`, `titular`, `licenca`,
`licenca_verificada`, `regime_exibicao`, `atribuicao_exigida`, `versao_data`,
`adequacao_doutrinaria`, `decisao`, `motivo`, `localizacao`, `adr_referencia`,
`observacoes`, `revisado_por`, `revisado_em`.

## Estrutura (ownership por pasta)

```
DEM-202610-003-inventario-de-fontes/
├── README.md            ← este índice
├── changelog.md         ← nasce no fechamento
└── planner/             ← intent · prd · spec (agora); design · plano-testes
```

## Histórico (data, não relógio)

| Data | Evento |
|---|---|
| 2026-10-17 | Intent criado (proposta da OLPF) |
| 2026-10-17 | ARQUITECT fecha as 3 questões e assina; PRD e spec escritos |
