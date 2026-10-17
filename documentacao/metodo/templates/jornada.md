# Template — `<agente>/jornada.md`

> Esqueleto do **livro-razão** de um agente numa DEM. Copie para `<pasta-do-agente>/jornada.md` (`dev/`, `eval/`, `deploy/`, `vision/`, `know/`) e **preencha**. A regra curta está no `AGENTS.md`; a **mecânica exata** é esta.

---

## Regras do livro-razão (leia uma vez)

1. **Dono único.** A `jornada.md` é do **agente que executa**; o `briefing.md` é do **PLANNER**. O PLANNER **lê** a sua jornada para avaliar — **nunca** a escreve por você.
2. **Append-only — o passado não se reescreve.** Nunca altere nem apague entradas, pontos/horários ou texto já escrito. Corrigir/retomar = **nova Tarefa** que referencia a anterior.
   - **Exceção (cabeçalho é derivado):** `Término` e `Tempo ativo` são **rollup** e **devem** ser atualizados a cada Tarefa. `Início` nunca muda.
3. **`Tarefa N` espelhada.** Cada intervenção do PLANNER = uma `## Tarefa N — <título>` no `briefing.md`; você responde com a **mesma** `Tarefa N` (mesmo título) na sua jornada.
4. **Jornada é o caminho, não o resultado.** Registre o que **tentou**, **onde bateu**, **por que** escolheu cada rumo (e descartou os outros), **o que validou** (comandos/saídas/evidências) e **cada desvio com justificativa**. O entregável final vai para os critérios de aceite (`planner/plano-testes.md`).
5. **Por que existe:** é a sua memória de trabalho **e** a prova que faz o PLANNER **aprovar um desvio necessário** em vez de quicar de volta.

---

## Métrica de tempo e custo

- **A métrica é `Tempo ativo` = Σ(término − início) das Tarefas — NÃO o SPAN.** O SPAN inclui o tempo de **despacho do ARQUITECT** (que toca vários projetos); esse gap **não conta** para nenhum agente.
- `briefing.md` mede o **PLANNER** (orquestração); `jornada.md` mede a **execução do agente** (o custo que justifica melhorias). Rollup por DEM no `README.md`.
- **Tokens:** **derivados** de uma fonte real (telemetria/gateway) quando disponível — consulta, **não** estimativa. Se a interface não expõe, registre **"não medido"**; **nunca invente valores**.

---

## Esqueleto (copie a partir daqui)

```
# Jornada do <PAPEL> — <DEM-...>: <título curto>

> Dono: <PAPEL>. Append-only. Runbook em `briefing.md`.

​```
Agente: <PAPEL>
Início:  AAAA-MM-DD HH:MM      ← nunca muda
Término: AAAA-MM-DD HH:MM      ← rollup, atualiza a cada Tarefa
SPAN: <término − início do relógio>
Tempo ativo: <Σ das Tarefas>   ← A MÉTRICA
Tokens: in <N> / out <N> (derivado | "não medido")
​```

## Tarefa 1 — <título espelhado do briefing>
Início: AAAA-MM-DD HH:MM

### Think
- assunções / ambiguidades declaradas

### List (se DEV/TLC)
- arquivos a criar/alterar + ordem + riscos → aguardar aprovação

### Execução & evidências
- o que tentou · onde bateu · por que escolheu · o que validou (comandos/saídas)
- cada desvio do plano + justificativa

Término: AAAA-MM-DD HH:MM

## Tarefa 2 — <correção/retomada, se houver>  (referencia a Tarefa 1)
...
```
