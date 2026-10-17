# README da DEM (template)

> Copie para `README.md` na raiz da pasta da DEM. Dono: PLANNER.

## Nome da DEM
`DEM-AAAAMM-<tracker>-<seq>-<slug>`

## Finalidade
[Objetivo breve da demanda — herdado do outcome do intent.]

## Relação com o roadmap
- Módulo: [N] · Fase: [0 · 1 · 2 · 3 · 4]
- Intent: `planner/intent.md` (status: …)

## Estrutura (ownership por pasta)
```
<DEM>/
├── README.md            ← este índice
├── changelog.md         ← resultado consolidado + veredito (PLANNER)
├── planner/             ← PLANO (PLANNER): intent · prd · spec · design · plano-testes
├── dev/                 ← DEVS:   briefing.md (PLANNER) + jornada.md (DEVS)
├── eval/                ← EVAL:   jornada.md
├── deploy/              ← DEPLOY: briefing.md (runbook) + jornada.md (DEPLOY)
├── vision/              ← VISION: briefing.md? + jornada.md  (só se há tela)
└── know/                ← KNOW:   jornada.md  (quando participa)
```
- **Pasta por agente:** a **ausência** de uma pasta indica que o agente não participou.
- Dentro da pasta: `briefing.md` (**PLANNER**) + `jornada.md` (**o agente**) — dono único por arquivo.

## ⏱️ Tempo e tokens por agente (rollup — derivado das jornadas)
> Fonte: `Tempo ativo` e `Tokens` do cabeçalho de cada `jornada.md`. Consolidado pelo PLANNER no fechamento. **Tempo ativo = Σ das tarefas**, não o SPAN.

| Agente | Tempo ativo | Tokens in/out |
|---|---|---|
| DEVS | — | — |
| EVAL | — | — |
| DEPLOY | — | — |

## Status
- [ ] Planejada
- [ ] Intent signed
- [ ] Em especificação
- [ ] Design aprovado
- [ ] Em implementação
- [ ] Em validação (EVAL/VISION)
- [ ] Concluída (aceite do ARQUITECT)
