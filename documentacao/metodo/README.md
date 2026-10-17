# Método — Desenvolvimento Governado por Agentes (Spec-Driven + INTENT)

> **O que é isto.** Um método completo e **project-neutral** para conduzir o desenvolvimento de software com **agentes de IA sob governança**. É a consolidação de um processo validado em produção ao longo de dezenas de entregas: papéis com fronteiras, cercas que evoluíram de textuais → estruturais → verificadas, e — a última cerca — a de **objetivo** (a camada INTENT).
>
> **Para quem.** Uma **IA condutora** (o papel PLANNER) que vai reger um projeto novo, com um humano no comando (ARQUITECT) e um ou mais agentes implementadores (DEVS). Este pacote é **autocontido**: não depende de nenhum outro documento externo.

---

## A tese em três frases

1. **Especialização de papéis reduz alucinação.** Cada agente tem uma missão, um dono único de cada arquivo e uma fronteira que não pode cruzar.
2. **Nada existe até estar no disco/git, verificado.** Declaração de agente nunca substitui conferência; veredito é amarrado a hash.
3. **Intent é o porquê; spec é o quê; DEM é o como.** A especificação não é o primeiro artefato — ela nasce de um objetivo assinado, o que fecha a cerca que as outras não cobriam.

## As duas unidades de trabalho

| Unidade | O que é | Duração | Dono |
|---|---|---|---|
| **ADR** (Architecture Decision Record) | A **lei** — uma decisão estrutural que rege muitas demandas | Longa (lei até ser substituída) | ARQUITECT decide |
| **DEM** (Demanda) | A **ação** — uma unidade tática de entrega (feature, fix, ajuste) | Curta (planejar → executar → entregar) | PLANNER conduz |

## Os papéis (visão rápida)

| Papel | Uma linha | Humano/IA |
|---|---|---|
| **ARQUITECT** | Dono da visão; origem e destino de toda DEM; assina os gates | Humano |
| **PLANNER** | Escriba, especificador, auditor; conduz a DEM e fecha o ciclo | IA (a IA condutora) |
| **DEVS** | Implementa o escopo da DEM via TLC; não decide escopo | IA ou humano |
| **EVAL** | Porteiro de qualidade; PASS/FAIL sobre hash, em estado limpo | IA |
| **VISION** | Guardião visual (só em DEM com tela) | IA |
| **DEPLOY** | Executa o GitFlow e as publicações com gates | IA |
| **KNOW** | Fonte de conhecimento consultável (opcional/futuro) | IA |
| **ORCHESTRATOR** | Roteador dos despachos (opcional/futuro) | IA |

Fichas completas, matriz de fronteiras e as **11 regras de ouro** em [`01-papeis/papeis-e-interacoes.md`](01-papeis/papeis-e-interacoes.md).

---

## Como adotar este método num projeto novo (passo a passo)

1. **Copie a pasta inteira** `metodo/` para a documentação do projeto novo (ela é autocontida).
2. **Preencha o perfil do projeto.** Copie [`perfil-do-projeto/perfil-do-projeto.template.md`](perfil-do-projeto/perfil-do-projeto.template.md), responda cada campo (stack, segurança, ambientes, convenções, rastreio). É **aqui** — e só aqui — que entram as escolhas específicas do seu projeto. Veja [`perfil-do-projeto/exemplo-agoracred.md`](perfil-do-projeto/exemplo-agoracred.md) como exemplo preenchido.
3. **Instale os arquivos de guarda no repositório de código.** Copie [`arquivos-de-guarda/`](arquivos-de-guarda/) (`AGENTS.md`, `CLAUDE.md`, `CONVENTIONS.md`) para a **raiz do repo** e complete os `[preencher]` com o perfil. Todo agente de código os lê antes de escrever.
4. **Registre suas primeiras ADRs.** Use [`05-decisoes-adr/ADR-000-template.md`](05-decisoes-adr/ADR-000-template.md). A lista mínima de decisões que todo projeto precisa tomar está em [`05-decisoes-adr/como-usar-adr.md`](05-decisoes-adr/como-usar-adr.md).
5. **Rode a primeira DEM.** Crie a pasta da DEM a partir de [`templates/`](templates/) e siga o ciclo de vida ([`00-visao-geral/ciclo-de-vida.md`](00-visao-geral/ciclo-de-vida.md)): **INTENT → (assina) → spec/prd/design/plano-testes → briefings → DEVS/TLC → EVAL → VISION → aceite → DEPLOY → fechamento**.

## Ordem de leitura recomendada (para a IA condutora)

| # | Documento | Por quê |
|---|---|---|
| 1 | [`00-visao-geral/filosofia.md`](00-visao-geral/filosofia.md) | Os dois pilares e a mentalidade |
| 2 | [`01-papeis/papeis-e-interacoes.md`](01-papeis/papeis-e-interacoes.md) | Quem faz o quê, fronteiras, 11 regras |
| 3 | [`02-guard-rails/guard-rails-e-tlc.md`](02-guard-rails/guard-rails-e-tlc.md) | Como todo agente se comporta (TLC) |
| 4 | [`03-camada-intent/camada-intent.md`](03-camada-intent/camada-intent.md) | A cerca de objetivo — o coração da V2 |
| 5 | [`04-estrutura-dem/estrutura-da-dem.md`](04-estrutura-dem/estrutura-da-dem.md) | Como uma DEM é organizada em disco |
| 6 | [`00-visao-geral/ciclo-de-vida.md`](00-visao-geral/ciclo-de-vida.md) | O fluxo ponta a ponta, com gates |
| 7 | [`01-papeis/protocolo-de-despacho.md`](01-papeis/protocolo-de-despacho.md) | Como se despacha e se consolida trabalho |
| 8 | [`04-estrutura-dem/gitflow.md`](04-estrutura-dem/gitflow.md) | Branches, releases, regras duras do DEPLOY |

## Mapa do pacote

```
metodo/
├── README.md                       ← você está aqui
├── 00-visao-geral/                 filosofia + ciclo de vida (fluxo e gates)
├── 01-papeis/                      fichas dos papéis, matriz, 11 regras, despacho
├── 02-guard-rails/                 princípio constitucional, 4 guard-rails, TLC
├── 03-camada-intent/               a camada INTENT (conceito) + métricas do gate
├── 04-estrutura-dem/               estrutura de pastas da DEM + GitFlow
├── 05-decisoes-adr/                como usar ADR + template + decisões mínimas
├── templates/                      todos os modelos copiáveis (intent, prd, spec, …)
├── perfil-do-projeto/              o SEU projeto entra aqui (stack, segurança, convenções)
└── arquivos-de-guarda/             AGENTS/CLAUDE/CONVENTIONS para a raiz do repo
```

## Convenções deste pacote

- **Idioma:** português (pt-BR). Ajustável no perfil do projeto.
- **Nomes de arquivo:** `kebab-case` ASCII.
- **README por pasta:** cada subpasta tem o seu, servindo de índice.
- **Method vs profile:** nenhum documento de método cita stack. Toda escolha técnica vive em `perfil-do-projeto/`. Se você encontrar uma tecnologia citada fora do perfil ou dos exemplos, é bug de portabilidade — corrija.

---

> **Origem.** Este método foi destilado de um processo real (empresa AgoraCred), onde nasceu como "arquiteturaV1" (papéis, ADRs, estrutura de DEM) e evoluiu para a "arquiteturaV2" (camada INTENT). Aqui as duas camadas estão **fundidas e neutralizadas** para transporte a qualquer projeto.
