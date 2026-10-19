# ADR-001: Stack fixa: Python/Reflex

- **Status:** Accepted — **Superseded in part by [ADR-014](ADR-014-saida-do-reflex.md)** (aceita em 2026-10-19; só a cláusula do **framework** é substituída)
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

A plataforma precisa de lições, progresso, correção humana e IA local. Já está
implementada e em produção com uma única linguagem. Toda tentativa de recomendação
externa sugeria front em React/Next — o que quebraria a stack.

## Decisão

Manter **Python 3.12 + Reflex** para front e back, PostgreSQL, ChromaDB e Ollama.
**Nada de Node/TS na aplicação** — Node existe apenas dentro da imagem, para o build
do frontend do Reflex.

## Consequências

**Positivas:**
- Uma linguagem para todo o produto; um runtime; deploy simples.
- O parser de referências já é Python e funciona.

**Negativas / trade-offs:**
- Reflex é nichado e tem ecossistema menor que React.
- Bibliotecas prontas em TS/JS (ex.: parsers bíblicos) não são usáveis.

## Impacto nas DEMs

- Toda DEM de código.
- Proíbe trocar a stack ou introduzir libs TS como dependência da aplicação.

