# Template — `<agente>/briefing.md`

> **Dono: PLANNER.** Handoff/runbook vivo para o agente (DEVS, EVAL, VISION, DEPLOY). O agente **lê** isto; a jornada dele vai em `jornada.md`. Cada intervenção do PLANNER = uma nova **Tarefa** titulada, espelhada na jornada do agente.

```markdown
# Briefing do <PAPEL> — <DEM-...>

PARA: <PAPEL>
DEM:  <id>
GATE: <intent|spec|eval|vision|deploy>

​```
Agente: PLANNER
Início:  AAAA-MM-DD HH:MM
Término: AAAA-MM-DD HH:MM
SPAN: 0h00
Tempo ativo: 0h00   ← Σ das tarefas (overhead de orquestração)
Tokens: in 0 / out 0 (derivado | "não medido")
​```

## Caminhos absolutos
intent: <abs>/planner/intent.md        # signed
spec:   <abs>/planner/spec.md          # quando aplicável
plano:  <abs>/planner/plano-testes.md  # para EVAL
código: <abs do repo>  branch: feature/<slug>  hash: <quando aplicável>

---

## Tarefa 1 — [handoff inicial]
**Início:** AAAA-MM-DD HH:MM · **Término:** HH:MM
- **Identidade** (DEM, repo, work item/ticket, branch, release).
- **Leitura TLC** (ordem dos documentos) · **Escopo** (faz / NÃO faz) · **Decisões do ARQUITECT** ·
  **Riscos** · **Restrições** · **Definição de pronto** · **GitFlow**.

## Tarefa 2 — [intervenção/correção, se surgir]
**Início:** AAAA-MM-DD HH:MM · **Término:** HH:MM
- [o que fazer em seguida — espelha a Tarefa 2 da jornada]
```

> Variações por papel: para o **EVAL**, o "briefing" é o `planner/plano-testes.md` (não há `eval/briefing.md` separado). Para o **DEPLOY**, o briefing é o **runbook** de publicação. Para o **DEVS/VISION**, é o handoff acima.
