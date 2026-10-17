# Template — `planner/plano-testes.md` (ancorado no intent)

> **PLANNER escreve. EVAL executa. Ninguém muda critério no meio.** Health do intent só entra se virar caso com evidência. Todo caso rastreia a uma origem no **intent** ou na **spec**. Guia: [camada-intent.md §6](../03-camada-intent/camada-intent.md).

## Contrato

| | |
|---|---|
| Arquivo | `planner/plano-testes.md` |
| Dono | PLANNER |
| Executor | EVAL |
| Entrada | `intent.md` **signed** + `spec.md` **signed** + hash da `feature/*` |
| Saída | `eval/jornada.md` — veredito `PASS\|FAIL\|BLOCKED` **sobre hash**, estado limpo |
| Não é | lista de tarefas DEVS, rubrica de gosto, aceite humano |

**Pré-condição** (PLANNER recusa o despacho se faltar): intent signed, spec signed, e cada caso traça — `H-*`→§6, `C-*`→§5, `N-*`→§4 Out, `F-*`→capacidade da spec.

---

## Bloco `planner/plano-testes.md`

```markdown
# Plano de testes — DEM-0xx / <slug>

status: draft | signed | superseded
owner: PLANNER
executor: EVAL
intent: planner/intent.md          # signed
spec:   planner/spec.md            # signed
signed_by: ARQUITECT
signed_at:

## Âncora
branch: feature/<slug>
hash_alvo: <preenchido no despacho PARA: EVAL — o hash que existe no git>
ambiente: homolog-local | ambiente-limpo
dados: fixtures em eval/fixtures/<slug>/   # versionadas; NÃO produção; NÃO residual

## Estado limpo (obrigatório — regra de ouro 3)
Antes de QUALQUER caso:
- [ ] volumes/dados da DEM zerados (script: eval/reset ou comando abaixo)
- [ ] fixtures aplicadas a partir do diretório acima (hash dos arquivos no cabeçalho da jornada)
- [ ] nenhum volume, cookie, storage ou tabela de rodada anterior
- [ ] comando de reset rodado e log no disco
Reset:
​```
<comando exato>
​```
Se o reset falhar → EVAL não testa. Veredito: BLOCKED (não FAIL).
Evidência residual = falso positivo. Round nulo.

## Rastreio
| ID | Tipo | Origem | Critério (1 linha) | Automatizável | Porteiro |
|----|------|--------|--------------------|---------------|----------|
| F-01 | funcional | spec §<cap> | | sim/não | EVAL |
| H-01 | health | intent §6.<n> | | sim | EVAL |
| C-01 | constraint | intent §5.<n> | | sim | EVAL |
| N-01 | non-goal | intent §4 Out | NÃO existe / NÃO foi construído | sim | EVAL |
| G-01 | gate humano | intent/spec | fluxo humano / decisão sensível / aceite | não | ARQUITECT |

Regras: 0 casos órfãos · 0 capacidades da spec sem F-* · todo §6 virou H-* ou saiu do intent ·
N-* prova AUSÊNCIA · G-* nunca é FAIL do EVAL.

## Casos

### F-01 — <nome>
- origem: spec §
- precondição: estado limpo + fixture <arquivo>
- passos: 1. … 2. …
- esperado: <observável, sem adjetivo>
- evidência: [ ] log [ ] query [ ] resposta [ ] screenshot
- FAIL se:

### H-01 — <invariante do intent>
- origem: intent §6.<n> · baseline: <número no disco>
- mede: <query/comando>
- esperado: não pior que baseline (limiar numérico)
- evidência: output do comando no disco, colado na jornada
- FAIL se: pior que o limiar OU baseline ausente no disco

### C-01 — <constraint>
- origem: intent §5.<n> · tipo: negativo (o agente NÃO pode)
- passos: tentar a violação
- esperado: bloqueio / ausência de campo / erro / nenhum dado sensível no payload
- evidência: diff de payload / schema / header
- FAIL se: a violação passa

### N-01 — <non-goal>
- origem: intent §4 Out
- esperado: artefato/rota/tabela NÃO existe neste hash
- evidência: busca no código / rota inexistente / schema sem coluna
- FAIL se: foi entregue "já que estávamos nisso"

### G-01 — <fluxo humano / decisão sensível>
- origem: spec/intent · porteiro: ARQUITECT
- EVAL registra: N-A + o que foi preparado (o que NÃO foi executado por falta de identidade humana)
- EVAL NÃO marca FAIL por isso

## Ordem de execução
1. Reset + prova de estado limpo (log no disco)
2. C-* (se falhar, o resto é irrelevante — pare)
3. N-* (non-goals)
4. F-* (capacidades)
5. H-* (health — depois do funcional, no mesmo hash)
6. G-* (anotar N-A; não bloqueia o veredito EVAL)

## Veredito (preenche EVAL, não o PLANNER)
hash: <40 chars> · estado_limpo: sim|não
C: PASS|FAIL|N-A · N: … · F: … · H: … · G: N-A (ARQUITECT)
agregado: PASS só se C+N+F+H = PASS e estado_limpo = sim
# BLOCKED se reset falhou, hash inexistente ou fixture ausente
```

## Fora deste plano

- UI/UX, design system, viewport → **VISION** (outro briefing, outro hash check).
- Deploy, backup, tag → **DEPLOY**.
- "Ficou melhor que X" → não é caso. Não há barra de gosto neste plano.
- Correção de código → **DEVS**, via PLANNER, depois de FAIL triado.

## Despacho (PARA: EVAL)

```
PARA: EVAL
DEM: 0xx
GATE: eval
intent: <abs>/planner/intent.md
spec:   <abs>/planner/spec.md
plano:  <abs>/planner/plano-testes.md
código: <abs>  branch: feature/<slug>  hash: <40 chars>
NÃO LER: dev/jornada.md
NÃO FAZER: corrigir código, mudar critério, validar estado residual
```

Antes de mandar, o PLANNER confere: `git cat-file -t <hash>` + `git branch --contains`; plano signed no disco; cada `H-*` com baseline no disco; reset reproduzível.

> **Sinal de que funcionou:** um FAIL nasce de `H-*` ou `N-*`, não só de `F-*`. Se a EVAL só quebra feature e nunca invariante/non-goal, o plano ainda não está lendo o intent.
