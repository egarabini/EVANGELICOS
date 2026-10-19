# Intent: DEM-202610-011 / fluxo-de-obras-e-estudos

status: signed
owner: PLANNER
signed_by: ARQUITECT
origin: decisão do ARQUITECT (19/10) — o fluxo de obras e estudos; substitui o escopo antigo da DEM-011 ("aprovação em dupla")
signed_at: 2026-10-19
supersedes: o escopo anterior ("aprovação em dupla do estudo") — o fluxo o engloba
open_questions_open: 0
nivel_agil: 3 — aprovação e dados
nota: implementa a **D-07** e a **ADR-011** (com a emenda do §9.1). É construída **na v1** (DEM-005) — não há o que migrar.

## 1. Problema

Hoje o estudo tem **uma** aprovação — o admin sozinho — e as **obras não têm fluxo de revisão**.
O revisor não tem papel no caminho, e a ADR-011 (assinatura + data + hash) **não está
implementada**. O resultado é o que a D-07 registra: o admin libera sozinho, sem revisão nem
rastro de conteúdo.

## 2. Outcome

**O fluxo de obras e estudos, em cinco passos, com os estados visíveis:**

1. o **Admin** importa e disponibiliza → **`em_revisao`**;
2. o **Revisor** avalia primeiro, registra o **parecer** e os **ajustes propostos**, e libera →
   **`aguardando_admin`**;
3. o **Admin** lê o parecer, **descreve e implementa os ajustes**, e libera para a plataforma →
   **`liberada`**;
4. o **Coordenador** **vincula/desvincula** ao seu ambiente e **ajusta os adendos** — autonomia e
   responsabilidade dele sobre como a obra é trabalhada no ambiente;
5. toda alteração da obra é do **Admin** e, **depois de liberada, volta como pendente de revisão**.

## 3. Afetados

O **admin** (importa, ajusta, altera), o **revisor** (o parecer), o **coordenador** (a vinculação
e os adendos), o **instrutor e o aluno** (recebem a versão liberada), o catálogo e a API.

## 4. Escopo

**In**
- os **estados** `em_revisao`, `aguardando_admin`, `liberada` (e o "pendente de revisão" da
  alteração) e as **transições** com as permissões;
- o **parecer** do revisor com os ajustes propostos;
- o **hash por versão** e o **registro da diferença** entre a versão vista pelo revisor e a
  liberada pelo admin (a emenda da ADR-011, §9.1);
- a **versão liberada disponível** enquanto a alterada espera revisão (o coordenador adota);
- os **adendos por ambiente** (a sobreposição; não alteram a obra base; identificados como do
  coordenador);
- o **portão de licença**: só se importa obra cuja fonte esteja **`entra`** no inventário (DEM-003);
- as **telas** do fluxo (admin/revisor/coordenador) — construídas na v1.

**Out (non-goals)**
- a **busca** (DEM-D), o **DAVID** (DEM-E);
- o **multi-ambiente real** (D-06) — o adendo por ambiente nasce com o ambiente único; o
  isolamento completo fica com o gatilho do D-06;
- a **publicação** (é do DEPLOY, ADR-016);
- a migração de obra/estudo já existente (os dados são de teste, limpos na virada).

## 5. Constraints

- **A ADR-011, com a emenda**: os ajustes **dentro do ciclo** não reabrem a revisão e ficam
  registrados com a **diferença** (hash da versão vista pelo revisor × a liberada); a regra 5 vale
  **depois de `liberada`**. A alternativa é a reassinatura — decisão do §9.1.
- **O portão de licença é bloqueante**: a fonte fora do inventário (`nao_entra`) não é importada —
  a decisão é da ADR-012 e não se contorna na tela.
- **A v1 é a base** (ADR-014 v3): o fluxo nasce em FastAPI/Jinja2/HTMX, não no Reflex.
- **Nível 3** (ADR-018): aprovação e dados — o processo cheio.

## 6. Health metrics

- **H-14** · o fluxo completo por papel: admin (`em_revisao`) → revisor (`aguardando_admin`) →
  admin (`liberada`) · baseline **não existe** · porteiro **EVAL**
- **H-15** · alteração depois de `liberada` **volta para revisão** (não substitui em silêncio) · baseline **não existe** · porteiro **EVAL**
- **H-16** · a importação de fonte **fora** do inventário é **bloqueada** · baseline **não existe** · porteiro **EVAL**
- **H-01** · a suíte verde · porteiro **EVAL**

## 7. Sinal de sucesso

O admin importa, o revisor opina, o admin ajusta e libera — e **o histórico mostra as duas
assinaturas e os hashes das versões**. O coordenador vincula a obra ao seu ambiente, ajusta os
adendos, e uma alteração posterior **não passa** sem a revisão.

## 8. Decisões já registradas (o fluxo do ARQUITECT, 19/10)

| # | Questão | Decisão |
|---|---|---|
| 8.1 | Os passos | **admin → revisor → admin → liberada**; o coordenador vincula/adenda |
| 8.2 | O parecer | o revisor registra o parecer **e os ajustes propostos** |
| 8.3 | A autonomia do coordenador | vincula/desvincula ao ambiente e **ajusta os adendos** |
| 8.4 | A alteração | é do **admin**; **depois de liberada**, volta como **pendente de revisão** |
| 8.5 | O portão de licença | só entra obra com a fonte **`entra`** no inventário |

## 9. Decisões (fechadas pelo ARQUITECT em 2026-10-19)

| # | Decisão |
|---|---|
| **9.1 (a)** | os ajustes **dentro do ciclo** não reabrem a revisão; a **diferença** (hash da versão vista pelo Revisor × a liberada pelo Admin) fica registrada; a regra 5 vale **depois de `liberada`** |
| **9.2** | a versão `liberada` **permanece disponível** enquanto a alterada espera revisão; o coordenador **adota quando quiser** |
| **9.3** | os adendos são **sobreposição por ambiente**, identificados como **do coordenador**; não alteram a obra base nem passam por revisão; o isolamento multi-ambiente fica com o gatilho do D-06 |
| **9.4** | portão de licença em **duas etapas**: **`nao_entra` bloqueia na importação** (o `em_revisao` não nasce) e **`depende` bloqueia na liberação** (revisa, mas não libera até a fonte virar `entra`) |
| **9.5** | o coordenador define **quais capítulos, em que ordem e com qual calendário** — em **fatia posterior** (nível 2), com o padrão "obra inteira, na ordem da obra, sem calendário"; o plano **nunca** altera a obra base |

**Status:** o intent passa a `signed` — as 4 perguntas estão fechadas; o próximo passo é a spec.

## 10.## 10. Fora de julgamento

A estrutura das telas, o formato do parecer, o nome dos estados (internal), a linguagem do hash.


