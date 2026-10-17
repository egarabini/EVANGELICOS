# Intent: DEM-202610-003 / inventario-de-fontes

status: signed
owner: PLANNER
signed_by: ARQUITECT
origin: OLPF da base de conhecimento + ADR-012 (política de fontes)
signed_at: 2026-10-17
supersedes: —
open_questions_open: 0
spec_citations: 100% — todo RF de `spec.md` cita §2, §4 In, §5 ou uma decisão do §8
nota_de_assinatura: as três questões foram fechadas pelo ARQUITECT em 2026-10-17; na 8.3 ele delegou a classificação doutrinária ao PLANNER ("pode colocar o que você interpretar e na revisão vamos adequar").

## 1. Problema

A frente de base de conhecimento vai ingerir material de terceiros, e **não existe
inventário**: ninguém consegue responder, olhando o projeto, *o que pode ser exibido, o que
só pode ser lido internamente e o que não pode entrar*.

Isso já custou tempo de verdade: a OLPF teve que perguntar o que fazer com `lff`/`sangue`,
com o atlas (que traz deuterocanônicos) e com o ACF. Sem inventário, cada ingestão refaz a
mesma análise e o risco jurídico cresce a cada fonte adicionada.

## 2. Outcome

O ARQUITECT abre **um documento único** e vê, para cada fonte do acervo: o que é, de quem
é, a licença, o regime de exibição, a atribuição exigida, a adequação doutrinária e a
decisão (**entra · não entra · depende**). **Nenhuma fonte fica sem classificação**, e o
que não entra tem o motivo escrito ao lado.

## 3. Afetados

ARQUITECT e PLANNER (decidem e mantêm), REVISOR (adequação doutrinária), e as DEMs
seguintes da frente (B a D), que passam a consultar o inventário em vez de redescobrir.

**Intocáveis:** o código da aplicação, o corpus e a produção — esta DEM não escreve neles.

## 4. Escopo

**In**
- catálogo de **todas** as fontes: corpus ACF, referências cruzadas OpenBible, obra e
  adendos, os seis projetos de `estudos/`, e as fontes dos originais (SBL GNT, WLC, MorphGNT)
- por fonte: identificação, titular, licença, condição de uso (trecho curto · integral
  interno · não exibir), atribuição exigida, versão/data, adequação doutrinária, decisão
- a lista do que **não entra**, com o motivo

**Out (non-goals)**
- persistir o registro no banco — é a **DEM-B**
- ingerir qualquer dado — é a **DEM-C**
- busca — é a **DEM-D**
- assistente do aluno — é a **DEM-E**
- verificar juridicamente as licenças "a confirmar" — viram pendência explícita com gatilho

## 5. Constraints (duras)

- Nenhuma fonte recebe "entra" sem **licença registrada**, ou marcada como *a confirmar*
  **com gatilho de revisão**.
- Não contrariar a ADR-012. Se uma linha do inventário contradisser, **para e reabre** este
  intent — não ajusta a política em silêncio.
- Esta DEM **não** toca código, banco nem produção.
- Nenhum dado pessoal envolvido (LGPD não se aplica a esta DEM).

## 6. Health metrics

- **H-01** · a suíte continua verde · baseline **82 testes** (`pytest tests`) · porteiro **EVAL**
- **H-02** · a lição do Cap. 21 e o corpus intocados · baseline **HTTP 200 + "João 3:16"** (verificado em produção) · porteiro **EVAL**
- **H-03** · nenhuma das 12 decisões da ADR-012 contradita no inventário · baseline **0 contradições** · porteiro **EVAL**

## 7. Sinal de sucesso

O ARQUITECT percorre o inventário e responde, para **qualquer** arquivo do acervo, *"isso
pode ser exibido ao aluno?"* — sem abrir um segundo documento. Isso é o aceite.

## 8. Perguntas abertas — fechadas pelo ARQUITECT em 2026-10-17

**Nenhuma aberta.**

| # | Pergunta | Decisão |
|---|---|---|
| 8.1 | Documento ou dado estruturado? | **Dado estruturado (CSV)**, para a DEM-B importar direto. |
| 8.2 | Fontes internas com o mesmo peso? | **Sim, mesmo peso** das externas. Sem anexo. |
| 8.3 | Quem atesta a adequação doutrinária? | **O PLANNER preenche com a sua interpretação**; o ARQUITECT revisa e ajusta o que for necessário. |

## 9. Fora de julgamento

Stack, schema, tabelas, telas, motor de busca e decomposição em tarefas.
