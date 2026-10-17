# Template — `planner/intent.md`

> Copie o bloco abaixo para `planner/intent.md` da DEM. **Um por DEM. Curto (≤ 1 página). Sem stack.**
> Dono de escrita: **PLANNER**. Dono de assinatura: **ARQUITECT**. Guia: [camada-intent.md](../03-camada-intent/camada-intent.md).

```markdown
# Intent: DEM-0xx / <slug>

status: draft | signed | superseded
owner: PLANNER
signed_by: ARQUITECT
origin: ideia | incidente | ticket | métrica | ADR
signed_at:
supersedes:
open_questions_open:      # nº — deve ser 0 no signed (ou risco aceito pelo ARQUITECT)
spec_citations:           # % das capacidades da spec que citam §2/§4 Out/§5 — 100% ao fechar a spec

## 1. Problema
O que dói, quem sente, evidência (ticket/métrica/incidente). Não hipótese solta.

## 2. Outcome
Estado observável quando isso existir. Frase de resultado, não de feature.
Ruim: "adicionar dashboard de status"
Bom:  "o cliente vê status, próximo passo e data esperada sem ligar"

## 3. Afetados
Usuários, papéis, sistemas tocados.
Intocáveis: …

## 4. Escopo
In:
-
Out (non-goals):   # ≥1 real, que doía cortar
-

## 5. Constraints (duras)
O que nenhum agente pode violar (autenticação existente, dados sensíveis, contrato/API intocável, requisitos legais).

## 6. Health metrics
O que não pode piorar enquanto o outcome é perseguido.
3 a 5 invariantes; cada uma com número (baseline no disco) e porteiro nomeado.
baseline em: planner/intent-health.md (ou número inline)

- <invariante> · baseline <número + fonte> · porteiro <EVAL|VISION|DEPLOY>

## 7. Sinal de sucesso
Como o ARQUITECT aceita o resultado. Observável (produção ou aceite).
Não é a suíte de testes — isso é o plano-testes.

## 8. Perguntas abertas
Só o ARQUITECT fecha. PLANNER lista, nunca responde.
- [ ]

## 9. Fora de julgamento
O que este intent NÃO toma: stack, schema, UX detalhada, tasks.
```

---

## Exemplo no tamanho certo

```markdown
# Intent: autoatendimento de status de solicitação
status: draft · owner: PLANNER · origin: métrica

## 1. Problema
Clientes ligam para a central para saber onde está a solicitação.
~1/3 do tempo de atendimento é consulta de status.

## 2. Outcome
Cliente vê status, próximo passo e data esperada no portal.

## 3. Afetados
Atendentes, time do portal, o serviço de solicitações.
Intocáveis: autenticação atual.

## 4. Escopo
Out (non-goals):
- Notificação proativa (e-mail/SMS) — outra DEM.

## 5. Constraints
Nenhum dado sensível novo na sessão do portal. Só a autenticação existente.

## 8. Perguntas abertas
- [ ] Parceiros externos também precisam de acesso?
```

Curto de propósito. Se o arquivo passou de ~1 página, já está especificando → **rejeita**.

## Checklist do PLANNER antes do `GATE: intent`

Ver a tabela de **saúde do artefato** em [camada-intent.md §5](../03-camada-intent/camada-intent.md). Resumo: outcome observável · ≥1 non-goal real · constraints violáveis por agente · nenhuma pergunta fechada pelo PLANNER · §9 sem stack/schema · ≤1 página · cada §6 com porteiro. **Falhou algum → continua `draft`.**
