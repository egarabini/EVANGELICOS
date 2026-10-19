# Briefing do DEVS — DEM-202610-016 (o experimento do provedor de identidade)

> **Para:** Codex (DEVS) · **De:** PLANNER · **Data:** 2026-10-19 · **o host fechado:** o provedor
> em **`oidc.homolog.didasko.app.br`** (um host só, neutro ao fornecedor); o FastAPI em
> **`/experimento`** no `homolog.didasko.app.br`.
> **1 a 2 dias.** **Não é** a decisão de adotar; **não altere o RF01**. O produto é o **relatório**.

## 1. O que ler

1. [`planner/intent.md`](../planner/intent.md) — o escopo (os 7 itens), os critérios (o **E-01..E-07**),
   o ambiente de homologação (§8) e as decisões.
2. [`planner/autorizacao-de-infra.md`](../planner/autorizacao-de-infra.md) — os itens **a-e** que o
   ARQUITECT autoriza (o Traefik, o banco, os limites, os segredos, o desmonte).
3. A **documentação oficial** do provedor (a versão atual; a API + o **Login V2 separado**; o
   `h2c`; a `LICENSING.md`) — não decida a arquitetura por tutoriais de terceiros.
4. O design da **DEM-005** (o marco 1: a v1, o FastAPI) e o `AGENTS.md` do código.

## 2. A tarefa (os 7 itens + o E-07)

1. O provedor em **`oidc.homolog.didasko.app.br`** (o **Postgres próprio**: o contêiner dedicado, a rede interna — **nunca** o `didasko_postgres`; o Traefik;
   o HTTPS), com a arquitetura oficial registrada (a API + o Login V2 separado; a API por `h2c`).
2. O login **OIDC** (authorization code + PKCE) no FastAPI do experimento, em **`/experimento`** no
   `homolog.didasko.app.br`, com o `authlib` (ou equivalente) e o **papel lido do token**.
3. O mapeamento: uma **organização → um ambiente**; um **papel** (o coordenador) → um papel do Didasko.
4. A **provisão por API**: o Didasko cria um instrutor, e ele entra.
5. A **troca obrigatória** no primeiro acesso, **pelo próprio provedor** (a D-11).
6. A **medição**: a memória (em repouso e no login) e a **latência com o Ollama ocupado** (o login
   com uma geração em andamento; o E-05: **≥ 10 logins**, a **mediana ≤ 2 s** e o **máximo ≤ 5 s**).
7. A **licença** (o AGPL-3.0-only no núcleo; o MIT no login; o uso como serviço separado e não
   modificado).
8. **E-07 — a independência do fornecedor**: a URL do emissor, o `client_id` e o segredo vêm de
   **variáveis de ambiente**; **nenhum nome do fornecedor** em caminho de código ou de rota do
   FastAPI. A verificação é a **leitura do diff** — o EVAL vai olhar.

**A v1 fica atrás de uma interface** (OIDC-ready): o didasko chama "quem é o usuário, o papel, o
ambiente"; a implementação é trocável.

## 3. O ambiente (a identificação)

| Item | Valor |
|---|---|
| O SSH | `didasko-vps` (o `didasko-deploy`; o `sudo -n docker`) |
| O diretório | `/home/didasko-deploy/experimentos/didasko/` — um clone **próprio** (o v0 é `/home/eduardo/didasko`) |
| O projeto do Compose | **`experimento-oidc`** (o `-p experimento-oidc`) |
| A rede do Traefik | **`deploy_didasko`** (a externa) |
| O `.env` | `experiments/zitadel/.env` (o **600**; fora do git) |
| Os volumes | os do projeto (nomeados); **o Postgres do experimento** é um **contêiner próprio** (a rede interna); **nunca** o `didasko_postgres` |

## 4. A infra (o que o ARQUITECT autoriza — os itens a-e)

**A autorização do ARQUITECT (19/10) já veio** — com as condições: o `/experimento` com a **basic
auth**; o **Postgres próprio** (nunca o `didasko_postgres`); o teto de **1 GB** na API; os segredos
com o `openssl rand` (sem imprimir; a senha do admin por **canal seguro**); o **desmonte** com a
confirmação na hora. E o **E-05**: ≥ 10 logins, a mediana ≤ 2 s e o máximo ≤ 5 s.

**O DNS** (o `oidc.homolog...` → o IP do site) é a única parte **já feita**.

## 5. As regras

- Branch `feature/DEM-202610-016-zitadel` a partir do `develop`, **em worktree separado**; PR; os
  commits pt-BR.
- **Não altere o RF01** da DEM-005 nem o `flow.py` da fatia 1; o experimento é **isolado**.
- **Sem segredo no repositório**; o `.env.example` com as chaves sem valor.
- **Nada de produção nem da v0**; só a homologação.
- Se um item do escopo não for possível (a versão, o serviço, a licença), **registre e siga** — o
  relatório é o produto.

## 6. O Definition of Done

- a **tabela dos E-01..E-07** (o PASS/FAIL de cada, com a evidência: o comando, a saída, o número);
- os números do **E-04** (a memória em MB) e do **E-05** (o login em s, com o Ollama ocupado);
- o esforço do **E-06** (em dias, por bloco: os papéis, os convites, o ciclo de vida, o tema);
- a **licença** (o que permite e o que impede);
- a **recomendação** (adotar/adiar/descartar) com a justificativa.
- o relatório na DEM-016 + o PR + o CI verde.

> O EVAL cego julga **uma rodada** contra os critérios. A decisão é do ARQUITECT — não adote nada.


