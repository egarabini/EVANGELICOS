# Jornada DEPLOY — landing em homologação — 2026-10-21

## Autorização e alvo

O ARQUITECT indicou executar `bash deploy/subir.sh --v1` no clone
`/home/didasko-deploy/homolog-v1`, na branch `feature/DEM-202610-005-landing`,
e confirmou neste atendimento a execução do SSH. Escopo: homologação da landing.
O workflow de produção por tag/main não atende à publicação desta branch em
homologação; executado o script específico indicado pelo ARQUITECT.

## Comandos e resultados

1. `ssh -o StrictHostKeyChecking=yes -o ConnectTimeout=15 didasko-vps`:
   a tentativa no ambiente restrito não chegou à autenticação. A conexão com
   acesso de rede ampliado entrou como `didasko-deploy`, sem solicitar senha.
2. `cd /home/didasko-deploy/homolog-v1 && git branch --show-current && git rev-parse HEAD && git status --short`:
   branch `feature/DEM-202610-005-marco1`, hash
   `3d289349a197a76b05496eb8e3a7601455285266`, checkout limpo.
3. `git fetch origin feature/DEM-202610-005-landing`: sucesso. O primeiro
   `git switch feature/DEM-202610-005-landing` falhou com `invalid reference`
   porque o fetch não criou a referência local.
4. `git switch -c feature/DEM-202610-005-landing FETCH_HEAD && git rev-parse HEAD && git status --short && git --no-pager diff 3d28934 -- deploy/subir.sh`:
   branch criada no hash `f9aa301a4a4a44745b787746d7deea1cda860df3`, checkout
   limpo; diferença do script conferida antes da execução.
5. `bash deploy/subir.sh --v1`: concluiu e devolveu o prompt sem erro.
   Saídas relevantes:
   - banco `didasko_v1` pronto;
   - `app-v1` recriada e `landing` criada;
   - `landing sem DATABASE_URL`;
   - `banco ja tem 5 usuarios — pulando o seed`;
   - primeira tentativa HTTP: login/raiz/homenagens 502 durante inicialização;
   - tentativa seguinte: `/login`, `/` e `/homenagens` responderam 200.
6. Diagnóstico somente leitura:
   `sudo -n docker ps --format '{{.Names}} {{.Status}}'`;
   `sudo -n docker inspect --format '{{.Name}} {{.State.StartedAt}}' $(sudo -n docker ps -q --filter ancestor=traefik)`;
   `sudo -n docker inspect --format '{{json .NetworkSettings.Networks}}' didasko_v1_landing`.
   Traefik iniciado em `2026-10-18T17:27:43.522467189Z` (não reiniciado);
   aplicação de produção com dois dias de execução; Postgres da v1 saudável,
   com 25 horas de execução. Landing ligada somente à rede de borda
   `deploy_didasko`, sem a rede interna do banco.
7. Verificação HTTPS externa a partir da estação, com `curl.exe --silent
   --show-error --output NUL --write-out ... --max-time 15`, para cada URL:
   - `https://homolog.didasko.app.br/`: **200**;
   - `https://homolog.didasko.app.br/homenagens`: **200**;
   - `https://homolog.didasko.app.br/login`: **200**;
   - `https://didasko.app.br/`: **200**.

## Próximo gate

Landing disponível para validação visual do ARQUITECT e posterior EVAL conforme
o despacho. Não houve publicação em produção, migração, seed ou reinício do Traefik.
