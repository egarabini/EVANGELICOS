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
