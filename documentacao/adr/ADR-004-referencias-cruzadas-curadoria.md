# ADR-004: Referências cruzadas do OpenBible e sua curadoria

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

O OpenBible publica ~344 mil referências cruzadas (CC-BY 4.0, base no *Treasury
of Scripture Knowledge*). Os votos são um **saldo** (mínimo −86): sem piso, uma
relação **rejeitada** pela comunidade entraria na lição. No corte de votos ≥ 10 a
média era de 21,7 passagens por citação.

## Decisão

Adotar o dado com **piso de votos ≥ 10** e **teto de 5 passagens por lição**, em
rodízio entre as citações do plano, com a **atribuição CC-BY no próprio bloco
renderizado**.

## Consequências

**Positivas:**
- Enriquece a lição com dado verificado, não com texto gerado.
- 96,6% das citações dos planos têm candidato.

**Negativas / trade-offs:**
- Usa apenas 13% do dado (45.036 de 344.799 pares).
- Depende do mapa canônico (mesmo da ADR-003).

## Impacto nas DEMs

- `referencias_cruzadas_service` e o importador do TSV.
