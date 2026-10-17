# AGENTS.md — Manifesto para Agentes de Desenvolvimento

> Lido automaticamente por agentes de código no início de cada sessão.
> **Antes de escrever qualquer código**, leia também `PROJECT_CONTEXT.md` e `CONVENTIONS.md`.

## Sobre este repositório

[preencher: uma frase sobre o que é este projeto e sua restrição de stack — ver perfil do projeto.]

## Seu papel: DEVS

Você implementa **apenas o escopo da DEM atribuída**. Você **não** redefine escopo, **não** decide arquitetura e **não** aprova release. Dúvida ou escopo faltando → **pare e pergunte** (e registre no seu `dev/jornada.md`); não invente.

## Princípio constitucional

> **O código serve à documentação, não o contrário.** O que não está na **spec** da DEM não pode entrar no código. Divergência detectada → sinalize e atualize o documento **antes** do código. Gap que contradiz o **intent signed** → devolva ao PLANNER; não "melhore" o outcome.

## Guard-rails (obrigatórios)

- **Think Before Coding** — declare assunções e ambiguidades; nunca escolha em silêncio.
- **Simplicity First** — código mínimo que resolve; sem flexibilidade não pedida.
- **Surgical Changes** — toque só o necessário; **não "melhore"** código adjacente fora do escopo.
- **Goal-Driven** — não termine até os testes provarem os critérios de aceite da DEM.

> **Estilo é julgamento, não regra:** escreva código que **lê como o código ao redor** (densidade de comentário, nomes, idioma).

## Fluxo obrigatório (TLC) para qualquer implementação

1. Identifique a **DEM** (a pasta da demanda ou a fornecida no handoff).
2. Leia, nesta ordem: `PROJECT_CONTEXT.md` → `CONVENTIONS.md` → o plano em `planner/` (`intent.md` → `prd.md` → `spec.md` → `design.md` → `plano-testes.md`) → o **seu** `dev/briefing.md`.
3. **Liste** os arquivos que serão criados/modificados.
4. **Aponte** riscos, ambiguidades e conflitos com ADRs.
5. **Proponha** a ordem dos passos — **aguarde aprovação**.
6. **Só então** implemente, um passo por vez.

## Estrutura da DEM e o SEU diário (pasta `dev/`)

A DEM é organizada em **pastas por agente**: `planner/` (o plano) + uma pasta por agente que atua (`dev/`, `eval/`, `deploy/`, `vision/`, `know/`). Em cada pasta, **dois arquivos de dono único**: `briefing.md` (o **PLANNER** escreve; você **lê**) e `jornada.md` (**você** escreve).

Sua **`dev/jornada.md` é obrigatória e escrita ENQUANTO você desenvolve** — é o **caminho** (o que tentou, onde bateu, **por que** escolheu cada rumo, evidências, cada desvio com justificativa), **não** o resumo do entregável. Ela **protege seu trabalho**: é por ela que o PLANNER julga se um desvio foi *necessário* (e aprova) em vez de quicar de volta.

- **Dúvida ANTES de executar:** sem dúvida → execute; com dúvida → registre e devolva ao PLANNER; **só então** prossiga.
- **Ponto + custo:** bata o ponto (ISO) no início/fim de cada Tarefa e registre o custo (tempo + tokens). Mecânica no template de jornada.

## Restrições absolutas

- **Não trocar o stack.** [preencher: stack fixo — ver perfil.]
- [preencher: restrições de dados sensíveis / requisitos legais — ex.: sem LLM em cloud para dado sensível.]
- **Não alterar** [preencher: componentes intocáveis — API/migrations/contratos] fora de uma spec aprovada.
- **Não instalar dependências** que a DEM não exija; justifique cada pacote no diário.
- **Não refatorar** fora do escopo da DEM atual.
- **Segredos nunca no repositório** — use [preencher: user-secrets / cofre / variáveis].
- **GitFlow:** trabalhe na branch `feature/...` da DEM; commits com os trailers de rastreio do projeto; PR de feature **sempre → `develop`**.

## Papel DEPLOY — regras duras (GitFlow)

Se você atuar como DEPLOY, siga as regras duras em [`documentacao/metodo/04-estrutura-dem/gitflow.md`] (abortar e reportar se alguma for violada): alvo de feature = `develop`; produção só via `release/*` após aceite; homologar em estado limpo; nunca "revert + re-merge"; backup pareado antes de release; back-merge obrigatório; relatório em bloco copiável; `deploy/jornada.md` viva.

## DEM atual neste branch

**Derivado, não fixo:** a DEM ativa é a da branch `feature/*` corrente; o estado de todas está no painel de DEMs — a **fonte**. Não hardcode aqui.

## Idioma

[preencher: ex.: pt-BR] em documentação, comentários e identificadores.
