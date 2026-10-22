# Jornada DEPLOY — landing em homologação — 2026-10-21

## Complemento do logo e alinhamento — 0c8f0ef

Após o ARQUITECT informar que a mudança visual não aparecia, foram identificadas
alterações adicionais no protótipo local e portadas no commit `0c8f0ef`.
CI https://github.com/egarabini/gsi_ebd/actions/runs/39698022094 **success**.
No clone da homologação, via SSH com host fixado: checkout limpo e branch
conferidos; `git fetch origin feature/DEM-202610-005-landing`, verificação de
`FETCH_HEAD` igual a `0c8f0ef`, `git merge --ff-only FETCH_HEAD`.
`COMPOSE_PROGRESS=plain BUILDKIT_PROGRESS=plain bash deploy/subir.sh --v1`
concluiu com exit 0: app e landing recriadas, landing sem `DATABASE_URL`,
cinco usuários existentes e seed pulado. Primeira tentativa HTTP 502 na
inicialização, seguinte com `/`, `/homenagens` e `/login` 200.

Verificação Chrome externa, ambas as páginas em 360 px: botão em x=22,4 px,
logo em x=78,4 px, largura de 45 px; URLs do CSS e logo com
`?v=20261021-menu2`. Capturas `homolog-logo2-landing-360.png` e
`homolog-logo2-homenagens-360.png` no diretório de capturas do DEVS.

## Reexecução solicitada pelo ARQUITECT — mesmo commit 74e3ee3

Pedido explícito para refazer o deploy no mesmo alvo. Conferências por SSH
(`BatchMode=yes`, `StrictHostKeyChecking=yes`, `ConnectTimeout=15`, alias
`didasko-vps`): checkout limpo na branch da landing; `git fetch origin
feature/DEM-202610-005-landing` retornou `FETCH_HEAD` igual ao `HEAD`,
`74e3ee3ec7ced47fbc99982e99aa05358ab04e57`. Não havia alteração posterior
publicada na branch; isso foi informado ao ARQUITECT. Run `39694772157`
reconferido: `completed`, `success`, mesmo hash.

Executado no clone `/home/didasko-deploy/homolog-v1`, após validar branch,
hash e checkout limpo: `COMPOSE_PROGRESS=plain BUILDKIT_PROGRESS=plain bash
deploy/subir.sh --v1`. Saída: app-v1 e landing recriadas, landing sem
`DATABASE_URL`, banco com cinco usuários (seed pulado); primeira tentativa
HTTP 502 durante inicialização, seguinte com as três rotas 200. Exit 0.

Verificação externa por `urllib.request.urlopen`: `/`, `/homenagens` e
`/login` da homologação 200; raiz de produção 200; CSS servido contém
`width: min(320px, 86vw)` e `.menu__botao:hover ~ .menu`.
`docker inspect` antes/depois confirmou horários inalterados de Traefik
(`2026-10-18T17:27:43.522467189Z`) e app de produção
(`2026-10-19T12:10:13.854096936Z`). Pronto para validação visual.

## Atualização do menu mobile — commit 74e3ee3

O ARQUITECT despachou explicitamente ao DEPLOY a publicação em homologação
do head `74e3ee3ec7ced47fbc99982e99aa05358ab04e57`, sem tocar na produção.

Comandos e resultados desta atualização:

1. `gh run view 39694772157 --repo egarabini/gsi_ebd --json headSha,status,conclusion`:
   `completed`, `success`, head exato `74e3ee3ec7ced47fbc99982e99aa05358ab04e57`.
2. SSH com `BatchMode=yes`, `StrictHostKeyChecking=yes`, `ConnectTimeout=15`,
   pelo alias `didasko-vps`, com acesso de rede ampliado. No diretório
   `/home/didasko-deploy/homolog-v1`, `git status --porcelain` vazio;
   branch da landing já existente, head anterior `f9aa301`.
3. `git fetch origin feature/DEM-202610-005-landing`; validação de `FETCH_HEAD`
   contra o hash autorizado; `git merge --ff-only FETCH_HEAD`; validação do
   `HEAD`: sucesso. Como a branch já existia e estava selecionada, foi
   atualizada por fast-forward, sem recriá-la.
4. `COMPOSE_PROGRESS=plain BUILDKIT_PROGRESS=plain bash deploy/subir.sh --v1`:
   exit 0. Postgres permaneceu em execução; `app-v1` e `landing` recriadas;
   `landing sem DATABASE_URL`; cinco usuários existentes, seed pulado.
   Primeira verificação deu 502 durante inicialização; seguinte deu **200**
   em `/`, `/homenagens` e `/login`.
5. `sudo -n docker inspect --format "{{.Name}}={{.State.StartedAt}}" didasko_traefik didasko_app`
   antes e depois: horários idênticos, respectivamente
   `2026-10-18T17:27:43.522467189Z` e `2026-10-19T12:10:13.854096936Z`.
   Traefik e aplicação de produção não foram reiniciados.
6. Verificação HTTPS externa via `urllib.request.urlopen`, timeout 15 s:
   três rotas da homologação **200**; input e label antes da marca nas duas
   páginas; CSS servido idêntico ao arquivo local do commit publicado,
   normalizando CRLF/LF. Raiz de produção também **200**.

Resultado: menu corrigido publicado em homologação; pronto para validação
visual do ARQUITECT. Nenhuma migração, seed ou alteração de produção.

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

## Cache versionado — commit 02eff4a (2026-10-22)

O ARQUITECT despachou ao DEPLOY a publicação do `02eff4a` (o porte do cache
versionado: HTML `no-cache`/`ETag`, CSS/WebP com hash no nome e cache longo
`immutable`), alvo `/home/didasko-deploy/homolog-v1`, branch
`feature/DEM-202610-005-landing`, informando o PR #8 e "o CI verde".

**Divergência encontrada antes de executar.** `gh` não estava no `PATH` desta
sessão (localizado depois em `C:\Program Files\GitHub CLI\gh.exe`, já
autenticado como `egarabini`, escopo `workflow`). Com a API pública do GitHub
confirmei `FETCH_HEAD` = `02eff4a` e o PR #8 aberto com esse head, mas **não
havia nenhum run de CI para esse commit** — nem concluído, nem em andamento —
mesmo após 15 minutos de espera (monitorado). Diagnóstico: `ci.yml` só dispara
automaticamente em `push`/`pull_request` para `develop`/`main`; nesta branch
(PR base `feature/DEM-202610-005-marco1`, não `develop`/`main`), todos os runs
anteriores do CI (`a753222`, `0c8f0ef`, `74e3ee3`, `f9aa301`) foram
`workflow_dispatch` manual. Para `02eff4a` isso ainda não havia sido feito —
não era demora, era ausência de disparo.

Registrei a divergência e devolvi a decisão ao ARQUITECT (AGENTS.md: "dúvida
antes de executar"). Autorizado a disparar o CI manualmente
(`gh workflow run CI --repo egarabini/gsi_ebd --ref
feature/DEM-202610-005-landing`, bloqueado uma vez pelo classificador de modo
automático por afetar recurso compartilhado, reautorizado em seguida). Run
`39771652866`, head `02eff4a`, monitorado até `completed`/`success`.

Com o gate de CI verde satisfeito, executado no clone
`/home/didasko-deploy/homolog-v1` via SSH (`didasko-vps`, `BatchMode=yes`,
`StrictHostKeyChecking=yes`, `ConnectTimeout=15`):

1. Estado inicial: branch `feature/DEM-202610-005-landing`, `HEAD` em
   `a753222`, checkout limpo.
2. `git fetch origin feature/DEM-202610-005-landing`: `FETCH_HEAD` =
   `02eff4a0b98b702aabdb975c25fe00ef81542252`.
3. `git merge --ff-only FETCH_HEAD`: fast-forward `a753222..02eff4a`, `HEAD`
   confirmado em `02eff4a`.
4. `COMPOSE_PROGRESS=plain BUILDKIT_PROGRESS=plain bash deploy/subir.sh --v1`:
   exit 0. `RUN python -m v1.landing_assets` gerou os assets com hash no nome
   (`landing.fbc3428c9a2a7e6a.css`, `logo-88.cb547affebd31652.webp`,
   `logo-440.9200e96557734c59.webp`, `logo-880.52025a27ad048e67.webp`);
   `app-v1` e `landing` recriadas; `landing sem DATABASE_URL`; banco já com
   cinco usuários — seed pulado; primeira tentativa HTTP 502 durante
   inicialização, seguinte com as três rotas 200.

**Verificação pós-deploy:**

- `sudo -n docker inspect --format '{{.Name}}={{.State.StartedAt}}'
  didasko_traefik didasko_app`: horários **inalterados**
  (`2026-10-18T17:27:43.522467189Z` e `2026-10-19T12:10:13.854096936Z`) — nem
  Traefik nem a app de produção foram reiniciados;
- HTTP externo (`curl`, estação local): `https://homolog.didasko.app.br/`,
  `/homenagens` e `/login` **200**; `https://didasko.app.br/` **200**;
- HTML servido pela homologação referencia exatamente os assets com hash
  gerados no build acima (CSS e os três tamanhos do logo) — a URL do CSS no
  ar é `landing.fbc3428c9a2a7e6a.css`.

## Próximo gate (02eff4a)

Nenhuma migração, seed ou alteração de produção. Pendente: avisar o ARQUITECT
de que a URL do CSS versionada (`landing.fbc3428c9a2a7e6a.css`) está no ar —
validação em **janela anônima** (sem `Ctrl+F5`): o logo recortado, o menu, o
celular, os textos de obra/estudo.
