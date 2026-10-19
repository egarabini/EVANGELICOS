# Autorização de infraestrutura — DEM-202610-016 (o experimento)

> **Para o ARQUITECT aprovar item a item (a ADR-016).** A configuração está pronta para revisão; o
> Codex executa o que for autorizado. **Nada toca a v0 nem a produção.**
> O ambiente identificado está na §8 do `intent.md`: o clone próprio em
> `/home/didasko-deploy/experimentos/didasko/`, o projeto **`experimento-oidc`**, a rede
> **`deploy_didasko`**, o `.env` em `experiments/zitadel/.env` (600).

## (a) O roteador do Traefik

**Dois routers** (via os labels do compose — o Traefik está com `exposedbydefault=false`):

| Router | A regra | O serviço |
|---|---|---|
| `oidc` | `Host(\`oidc.homolog.didasko.app.br\`)` — os paths do provedor: a API (`/oauth/v2/*`, `/.well-known/*`, `/admin/*`?) e o login V2 (`/ui/v2/login/*`), conforme a doc oficial | o provedor (a API + o Login V2, o mesmo host) |
| `experimento` | `Host(\`homolog.didasko.app.br\`) && PathPrefix(\`/experimento\`)` | o FastAPI do experimento |

Ambos: o `entrypoints=websecure` e o `tls.certresolver=le` (o LE por **httpchallenge**, como o v0 já
usa). **O que o ARQUITECT aprova**: a regra dos hosts e o roteamento.

## (b) O banco e o papel no Postgres

No **`didasko_postgres`** (o serviço existente; **sem** tocar no banco `didasko` da v0):

```sql
CREATE ROLE zitadel LOGIN PASSWORD '<o segredo gerado na VPS>';
CREATE DATABASE zitadel OWNER zitadel ENCODING 'UTF8' TEMPLATE template0;
-- o papel não recebe acesso a nada da v0; a conexão do provedor usa só o banco `zitadel`
```

**O que o ARQUITECT aprova**: a criação do papel e do banco **com o owner próprio** e a **ausência
de acesso** ao `didasko`.

## (c) Os limites de memória dos contêineres

| Contêiner | O limite | A justificativa |
|---|---|---|
| o provedor (a API) | **512 MB** | 2 vCPU/12 GB na VPS; o provedor em Go |
| o Login V2 | **256 MB** | o serviço de login (a UI) |
| o FastAPI do experimento | **128 MB** | um cliente OIDC mínimo |

**O total**: ~**896 MB** — abaixo do **E-04** (o < 1 GB em repouso). **O que o ARQUITECT aprova**: os
limites (a memória é o critério do experimento; se o total real passar de 1 GB em repouso, o E-04
falha — e isso é o dado).

## (d) Os segredos do provedor

- A **chave mestra** e a **senha do administrador** do provedor são **geradas na VPS** (o
  `openssl rand -base64 32` ou o setup do próprio provedor) e ficam no
  `experiments/zitadel/.env` (o **modo 600**, o dono `didasko-deploy`).
- **Nunca** no repositório, no chat ou no log do CI (a ADR-008).
- **O que o ARQUITECT aprova**: a geração na VPS e a permanência no `.env` (não versionado).

## (e) O desmonte ao final

O procedimento (a ser executado **com a autorização do ARQUITECT**, ao final do experimento):

```bash
# no diretório do experimento, na VPS:
docker compose -p experimento-oidc down -v        # os contêineres + os volumes nomeados do projeto
psql -h ... -U didasko -d postgres -c "DROP DATABASE zitadel;"   # o banco do provedor (destrutivo)
psql -h ... -U didasko -d postgres -c "DROP ROLE zitadel;"
# a remoção do clone /home/didasko-deploy/experimentos/didasko/
```

**O que o ARQUITECT aprova**: o `down -v` (os volumes do projeto) e o **DROP** do banco/papel — a
**exclusão de dados** exige autorização **específica** (a ADR-016); ela é registrada na jornada.

---

## O que já está feito

- **O DNS**: o `oidc.homolog.didasko.app.br` → o IP do site — **já criado pelo ARQUITECT** (a base
  `didasko.app.br` e o `homolog.didasko.app.br` resolvem para a VPS).
- **O ambiente** identificado (§8 do intent).
- **O código** do experimento: o Codex prepara no worktree/`experiments/zitadel/` (sem infra).

## O que o Codex faz sem autorização

O worktree, o `experiments/zitadel/`, a interface de identidade, o OIDC/PKCE com o `authlib`, a
provisão por API, o Compose (a config pronta), as ferramentas de medição e os testes — **o local**.
A infra entra quando o ARQUITECT aprovar os itens a-e.
---

## As decisões do ARQUITECT (2026-10-19)

| # | Decisão |
|---|---|
| **a** | **APROVADO** — os routers; o `/experimento` **com a basic auth do Traefik** |
| **b** | **APROVADO COM MUDANÇA** — o **Postgres próprio** (o contêiner dedicado, a rede interna); **nunca** o `didasko_postgres`; só o serviço **roteado** na `deploy_didasko` |
| **c** | **APROVADO COM AJUSTE** — o teto de **1 GB** na API (o 512 pode matar o `start-from-init`); o 256 no login e o 128 no FastAPI; o E-04 mede o **real** |
| **d** | **APROVADO** — o `openssl rand` na VPS, o `.env` 600, **sem imprimir**; a senha do admin por **canal seguro**, nunca no chat/log |
| **e** | **PLANO APROVADO** — o `down -v` do `experimento-oidc` (só os volumes dele); a execução com a **confirmação do ARQUITECT na hora**, os comandos exatos listados antes |
| **E-05** | **≥ 10 logins** com o Ollama ocupado; a **mediana ≤ 2 s** e o **máximo ≤ 5 s** |

O `experiment.yml` fica **aceito** e é **removido junto com o experimento**. O relatório diz "o código
está pronto; o veredito depende da homologação" **até os números existirem** — a recomendação só
vira "adotar/adiar/descartar" **depois** deles.
