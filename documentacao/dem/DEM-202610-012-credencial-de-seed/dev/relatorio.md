# DEM-202610-012 — relatório

- **Branch:** `feature/DEM-202610-012-credencial-de-seed`.
- **PR:** https://github.com/egarabini/gsi_ebd/pull/3 → `develop`.
- **Commit:** `427e8bb`.
- **Arquivos:** `gsi_ebd/data/seed.py`, `tests/test_seed.py`, `.env.example`, `README.md`, `deploy/DEPLOY.md`, `deploy/subir.sh`.
- **Testes:** `.venv/Scripts/python.exe -m pytest tests -q --basetemp=.pytest_cache/dem012-suite1`, executado no diretório do app: **128 passed** (113 existentes + 15 novos), com 18 avisos de depreciação. `bash -n deploy/subir.sh` e `git diff --check` passaram.
- **Decisões:** validação da variável em tempo de execução, antes do banco; hash bcrypt preservado; todos os novos usuários exigem troca; senha não registrada nos logs. Login já encaminhava para troca, inclusive admin; teste de comportamento adicionado para cada papel, sem alterar autenticação.
- **Fora de escopo:** D-10 e registros históricos, rotação dos usuários existentes, Compose, dependências, schema, CI, secrets e VPS.

## Pendências para o PLANNER

1. O Compose não repassa `SEED_PASSWORD` ao serviço `app`. O ARQUITECT determinou não alterá-lo; decidir sobre `SEED_PASSWORD: ${SEED_PASSWORD:-}` em `environment`. Sem o repasse, o seed em banco novo aborta mesmo se o `.env` da VPS tiver a variável.
2. `subir.sh` trata falha do seed como aviso e pode continuar. Política preservada por escopo; avaliar antes de publicar para um banco novo.
3. Rotação de usuários existentes permanece operação do ARQUITECT. A correção não altera credenciais já persistidas nem fecha a D-10.
4. CI **verde**: https://github.com/egarabini/gsi_ebd/actions/runs/39308015107 (Python 3.12). EVAL cego **PASS** em `427e8bbffee73b3f1146b3daa25a91736136dbe7`, com 128 testes verdes; ver `eval/parecer.md`. Não foi feito merge nem deploy.
