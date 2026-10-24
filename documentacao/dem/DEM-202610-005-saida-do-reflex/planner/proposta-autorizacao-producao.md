# A proposta de autorização da produção — a landing (o marco 2L)

> **A revisão do ARQUITECT (23/10)** — os 7 pontos incorporados. **O ato é do ARQUITECT; nada é
> executado sem ele.**

## 1. O roteador (o Traefik) — os rótulos

O serviço da landing (a v1) entra com um roteador próprio, na **mesma rede de borda** da v0, com a
**prioridade explícita** maior:

```yaml
- traefik.enable=true
- traefik.docker.network=deploy_didasko
- traefik.http.routers.landing-prod.rule=Host(`didasko.app.br`) && (Path(`/`) || PathPrefix(`/static/landing/`))
- traefik.http.routers.landing-prod.priority=200
- traefik.http.routers.landing-prod.entrypoints=websecure
- traefik.http.routers.landing-prod.tls=true
```

**O `tls=true` só — sem o `certresolver`** (a revisão, o ponto 5): o certificado do `didasko.app.br`
**já existe** (o Traefik o serve pelos rótulos da v0); o `tls=true` usa o certificado existente, e
**nenhum pedido novo ao Let's Encrypt é feito**.

**A regra**: o `Path(/)` é **exato** (o `/login` não é o `/`) e o `PathPrefix(/static/landing/)` só
alcança os assets da landing. O `/login`, o `/homenagens`, o `/aluno` e o resto **não casam** com a
regra nova → **continuam na v0**, pelo roteador dela.

## 2. Os limites (os números)

- **A memória**: **`mem_limit: 512m`** (512 MiB);
- **A CPU**: **`cpus: 0.50`** (meio vCPU);
- **A rede**: **só a `deploy_didasko`** (a borda); sem a `interna`; **sem `DATABASE_URL`**.

São os mesmos valores da homologação (o §2 do compose `v1-homolog.yml`), e o serviço é estático (só
serve o HTML/CSS/WebP).

## 3. Como o contêiner chega à produção

- **O stack**: o `deploy/app-v1.Dockerfile` (o `python:3.12-slim`), o comando
  `python -m uvicorn v1.landing:create_app --factory`;
- **O projeto do Compose**: o **`deploy`** (o mesmo da v0), com o serviço **`landing`** — o
  `container_name: didasko_v1_landing`;
- **A tag**: o `v*` (o SemVer) **pelo `deploy.yml`** (o GitHub Actions) — o pipeline que já publica a
  v0; **o mesmo processo**, o serviço a mais;
- **Os 5 contêineres da v0 NÃO são recriados**: o deploy sobe **só o serviço `landing`** (o
  `--force-recreate --no-deps landing`) — o `didasko_app`, o `didasko_traefik`, o `didasko_postgres`,
  o `didasko_chromadb` e o `didasko_ollama` **ficam com o `StartedAt` inalterado**.

## 4. As duas etapas (a subida)

**(a) O contêiner SEM os rótulos de roteador** — a subida só do serviço, sem o Traefik o enxergar
(o `traefik.enable=false` na primeira subida); o teste **por dentro** da VPS:
- o `docker exec didasko_v1_landing curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/` →
  **200**, o HTML com o `<title>` da landing;
- o `/homenagens` → **200** (o layout, a página sem o link);
- o contêiner sem o `DATABASE_URL` e só na borda.

**(b) Só então os rótulos** — o **ato do ARQUITECT**: a subida com os rótulos do §1. Depois:
- a **base** do §5 (o antes × o depois);
- o **teste** do `/login` (o 307), do `/homenagens` (o 307) e do app da v0;
- o `StartedAt` dos 5 contêineres da v0 **inalterado**.

**A volta atrás** = remover os rótulos (o `traefik.enable=false` ou o down **do serviço** da landing)
e recriar **só** o serviço — **o Traefik nunca reinicia**; ele relê os rótulos sozinho.

## 5. A base (os códigos de hoje — a produção não foi tocada)

| A rota | Hoje (a v0) | Depois (o esperado) |
|---|---|---|
| `/` | **200** | **200** (a landing da v1) |
| `/login` | **307** | **307** (a v0; o redirect) |
| `/homenagens` | **307** | **307** (a v0) |

**A regra do teste (a revisão, o ponto 1)**: **registrar os códigos de hoje ANTES** e comparar os
**mesmos códigos DEPOIS** — o `/` deve mudar de **origem** (a v0 → a v1), **não** de código; o
`/login` e o `/homenagens` devem **continuar iguais**.

## 6. Os rótulos reais do roteador da v0 (a prova do ponto 6)

```
traefik.http.routers.didasko.entrypoints = websecure
traefik.http.routers.didasko.rule = Host(`didasko.app.br`) || Host(`www.didasko.app.br`)
traefik.http.routers.didasko.tls.certresolver = le
```

**Nenhum `priority`** — o roteador da v0 usa a **prioridade padrão** (calculada pelo Traefik pelo
tamanho da regra, não explícita). O `priority=200` da landing **vence** qualquer rota da v0 no `/`.
**A verificação antes de executar**: `docker inspect didasko_app` para conferir que **nenhum** rótulo
da v0 tem a `priority` > 200.

## 7. A ordem (a revisão, o ponto 7)

1. **O DEPLOY** roda o `subir.sh --v1` **com o head `67f0623`** (o fix do hero/o menu a zero/o YAML
   limpo/o `.gitignore`), na homologação;
2. **O ARQUITECT valida em janela anônima** (o 360 sem o logo do hero, o painel encostado, o rótulo
   AA, o link das homenagens ausente);
3. **A proposta** (este documento) — o **ato do ARQUITECT**;
4. **A etapa (a)** — o contêiner sem os rótulos, o teste por dentro;
5. **A etapa (b)** — os rótulos (o ato), o teste do §5 (a base × o depois).

## O que **não** muda

- o **`/login`** e o app da v0 — o roteador novo não os toca;
- o **`/homenagens`** — a v0 tem a própria (a v1 não entra);
- o **certificado** — o `tls=true` usa o existente, **sem** o let's Encrypt novo;
- o **Traefik** (sem restart) e o **domínio** (o mesmo `didasko.app.br`);
- os **5 contêineres da v0** (o `StartedAt` inalterado).
## O aceite do ARQUITECT — 23/10

**O ARQUITECT deu o ACEITE da proposta de autorização da produção** (a revisão dos 7 pontos).

**A execução (a ordem do ARQUITECT):**

1. **A etapa (a)** — o contêiner da landing sobe na produção **SEM os rótulos de roteador** (o
   `traefik.enable=false`) e é **testado por dentro** (o `docker exec curl` → o `/` 200, o HTML da
   landing; o `/homenagens` 200; o contêiner sem o `DATABASE_URL` e só na borda); os **5 contêineres
   da v0 não são recriados**;
2. **A etapa (b)** — **o ato do ARQUITECT**: os rótulos do §1 (o `tls=true` **sem** o
   `certresolver`; o `priority=200`); o teste do **§5** (a base × o depois);
3. **A volta atrás** = remover os rótulos e recriar **só** o serviço da landing; **o Traefik NUNCA
   reinicia**.

**O que NÃO muda**: o `/login` (o 307) e o app da v0; o `/homenagens` (o 307); o certificado (o
`tls=true` usa o existente); os **5 contêineres da v0** (o `StartedAt` inalterado).
## A etapa (a) — EXECUTADA (23/10)

O DEVS subiu o serviço `landing` no `deploy/docker-compose.producao.yml` (**o commit `8805705`**, o CI
verde) com o **`traefik.enable=false`** e **nenhum outro rótulo** — o Traefik **não o enxerga**. O up
isolado, com o `--no-deps landing`.

**Verificado:**
- `didasko_app`, `didasko_postgres`, `didasko_chromadb`, `didasko_ollama`, `didasko_traefik`: o
  **`StartedAt` idêntico** antes/depois — **nenhum recriado**;
- o **`didasko_landing`**: criado, rodando, o `StartedAt` novo;
- **por dentro** (sem o `curl` na imagem — o Python do container): o `/` → **200** com o título da
  landing; o `/homenagens` → **200**;
- **sem o `DATABASE_URL`**; só na rede **`deploy_didasko`** (a única da produção — não há o split
  interna/borda como na homologação).

**A divergência que o DEVS encontrou e resolveu com o ARQUITECT antes de agir**: o clone de produção
estava no **HEAD destacado da tag `v0.1.0`** (sem a árvore `v1/`). Ele fez o **checkout cirúrgico dos
3 caminhos** necessários, mantendo o clone identificado como `v0.1.0`. **O estado deixado**: o clone
de produção fica com esses 3 caminhos **modificados na árvore de trabalho** (não comitados) sobre a
tag — **esperado** até a etapa (b) ou uma limpeza.

**A etapa (b)** — os rótulos de rota — é **ato separado do ARQUITECT**.
## A decisão da etapa (b) — **AUTORIZADA** com 6 condições (23/10)

**1. A prova de origem do `/` NÃO é o `<title>`** — a v0 tem o **mesmo** título ("Didasko — Estudos
Bíblicos Dirigidos"). A prova é:
- (a) o HTML do `/` contém **`/static/landing/landing.<hash>.css`**;
- (b) esse CSS responde **200** com o **`cache-control: immutable`**;
- (c) o HTML da v0 usa **`/assets/...`** — conferir um desses assets respondendo **200 depois**, para
  provar que **o resto continua na v0**.

**2. Repetir a linha de base do `/` várias vezes antes do ato** (o ARQUITECT observou um **200 de 43
bytes, `Server: granian`**, que pode ser artefato). **A base atual**: o `/` **200**; o `/login`, o
`/homenagens`, o `/aluno`, o `/admin` **307**; o `/static/landing/x.css` **404**.

**3. A DÍVIDA COM PRAZO** — **"resolver antes de qualquer outro deploy em produção"**: o clone de
produção no **HEAD destacado da `v0.1.0`** com os **3 caminhos da v1** e os **rótulos novos** como
alterações **não commitadas**. Resolver com **commit na branch certa**, **NUNCA** com o `git add -A`.

**4. O comando exato da volta atrás** — **escrito e à mão** (o remover os rótulos + o recriar só o
serviço da landing) e, de preferência, **validado antes do ato**.

**5. O passo 1 é OBRIGATÓRIO** — o `docker inspect didasko_app`: **nenhum rótulo com `priority`
explícita > 200**. Se houver, **PARAR** e devolver ao ARQUITECT.

**6. Manter**: o `priority=200`, o `Path(/)` **exato**, **sem o `certresolver`**, o
`traefik.docker.network`, o `--force-recreate --no-deps`, **NUNCA reiniciar o Traefik**, a **v0
intocada** (o `StartedAt` dos 5 contêineres inalterado).
## A etapa (b) — EXECUTADA (23/10) — **a landing NO AR (a raiz de `didasko.app.br`)**

**O passo 0 (a base, 5x)**: o `/` **200**, **45299 bytes estável** (o "43 bytes" do despacho **não
reproduzido** — é a página real); o `/login`, o `/homenagens`, o `/aluno`, o `/admin` → **307**; o
`/static/landing/x.css` → **404**.

**O passo 1 (a parada obrigatória)**: o `didasko_app` **sem nenhum `priority` explícito** — a condição
satisfeita, seguiu.

**O passo 2**: os 6 rótulos (**o commit `5d625ed`**). **O CI falhou na primeira tentativa** — o
comentário "seguem na v0" → "seguem no roteador da v0" quebrou um teste que cobra a **frase literal**
no arquivo. O **`c6d5d86`** corrigiu, o CI verde — **nada tocou a VPS enquanto estava vermelho**.

**O passo 3**: o `--force-recreate --no-deps landing`; **o Traefik NÃO reiniciado**.

**O passo 4 (a prova de origem — não o `<title>`)**:
- o `/` contém **`/static/landing/landing.dfa7e29213827a3a.css`**;
- esse CSS → **200** com o **`Cache-Control: public, max-age=31536000, immutable`**;
- um asset da v0 (**`/assets/manifest-8ba4429c.js`**) → **200** — **o resto continua na v0**;
- o `/login`, o `/homenagens`, o `/aluno`, o `/admin` → **307**, inalterados.

**O passo 5**: os **5 `StartedAt` da v0 idênticos** ao início da sessão (nenhum tocado em **nenhuma**
das duas etapas); o `didasko_landing` com o `StartedAt` novo do force-recreate.

**A volta atrás** (escrita e pronta, **não usada**):

```bash
cd /home/didasko-deploy/didasko
git checkout 8805705 -- deploy/docker-compose.producao.yml
sudo -n docker compose --env-file .env -f deploy/docker-compose.producao.yml up -d --force-recreate --no-deps landing
```

**A raiz pública de `didasko.app.br` já serve a landing da v1.**

## A dívida com prazo — ABERTA (resolver antes de qualquer outro deploy em produção)

- **O que**: o clone de produção no **HEAD destacado da `v0.1.0`** com os **3 caminhos da v1** e os
  **rótulos novos** como alterações **não commitadas**;
- **Como resolver**: um **commit na branch certa** (a da landing ou uma branch de produção dedicada) —
  **NUNCA** o `git add -A`;
- **Até lá**: **nenhum outro deploy em produção** sem resolver.
## O rollback (23/10) — a produção de volta à `v0.1.0`

O DEPLOY rolou a produção para a **`v0.1.0`**:

1. **o `docker stop/rm didasko_landing`** — **a lacuna identificada antes de executar**: o
   `checkout --force` tira o `landing` do **arquivo do compose**, mas **sem o `--remove-orphans`** o
   contêiner **órfão continuaria no ar** com os rótulos do Traefik, **servindo o `/`** — o `docker rm`
   do contêiner foi o passo que faltava;
2. o **`git checkout --force refs/tags/v0.1.0`** (confirmado);
3. o **`bash deploy/subir.sh --pular-import`** (exit 0).

**Verificado:**
- o **`postgres`, o `chromadb`, o `ollama` e o `traefik`**: o `StartedAt` **idêntico ao de 18/10** —
  **nunca tocados hoje**, em **nenhuma** das três ações (a etapa a, a etapa b, o rollback);
- o **`app`**: recriado (esperado — voltou à imagem da `v0.1.0`);
- o **`didasko_landing`**: **não existe mais**, nem parado;
- o **`https://didasko.app.br/`**: **200**, **45299 bytes** (o tamanho original da v0), **sem o CSS da
  landing**.

**A produção está de volta EXATAMENTE ao estado anterior à landing.**

## A lição do rollback

**O rollback de um serviço novo exige o `docker rm` do contêiner (ou o `--remove-orphans`)**: o
`checkout --force` sozinho **NÃO derruba** o contêiner órfão — o compose **não o gerencia mais** (o
serviço saiu do arquivo), mas ele **continua rodando** com os **rótulos do Traefik** e **serve o `/`**.

**A regra**: a **volta atrás** de um serviço que entra no compose é **duas coisas** — o **checkout da
tag** (o compose sem o serviço) **e a remoção do contêiner** (o `stop/rm` ou o `--remove-orphans`).
**Sem a segunda, a primeira é uma ilusão**: o `/` continua sendo o serviço novo.
## A REGRA do rollback (23/10)

**Voltar de um serviço que entrou no compose exige DUAS ações:**

1. o **`checkout --force` da tag antiga** (o compose sem o serviço);
2. a **remoção do contêiner** (o `docker rm -f` do serviço **ou** o `--remove-orphans`).

**Sem a segunda, a primeira é uma ilusão**: o compose diz "não há landing" e o `/` continua sendo a
landing (o contêiner órfão com os rótulos do Traefik). **A proposta do `--remove-orphans`**: o
`dev/despacho-subir-remove-orphans.md` — **infraestrutura, só com a autorização do ARQUITECT**.
## O motivo do rollback — **REGISTRADO** (23/10)

**A resposta do ARQUITECT**: **motivo NÃO REGISTRADO**.

**O que o registro tem**: o **quando** (o deploy de 16:36 a 16:43; o rollback ~16:47), o **como** (o
`docker stop/rm didasko_landing` + o `git checkout --force refs/tags/v0.1.0` + o `subir.sh`), e a
**prova** de que o **deploy da `v0.1.1` foi `success`** (o run `39988210363`, "publicar na VPS") e o
**logo foi descartado** (o fix está na `v0.1.1`). **O porquê não foi registrado.**

## O critério de "resolvido" antes da próxima subida

**A decisão do ARQUITECT** (as 3 condições):

1. **o motivo ser dito e registrado** (na jornada do DEPLOY ou neste documento) — **sem isso, não há o
   que verificar**: um rollback sem motivo escrito não tem como ser evitado nem repetido;
2. **a ordem do ARQUITECT** — a produção **segue na `v0.1.0`** até ela;
3. **se o motivo for o visual ou a janela** (as hipóteses que o registro permite), o **registro do que
   mudou** antes da nova subida.

**A produção**: **na `v0.1.0`** até a ordem do ARQUITECT.
## A RE-SUBIDA da `v0.1.1` — a decisão do ARQUITECT (23/10)

### 1. O motivo do rollback

**"Motivo não registrado"** — registrado **assim**, **sem hipótese**. **Não inventar causa.**

### 2. A ordem

**Subir a `v0.1.1` de novo na produção**, como **deploy planejado**, **pelo pipeline**:

- o **`workflow_dispatch`** do `deploy.yml` com a **tag `v0.1.1`** e o **`environment producao`**;
- **a aprovação do environment é do ARQUITECT** (no GitHub);
- o **DEPLOY dispara, acompanha e diagnostica** (o ADR-016).

### 3. As condições (obrigatórias)

**ANTES:**
1. **a janela curta e avisada** pelo ARQUITECT — o `up -d --build` **recria o app da v0**;
2. **a volta atrás escrita ANTES** — agora com **DOIS passos**:
   - **(a)** o `git checkout --force refs/tags/v0.1.0` + o `subir.sh`;
   - **(b)** o **`docker rm -f didasko_landing`** (ou o `--remove-orphans`).
   **Sem o (b), o rollback é ilusório** (o contêiner órfão continua servindo o `/`);
3. **a linha de base registrada**: o `/` **200** com **45299 bytes**; o `/login`, o `/homenagens`, o
   `/aluno`, o `/admin` **307**; o `/static/landing/x.css` **404**.

**DEPOIS (a conferência):**
4. o `/` **contém** o `/static/landing/landing.<hash>.css`; **esse CSS** → **200** com o
   `cache-control: immutable`;
5. o `/login`, o `/homenagens`, o `/aluno`, o `/admin` → **307**; o `x.css` → **404**;
6. **a v0 funcionando** (o `/login`);
7. o **clone da VPS** com o **`git status` LIMPO** na **tag `v0.1.1`**;
8. os **`StartedAt` registrados na jornada**.

**SE QUALQUER ITEM FALHAR: PARAR e avisar o ARQUITECT antes de qualquer rollback.**

### 4. As obras e a infraestrutura

- **as obras seguem** (o EVAL cego do #9 em curso);
- **nada de infraestrutura nova** (o `--remove-orphans` no script) **sem a autorização do ARQUITECT**.
## A `v0.1.1` **EM PRODUÇÃO** (23/10) — o deploy pelo pipeline

O DEPLOY disparou o **`deploy.yml`** com a **tag `v0.1.1`** (o run **`40040835237`**); **todos os
passos success**, incluindo o **`pg_dump` verificado** e a **verificação HTTP externa do próprio
pipeline**.

**Os 5 itens do "depois", todos confirmados:**

1. o `/` **contém** o `/static/landing/landing.dfa7e29213827a3a.css`; esse CSS → **200** +
   **`immutable`**;
2. o `/login`, o `/homenagens`, o `/aluno`, o `/admin` → **307**; o `/static/landing/x.css` → **404**;
3. a **v0 funcionando**: o `/login` → **200**, o título correto;
4. o **clone da VPS**: o **`git status` LIMPO**, na **tag `v0.1.1`**;
5. os **`StartedAt`**: os **4** (`postgres`/`chromadb`/`ollama`/`traefik`) **idênticos ao de 18/10** —
   o **Traefik nunca reiniciado** em nenhum ato de hoje; o **`app` e o `landing`** recriados pelo
   **próprio pipeline**.

**Nenhum item falhou**; a **volta atrás** (os 2 passos corretos) **não precisou ser usada**.

**A nota do ADR-016**: o deploy **entrou direto**, sem a aprovação manual do `environment producao` —
**consistente com o ADR-016** (o *required reviewer* foi removido; a **autorização é por release
aceito**).
## O merge do #9 (24/10) — a fatia 2 na develop

O ARQUITECT mesclou o **#9** na `develop`: o **merge commit `d927467`** (24/10, 03:58 UTC),
**SEM o `--admin`** — o **CI no `pull_request` verde**.

**A opção A do CI funcionou**: o check `testes (pytest)` **no PR**, e o merge **sem o `--admin`** —
exatamente o que a correção prometia (o problema do #8 não se repete).

**O próximo**: o **DEPLOY** sobe a **`develop` pós-merge** (o `d927467`) na **homologação** (o
`subir.sh --v1`) + o **seed dos alunos fake UMA VEZ** (o `DIDASKO_AMBIENTE=homologacao`). **A
produção NÃO é tocada; o seed nunca roda em produção.**
## O deploy da homologação (24/10) — a fatia 2 no ar (com o gap do seed)

O DEPLOY subiu a **`develop` pós-merge** (o **`d927467`**) na **homologação**: o **`subir.sh --v1`
exit 0**; o `/`, o `/homenagens` e o `/login` → **200**.

**O seed**: rodou **uma vez** (exit 0; os **2 alunos fake** no banco). O **`SEED_PASSWORD`** e o
**`DATABASE_URL`** **nunca passaram pelo terminal do DEPLOY** — leram e substituíram **inteiramente do
lado do servidor**.

**O GAP**: o **`studyassignment` ficou com 0 linhas** — o seed é **fail-open**: sem **nenhuma `Obra`
com o `versao_liberada_id`** no `didasko_v1` (o **0/0** confirmado), ele **cria só os alunos e sai em
silêncio**, sem o estudo nem o assignment.

**Os `StartedAt`**: o **`app-v1`** e o **`landing`** recriados; o **`postgres-v1`** e o **Traefik**
**intocados**.
