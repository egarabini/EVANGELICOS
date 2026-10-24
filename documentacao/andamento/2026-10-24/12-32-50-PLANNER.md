## PLANNER - DeepSeek

**O EVAL cego da fatia 2 disparado (o subagente `13de3de9`); o que ele vai julgar e o que esperar.**

**O disparo (é o PLANNER quem dispara o EVAL):**

- o **EVAL cego** da fatia 2 (o PR #12, o `3e0e48f`; o CI `40106321822` — **277 v0 + 213 v1**) —
  disparado como **subagente** (`13de3de9`), com o **briefing** escrito em
  `eval/briefing-eval-fatia2-estudo.md`;
- **o que ele julga** (10 critérios): a **criação do Estudo** (o POST → 303; as 3 entidades); a
  **fila do Revisor**; o **parecer**; a **liberação pelos dois** (o Admin sozinho → 409); a **N
  imutável**; o **hash LF+NFC**; os **fake na lista** (o `Progress`/o `UserResponse`); o **menu**
  (o ADMIN → o Estudos; o REVISOR → as Avaliações); a **matriz** (o permitido **e** o negado + a
  vacuidade); os **277/213** e o CI.

**O padrão do registro (o que fica combinado):**

- **a cada disparo/entrega, o PLANNER registra no `andamento/`** — o dia na pasta, o `HH-MM-SS-PLANNER.md`,
  o `## PLANNER - DeepSeek` e o resumo do que foi feito;
- **o EVAL disparado** (este registro) → **o parecer do EVAL** (o próximo registro, quando ele voltar)
  → **a correção/a decisão**.

**O estado:**

- a **produção segue na `v0.1.1`**; o **deploy da homologação** tem o despacho pronto
  (`dev/despacho-deploy-homolog-painel.md`);
- o defeito **"volta à landing" segue A CONFIRMAR** — o endereço e os passos do ARQUITECT;
- o **1b** — só depois.

**Pendente:** o **parecer do EVAL** → a **sua decisão** (o merge do #12) → o **deploy da homologação**
→ a **validação do painel logado** → o **1b**.
