# Como usar ADRs

## O que é

Uma **ADR** (Architecture Decision Record) registra uma **decisão estrutural** — uma lei do projeto. Não descreve tarefas; descreve uma escolha e suas consequências. Padrão: **MADR** (Markdown Any Decision Records).

## Ciclo de vida

```
Proposed → Accepted → Deprecated | Superseded by [ADR-NNN]
```

- O aceite é do **ARQUITECT**.
- Uma vez `Accepted`, é lei até ser substituída. **Nenhuma DEM pode contrariá-la** — se precisar, o ARQUITECT cria uma nova ADR que a substitui **antes** de a DEM começar.

## Convenções

- Numeração **contínua e única** no projeto: `ADR-001`, `ADR-002`, … (nunca reutilize número).
- Arquivo: `ADR-NNN-titulo-em-kebab-case.md`, a partir de [ADR-000-template.md](ADR-000-template.md).
- Mantenha um índice (README da pasta de ADRs) com número, assunto e status.
- Uma ADR **refina** ou **substitui** outra explicitamente — nunca contradiz em silêncio.

## Decisões mínimas que todo projeto novo precisa tomar

Antes da primeira DEM, registre (uma ADR cada, ou agrupadas com bom senso):

| # | Decisão | Por quê |
|---|---|---|
| 1 | **Stack e tecnologias-base** | Fixa o "não trocar o stack"; alimenta o [perfil do projeto](../perfil-do-projeto/perfil-do-projeto.template.md). |
| 2 | **Estratégia de branches (GitFlow)** | Define ambientes, releases e as regras duras do DEPLOY. Ver [gitflow.md](../04-estrutura-dem/gitflow.md). |
| 3 | **Guard-rails de agentes + TLC + arquivos de guarda** | Autoriza delegar código a agentes com segurança. Ver [guard-rails-e-tlc.md](../02-guard-rails/guard-rails-e-tlc.md). |
| 4 | **Estrutura única de DEM (ownership por pasta)** | Torna o controle estrutural, não textual. Ver [estrutura-da-dem.md](../04-estrutura-dem/estrutura-da-dem.md). |
| 5 | **Camada INTENT como gate de objetivo** | A 11ª regra; a cerca de objetivo. Ver [camada-intent.md](../03-camada-intent/camada-intent.md). |
| 6 | **Gestão de segredos** | Onde vivem credenciais/chaves; nunca no repositório. |
| 7 | **Observabilidade** | Como se instrumenta e se lê o comportamento em runtime. |
| 8 | **Métrica de custo/tamanho por DEM** | Base do rollup de tempo/tokens e da priorização. |

> As decisões 2–5 já estão **descritas** neste método — a ADR do seu projeto só precisa **adotá-las** (e ajustar o que o perfil exigir). As demais são específicas do seu contexto.

## Relação com as DEMs

- A `spec`/`design` de cada DEM **cita** as ADRs que a regem.
- O checklist de regressão arquitetural no fechamento confere que a entrega não violou nenhuma ADR `Accepted`.
