# Changelog — DEM-202610-012

## 2026-10-19 — implementação entregue para revisão

- Commit do código: `427e8bbffee73b3f1146b3daa25a91736136dbe7`.
- PR: https://github.com/egarabini/gsi_ebd/pull/3 → develop.
- Seed exige SEED_PASSWORD e troca no primeiro acesso de todos os novos usuários; contas existentes preservadas; removidas credenciais do escopo operacional.
- 128 testes verdes localmente e EVAL cego PASS. CI Python 3.12 verde: https://github.com/egarabini/gsi_ebd/actions/runs/39308015107.
- Repasse da variável pelo Compose e política de falha do subir.sh registrados para o PLANNER, sem alterações fora do escopo.
- Aceite, merge e release não executados; não representa fechamento da D-01 nem da D-10.
