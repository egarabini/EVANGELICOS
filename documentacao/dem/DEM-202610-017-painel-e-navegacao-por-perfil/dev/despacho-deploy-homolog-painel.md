# Despacho ao DEPLOY — a homologação do painel (a develop pós-merge)

> **O ARQUITECT valida o painel logado.** A **produção NÃO é tocada.**

## 1. O alvo

- o clone **`/home/didasko-deploy/homolog-v1`**;
- a **`develop` pós-merge** do #11 — o **`b5573bd`**;
- o **`.env.v1-homolog`** (o `DATABASE_URL` do `didasko_v1`, o `LANDING_LOGIN_URL`, o
  `SESSION_SECRET`).

## 2. O que fazer

1. o `git fetch origin` + o `git switch --detach origin/develop`;
2. **conferir o HEAD**: o `git log --oneline -1` → o **`b5573bd`** (a lição do "não mudou": o clone
   **antes** do `subir.sh`);
3. o **`bash deploy/subir.sh --v1`** (o `--force-recreate` **só** a `app-v1` e o `landing`; o
   Traefik **não** reinicia; a produção **não** é tocada);
4. **NÃO rodar o seed** dos fake — a **dívida 15** (o seed exige a obra liberada; a decisão é do
   ARQUITECT).

## 3. A conferência

- o `/` → **200**; o `/homenagens` → **200**; o `/login` → **200**;
- o `/admin` → **401** (o anônimo);
- o `/admin/obras` → **401** (o anônimo);
- **o registro**: o HEAD (o `b5573bd`), os 200s/401, os `StartedAt` (o `app-v1`/o `landing`
  recriados; o `postgres-v1`/o Traefik intocados).

## 4. O prompt para o DEPLOY

```text
O DEPLOY: a homologacao do painel (a develop pos-merge, o b5573bd).

O ALVO: o clone /home/didasko-deploy/homolog-v1; a develop pos-merge (o b5573bd); o .env.v1-homolog.

1. O git fetch + o git switch --detach origin/develop.
2. CONFERIR o HEAD: o git log --oneline -1 -> o b5573bd (antes do subir.sh).
3. O bash deploy/subir.sh --v1 (o --force-recreate so a app-v1 e o landing; o Traefik NAO reinicia; a
   producao NAO e tocada).
4. NAO rodar o seed dos fake (a divida 15).

A CONFERENCIA: o / 200; o /homenagens 200; o /login 200; o /admin 401 (o anonimo); o /admin/obras
401. O registro: o HEAD, os 200s/401, os StartedAt.

NAO: a producao; o seed; o Traefik.
```

## 5. O que o ARQUITECT valida depois

- o **painel logado** (o `/admin` e o `/revisor` com o menu por perfil) — na **janela anônima**;
- o **"Alterar senha"** e o **"Sair"** em todos os papéis;
- o **painel do Admin** (as obras/os coordenadores/os instrutores/os alunos) e o **do Revisor** (a
  fila/o histórico).
