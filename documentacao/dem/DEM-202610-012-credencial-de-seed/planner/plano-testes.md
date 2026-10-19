# Plano de testes — DEM-202610-012 / credencial de seed

> Nível 3 (ADR-018). O EVAL é cego and julga pelo plano. **Revisão de 19/10**: a varredura do
> N-01 tem **escopo de lista** (§5 da spec), não "repositório inteiro".

## 1. Funcionais (F)

| ID | Caso | Esperado | Cobre |
|---|---|---|---|
| **F-01** | seed sem `SEED_PASSWORD` | exit ≠ 0, mensagem clara, **0 usuários criados** | RF02 · H-10 |
| **F-02** | seed com `SEED_PASSWORD=` (vazia) | tratada como ausente (aborta) | RF02 |
| **F-03** | seed com `SEED_PASSWORD="x"` em banco limpo | cria os usuários com o hash de `"x"` | RF01 |
| **F-04** | **todos** os usuários do seed | `must_change_password=True`, **inclusive o admin** | RF03 · H-10 |
| **F-05** | seed re-executado | idempotente: nada sobrescrito, nada duplicado | RF05 |
| **F-06** | `.env.example` | contém `SEED_PASSWORD=` **sem valor real** | RF06 |
| **F-07** | `deploy/subir.sh` | **não** imprime a senha no fim do deploy | RF07 |

## 2. Negativos (N)

| ID | Caso | Esperado |
|---|---|---|
| **N-01** | a senha em algum dos **5 arquivos do RF04** | **zero** ocorrências |
| **N-02** | a senha do seed aparece em log de execução | **não** aparece |
| **N-03** | seed sem a variável em banco **já populado** | o RF02 vence: aborta antes de olhar o banco |
| **N-04** | a varredura **do repositório** | retorna **apenas** as exceções da spec §5: `ADR-008*`, os registros de DEM/EVAL, `Diagnostico/*.md`, `states/admin.py`, `pages/admin.py` — e o teste **lista** quais são |

## 3. Contratos (C)

| ID | Caso | Esperado |
|---|---|---|
| **C-01** | `requirements.txt` / `requirements-dev.txt` | intactos |
| **C-02** | `git diff` em `gsi_ebd/models/` | vazio (sem schema) |
| **C-03** | `tests/test_paginas.py` | 9/9 |

## 4. Saúde (H)

- **H-01** · `pytest tests -q` (do diretório do app) → **113 + novos** · porteiro **EVAL**
- **H-10** · seed sem a variável (ou vazia) falha · porteiro **EVAL**
- **H-11** · zero `senha123` **no escopo do RF04** · porteiro **EVAL**

## 5. Verificação manual (ARQUITECT, no fechamento do D-01)

1. definir `SEED_PASSWORD` no `.env` de produção;
2. **trocar a senha do admin no site** (não é código — é operação);
3. decidir o que fazer com os usuários demo (remover ou trocar);
4. confirmar o D-01 e o D-10 no [`DIVIDAS-ACEITAS-ATE-A-V1`](../../visao/DIVIDAS-ACEITAS-ATE-A-V1.md).

## 6. Baseline

| Métrica | Hoje | Esperado |
|---|---|---|
| `senha123` nos 5 arquivos do RF04 | existe (`seed.py`, `README.md`, `DEPLOY.md`, `subir.sh`) | **zero** |
| `senha123` no repo (fora das exceções) | — | **só as exceções listadas** |
| admin com troca obrigatória | **não** | **sim** |
| seed sem `SEED_PASSWORD` | usa `senha123` | **aborta** |
| saída do deploy | imprime a senha | **não imprime** |
| suíte | 113 | 113 + novos |
