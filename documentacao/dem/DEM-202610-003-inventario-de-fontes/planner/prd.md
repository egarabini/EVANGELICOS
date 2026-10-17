# PRD — DEM-202610-003 / inventário de fontes

> Dono: PLANNER. Escrito **após** o `intent.md` estar `signed`.

## 1. Referência

Intent: [`intent.md`](intent.md) — **signed** em 2026-10-17 (`open_questions_open: 0`)

## 2. Problema

A frente de base de conhecimento vai ingerir material de terceiros e **não existe
inventário**. Ninguém consegue responder, olhando o projeto, o que pode ser exibido ao
aluno, o que só pode ser lido internamente e o que não pode entrar. Cada ingestão refaz a
mesma análise, e o risco jurídico cresce a cada fonte.

## 3. Objetivo

Um **registro único e estruturado** de todas as fontes do acervo, onde cada uma tem
licença, regime de exibição, atribuição e decisão registrados — consultável antes de
qualquer ingestão, importável pela DEM-B sem retrabalho.

## 4. Componentes / atores afetados

- **ARQUITECT** — decide o que entra e revisa a adequação doutrinária.
- **PLANNER** — levanta, classifica e mantém o inventário.
- **REVISOR** (futuro) — assume a adequação doutrinária quando existir.
- **DEM-B, C e D** — passam a consultar o inventário em vez de redescobrir.

## 5. Critérios de sucesso (mensuráveis)

- [ ] **100% das fontes** do acervo catalogadas — nenhuma fonte sem linha.
- [ ] Toda linha tem **licença** ou a marca explícita *a confirmar* **com gatilho**.
- [ ] Toda linha tem **regime de exibição** e **decisão**; quando a decisão não é "entra",
      o **motivo** está escrito.
- [ ] **Zero contradições** com as 12 decisões da ADR-012.
- [ ] O arquivo é **CSV válido**, importável, com colunas conforme a spec.
- [ ] O ARQUITECT consegue responder "isso pode ser exibido ao aluno?" **sem abrir outro
      documento**.

## 6. Escopo

### Incluído

- catálogo de todas as fontes: corpus ACF, comentários, referências cruzadas, obra e
  adendos, os seis projetos de `estudos/`, e as fontes dos originais (SBL GNT, WLC, MorphGNT)
- a lista do que **não entra**, com motivo — inclusive o que já foi excluído por decisão
- um `README` curto explicando as colunas e como manter o inventário

### Fora do escopo (intent §4 Out)

- persistir o registro no banco (DEM-B)
- ingerir qualquer dado (DEM-C)
- busca e exibição (DEM-D)
- o agente DAVID (DEM-E)
- **verificar juridicamente** as licenças marcadas *a confirmar* — elas ficam com gatilho

## 7. Restrições

- **ADR-012** manda: nenhuma fonte "entra" sem licença registrada ou *a confirmar* com
  gatilho. Contradição detectada → para e reabre o intent.
- **Não toca código, banco nem produção.** Esta DEM produz documento e dado.
- **LGPD:** nenhum dado pessoal envolvido.
- **Sem prazo:** entrega por gate.

## 8. Dependências

- **ADR-012** — as 12 decisões que o inventário aplica linha a linha.
- **OLPF** da frente — origem do escopo e das fontes.
- **Acervo existente** — `estudos/` (6 projetos), corpus, `docs/base` da obra.
