# Changelog — DEM-005, marco 1

## 2026-10-20 — esqueleto da v1 entregue para revisão

- Commit do código: `4a344dd3ea5e46a491d14e5769a1ad04527ee17d`.
- Commit do isolamento do Compose: `4f9e9c9c07e25aa2f9cf6e393ca1d036a8e689d4`.
- PR: https://github.com/egarabini/gsi_ebd/pull/7 → `develop`.
- CI verde: https://github.com/egarabini/gsi_ebd/actions/runs/39451719272 e
  https://github.com/egarabini/gsi_ebd/actions/runs/39452803850.
- Suíte da v1: 37 passaram, a partir de `v1/`. Regressão da v0: 269 passaram.
- Homologação em `https://homolog.didasko.app.br/login` (HTTP 200), certificado
  Let's Encrypt YR2, banco `didasko_v1` no baseline `0001_baseline`. O Traefik da v0
  não foi reiniciado.
- EVAL cego ainda não rodou. Sem merge.
