# ADR-007: Estrutura de DEM + gate INTENT

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

A causa dos retrabalhos recentes não foi técnica: foi planejar o **como** antes de
assinar o **porquê**. O caso mais claro é o plano das bibliotecas v1 → v2: eu modelei o
schema, o ARQUITECT corrigiu o modelo do produto, e o schema foi refeito.

## Decisão

Toda mudança nasce de um `intent.md` (≤ 1 página, sem stack) assinado pelo
ARQUITECT. Sem `status: signed`, **nenhuma spec abre**. A DEM usa o pacote único de
pastas (`planner/`, `dev/`, `eval/`, `deploy/`, `vision/`).

## Consequências

**Positivas:**
- O *porquê* vira artefato, não memória de sessão.
- Spec enxuta: capacidade órfã é removida.

**Negativas / trade-offs:**
- Um passo a mais antes de qualquer código.

## Impacto nas DEMs

- Toda DEM. A DEM piloto é a primeira a rodar o ciclo completo.
