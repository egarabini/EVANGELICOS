# DEM-202610-005 — Saída do Reflex (FastAPI + Jinja2 + HTMX)

## Finalidade

Migrar a aplicação do **Reflex** para **FastAPI + Jinja2 + HTMX**, **por rotas**, com
convivência atrás do Traefik, **paridade primeiro** e volta atrás possível a cada tela.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — **rascunho** do AUXILIAR-ARCHITECT
  (o ARQUITECT já decidiu 8.1, 8.2, 8.3 e 8.7)
- **ADR-014 (Proposed)** — substitui a **ADR-001** quando aceita; **nenhum código antes disso**
- **Depende da DEM-004** (CI): sem rede de segurança não se migra rota a rota
- Ordem: **admin e telas novas primeiro; lição do aluno por último** (protege H-02)

## Estado

- [x] Intent escrito (rascunho do AUXILIAR-ARCHITECT)
- [ ] **Intent assinado** pelo ARQUITECT
- [ ] **ADR-014 aceita** — condição para qualquer código
- [ ] Spec + design + **baselines que faltam** (matriz papel × rota, inventário das rotas atuais)
- [ ] Migração por rota, com paridade
- [ ] EVAL por rota + aceite

## O que a medição já mostrou

| Camada | Linhas | Importa Reflex? |
|---|---|---|
| `models/` | 753 | não |
| `scripts/` | 898 | não |
| `ai/` | 87 | não |
| `services/` | 2.003 | **8 de 13 arquivos**, quase só por `rx.session` |
| `states/` + `pages/` + `components/` | **~3.300** | sim — **é o que se reescreve** |

## Perguntas abertas (do intent)

- **9.1** A **DEM-002** (guarda de papel no `/admin`) é feita **agora, no Reflex** ou já na base
  nova? *Recomendação: agora — o furo existe hoje e a migração não é desculpa para deixá-lo.*
- **9.2** Ritmo: várias DEMs por rota ou uma DEM com entregas?
- **9.3** Direção de UX.

## Histórico (data, não relógio)

| Data | Evento |
|---|---|
| 2026-10-18 | Intent do AUXILIAR-ARCHITECT; PLANNER redige a ADR-014 (Proposed) e registra a DEM |
