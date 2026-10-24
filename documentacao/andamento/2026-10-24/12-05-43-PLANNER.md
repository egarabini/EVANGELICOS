## PLANNER - DeepSeek

**O #11 mesclado (o `b5573bd`); a fatia 2 despachada; o deploy da homologação despachado.**

**O que foi feito e registrado nesta interação:**

- **O PR #11 (a fatia 1) MESCLADO** na develop: o merge commit **`b5573bd`** (24/10, 15:04 UTC), o CI
  verde no PR, **sem o `--admin`**.
- **A FATIA 2 despachada** (`dev/despacho-fatia2-estudo.md`):
  1. a **criação do Estudo** pelo Admin (o `/admin/estudos` + o `/admin/estudos/nova` — a obra
     aplicada em capítulos);
  2. as **avaliações/liberações** do Revisor (o `/revisor/avaliacoes`; o **ADR-020**: a assinatura do
     Revisor + a liberação do Admin; a **N imutável**; o **hash LF+NFC**);
  3. os **testes dos fake na lista** (o `/admin` — o "Aluno Fake A/B" com os resultados);
  - as **rotas novas na matriz** (sem teste vacuoso); o **EVAL cego** (o máximo de 2);
  - **o prompt para o DEVS está no despacho** (a regra: o despacho explica; o prompt é o que se envia).
- **O DEPLOY DA HOMOLOGAÇÃO despachado** (`dev/despacho-deploy-homolog-painel.md`): a develop
  pós-merge (o `b5573bd`); o `subir.sh --v1`; **a produção NÃO é tocada**; o **seed NÃO roda** (a
  dívida 15); **o prompt para o DEPLOY está no despacho**.
- **O defeito "volta à landing" segue A CONFIRMAR** — o endereço e os passos são do ARQUITECT.

**Pendente (a ordem):**

1. o **DEVS** da fatia 2 → o **EVAL cego** (o máximo de 2) → o **merge**;
2. o **DEPLOY** da homologação → a **validação do painel logado** pelo ARQUITECT;
3. o **1b** — só depois.
