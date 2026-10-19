# ADR-011: Aprovação de conteúdo assinada e amarrada ao hash

- **Status:** Accepted — **emenda em proposta: [ADR-019](ADR-019-fluxo-de-obras-e-estudos.md)** (a assinatura como intervalo do ciclo de revisão, com os dois hashes)
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

A Ação 1 (o Administrador e o Revisor avaliam e liberam o estudo) é um **fluxo
humano sem evidência**: não há registro verificável de quem aprovou o quê. Pior: se o
conteúdo mudar depois, a aprovação continua "valendo" — aprovação sem amarração ao
conteúdo é teatro. O estudo pode nascer de uma ferramenta de transformação, o que
aumenta o risco de erro doutrinário.

## Decisão

A aprovação registra **revisor + data + hash do conteúdo**. A transição do estudo
para `liberado` é **bloqueada no código** sem assinatura válida para o hash **atual**;
qualquer mudança de conteúdo invalida a aprovação automaticamente. Revisão em lote com
amostragem fica como **opção futura** (hoje são 34 capítulos: revisa-se 100%).

## Consequências

**Positivas:**
- Prova verificável de aprovação, alinhada à regra 9 do método (veredito amarrado a hash).
- Impede publicar conteúdo alterado sob aprovação antiga.

**Negativas / trade-offs:**
- Mais um campo e um guard de transição no modelo do Estudo.
- Revisão vira etapa bloqueante de verdade — inclusive para o ARQUITECT.

## Impacto nas DEMs

- **DEM piloto** (Estudo).
- Refina a ADR-005; não a substitui.

