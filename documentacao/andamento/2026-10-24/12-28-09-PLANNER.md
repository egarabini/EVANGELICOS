## PLANNER - DeepSeek

**A fatia 2 entregue (o PR #12) e o EVAL cego disparado.**

**O que foi feito e registrado nesta interação:**

- **A FATIA 2 no PR #12** (o `3e0e48f`; o CI `40106321822` — **277 v0 + 213 v1**; a branch nova a
  partir do `b5573bd`):
  1. **a criação do Estudo** (o `/admin/estudos` + o `/admin/estudos/nova`; o POST → 303; o `Estudo` +
     o `EstudoCapitulo` + o `EstudoVersao` N=1);
  2. **as avaliações/liberações** (o `/revisor/avaliacoes`; o **ADR-020**: a assinatura do Revisor + a
     liberação do Admin; o **Admin sozinho → 409**; a **N imutável**; o **hash LF+NFC**);
  3. **os fake na lista** (o `GET /admin` → o "Aluno Fake A/B" + o `Progress` + o `UserResponse`);
  - o **menu** (o ADMIN vê o "Estudos"; o REVISOR vê as "Avaliações"); a **matriz** (a 15 + a
    vacuidade).
- **O EVAL cego disparado** (`13de3de9`) — o briefing escrito (`eval/briefing-eval-fatia2-estudo.md`).
- **O defeito "volta à landing" segue A CONFIRMAR** — o endereço e os passos do ARQUITECT.
- **O deploy da homologação**: o despacho **pronto** (`dev/despacho-deploy-homolog-painel.md`) — a ser
  entregue ao DEPLOY.

**Pendente (a ordem):**

1. o **EVAL** → o **merge** (a ordem do ARQUITECT);
2. o **DEPLOY** da homologação → a **validação do painel logado**;
3. o **1b** — só depois.
