# ADR-020: A autoridade na obra e a disponibilidade (emenda a 011 e 019)

- **Status:** **Accepted** — decisão do ARQUITECT em **2026-10-19**.
- **Data:** 2026-10-19
- **Decisores:** ARQUITECT (Eduardo) · redação do PLANNER
- **Gatilho:** Operação — a semântica de quem pode o quê na obra e o que é a "disponibilidade"
- **Emenda (explícita):** **[ADR-011](ADR-011-aprovacao-de-conteudo-assinada.md)** (a liberação depende
  dos dois) e **[ADR-019](ADR-019-fluxo-de-obras-e-estudos.md)** (o `contestar` do Revisor vira
  **solicitação de revisão**, decidida pelo Admin; a salvaguarda do "contestar" muda)

---

## Decisão

1. **O registro da obra é do Admin**, e **toda alteração é dele**.
2. **A liberação depende dos dois**: a assinatura válida do Revisor **para a versão vista** **e** a
   liberação do Admin. É o **único bloqueio duro**; não existe "forçar liberação".
3. O Revisor é **auxiliar de qualidade**: parecer, ajustes propostos, assinatura e **solicitação de
   revisão**. Ele **não** muda estado nem disponibilidade.
4. **A versão liberada N é imutável.** Todo ciclo de revisão cria a **N+1**.
5. Havendo necessidade de revisão numa obra liberada, ela fica **suspensa para novos alunos**; quem já
   usa continua na versão em que está e recebe o aviso de que uma nova versão está a caminho. A N fica
   **`substituida`** quando a N+1 é liberada, e continua **legível** por quem está fixado nela.
6. **A disponibilidade é um conceito próprio** (não o status da versão):
   `aberta` | `suspensa_para_novos`. Vai a suspensa quando o Admin **abre um ciclo** (o `alterar` ou o
   `aceitar` de uma solicitação); volta a aberta ao **liberar a N+1** ou ao **cancelar o ciclo**.
7. **A `contestar` do Revisor vira `solicitar_revisao`** — um pedido registrado. Só o Admin decide:
   **aceitar** (a N+1 em revisão + a suspensão) ou **dispensar** (**motivo obrigatório**, visível ao
   Revisor). Só o Admin abre, suspende, cancela e libera.
8. **A vinculação e a atribuição são fixadas em `versao_id`.** A suspensão bloqueia **novas**
   vinculações/atribuições, não as existentes.
9. *(Opcional)* O Revisor pode **registrar uma posição** (`concordo`/`objeto`, com texto) sobre as
   decisões do Admin — visível na trilha e ao Admin, **sem bloquear**. **Adotado** (o custo é um tipo
   de evento).
10. **A 9.2 da DEM-005 fica superada no que toca à suspensão**: a versão liberada **não** fica
    disponível para novos — quem já está fixado continua; os novos aguardam a N+1.

## Consequências

- **A v5 do design está substituída** (a mesma versão voltar a `em_revisao`); o F-06 do plano estava
  errado — o código do Codex que criava uma versão nova era o comportamento correto.
- O **status `substituida`** ganha uso; a imutabilidade da N é uma regra de aplicação (o trigger/ACL
  contra SQL direto é do deploy da v1).
- O **Revisor perde o poder de retirar a obra do ar** — e ganha a **solicitação** e a **posição**
  registradas. A salvaguarda da ADR-019 deixa de ser um botão que suspende: passa a ser um **pedido**
  que o Admin decide.
- O **aluno já vinculado** não perde a versão; o **novo aluno** espera. É a regra 4 na prática.

## Referências

[ADR-011](ADR-011-aprovacao-de-conteudo-assinada.md) · [ADR-019](ADR-019-fluxo-de-obras-e-estudos.md) ·
[DEM-011](../../dem/DEM-202610-011-fluxo-de-obras-e-estudos/planner/design.md) (o design v7) ·
[DEM-005](../../dem/DEM-202610-005-saida-do-reflex/planner/spec.md) (o 9.2 superado em parte)
