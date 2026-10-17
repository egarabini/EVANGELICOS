# ADR-006: Guard-rails de agente + TLC + arquivos de guarda

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

Agentes sem limites alucinam, quebram alinhamento e escalam privilégio. Já vivemos
os três: código inventado fora de escopo, deploy que derrubou produção e decisões de
escopo tomadas sem assinatura.

## Decisão

Adotar os quatro guard-rails (Think Before Coding, Simplicity First, Surgical
Changes, Goal-Driven) e o ritual **TLC** (Think → **List aprovado** → Code), com os
arquivos de guarda no repositório: `AGENTS.md`, `CONVENTIONS.md`,
`PROJECT_CONTEXT.md`.

## Consequências

**Positivas:**
- O agente declara plano antes de escrever; desvio fica auditável.
- Instruções duram mais que a sessão.

**Negativas / trade-offs:**
- Cerimônia extra em toda implementação.

## Impacto nas DEMs

- Toda DEM de código. Os guardas são lidos antes de qualquer escrita.
