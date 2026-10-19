# Jornada — DEM-202610-012

## 2026-10-19 — Think e List

Intent assinado e briefing lidos. O ARQUITECT aprovou a lista de arquivos e testes neste atendimento. Notas adicionais: não alterar Compose; registrar o repasse ausente de SEED_PASSWORD ao app; verificar o redirecionamento do primeiro login inclusive do admin.

Branch do código: `feature/DEM-202610-012-credencial-de-seed`, criada a partir de `develop`; `origin/develop` conferida sem commits adicionais. Sem alterações prévias no código.

## Implementação

- `gsi_ebd/data/seed.py`: leitura de SEED_PASSWORD sem default; ausência e valor vazio abortam antes do acesso ao banco; funções de criação de usuários também validam a variável. Todos os novos usuários com troca obrigatória; removidas senhas dos logs. Usuários existentes preservados.
- `.env.example`: variável documentada sem valor.
- `README.md`, `deploy/DEPLOY.md` e `deploy/subir.sh`: removida credencial operacional; documentação da configuração e da pendência do Compose.
- `tests/test_seed.py`: 15 casos, com bancos SQLite descartáveis e senha de teste gerada em fixture. Cobertura de hash, troca obrigatória, idempotência, ausência/valor vazio inclusive com banco populado, logs, exemplo, varreduras e login de todos os papéis.
- Login existente já encaminha para `/perfil/alterar-senha`, inclusive admin. Testado pelo handler real e sessão SQLite, sem mudança no fluxo.

## Validação

- Primeira tentativa de teste bloqueada pelo acesso ao TEMP do usuário; usado `--basetemp` em `.pytest_cache`, dentro do workspace. Comparação inicial de EventSpec corrigida para observar o redirect e seu destino, evitando comparação booleana de Var do Reflex.
- Do diretório `ESTUDOS_BIBLICOS/GSI_EBD`: `.venv/Scripts/python.exe -m pytest tests -q --basetemp=.pytest_cache/dem012-suite1`: **128 passed**, 18 avisos de depreciação preexistentes de datetime.utcnow.
- `bash -n deploy/subir.sh` e `git diff --check`: passaram.
- Varredura do escopo: zero ocorrências da credencial antiga. Exceções remanescentes: `gsi_ebd/states/admin.py`, `gsi_ebd/pages/admin.py` (D-10), `Diagnostico/plano-hierarquia-e-equipes.md` e `Diagnostico/roteiro-de-testes.md` (histórico).

## Pendências e fronteiras

- Compose não repassa SEED_PASSWORD ao app. Defini-la no .env da VPS não basta; o PLANNER deve decidir sobre `SEED_PASSWORD: ${SEED_PASSWORD:-}`. Compose mantido intacto por instrução explícita.
- O subir.sh existente trata falha do seed como aviso (`|| aviso`); logo o seed aborta, mas esse script pode prosseguir. Não alterado, conforme escopo; informar ao PLANNER antes de uma publicação em banco novo.
- D-10 e rotação de contas existentes fora do escopo. Sem alteração de schema, dependências, VPS, secrets, guardas ou CI. Sem deploy.
- EVAL cego e CI do PR ainda pendentes nesta etapa do registro.
