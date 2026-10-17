# Protocolo de despacho e consolidação

> Como o trabalho circula entre os papéis sem furar cercas. O despacho endereça **o papel**; quem recebe fora do seu papel **devolve**.

## 1. Cabeçalho de despacho

Todo briefing/mensagem de trabalho abre com três campos:

```
PARA: <PAPEL>          # DEVS | EVAL | VISION | DEPLOY | PLANNER
DEM:  <id da DEM>
GATE: <gate>           # intent | spec | eval | vision | deploy
```

- Quem recebe um despacho fora do seu papel **devolve** (não executa).
- O valor de `GATE:` diz em que porteiro o trabalho está. **A ordem é `intent` → `spec` → `eval` → `vision` → `deploy`.**
- `GATE: spec` sem intent `signed` = mis-roteamento → **devolve**.

## 2. Caminhos absolutos no despacho

O bloco de despacho pronto inclui **os caminhos absolutos** que o agente precisa, para não haver ambiguidade de onde ler/escrever:

```
intent: <abs>/planner/intent.md          # signed
spec:   <abs>/planner/spec.md            # signed (quando aplicável)
plano:  <abs>/planner/plano-testes.md    # para o EVAL
código: <abs do repo>   branch: feature/<slug>   hash: <40 chars quando aplicável>
```

- O **caminho do intent** acompanha todo despacho `PARA: DEVS|EVAL|VISION` — é o norte contra o qual se julga "melhoria".
- Para o EVAL, o despacho carrega também o **hash alvo** (que precisa existir no git).

## 3. Pré-condições de consolidação (auditadas pelo PLANNER, nunca aceitas por declaração)

Antes de o PLANNER dar qualquer parecer ou fechar um gate:

1. **O hash citado existe** — confira (`git cat-file -t <hash>` + `git branch --contains <hash>`).
2. **A jornada está materializada no disco**, com cabeçalho completo (ponto ISO + Tempo ativo + Tokens).
3. **Alegação de correção → diff verificado.** Lista de correção → **triada contra o código real**.
4. **`GATE: intent`:** `planner/intent.md` no disco, `status: signed`; toda capacidade da spec cita §2/§4 Out/§5; retorno "não era o que queríamos" → conferência contra o intent **no disco**, não contra a memória.

## 4. Ferramentas "propõe-e-aplica"

Algumas instâncias (ex.: um agente que gera arquivos mas não faz git) **nunca declaram "feito"**:

1. O agente **gera uma proposta** — arquivo **novo**, caminho relativo, **só na pasta do próprio papel**.
2. O **ARQUITECT confere o caminho** (no cabeçalho do diff) e **aplica** o Accept.
3. O **PLANNER verifica** no disco que o que foi aplicado é o que se esperava.

Isso preserva a regra 9 (nada existe até o disco, verificado) mesmo com ferramentas que não têm capacidade de escrita direta.

## 5. Métricas por tarefa (tempo e tokens)

- Cada `briefing.md`/`jornada.md` carimba **Tempo ativo** (Σ das durações das tarefas, **não** o SPAN do relógio) e **Tokens in/out** por tarefa.
- No fechamento, o PLANNER faz o **rollup** no `README.md` da DEM.
- **Tokens são derivados** de uma fonte real (gateway/telemetria) quando disponível — consulta, **não** estimativa. Se a interface não expõe, registre "não medido"; **nunca invente valores**.

Ver a mecânica exata da jornada em [`../templates/jornada.md`](../templates/jornada.md).

## 6. Retorno da publicação — o CALLBACK estruturado

O DEPLOY **reporta**; o PLANNER **registra**. O callback é a única interface de retorno da publicação e é entregue como **bloco de texto copiável**, contendo no mínimo: o que rodou, resultado/defeito, ação tomada, e os dados (PRs, hashes, tag). Campo faltante = callback incompleto → o PLANNER não fecha.
