# A camada INTENT

> **Intent é julgamento. Spec é contrato. São jobs diferentes.** O erro comum é deixar o PLANNER *decidir* o que só cabe ao ARQUITECT. O PLANNER **escreve** o rascunho; o ARQUITECT **assina** o objetivo.

## 1. O que é

Um **proto-spec**. Captura o que se quer, por quê, para quem, o que **não** se quer e quais restrições são inegociáveis. **Sem stack. Sem schema. Sem tasks.**

A spec descreve o software. O intent pergunta outra coisa:

> Por que estamos mudando o sistema, qual outcome precisa existir, o que precisa permanecer verdadeiro, e como vamos provar que o outcome aconteceu?

Sem essa camada, ARQUITECT + PLANNER convergem numa SPEC que **já é uma solução**. O PRD herda a solução, os DEMs a implementam, e ninguém no fim consegue responder *"isso ainda é o que queríamos?"*.

- **É artefato, não papel.** Nenhum agente novo.
- **Dono de escrita:** PLANNER (já é o escriba). **Dono de assinatura:** ARQUITECT (já é a origem).
- **Um intent por DEM:** `planner/intent.md`. Não um `intent.md` gigante do produto.

## 2. O que vai dentro / o que não vai

**Vai**

- Problema (o que dói hoje, com evidência — ticket/métrica/incidente, não hipótese).
- Outcome (estado **observável**, não feature).
- Quem é afetado (usuários + sistemas) e o que é **intocável**.
- Escopo / exclusões (**non-goals**).
- Constraints duras (o que o agente **não pode** violar).
- Health metrics (o que **não pode piorar**).
- Perguntas abertas (explícitas; ninguém inventa a resposta).
- Sinal de sucesso (como o ARQUITECT aceita — observável, não teste unitário).

**Não vai**

- Stack, lib, schema, endpoints.
- User stories, Gherkin, tasks.
- Arquitetura, ADRs, diagramas de componente.
- Estimativa, sprint, DEM.

> **Régua operacional:** se um implementer ainda precisaria perguntar *"mas o que a gente está tentando alcançar?"*, o intent **não** está pronto. Se o PLANNER ainda precisaria perguntar *"qual banco?"*, o intent está **no nível certo**. Se o PLANNER começou a escrever "vamos usar X com tabela Y", o arquivo virou spec → **rejeita**.

Tamanho: **≤ 1 página**. Passou disso, já está especificando.

## 3. Protocolo da sessão ARQUITECT ↔ PLANNER (antes de qualquer SPEC)

1. O ARQUITECT descreve o problema em **linguagem crua**. Sem formalismo.
2. O PLANNER pergunta como **analista**: quem sente, o que "melhor" significa em estado observável, o que está fora (mesmo "já que estamos nisso"), o que **não pode piorar**, o que **ainda não sabemos**.
3. O PLANNER **redige** `planner/intent.md` no template. **Não escolhe solução.**
4. O ARQUITECT corrige o que foi mal entendido. **Fecha** perguntas ou marca como abertas (§8).
5. O ARQUITECT muda `status: signed`. **Só então** o PLANNER está autorizado a abrir SPEC.

O PLANNER **para de perguntar** quando um implementer não precisaria mais de "o que estamos tentando alcançar?" — e ainda precisaria de "qual banco?". Se a segunda pergunta sumiu, virou spec.

## 4. Health metrics — o §6 do intent

O **outcome (§2) diz o que muda**; a **health metric (§6) diz o que não pode piorar**. Se os dois descrevem a mesma coisa, um deles está errado.

**Teste de admissão** (o PLANNER aplica; senão não entra no §6):

| Teste | Passa | Falha |
|---|---|---|
| Observável agora | tem baseline no disco/git ou em produção | "manter qualidade alta" |
| Independente do outcome | é outra variável | outcome reescrito como métrica |
| Violável por um DEM | EVAL/VISION/DEPLOY consegue FAIL | só o ARQUITECT "sente" |
| Barato de checar | comando, query, jornada existente | exige sistema novo (isso é outra DEM) |

**3 a 5 invariantes.** Mais que isso é spec disfarçada. Cada uma tem um **porteiro nomeado**:

```
Segurança / dados sensíveis → EVAL + gate ARQUITECT
Jornada existente           → EVAL em estado limpo
Performance / contrato      → EVAL (p95, suíte)
Tela adjacente              → VISION sobre hash, não sobre gosto
Publicação                  → DEPLOY (backup pareado, ambiente limpo)
Custo / tokens              → rollup no README da DEM
```

**Anti-padrões que o PLANNER recusa no §6:**

- Health metric = o próprio outcome ("clientes usam o portal").
- Health metric sem número **e** sem dono de checagem.
- "UX premium", "código limpo", "cobertura boa".
- Copiar o design system inteiro para o §6 (isso já é VISION).

## 5. Saúde do artefato — o intent está assinável?

**Isto NÃO vai no §6.** É checklist do PLANNER **antes** do `GATE: intent`. Se falhar, o arquivo continua `draft`.

| Sinal | Saudável | Doente |
|---|---|---|
| Outcome | estado observável | nome de feature |
| Non-goals | ≥1 real, que doía cortar | vazio ou tautológico |
| Constraints | duras, violáveis por agente | "seguir boas práticas" |
| Perguntas abertas | listadas, nenhuma respondida pelo PLANNER | 0 perguntas *e* 0 incerteza, ou PLANNER fechou sozinho |
| §9 Fora de julgamento | stack/schema/UX fora | já escolheu a tecnologia |
| Tamanho | ≤ 1 página | spec precoce |
| Rastreio | cada §6 tem porteiro | métrica órfã |
| Independência | ainda se perguntaria "qual banco?" | já não — virou spec |

> **Intent doente não se corrige na spec.** Reescreve o intent, ou não assina.

Dois números que o PLANNER cola no cabeçalho: `open_questions_open` (= 0 no signed, ou risco aceito) e `spec_citations` (= 100% depois da spec).

## 6. Como o EVAL encaixa, sem virar tribunal de gosto

> **Health metric do §6 que não gera critério no `plano-testes` não existe.**

Ao fechar a spec, o PLANNER **promove**:

```
intent §6 linha N  →  plano-testes caso H-N  →  EVAL PASS/FAIL sobre hash
```

Se não der para promover, a linha **sai** do intent (era desejo) ou vira **pergunta aberta** (§8).

- **VISION** só entra se a métrica for **regressão de tela fora** da DEM ("não piorar X"). Tela *da* DEM é critério de spec, não health.
- **DEPLOY** não ganha health de intent, salvo quando o outcome toca **publicação**.

Sinal de que o §6 está certo: **pelo menos um FAIL de EVAL na piloto nasce de uma health metric** (ou de um non-goal), não só de uma feature. Se isso nunca acontece, o parágrafo é literatura.

## 7. Ativação num projeto (sem quebrar o que já roda)

1. **Gate duro.** O PLANNER recusa abrir spec sem `intent.md` `signed` no mesmo slug.
2. **Um intent por mudança.** SPEC, PRD e DEMs daquela mudança apontam para o arquivo.
3. **Intent é estável, spec evolui.** Mudou o **porquê** → novo intent (ou `superseded`). Mudou o **como** → nova spec. Não misture.
4. **DEM piloto:** escolha uma com outcome claro e **tentação de inflar spec** (toda DEM com tela serve). Sucesso = a spec ficou **mais curta** e ≥1 "já que estamos nisso" morreu no §4 Out.

> Template: [`../templates/intent.md`](../templates/intent.md) · Métricas do gate: [metricas-de-governanca.md](metricas-de-governanca.md).
