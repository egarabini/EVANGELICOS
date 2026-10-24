## PLANNER - DeepSeek

**A fatia 1 da DEM-017 — o fix das 4 ressalvas registrado; o ponto de retomada.**

**O que foi feito e registrado nesta interação:**

- **O fix das 4 ressalvas aplicado** (o `a18fcb1`; o CI `40100843953` — **277 da v0 + 172 da v1**):
  1. **as casas POR VERSÃO** — as chaves seguem compartilhadas no `rbac.py`; o `HOME_DO_PAPEL` da v0
     **voltou ao que era** (o REVISOR → o `/admin`, a v0 congelada); a v1 ganhou o **`HOME_DO_PAPEL_V1`**
     (o REVISOR → o `/revisor`); o teste **"revisor entra: 9.2a" REVERTIDO** (não relaxado); a
     **invariante da casa em cada mapa** (o `test_invariante_casa_do_papel` + o `test_rf02_invariante_casa_v1`);
  2. **a cobertura** — o `test_painel_admin` cobre a **obra disponível** (o `versao_liberada_id` + a
     `aberta`), o **`completed=True`** e o **`recusada`**;
  3. **o `VinculoObra` renderizado** ("Obras vinculadas") — a recomendação do PLANNER;
  4. **o "Alterar senha" e o "Sair" no menu de TODOS os papéis** (o ADMIN, o REVISOR, o COORDENADOR, o
     INSTRUTOR e o ALUNO) — **com teste por papel**; o restante do menu dos demais papéis fica na
     fatia 3.
- **O registro**: a correção na **jornada do parecer** (`eval/jornada-painel.md`) e no **andamento do
  dia**.
- **O CI**: o `40100843953` `SUCCESS` (**277 v0 + 172 v1**).

**O estado:**

- o **PR #11** pronto — **sem o EVAL** (a conferência rápida, não uma rodada 2) e **sem o `subir.sh`**;
- a **produção segue na `v0.1.1`** (a landing no ar);
- o defeito **"volta à landing"** segue **A CONFIRMAR** — o endereço e os passos são do ARQUITECT;
- a **dívida 15** (o seed dos fake na homologação) segue aberta — a (b) e a (c).

**Pendente (a ordem):**

1. a **conferência rápida do ARQUITECT** (a suíte da v0 intacta — o Revisor no `/admin`; o menu por
   papel; a casa por versão — a v0 no `/admin`, a v1 no `/revisor`);
2. a **ordem do merge** do #11;
3. a **fatia 2** da DEM-017 (a criação do Estudo + as avaliações/liberações + os testes dos fake);
4. o **1b** (o Zitadel) — depois, com as pendências dele (a infra do `oidc` e o AGPL).
