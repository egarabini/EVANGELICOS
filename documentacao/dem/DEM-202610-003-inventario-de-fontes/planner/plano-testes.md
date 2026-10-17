# Plano de testes — DEM-202610-003 / inventario-de-fontes

status: draft
owner: PLANNER
executor: EVAL
intent: `planner/intent.md` — signed 2026-10-17
spec: `planner/spec.md` — aprovada 2026-10-17
design: `planner/design.md`
signed_by: ARQUITECT
signed_at:

## Âncora

- **branch:** `feature/DEM-202610-003-inventario-de-fontes`
- **hash_alvo:** `<preenchido no despacho para o EVAL>`
- **ambiente:** local, somente leitura do repositório. **Não há produção envolvida.**
- **estado limpo:** não se aplica a banco. O equivalente é: o CSV é lido do git, não de
  memória; o verificador roda do zero.

## Rastreio

| ID | Tipo | Origem | Critério | Automatizável | Porteiro |
|----|------|--------|----------|---------------|----------|
| F-01 | funcional | spec RF01 | CSV com BOM, `;`, 17 colunas na ordem declarada | sim | EVAL |
| F-02 | funcional | spec RF02 | granularidade por fonte; sensus com uma linha por id | sim | EVAL |
| F-03 | funcional | spec RF03 | `a confirmar` ⇒ gatilho completo (§6.3) | sim | EVAL |
| F-04 | funcional | spec RF04 | `regime_exibicao` ∈ conjunto | sim | EVAL |
| F-05 | funcional | spec RF05 | `decisao` ∈ conjunto; motivo obrigatório quando ≠ entra | sim | EVAL |
| F-06 | funcional | spec RF06 | zero contradição com a ADR-012 | **não** (julgamento) | EVAL |
| F-07 | funcional | spec RF07 | `adequacao_doutrinaria` preenchida; revisão pendente registrada | sim | EVAL |
| F-08 | funcional | spec RF08 | internas e externas no mesmo arquivo | sim | EVAL |
| F-09 | funcional | spec RF09 | arquivos nos caminhos declarados | sim | EVAL |
| F-10 | funcional | spec RF10 | 13 exclusões presentes como `nao_entra` com motivo | sim | EVAL |
| H-01 | health | intent §6 | suíte continua **82 verdes** | sim | EVAL |
| H-02 | health | intent §6 | lição do Cap. 21 intocada (corpus/produção sem escrita) | sim | EVAL |
| H-03 | health | intent §6 | 0 contradições com as 12 decisões da ADR-012 | **não** | EVAL |
| C-01 | constraint | intent §5 | nenhum arquivo de código/banco tocado | sim | EVAL |
| N-01 | non-goal | intent §4 Out | nada persistido no banco (DEM-B) | sim | EVAL |
| N-02 | non-goal | intent §4 Out | nenhuma ingestão (DEM-C) | sim | EVAL |
| N-03 | non-goal | intent §4 Out | nenhuma busca/tela (DEM-D) | sim | EVAL |
| N-04 | non-goal | intent §4 Out | nenhum léxico ou original ingerido | sim | EVAL |
| N-05 | non-goal | intent §4 Out | nenhuma licença "a confirmar" resolvida por suposição | sim | EVAL |
| G-01 | gate humano | intent §7 | aceite do ARQUITECT: responder "pode exibir ao aluno?" para qualquer fonte | não | ARQUITECT |

## Casos

### F-01 — estrutura do arquivo
- passos: 1. `python verificar_inventario.py` 2. conferir o bloco "estrutura"
- esperado: BOM presente, delimitador `;`, 17 colunas na ordem, 0 linha malformada
- FAIL se: faltar BOM, coluna extra/faltando, linha com nº de campos ≠ 17

### F-02 — granularidade por fonte
- passos: contar linhas cujo `fonte` começa com `Sensus — `
- esperado: **46** linhas (uma por id do `DATA_LICENSES.md`)
- evidência: contagem + lista dos ids encontrados
- FAIL se: < 46, ou algum id do arquivo faltar

### F-03 — gatilho completo
- passos: para cada linha com `licenca = a confirmar`, conferir `observacoes`
- esperado: contém **o quê**, **com quem** e **quando** (as três partes)
- FAIL se: qualquer `a confirmar` com `observacoes` vazio ou incompleto

### F-10 — exclusões como linha
- passos: buscar as 13 exclusões do RF10
- esperado: todas presentes com `decisao = nao_entra` e `motivo` não vazio
- FAIL se: alguma ausente ou sem motivo

### H-01 / C-01 — nada regrediu
- passos: `pytest tests -q` no repositório de código; `git diff --stat` do código
- esperado: 82 verdes; **diff vazio** em `gsi_ebd/`
- FAIL se: teste falhar ou houver qualquer alteração em código

### N-01..N-05 — non-goals (provam AUSÊNCIA)
- passos: buscar no diff e no CSV
- esperado: nenhuma tabela criada, nenhum importador novo, nenhuma tela, nenhum léxico,
  nenhum `a confirmar` preenchido por suposição (todo gatilho preservado)
- FAIL se: qualquer item aparecer

### F-06 / H-03 — julgamento (não automatizável)
- passos: conferir linha a linha as 12 decisões da ADR-012 contra o CSV
- esperado: 0 contradição
- evidência: tabela das 12 decisões com a linha correspondente ou "n/a"

### G-01 — aceite humano
- o ARQUITECT percorre o CSV e responde, para uma amostra, "pode exibir ao aluno?".
- EVAL registra N-A.

## Ordem de execução

1. `F-01` → `F-02` (estrutura antes de conteúdo)
2. `F-03`, `F-04`, `F-05`, `F-07`, `F-08`, `F-09`, `F-10`
3. `C-01`, `N-01..N-05`
4. `H-01`, `H-02`
5. `F-06`/`H-03` (julgamento, por amostragem declarada)
6. `G-01` (N-A)

## Veredito (preenche o EVAL)

```
hash: <40 chars>
F: PASS|FAIL · H: PASS|FAIL · C: PASS|FAIL · N: PASS|FAIL · G: N-A (ARQUITECT)
agregado: PASS só se F+H+C+N = PASS
```

## Despacho (PARA: EVAL)

```
PARA: EVAL
DEM: DEM-202610-003
GATE: eval
intent: C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-003-inventario-de-fontes\planner\intent.md
spec:   ...\planner\spec.md
plano:  ...\planner\plano-testes.md
artefato: C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\fontes\
NÃO LER: dev/jornada.md
NÃO FAZER: corrigir o CSV, mudar critério, "completar" linha com suposição
```
