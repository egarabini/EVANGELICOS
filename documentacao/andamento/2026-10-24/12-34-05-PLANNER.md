## PLANNER - DeepSeek

**A homologação do painel no ar (o `b5573bd`); o próximo é a validação do ARQUITECT.**

**O deploy (o DEPLOY, na homologação):**

- a develop **pós-merge** (o **`b5573bd`**) no ar em `homolog.didasko.app.br` — o **HEAD conferido
  antes** do deploy;
- o **`subir.sh --v1`** recriou **só** a `app-v1` e o `landing`; o **`postgres-v1`** e o **Traefik**
  ficaram **intocados**;
- **o seed NÃO rodou** — o banco já tinha os **7 usuários** (a **dívida 15 preservada**);
- **a produção intocada** (o `didasko_app`/o `didasko_landing`/o `didasko_postgres` e o Traefik **sem
  alteração**).

**A conferência anônima** (o DEPLOY): o `/` **200**; o `/homenagens` **200**; o `/login` **200**; o
`/admin` **401**; o `/admin/obras` **401**.

**O próximo — do ARQUITECT:**

- a **validação do painel logado** (o **Admin** e o **Revisor**) na **janela anônima**;
- o que olhar: o `/admin` (as obras/os coordenadores/os instrutores/os alunos), o `/revisor` (a
  fila/o histórico), o **menu por perfil**, o **"Alterar senha"** e o **"Sair"**.

**O estado:**

- o **EVAL cego da fatia 2** (o `13de3de9`) segue **rodando** — o parecer chega por mensagem;
- o defeito **"volta à landing"** segue **A CONFIRMAR** — o endereço e os passos do ARQUITECT;
- o **1b** — só depois.

**Pendente:** o **parecer do EVAL** → a **sua decisão** (o merge do #12) → a **validação do painel
logado** → o **1b**.
