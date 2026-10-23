# Changelog — DEM-202610-011, fatia 2

## 2026-10-23

- Branch **nova** `feature/DEM-202610-011-fatia2-obras` a partir da `develop` `5c0bc3e` (marco 1 + landing). **Não** reusa o PR #5.
- 3 chaves no `rbac.py`; matriz 15 células (permitido e negado) + prova de vacuidade; ADR-020; seed de alunos fake só na homologação `didasko_v1`.
- Suíte local: 130 testes v1 + 273 regressão. `3f9246e` (obras) + `8ae1a3c` (CI opção A: `pull_request` sem filtro de `branches`). [CI verde no `pull_request`](https://github.com/egarabini/gsi_ebd/actions/runs/40038703819). Check `testes (pytest)` no [PR #9](https://github.com/egarabini/gsi_ebd/pull/9), sem `--admin`. EVAL cego pendente (máximo de 2 rodadas).

## 2026-10-19

- `3b5f56c8964b7efcb10de085617717038abd2930` — etapas A/B: v1 local, sessão/CSRF/H-14/matriz, telas Admin/Revisor, integração e CI separado.
- PR [#5](https://github.com/egarabini/gsi_ebd/pull/5) → develop.
- 157 testes v1 + 269 regressão; três mutações detectadas; login HTTP local verificado. Sem merge/deploy.


CI confirmado no commit `3b5f56c8964b7efcb10de085617717038abd2930`: **269 testes de regressao + 157 testes da v1 passaram**, com a suite da v1 executada de `v1/`. [Execucao verde](https://github.com/egarabini/gsi_ebd/actions/runs/39339058255). PR #5 permanece aberto para develop; EVAL e aceite pendentes.
