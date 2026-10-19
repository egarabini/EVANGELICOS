# Intent: DEM-202610-016 / o experimento do provedor de identidade

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: decisão do ARQUITECT de 2026-10-19 — o experimento com prazo no marco 1 da v1
signed_at:
supersedes: —
open_questions_open: 1
nivel_agil: 2 — (ADR-018) uma rodada de EVAL; a homologação; **não** altera o RF01 até o resultado
duracao: **1 a 2 dias**
host: **`oidc.homolog.didasko.app.br`** (o provedor) · o FastAPI em **`/experimento`** no `homolog.didasko.app.br`
nota: este experimento **não é** a decisão de adotar. É uma prova de viabilidade com critério (o
E-01..E-07) e uma recomendação. A autenticação própria da v1 continua prevista, atrás de uma
interface (§4).

## 1. Problema

A v1 vai ter autenticação própria (o RF01 da DEM-005) — e é justamente onde apareceram os problemas
das dívidas: a troca obrigatória de senha como **redirect** (a D-11), o coordenador criado com a
senha fixa (a D-10), o bloqueio por tentativas, a recuperação de senha. É código nosso, com história
de defeito.

O ARQUITECT conhece o **Keycloak** e se interessou pelo **Zitadel** porque: o modelo **multi-tenant**
(organizações, projetos, a gestão delegada) casa com o "ambiente" do Didasko e com o coordenador
administrando os seus usuários; é certificado **OIDC**, exige **PostgreSQL** (que já temos) e traz a
**tela de login pronta**. E a decisão é mais barata **agora**: nada depende da auth e não há usuários
a migrar.

## 2. Outcome

**Um go/no-go com evidência**: o relatório com os números do E-04/E-05, o esforço do E-06, a
**independência do fornecedor** (o E-07) e a **recomendação**. Nada muda no RF01 antes do resultado.

## 3. O escopo (os 7 itens do ARQUITECT)

1. **Subir** o provedor na homologação, no host **`oidc.homolog.didasko.app.br`** (um host só, neutro
   ao fornecedor), com o banco próprio no mesmo Postgres, atrás do Traefik, com HTTPS — com a
   arquitetura oficial registrada (a API + o **Login V2 separado**, a API por **`h2c`**).
2. **Login OIDC** (authorization code + PKCE) de um usuário de teste no FastAPI do experimento, em
   **`/experimento`** no `homolog.didasko.app.br`, validando o token com biblioteca padrão (o
   `authlib`) e lendo o **papel** do token.
3. **Mapear** uma organização do provedor a um **ambiente** do Didasko e um papel (o coordenador) a um
   papel do Didasko.
4. **Provisionar por API**: o Didasko (como coordenador) cria um instrutor no provedor e ele entra.
5. **A troca obrigatória** de senha no primeiro acesso, feita **pelo próprio provedor** (o D-11).
6. **Medir**: a memória do(s) contêiner(es) em repouso e durante um login; o tempo de login com o
   **Ollama ocupado** (a VPS de 12 GB, o Ollama em CPU — o hash de senha disputa os núcleos).
7. **Registrar a licença** atual (o núcleo **AGPL-3.0-only**; o login com **exceção MIT**) e o que ela
   implica usando-o como **serviço separado e não modificado**.

## 4. Constraints

- **1 a 2 dias**; **a homologação**; o **Postgres próprio** (o contêiner dedicado); **a v0 e a produção intocadas**.
- **Um host só**: o provedor em `oidc.homolog.didasko.app.br` (o nome é neutro ao fornecedor — se
  mudar, o host permanece; mas a URL do emissor pode ter caminho do fornecedor, e trocar de provedor
  ainda exige reconfigurar o cliente OIDC).
- **Não altera o RF01** até o resultado; a autenticação fica **atrás de uma interface** (OIDC-ready).
- A **infra é do ARQUITECT** (os itens da §7); o DNS é a **única parte já feita**.

## 5. Os critérios de aceite (o E-01..E-07)

| # | Critério | Passa se |
|---|---|---|
| **E-01** | o login OIDC | o usuário de teste entra e o FastAPI lê o papel do token |
| **E-02** | a provisão por API | o Didasko cria um instrutor e ele entra |
| **E-03** | a D-11 | o primeiro acesso exige a troca, **sem código nosso** |
| **E-04** | a memória | o conjunto do provedor **abaixo de 1 GB** em repouso |
| **E-05** | a latência com o Ollama ocupado | **≥ 10 logins** com o Ollama ocupado; **mediana ≤ 2 s** e **máximo ≤ 5 s** (a decisão do ARQUITECT) |
| **E-06** | o esforço | o relatório estima o custo restante, em dias, para o fluxo completo |
| **E-07** | **a independência do fornecedor** | a URL do emissor, o `client_id` e o segredo vêm de **variáveis de ambiente**; **nenhum nome do fornecedor** aparece em caminho de código ou de rota do FastAPI — verificado pela **leitura do diff** |

## 6. Health e sinal

- **O sinal**: o relatório com a **tabela dos E-01..E-07**, os números do E-04/E-05, o esforço do
  E-06 e a **recomendação** — com a justificativa.
- **O porteiro**: o EVAL cego, **uma rodada**, contra os critérios.

## 7. As autorizações de infraestrutura (o ARQUITECT aprova item a item)

O detalhe com a configuração pronta está em [`autorizacao-de-infra.md`](autorizacao-de-infra.md).

| # | Item | De quem |
|---|---|---|
| **a** | O **roteador do Traefik**: o host `oidc.homolog...` (o provedor) e o `/experimento` no `homolog...` — este com a **basic auth do Traefik** | **APROVADO** |
| **b** | **MUDANÇA**: um **Postgres próprio** (o contêiner dedicado, a rede interna; **nunca** o `didasko_postgres`); só o serviço roteado na `deploy_didasko` | **APROVADO COM MUDANÇA** |
| **c** | **AJUSTE**: o teto de **1 GB** na API (o `start-from-init`); o 256 no login e o 128 no FastAPI; o E-04 mede o **real** | **APROVADO COM AJUSTE** |
| **d** | Os segredos com o `openssl rand` na VPS, no `.env` 600, **sem imprimir**; a senha do admin vai ao ARQUITECT por **canal seguro** | **APROVADO** |
| **e** | O **desmonte**: o `down -v` do `experimento-oidc`; a execução com a **confirmação do ARQUITECT na hora**, os comandos listados antes | **PLANO APROVADO** |

**O DNS**: o registro A de `oidc.homolog.didasko.app.br` → o mesmo IP do site — **já é do ARQUITECT e
é a única parte feita** (o `didasko.app.br` e o `homolog.didasko.app.br` resolvem para a VPS; o host
novo falta).

## 8. O ambiente de homologação (a identificação — para o Codex)

| Item | Valor |
|---|---|
| O SSH | `didasko-vps` (o usuário `didasko-deploy`; o `sudo -n docker` para o docker) |
| O diretório do experimento | `/home/didasko-deploy/experimentos/didasko/` — um **clone próprio**, isolado do v0 (`/home/eduardo/didasko`) e do clone do deploy (`/home/didasko-deploy/didasko`) |
| O projeto do Compose | **`experimento-oidc`** (o `-p experimento-oidc`; os contêineres e os volumes prefixados por ele) |
| A rede do Traefik | **`deploy_didasko`** (a externa, já existente) |
| O `.env` | `/home/didasko-deploy/experimentos/didasko/experiments/zitadel/.env` (o modo **600**, o dono `didasko-deploy`) — **fora do git** |
| Os volumes | os do projeto `experimento-oidc` (nomeados) — **nenhum volume da v0**; o banco é o **serviço Postgres existente** |
| O Postgres | **um contêiner próprio do experimento** (o projeto `experimento-oidc`, a **rede interna**); **nunca** o `didasko_postgres`; só o serviço **roteado** entra na `deploy_didasko` |

## 9. Decisões já registradas

| # | Questão | Decisão |
|---|---|---|
| 9.1 | A DEM | **própria, nível 2** |
| 9.2 | O executor | **Codex** |
| 9.3 | O host | **um só**: `oidc.homolog.didasko.app.br` (o nome neutro; o FastAPI em `/experimento`) |
| 9.4 | O limite do E-05 | **≤ 5 s** de ponta a ponta, o p95 de 3 medições |
| 9.5 | A decisão | **o ARQUITECT**, com o relatório; se adotar, **ADR nova** + o RF01 + os marcos 1/2 |
| 9.6 | A produção (se adotar) | o provedor numa **instância nova e limpa** em `oidc.didasko.app.br`; o host de homologação é **descartado**, não renomeado |

## 10. As autorizações (fechadas pelo ARQUITECT em 2026-10-19)

- [x] **10.1** A infraestrutura (a §7, o a-e) — **aprovada**, com a mudança do **Postgres próprio** e o ajuste do **1 GB**.
- [x] **10.2** O E-05 — **≥ 10 logins**, a **mediana ≤ 2 s** e o **máximo ≤ 5 s**. O relatório diz "o código está pronto; o veredito depende da homologação" até os números existirem.

## 11. Fora de escopo

A migração de usuários da v0 (não há); o deploy/o pipeline da v1; a adoção (a decisão é depois).









