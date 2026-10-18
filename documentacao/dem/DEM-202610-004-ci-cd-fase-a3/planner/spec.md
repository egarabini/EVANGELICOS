# Spec — DEM-202610-004 / CI/CD (Fase A3)

> Dono: PLANNER. Cada capacidade cita um **outcome** (intent §2), um **non-goal**
> (§4 Out) ou uma **constraint** (§5). A DEM tem **duas entregas**: Etapa 1 (CI) e Etapa 2 (CD).

## 1. Referência

PRD: ver o próprio intent (a DEM é pequena; o PRD seria repetição) · Intent: [`intent.md`](intent.md) — **signed** 2026-10-17
ADRs: **009** (GitFlow + Copilot) · **010** (publicação por CI) · **008** (segredos)

## 2. Requisitos funcionais — Etapa 1 (CI)

- [ ] **RF01:** Todo PR para `develop` ou `main` executa a **suíte de testes** e mostra o
  resultado como **check do PR**. — *(intent §2 · 9.5)*
- [ ] **RF02:** Todo push para `develop` ou `main` executa a mesma suíte. — *(intent §2)*
- [ ] **RF03:** O workflow roda em **runner do GitHub** (ubuntu), sem acesso à VPS. — *(intent §8.2)*
- [ ] **RF04:** `develop` e `main` passam a ter **proteção** exigindo o check da CI para merge. — *(intent §4 In · ADR-009)*
- [ ] **RF05:** O check **falha fechado**: erro de instalação ou de teste reprova o PR. — *(intent §5)*

## 3. Requisitos não funcionais

- **Tempo:** a CI completa em ≤ 15 min (timeout de 20).
- **Cache:** dependências em cache por `requirements.txt`, para não reinstalar tudo a cada PR.
- **Concorrência:** push novo cancela a execução anterior da mesma ref.
- **Segurança:** nenhum segredo é usado na Etapa 1; `permissions: contents: read`.
- **Compatibilidade:** Python 3.12 (a versão da imagem de produção).
- **Sem corpus:** a suíte usa dublês; a CI **não** precisa de corpus, ChromaDB nem Ollama.

## 4. Contratos

Workflow: `.github/workflows/ci.yml`, evento `pull_request` + `push` (branches `develop`,
`main`) + `workflow_dispatch`. Job único `testes`, passo `python -m pytest tests -q`.

Check obrigatório na proteção: `testes (pytest)`.

## 5. Edge cases

- **PR de fork** — o workflow usa só `contents: read`; nenhum segredo é exposto.
- **Dependência quebrada no `requirements.txt`** — a instalação falha e o PR reprova (RF05).
- **Falha intermitente** — o check pode ser reexecutado manualmente (`gh run rerun`); não se
  aprova PR com check vermelho.
- **Workflow na base mas não na branch** — a CI roda a partir da base do PR; por isso o
  workflow entra primeiro em `develop`.

## 6. Etapa 2 (CD) — fora desta entrega

Deploy por tag/merge em `main`, com `pg_dump` antes, chave em secret e verificação HTTP ao
final. Depende da **chave nova** (decisão 9.3) e será especificada quando a Etapa 1 estiver
verde — o intent já a cobre, a spec dela vem depois.

## 7. Critérios de aceitação — Etapa 1

- [ ] **CA01:** o PR #1 (DEM-001) passa a mostrar o check `testes (pytest)`; verde com a
  suíte atual (82 testes).
- [ ] **CA02:** um PR com teste quebrado **não pode ser mergeado** (proteção ativa).
- [ ] **CA03:** `develop` e `main` protegidas exigindo o check.
- [ ] **CA04:** nenhum segredo criado nesta entrega.
- [ ] **CA05:** a produção não é tocada (nenhum deploy disparado).
