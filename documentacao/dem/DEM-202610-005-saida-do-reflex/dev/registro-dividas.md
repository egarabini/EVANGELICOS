# O registro de dívidas — o estado em 23/10

> Atualizado após o marco 2L (a landing em produção). **As decisões são do ARQUITECT**; as
> recomendações do AUXILIAR/PLANNER não o são.

## Fechadas pela v1 (o marco 1 + o 2L)

| A dívida | Como fechou |
|---|---|
| **D-05** | o marco 1 (a v1 base) entregou |
| **D-08 / D-10 / D-11** | fechadas na v1 (a verificação do marco 1) |
| **os débitos de infra do 2L** | o cache versionado, o AA, o link condicional — **com testes** |

## Abertas — dependem do **ARQUITECT**

| A dívida | O que é |
|---|---|
| **D-01** | a **rotação das contas** e da **senha `senha123` do admin de produção** |
| **D-02** | a **chave operacional** (o acesso à VPS) |
| **D-06** | o **pin da versão do Traefik** (hoje `latest`) |
| **os dados reais** | os **depoimentos reais** e os **dados reais de contato** — o `landing.yaml` está **vazio de propósito** |

## Abertas — do PLANNER/DEVS (a próxima frente)

| A dívida | O que é |
|---|---|
| **D-09** | (o registro do marco 1) |
| **as obras (a DEM-011, fatia 2)** | o PR #5 (rascunho) **duplica o esqueleto do marco 1** — **recriar a branch a partir da `develop`** (o `despacho-obras-fatia2.md`) |
| **o marco 1b (o Zitadel)** | o design/o plano/o briefing prontos; **só conferir** (o `marco-1b-pendencias.md`); a ordem: **as obras antes** |

## As novas — registradas em 23/10

### 1. O clone de produção divergente — **COM PRAZO**

- **O quê**: o clone da VPS no **HEAD destacado da `v0.1.0`** com os **3 caminhos da v1** + o
  **`deploy/docker-compose.producao.yml`** (os rótulos da etapa b) como **alterações não commitadas**;
- **O prazo**: **antes de qualquer outro deploy em produção**;
- **A resolução**: a **tag nova** (a `v0.1.1`, a decisão do ARQUITECT) + o **checkout** no clone +
  **sem commit na VPS** (o `despacho-divida-clone.md`);
- **A garantia**: a **tag `v0.1.0` intacta**; os **6 contêineres com o `StartedAt` inalterado**; o
  Traefik **não** reinicia.

### 2. A landing lerá o banco da v1 (depois da virada)

- **O quê**: os **depoimentos** e a **configuração do site** passam a ser **entidades do `didasko_v1`**,
  **editáveis pelo Admin**;
- **O porquê**: hoje a landing lê o **`landing.yaml`** versionado (o sem-banco, a opção A); depois da
  virada, o Admin edita **pela interface**, sem PR;
- **O cuidado**: a landing **continua sem** o `DATABASE_URL` **até** a virada — a decisão do
  ARQUITECT.

### 3. O `/homenagens` fora da produção

- **O quê**: a página fica **fora** da produção; o **link só aparece** quando houver **homenagens**
  no `landing.yaml` (o `homenagens: []` vazio);
- **A decidir**: quando houver conteúdo real (o consentimento registrado), o `/homenagens` entra na
  proposta de produção **naquele momento** — não antes.

## A nota do método

**Cada dívida tem um dono e um critério de fechamento.** As que dependem do ARQUITECT estão **paradas
nele** — e é por isso que elas **não** devem ser "resolvidas" por conveniência: o D-01 (a rotação) é
uma **decisão de segurança**, o D-06 (o pin) é uma **decisão de estabilidade**, e os **dados reais**
são uma **decisão editorial**.
## As decisões do ARQUITECT (23/10) — o registro atualizado

- **D-01** (a rotação das contas e da senha `senha123` do admin da v0): **EM EXECUÇÃO PELO
  ARQUITECT — AGORA**. Não entra no 1b; fica neste registro como **em execução**, até a confirmação
  dele.
- **A ORDEM**: **as obras antes do 1b** (a decisão do ARQUITECT).
- **A tag `v0.1.1`**: **tratada como DEPLOY PLANEJADO** — o `v*` dispara o `deploy.yml` (o backup do
  banco, o `checkout --force` da tag, o `subir.sh`, a conferência HTTP). O `checkout --force` resolve
  a divergência do clone; a garantia deixa de ser o "`StartedAt` inalterado" (o `subir.sh` roda o
  `$COMPOSE up -d --build` — o compose inteiro) e passa a ser **"a v0 e a landing no ar, conferidas
  pelos códigos da linha de base"**. O despacho reescrito: o `dev/despacho-divida-clone.md`.
- **O PLANNER leu o `subir.sh`/o `deploy-entry`** e confirmou: o deploy sem `--v1` sobe o compose
  inteiro e **mantém o `didasko_landing`** — **a condição está satisfeita**, não é preciso mudar o
  script de entrada.
- **Nenhum despacho do clone antes do merge do PR #8** (o ARQUITECT o mescla) **e da leitura do
  `subir.sh`** (feita). Os despachos das obras seguem **depois do merge do #8**, na branch recriada a
  partir da `develop`.
- **O PR #8**: **rebaseado na `develop`** (o `f8ffe0a`, os 71 testes) — **o ARQUITECT o mescla**.
## As novas de 23/10 (a tarde)

### 4. O CI não aparece no PR empilhado (a proteção exige o check)

- **O quê**: o check `testes (pytest)` não aparece nos PRs cuja **base é uma `feature/*`** (o
  `pull_request: branches: [develop, main]` do `ci.yml` não dispara); a proteção da develop **exige**
  o check → o merge **exige o `--admin`** (foi o caso do #8);
- **A correção proposta** (a decisão do ARQUITECT): o `pull_request` **sem o `branches`** (ou o
  `branches: [develop, main, "feature/**"]`) — o `dev/despacho-ci-protecao.md`;
- **O prazo**: antes dos próximos PRs.

### 5. O PR #8 mesclado — a tag `v0.1.1` preparada

- **O merge**: o `5c0bc3e` (23/10, 16:32 UTC), com o `--admin` (a causa acima);
- **A tag `v0.1.1`**: **criada localmente** no `5c0bc3e` (a anotada, a mensagem "a landing da v1 na
  producao (o marco 2L)");
- **O push da tag e a aprovação do `environment: producao`**: **do ARQUITECT**;
- **A volta atrás**: o deploy da `v0.1.0` (`git checkout --force refs/tags/v0.1.0` + o `subir.sh`);
- **Nada em produção** sem o aceite do ARQUITECT.
### 6. O rollback manual (23/10)

- **o quê**: o rollback da `v0.1.1` foi **manual, fora do pipeline** (o `docker rm` do
  `didasko_landing` + o `checkout --force` da `v0.1.0` + o `subir.sh`); o clone da produção está de
  novo no **HEAD destacado da `v0.1.0`**;
- **a janela de indisponibilidade do app**: o `app` foi **recriado duas vezes** (a etapa a/b + o
  rollback) — a janela real, a registrar na jornada do DEPLOY;
- **a proposta da correção**: o `--remove-orphans` no `subir.sh`/`deploy-entry` (o
  `dev/despacho-subir-remove-orphans.md`) — **infraestrutura, só com a autorização do ARQUITECT**.

### 7. A produção na `v0.1.0` até a decisão do ARQUITECT

- **nenhum deploy novo da `v0.1.1`** sem a ordem dele;
- **antes** dele explicar **por que a produção voltou à `v0.1.0`** e **o que (se algo) precisa mudar**
  antes de subir de novo;
- a **tag `v0.1.1`** segue no repositório (a referência de "a landing em produção"), mas **a
  produção fica na `v0.1.0`** até a decisão.
### 8. O "por quê" do rollback — uma LACUNA no registro (23/10)

**O registro tem o QUANDO e o COMO, não o PORQUÊ:**

- **o quando**: o deploy da `v0.1.1` correu de 16:36:42Z a 16:43:17Z; o rollback veio ~5 min depois
  (~16:47);
- **o como**: o `docker stop/rm didasko_landing` + o `git checkout --force refs/tags/v0.1.0` + o
  `subir.sh --pular-import`;
- **o porquê**: **não está no registro**.

**O que o registro PROVA:**

- **o deploy da `v0.1.1` foi um SUCESSO** — o run `39988210363`, o job "publicar na VPS" =
  **`success`** (16:36:42→16:43:17); a landing **foi ao ar**;
- **o rollback NÃO foi a recuperação de uma falha técnica** — foi uma **DECISÃO**, tomada ~5 min
  depois de um deploy que funcionou.

**A decisão do ARQUITECT (a orientação 4)**: **antes de qualquer novo deploy da `v0.1.1`**, ele
**explica** por que a produção voltou à `v0.1.0` e o que (se algo) precisa mudar.

**A LACUNA a fechar**: o "porquê" precisa ser **registrado** (na jornada do DEPLOY ou neste registro)
**no momento em que for dito** — **um rollback sem motivo registrado é um rollback que ninguém
consegue repetir nem evitar**.
### 9. A hipótese do logo — DESCARTADA (a verificação de 23/10)

**A hipótese do ARQUITECT**: o rollback teria sido ocasionado pela **alteração do logo** que "não
funcionava em homologação".

**A verificação (o código, não a memória):**

- o CSS **dentro do merge `5c0bc3e`** (o commit da `v0.1.1`) tem o **`.hero__visual { display: none }`**
  dentro do `@media (max-width: 960px)` — **o fix do logo está na `v0.1.1`**;
- o **`67f0623`** (o commit original do fix) **não é ancestral** do `5c0bc3e` — ele foi **rebaseado**
  no **`5d82b0a`** (o mesmo conteúdo, o SHA novo); a **ancestralidade** não é o teste certo, o
  **conteúdo** é — e o conteúdo entrou;

**A conclusão**: **o logo NÃO foi a causa do rollback** — a `v0.1.1` **levou o fix**, e o deploy da
`v0.1.1` foi **`success`** (o run `39988210363`, "publicar na VPS"). **A produção subiu com o logo
correto.**

**A hipótese fica descartada**; **a causa do rollback continua sem registro** — o "porquê" é do
ARQUITECT (a orientação 4), e o registro espera por ele.
### 10. O CI (a opção A) — **FECHADO** (o PR #9, o `8ae1a3c`)

O DEVS implementou a **opção A** no **PR #9** (o commit **`8ae1a3c`**):

- o **`ci.yml`**: o **`pull_request:` sem o filtro de `branches`** — todo PR dispara o CI;
- o **`tests/test_ci.py`**: trava o contrato (se alguém reintroduzir o filtro, o teste quebra);
- **o push no PR #9 disparou o `pull_request` sozinho** — **sem o `workflow_dispatch`, sem o
  `--admin`**;
- o check **`testes (pytest)` verde no PR** (o run `40038703819`).

**A verificação**: o PR #9 mostra o check verde — **o problema do #8** (o merge com o `--admin`)
**não se repete**. **A dívida fecha.**
### 11. O `environment producao` **SEM aprovador** (a correção do AUXILIAR, 23/10)

**O fato**: o `environment producao` **NÃO tem aprovador** — é uma **dívida aceita até a v1**.
**Qualquer tag `v*` ou `workflow_dispatch` do `deploy.yml` executa na hora** (o deploy do
`40040835237` entrou direto, sem a parada de aprovação).

**A REGRA (registrada)**: **enviar a tag `v*` = autorizar o deploy.** O **push da tag é o ato** — o
pipeline **não pergunta**. **A decisão de "subir" é no momento do push**, não numa aprovação
posterior.

**A dívida a decidir (o ARQUITECT)**: **recolocar o *required reviewer*** no `environment producao`
**antes de a v1 ter dados reais**. Até lá, **a autorização é por release aceito** (o ADR-016) — e a
**tag é o gatilho**.

**A consequência prática**: **não empurrar uma tag `v*` para "testar"** — cada push de tag é um
deploy em produção, com o `up -d --build` recriando o `app` da v0.
### 13. O seed dos alunos fake **não wired** ao `subir.sh` (a dívida, 23/10)

- **o quê**: o `v1/seed_homolog_estudo.py` **não é chamado** pelo `subir.sh` (0 refs); a homologação
  sobe **sem** os alunos fake;
- **a decisão (o ARQUITECT)**: rodar o seed **UMA VEZ**, à mão, no **despacho do deploy** da
  homologação (com o `DIDASKO_AMBIENTE=homologacao`) — **sem isso a validação visual vê as telas
  vazias**;
- **a dívida**: decidir depois se vira **passo do script** (a decisão de infraestrutura é do
  ARQUITECT);
- **a regra**: **o seed NUNCA roda em produção** — o `recusar_producao` é o guard (o
  `DIDASKO_AMBIENTE=homologacao` obrigatório).

### 14. As obras NÃO vão à produção (a decisão do ARQUITECT, 23/10)

- **nada das obras vai à produção** (o seed nunca roda em produção);
- **o 1b (o Zitadel)** continua **depois da validação visual** das obras, e exige a **autorização de
  infraestrutura** do ARQUITECT (o Zitadel em produção) e a **avaliação da licença AGPL**.

### 15. O seed rodou, mas sem obra liberada → sem estudo/assignment (24/10)

- **o quê**: o `subir.sh --v1` do `d927467` (a `develop` pós-merge do #9, fatia 2) subiu limpo
  (200 em `/`, `/homenagens`, `/login`); o `v1.seed_homolog_estudo` rodou **uma vez**, exit 0, e
  criou os **2 alunos fake** (`aluno.fake.a`/`b@homolog.didasko.local`, confirmados no `psql`) —
  mas `studyassignment` ficou com **0 linhas**;
- **a causa**: `popular()` chama `_estudo_da_obra_liberada()`, que procura uma `Obra` com
  `versao_liberada_id` preenchido; **não existe nenhuma** em `didasko_v1`
  (`select count(*), count(versao_liberada_id) from obra` → `0 / 0`). Sem obra liberada, a função
  retorna `None` e `popular()` **sai silenciosamente** (fail-open) — sem estudo, sem assignment,
  sem erro, sem aviso no stdout;
- **a consequência**: o `/aluno` do `aluno.fake.a` mostra a lista **vazia** até existir uma obra
  liberada em homologação — não é falha do seed nem do deploy, é pré-condição que ninguém havia
  atendido ainda;
- **o que NÃO fiz**: não testei o login HTTP do `/aluno` (exige o `SEED_PASSWORD` em texto plano,
  que não li — ADR-015); não fabriquei uma obra/versão liberada no banco para contornar (decisão de
  conteúdo, não do DEPLOY);
- **a decisão do ARQUITECT**: seguir assim, registrar o gap e fechar a tarefa de deploy — a
  liberação de uma obra em homologação (pela aplicação) e a re-execução do seed (idempotente para
  os alunos, mas vai preencher o estudo/assignment uma vez liberada) ficam para depois.
### 15. O seed dos alunos fake é **fail-open** (o `studyassignment` com 0 linhas) — 24/10

- **o quê**: o deploy da homologação (o `d927467`) rodou o seed **uma vez** (exit 0; os **2 alunos
  fake** no banco), mas o **`studyassignment` ficou com 0 linhas** — o seed é **fail-open**: sem
  **nenhuma `Obra` com o `versao_liberada_id`** no `didasko_v1` (o **0/0**), ele **cria só os
  alunos** e **sai em silêncio**, sem o estudo nem o assignment;
- **a decisão (o ARQUITECT)**: **seguir assim, registrar e fechar** — a **liberação de uma obra em
  homologação** e a **re-execução do seed** ficam **para depois**;
- **as dívidas internas**: (a) o seed **deveria falhar** (não sair em silêncio) sem a obra liberada;
  (b) a obra de homologação precisa ser **liberada** (o fluxo do Admin/Revisor) antes do seed; (c) o
  **login HTTP do `/aluno` não foi testado** (o `SEED_PASSWORD` em texto plano — o DEPLOY não o leu,
  corretamente);
- **a consequência**: a **validação visual** das telas do aluno fake **vê as telas vazias** até a
  obra ser liberada e o seed re-executado — **o gap é de conteúdo, não de código**.
### 16. A passada técnica do AUXILIAR (24/10) — a homologação sem credencial

**O resultado (a homologação):**

- o `/admin/obras`, o `/admin/obras/nova`, o `/revisor/obras`, o `/obras`, o `/aluno`, o
  `/aluno/licao/1`: **401** para o **anônimo** (a autenticação);
- o `POST /admin/obras` **sem sessão/CSRF**: **403** (o CSRF);
- o `/openapi.json` e o `/docs`: **404** (o **não exposto**);
- o `/login`: **200**;
- a **produção** (`didasko.app.br`): o `/admin/obras`, o `/revisor/obras`, o `/obras`: **404** —
  **nada das obras vazou**.

**NÃO verificado**: a **matriz de papéis com login real** (Admin/Revisor/aluno) — **sem a
credencial**; a cobertura atual = os testes (a matriz de 15 células, o EVAL PASS). **Fica para a
validação visual do ARQUITECT.**

**Os pedidos do AUXILIAR** (a #17):

1. o **seed fail-closed** (o `dev/despacho-seed-fail-closed.md`) — o seed **falha** com mensagem clara
   sem a obra liberada;
2. **depois** da validação do **fluxo de liberação** pelo ARQUITECT na homologação, **usar a obra
   criada por ele** para liberar e **re-executar o seed** dos alunos fake.
### 15-atualizada — o seed **fail-closed** (o PR #10, o `00f844b`) — a (a) FECHOU

- **o fix**: o `_exigir_obra_liberada` no `v1/seed_homolog_estudo.py` — o
  `select(Obra).where(Obra.versao_liberada_id.is_not(None)).first()`; se `None` → o **`RuntimeError`**
  com a mensagem clara ("o seed exige ao menos uma Obra com `versao_liberada_id`; libere a obra no
  fluxo do Admin/Revisor");
- **a ordem**: o `recusar_producao` → o `DIDASKO_AMBIENTE` → o `DATABASE_URL` → o `SEED_PASSWORD` → **a
  obra liberada** → os alunos (o `recusar_producao` **primeiro**, como o EVAL exigiu);
- **o teste**: o `test_popular_recusa_sem_obra_liberada` (o `pytest.raises`); a suíte local **139**;
  o CI `40061955876` **success**;
- **a (a) da dívida 15 FECHOU**; as **(b)** (a liberação da obra em homologação) e **(c)** (o login
  HTTP do `/aluno`) **ficam** — dependem da obra criada/liberada pelo ARQUITECT.
