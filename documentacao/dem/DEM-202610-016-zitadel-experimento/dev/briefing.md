# Briefing do DEVS — DEM-202610-016 (o experimento do Zitadel)

> **Para:** Codex (DEVS) · **De:** PLANNER · **Data:** 2026-10-19
> **1 a 2 dias.** O experimento **não é** a decisão de adotar: é uma prova de viabilidade com
> critério (o E-01..E-06) e uma recomendação. **Não altere o RF01** da DEM-005.

## 1. O que ler

1. [`planner/intent.md`](../planner/intent.md) — o escopo, os critérios e as regras.
2. A **documentação oficial** do Zitadel (a versão atual; se há o **serviço de login separado**) —
   não use tutoriais de terceiros para decidir a arquitetura.
3. O design da **DEM-005** (o marco 1: a v1, o FastAPI, o `didasko_v1`) e o `AGENTS.md` do código.
4. A `ADR-018` (o nível 2: uma rodada de EVAL).

## 2. A tarefa (os 7 itens do intent)

1. Subir o Zitadel na **homologação** (o banco próprio no Postgres; o Traefik; o HTTPS), com a
   versão e os serviços registrados (o login separado?).
2. O login **OIDC** (authorization code + PKCE) no FastAPI do marco 1, com o `authlib` (ou
   equivalente) e o **papel lido do token**.
3. Mapear uma **organização → um ambiente** e um **papel** (o coordenador) → um papel do Didasko.
4. A **provisão por API**: o Didasko cria um instrutor e ele entra.
5. A **troca obrigatória** no primeiro acesso, pelo Zitadel (o D-11).
6. Medir a **memória** (em repouso e no login) e a **latência** com o **Ollama ocupado** (o login
   com uma geração em andamento).
7. Registrar a **licença** (a atual) e o que ela implica como serviço separado e não modificado.

**A v1 fica atrás de uma interface** (OIDC-ready): mesmo que o experimento passe, o código do
didasko chama "quem é o usuário, o papel, o ambiente" — e a implementação (o Zitadel × a própria) é
trocável.

## 3. A infraestrutura (o que é do ARQUITECT)

| Item | Ação |
|---|---|
| o **host** do Zitadel (o DNS) | o Codex **pede** ao ARQUITECT; propõe o nome no PR |
| o **roteador do Traefik** | o Codex prepara a config; o ARQUITECT aplica (a autorização) |
| o **banco/usuário** do Zitadel no Postgres | o Codex pede a criação; o ARQUITECT executa |

**Nada de produção, nada da v0.** O experimento roda só na homologação.

## 4. As regras

- Branch `feature/DEM-202610-016-zitadel` a partir do `develop`; PR; commits pt-BR.
- **Não altere o RF01 da DEM-005** nem o `flow.py` da fatia 1; a interface de auth é **nova** e
  isolada (o didasko a consome; o experimento a implementa).
- **Não inclua segredo no repositório**: o `.env` do experimento (o client id/secret do OIDC) fica
  fora; o `.env.example` ganha as chaves sem valor.
- **Se o Zitadel exigir um serviço separado de login**, registre a arquitetura real (a doc oficial).
- Se um item do escopo não for possível (a versão, a licença, o serviço), **registre e siga** — o
  relatório é o produto.

## 5. O Definition of Done

- a **tabela dos E-01..E-06** (o PASS/FAIL de cada, com a evidência: o comando, a saída, o número);
- os **números do E-04 e do E-05** (a memória em MB; o login em s; o Ollama ocupado);
- o **esforço do E-06** (em dias, por bloco: os papéis, os convites, o ciclo de vida, o tema);
- a **recomendação** (adotar/adiar/descartar) com a justificativa;
- o relatório curto + o PR + o CI verde.

> O EVAL cego julga **uma rodada** contra os critérios. A decisão é do ARQUITECT, com o relatório.
