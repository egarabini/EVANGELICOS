# CONVENTIONS.md — documentação, git e processo

## Documentação

- UTF-8 sem BOM; um `# H1` por arquivo; listas com `-`; code fences com linguagem.
- **pt-BR com acentuação** em `documentacao/`. Código e comentários de código: **sem acento**.
- Templates de DEM copiados de `documentacao/metodo/templates/` — **nunca apagar seções**;
  se não se aplica, escreva "N/A" e o motivo.
- Toda decisão estrutural vira ADR em `documentacao/adr/`, numeração contínua e única.

## Commits

- `tipo(escopo): descrição curta` (Conventional Commits).
- Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, `build`, `ci`.
- Trailer com o id da DEM: `DEM-AAAAMM-<seq>`.
- O hash do commit é registrado no `changelog.md` da DEM.

## Branches (GitFlow — ADR-009)

- `main` = produção (tags SemVer) · `develop` = integração.
- `feature/DEM-AAAAMM-<seq>-<slug>` a partir de `develop`; PR → `develop`.
- `release/x.y.z` e `hotfix/x.y.z` exigem back-merge em `develop` e tag.
- Produção **só** por `release/*`/`hotfix/*` via CI (ADR-010).

## DEMs

- Pasta: `documentacao/dem/DEM-AAAAMM-<seq>-<slug>/` com `planner/`, `dev/`, `eval/`,
  `deploy/` (e `vision/` só se houver tela).
- Um dono único por arquivo: `briefing.md` é do PLANNER; `jornada.md` é do próprio agente.
- Jornada registra **data** (sem relógio/tokens — decisão do ARQUITECT).
