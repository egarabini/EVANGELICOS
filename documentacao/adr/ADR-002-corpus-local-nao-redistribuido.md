# ADR-002: Corpus bíblico local, não redistribuído

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

A lição exibe Escritura verificada; o texto disponível é a **ACF 2007 + comentários
de Matthew Henry** (378 MB), que é tradução protegida por direitos autorais. Embutir
isso no repositório ou na imagem significaria redistribuir a obra.

## Decisão

O corpus fica **fora do git** e **fora da imagem**, montado no container como
`:ro` a partir de uma cópia na VPS. O app só lê.

## Consequências

**Positivas:**
- Não redistribui obra protegida.
- A imagem continua leve.

**Negativas / trade-offs:**
- Mais um passo manual de deploy (cópia do corpus para a VPS).
- Clone do repositório não traz o corpus; testes que dependem dele não rodam em CI.

## Impacto nas DEMs

- Deploy e importadores.
- Qualquer DEM que precise do corpus em CI precisa de fixture própria.
