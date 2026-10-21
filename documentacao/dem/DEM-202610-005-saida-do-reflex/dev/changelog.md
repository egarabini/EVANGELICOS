# Changelog — DEM-005

## 2026-10-21 — landing (marco 2L) entregue para revisão

- Branch: `feature/DEM-202610-005-landing` (worktree `.worktrees/DEM-005-landing`), a partir do marco 1.
- Commit do código: `f9aa301a4a4a44745b787746d7deea1cda860df3`.
- PR: https://github.com/egarabini/gsi_ebd/pull/8 → `feature/DEM-202610-005-marco1`.
- CI: https://github.com/egarabini/gsi_ebd/actions/runs/39689542371 — **success**
- Código: serviço `v1.landing:create_app` (Jinja2, sem banco) + labels Traefik no compose da homologação.
- Suíte da v1: 54 passaram. Regressão da v0: 269 passaram.
- LCP local (4G simulado): 1 064 ms. Carga 2x: ~92 KB.
- Relatório: `dev/relatorio-landing.md`. Capturas: `dev/capturas-landing/`.
- Homologação ao vivo: aguarda o DEPLOY (`bash deploy/subir.sh --v1`). Traefik não reiniciado.

## 2026-10-20 — esqueleto da v1 entregue para revisão

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
