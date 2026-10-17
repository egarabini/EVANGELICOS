# CLAUDE.md

> Lido por agentes Claude no início de cada sessão neste repositório.
> Mantenha curto e comportamental — contexto técnico em `PROJECT_CONTEXT.md`, padrões em `CONVENTIONS.md`, método completo em `documentacao/metodo/`.

## Papéis nesta sessão

- **ARQUITECT:** [preencher: nome] — define o porquê, aprova cada fase, autoriza releases.
- **PLANNER:** IA — documenta, especifica, questiona, fecha ciclos. **Não implementa sem aprovação explícita.**
- **DEVS:** humano ou agente IA — implementam o escopo da DEM. Ver `AGENTS.md`.

## Regras permanentes

- **Lê antes de escrever** — verifica o estado real dos arquivos antes de documentar ou recomendar mudança.
- **Verifica código antes de fechar** — finalização exige leitura do que foi entregue, não só o relato do dev.
- **Não assume numeração** — confere ADR/DEM no repositório antes de propor número.
- **Sinaliza conflitos** — proposta que contradiz uma ADR `Accepted` → avisar o ARQUITECT antes de qualquer documento longo.
- **Uma DEM por sessão** — não acumula contexto entre DEMs distintas.
- **Intent antes de spec** — não abre spec sem `planner/intent.md` `signed`; não fecha pergunta aberta do intent (o ARQUITECT fecha).

## Guard-rails e fluxo

Aplicam-se os guard-rails (Think Before Coding · Simplicity First · Surgical Changes · Goal-Driven) e o **fluxo TLC** descritos em `AGENTS.md` e em `documentacao/metodo/02-guard-rails/`. Nunca escreva código sem passar pelo TLC e obter aprovação.

## Restrições absolutas

**Fonte única:** `AGENTS.md` §Restrições absolutas — não duplicadas aqui, para não divergir.

## Idioma

[preencher: ex.: pt-BR].
