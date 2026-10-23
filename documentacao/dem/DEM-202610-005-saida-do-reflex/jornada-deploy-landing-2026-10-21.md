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

## Fix do parecer do EVAL — commit a703389 (2026-10-22)

O ARQUITECT despachou a publicação do `a703389` (o fix dos dois bloqueios do
EVAL: o contraste do `.botao--primario` e a remoção do placeholder do
contato). Antes de publicar, disparado o CI manualmente (mesmo motivo do
`02eff4a`: a branch só recebe `workflow_dispatch`, nunca automático) — run
`39835747275`, **success**, head `a703389`.

No clone `/home/didasko-deploy/homolog-v1`: `git fetch` (`FETCH_HEAD` =
`a703389`), `git merge --ff-only` a partir de `02eff4a`, `subir.sh --v1` exit 0.
Verificado: `/`, `/homenagens`, `/login` **200**; Traefik e app de produção com
os mesmos horários de início (não reiniciados); placeholder com **0**
ocorrências no HTML; CSS novo (`landing.e8784ecbc0f4a9c1.css`) com o gradiente
escuro do botão; `Content-Type: image/webp` no logo.

## Fix do cartão de contato — commit 52495cd (2026-10-22)

Novo despacho: publicar o `52495cd` (escurece o `.contato__cartao` com o mesmo
par de pontas escuras do botão, mais os testes de contraste WCAG). CI
disparado manualmente de novo (mesma causa) — run `39856130366`, **success**,
head `52495cd`.

No clone de homologação: `git fetch` (`FETCH_HEAD` = `52495cd`), `git merge
--ff-only` a partir de `a703389` — trouxe também um comentário no
`docker-compose.v1-homolog.yml` (sem mudança funcional de rota/label).
`subir.sh --v1` exit 0. Verificado: `/`, `/homenagens`, `/login` **200**;
Traefik e app de produção com os mesmos horários de início (não reiniciados);
CSS novo (`landing.b7d755afbdfcf7fc.css`) com
`background: linear-gradient(125deg, #3B1470, #4B1E8C)` no `.contato__cartao`.

## Próximo gate (52495cd)

Nenhuma migração, seed ou alteração de produção, nem do Traefik. Pendente:
avisar o ARQUITECT de que o cartão e os assets novos estão no ar — validação
em **janela anônima**: o cartão do contato em **360 e 1440**, o contraste
**>= 4,5**.

## Link de homenagens escondido sem item ativo — commit 906a6dd (2026-10-23)

Relatório do DEVS: `906a6dd` esconde o menu, a seção `#homenagens` e o link do
rodapé do `index.html` quando `v1/landing.yaml` não tem nenhuma homenagem
`ativo: true` (hoje vazio). `/homenagens` continua acessível direto na
homologação (Path), fora do escopo deste commit. DoD do DEVS: 67+269 testes,
CI https://github.com/egarabini/gsi_ebd/actions/runs/39931396359 — reconferido
antes de publicar: `headSha` = `906a6dd`, `success`. `subir.sh --v1` não foi
rodado pelo DEVS (ADR-016).

No clone de homologação: `git fetch` (`FETCH_HEAD` = `906a6dd`), `git merge
--ff-only` a partir de `906a6dd` (sic, de `52495cd`) — trouxe também
`deploy/docker-compose.producao.yml` (4 linhas) e um ajuste no
`docker-compose.v1-homolog.yml`; conferido em `deploy/subir.sh` que o `--v1`
troca a variável `COMPOSE` para o arquivo da v1-homolog (linha 99) e nunca
aplica o compose de produção — o `docker-compose.producao.yml` alterado é só
a **proposta** de roteamento da v1 para produção, ainda sem autorização, sem
efeito neste deploy.

`subir.sh --v1` exit 0 (build sem cache desta vez — a digest da imagem
`python:3.12-slim` mudou; só mais lento, sem erro). Verificado: `/`,
`/homenagens`, `/login` **200**; produção `/` **200**; Traefik e app de
produção com os mesmos horários de início (não reiniciados); o HTML do `/`
com **zero** ocorrências de `href="/homenagens"`, `id="homenagens"` ou
"Homenagens" — confirma que o link some com o `landing.yaml` vazio.

## Próximo gate (906a6dd)

Nenhuma migração, seed ou alteração de produção/Traefik. Pendente: o EVAL
confere o HTML do `/` sem o link (conforme o relatório do DEVS); quando o
ARQUITECT preencher uma homenagem com `ativo: true` no `landing.yaml`, o link
deve voltar sozinho — não testado nesta rodada (o arquivo commitado continua
vazio).

## Head final do marco 2L — commit 2ca4610 (2026-10-23)

Despacho do ARQUITECT: publicar o `2ca4610` (o painel do menu encostado no
hover, o AA do rótulo e do passo da trilha). CI já informado no despacho —
reconferido antes de publicar: `headSha` = `2ca4610`, `success`, run
`39933115533`.

No clone de homologação: `git fetch` (`FETCH_HEAD` = `2ca4610`), `git merge
--ff-only` a partir de `906a6dd` — só CSS e testes, sem compose/infra.
`subir.sh --v1` exit 0. Verificado: `/`, `/homenagens`, `/login` **200**;
produção `/` **200**; Traefik e app de produção com os mesmos horários de
início (não reiniciados); link de homenagens continua ausente no `/`; CSS
novo (`landing.9175a181a37bc78b.css`) confirma os três pontos do fix:
`.menu { top: calc(100% - 13px); ... }` (o painel encostado — o `top: 100%`
deixava 13,7px de vão e o hover fechava ao atravessar), `.rotulo { color:
#9A3412; }` (o laranja original caía a 2,42–2,96:1) e o `.trilha__passo span`
com o mesmo gradiente de pontas escuras do botão/cartão.

## Próximo gate (2ca4610)

Nenhuma migração, seed ou alteração de produção/Traefik. Pendente: avisar o
ARQUITECT — validação em **janela anônima**: o painel encostado no hover, o
AA do rótulo, o link das homenagens ausente.
## O deploy do `2ca4610` — o head final do 2L (23/10)

O DEPLOY publicou o `2ca4610` na homologação: o CI `39933115533` reconferido (o `headSha` =
`2ca4610`, success); o fast-forward `906a6dd..2ca4610` (só CSS e testes); o `subir.sh --v1` exit 0.

**O CSS servido** (`landing.9175a181a37bc78b.css`):
- o `.menu { top: calc(100% - 13px) }` — o painel **encosta** no hover (o `top: 100%` deixava os
  13,7 px que fechavam o menu ao atravessar o cursor);
- o `.rotulo { color: #9A3412 }` — o laranja original caía a 2,42–2,96:1; agora o AA;
- o `.trilha__passo span` com o mesmo gradiente de pontas escuras do botão/cartão.

**As rotas**: o `/`, o `/homenagens` e o `/login` **200**; a produção `/` **200**; o Traefik e o app
da produção **não reiniciados**; **o link das homenagens continua ausente no `/`** (o yaml vazio).

**Para a validação do VISION** (a janela anônima): o painel encostado no hover, o AA do rótulo, o
link das homenagens ausente.
