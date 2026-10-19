# Intent: DEM-202610-014 / codex-como-devs-e-deploy

status: signed
owner: PLANNER
signed_by: ARQUITECT
origin: decisão do ARQUITECT de 2026-10-19
signed_at: 2026-10-19
supersedes: —
open_questions_open: 0
nivel_agil: 1 — decisão de processo, não código de produto
nota: o Codex roda na máquina do ARQUITECT, em sessão própria; o modelo e a conta são informados por ele. A DEM-012 é a próxima DEM executada por ele.

## 1. Problema

O papel **DEVS** e o papel **DEPLOY** são papéis, não runtimes. O Codex já é DEVS no outro
projeto do ARQUITECT e funciona bem; manter dois runtimes diferentes aqui só para separar
implementar de publicar acrescenta operação sem acrescentar segurança.

## 2. Decisão

**O Codex acumula DEVS e DEPLOY** neste projeto. A independência entre **implementar** e
**publicar** é garantida pelos **gates**, não pelo runtime:

- **EVAL cego** julga o código (o plano de testes da DEM);
- **CI verde** é o portão do merge;
- **o aceite na tag é do ARQUITECT** — a ADR-016 segue: o DEPLOY só publica **tag já aceita**;
- **na DEM que ele implementa não há tag nem publicação**.

## 3. O que não muda

- A ADR-016 (publicação pelo CI, tag já aceita, os gates).
- O fluxo branch + PR; o EVAL cego; o CI.
- As rodadas e os defeitos do EVAL ficam no **registro normal** — sem métrica de piloto.

## 4. Fora de escopo

- **Métricas de piloto e parecer comparativo** — a decisão não é experimento.
- O Codex publicar a **própria** DEM (a tag é do release, com o aceite do ARQUITECT).

## 5. Sinal de sucesso

A DEM-012 sai do Codex, passa pelo EVAL e pelo CI, e a tag/ publicação acontece só no release
— com o aceite do ARQUITECT. O executor não é juiz do próprio trabalho.
