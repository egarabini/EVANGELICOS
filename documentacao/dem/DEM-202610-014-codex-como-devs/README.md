# DEM-202610-014 — O Codex acumula DEVS e DEPLOY

## Decisão (2026-10-19)

O **Codex** é o executor dos papéis **DEVS** e **DEPLOY** neste projeto. Ele já é DEVS no outro
projeto do ARQUITECT e funciona bem; aqui ele também conduz o deploy, para simplificar a operação
da VPS. **É uma decisão de processo, não um experimento** — não há métrica de piloto nem parecer
comparativo.

## Os gates que preservam a independência

O que separa **quem implementa** de **quem publica** não é o runtime — é a sequência de gates:

| Gate | De quem |
|---|---|
| **O Codex implementa** (DEVS): branch + PR | Codex |
| **EVAL cego** julga o código pelo plano de testes da DEM | EVAL |
| **CI verde** no PR | CI |
| **Aceite na tag** | **ARQUITECT** |

A **ADR-016 segue inteira**: o DEPLOY só publica **tag já aceita** — e **na DEM que o Codex
implementa não há tag nem publicação**. Isso é o que impede o executor de ser juiz do próprio
trabalho.

## A DEM-012

É a próxima DEM, implementada pelo Codex. O pacote está em
[`DEM-202610-012`](../DEM-202610-012-credencial-de-seed/planner/intent.md) (intent assinado,
spec e plano revisados). O EVAL julga; o merge é pelo CI; a tag e a publicação ficam para o
release.

## Estado

- [x] Decisão registrada (19/10).
- [x] O pacote da DEM-012 pronto.
- [ ] A DEM-012 executada pelo Codex (branch + PR).
- [ ] O EVAL + o CI + o aceite.
