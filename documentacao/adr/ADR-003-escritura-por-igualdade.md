# ADR-003: Escritura por igualdade, não por similaridade

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

A busca de uma referência citada no plano (ex.: "João 3:16") era feita por
**similaridade semântica** usando a referência como consulta. Medido em produção:
`buscar('João 3:16')` devolvia **Mateus 4:12** e **João 4:1**, ambos acima do corte de
score — a lição exibiria o versículo errado.

## Decisão

Localizar uma passagem é **igualdade**: filtro por metadado exato
(`referencia = 'Joao 3:16'`). A similaridade continua existindo, mas só para
perguntar **por assunto**.

## Consequências

**Positivas:**
- Resultado exato, sem limiar de score, sem versículo trocado.
- Quando não encontra, devolve vazio em vez de errado.

**Negativas / trade-offs:**
- Depende do mapa canônico dos 66 livros e das 3 grafias próprias do corpus (Cantares, Abdias, Filemon).

## Impacto nas DEMs

- `escritura_service` e a integração de referências cruzadas.
- DEMs que exibam Escritura devem usar o caminho por igualdade.
