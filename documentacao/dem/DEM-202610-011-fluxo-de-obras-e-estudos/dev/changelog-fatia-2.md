# Changelog — DEM-202610-011, fatia 2

## 2026-10-23 — fix do EVAL (critério 5)

- `test_estudo_fake.py`: login real `aluno.fake.a`, GET 200, POST 303, `UserResponse`/`Progress` pelo handler; `aluno.fake.b` na obra não liberada → vazio/403.
- `recusar_producao` exige `DIDASKO_AMBIENTE=homologacao`; vazio/desconhecido recusa; `popular()`/`run()` no SQLite `didasko_v1.db`.
- Caminho HTTP mínimo `v1/routers/aluno.py` (sem a UI completa do aluno).
- Commit `48f97f8`. Suíte local: **138** v1 + **273** v0. [CI `pull_request` 40043436945](https://github.com/egarabini/gsi_ebd/actions/runs/40043436945). Relatório e briefing atualizados (#9/`3f9246e`/130+272 na 1ª rodada; 2ª rodada neste fix).

## 2026-10-23

- Branch **nova** `feature/DEM-202610-011-fatia2-obras` a partir da `develop` `5c0bc3e` (marco 1 + landing). **Não** reusa o PR #5.
- 3 chaves no `rbac.py`; matriz 15 células (permitido e negado) + prova de vacuidade; ADR-020; seed de alunos fake só na homologação `didasko_v1`.
- Suíte local: 130 testes v1 + 272 regressão (o 273 inclui o tests/test_ci.py, que so existe a partir do 8ae1a3c). `3f9246e` (obras) + `8ae1a3c` (CI opção A: `pull_request` sem filtro de `branches`). [CI verde no `pull_request`](https://github.com/egarabini/gsi_ebd/actions/runs/40038703819). Check `testes (pytest)` no [PR #9](https://github.com/egarabini/gsi_ebd/pull/9), sem `--admin`. EVAL cego pendente (máximo de 2 rodadas).

## 2026-10-19

- `3b5f56c8964b7efcb10de085617717038abd2930` — etapas A/B: v1 local, sessão/CSRF/H-14/matriz, telas Admin/Revisor, integração e CI separado.
- PR [#5](https://github.com/egarabini/gsi_ebd/pull/5) → develop.
- 157 testes v1 + 269 regressão; três mutações detectadas; login HTTP local verificado. Sem merge/deploy.


CI confirmado no commit `3b5f56c8964b7efcb10de085617717038abd2930`: **269 testes de regressao + 157 testes da v1 passaram**, com a suite da v1 executada de `v1/`. [Execucao verde](https://github.com/egarabini/gsi_ebd/actions/runs/39339058255). PR #5 permanece aberto para develop; EVAL e aceite pendentes.
