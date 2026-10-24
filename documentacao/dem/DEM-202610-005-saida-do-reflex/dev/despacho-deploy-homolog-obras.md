# Despacho ao DEPLOY — a homologação das obras (a fatia 2)

> **O DEPLOY sobe a `develop` pós-merge do #9 na homologação (`subir.sh --v1`) e roda o seed dos
> alunos fake UMA VEZ.** **Nada das obras vai à produção; o seed nunca roda em produção.**

## O alvo

- o clone **`/home/didasko-deploy/homolog-v1`**;
- a **`develop` pós-merge do #9** (o merge é por **ordem expressa do ARQUITECT**);
- o **`.env.v1-homolog`** (o `DATABASE_URL` do `didasko_v1`, o `LANDING_LOGIN_URL`, os segredos).

## ANTES

1. o `git fetch origin` + o `git switch`/`checkout` da **`develop` pós-merge** (o commit do merge do
   #9);
2. conferir o **`.env.v1-homolog`** — o **`DATABASE_URL`** aponta para o **`didasko_v1`**; o
   **`SESSION_SECRET`** presente; **sem** o `DIDASKO_AMBIENTE` no `.env` (o seed o exige **no
   comando**, não no arquivo);
3. a **volta atrás escrita**: o `git checkout --force` do commit anterior + o `subir.sh --v1`.

## O SEED (o passo NOVO — UMA VEZ, na homologação)

**Sem isso a validação visual vê as telas vazias.**

```bash
cd /home/didasko-deploy/homolog-v1
DIDASKO_AMBIENTE=homologacao \
DATABASE_URL="postgresql+psycopg2://didasko_v1:...@didasko_v1_postgres:5432/didasko_v1" \
sudo -n docker exec -e DIDASKO_AMBIENTE=homologacao -e DATABASE_URL="..." \
  didasko_v1_app python -m v1.seed_homolog_estudo
```

- **O `DIDASKO_AMBIENTE=homologacao` é obrigatório** — o seed recusa o vazio/o desconhecido/o
  `producao` (o `recusar_producao`);
- **O `DATABASE_URL`** é o do **`didasko_v1`**;
- **O resultado a registrar**: os **2 alunos fake** (`aluno.fake.a` / `aluno.fake.b`), o **estudo**, o
  **assignment** — e a **confirmação de que rodou no banco de homologação** (não na produção).

**A regra**: **o seed roda UMA VEZ** — se rodar de novo, é idempotente (o `popular()` não duplica).
**E o seed NUNCA roda em produção**: o `recusar_producao` é o guard.

## O DEPLOY

4. o **`bash deploy/subir.sh --v1`** (o `--force-recreate` **só** a `app-v1` e o `landing`; o
   `--no-deps`);
5. os **200** do `/`, do `/homenagens` e do `/login`.

## DEPOIS (a conferência)

6. os **2 alunos fake** no banco (o `psql` do `didasko_v1`: o `select` dos `users` com o
   `aluno.fake`; o `assignment` do `aluno.fake.a`);
7. o **`/aluno`** (o login do `aluno.fake.a` → a lista com o estudo; a lição; o POST);
8. **registrar na jornada**: o resultado do seed, os 200s, o `StartedAt` dos contêineres (o
   `--force-recreate` recria o `app-v1`/o `landing`; o `postgres-v1`/o Traefik não são tocados).

## A dívida

**O seed não está wired ao `subir.sh`** (0 refs) — **o registro**: `dev/registro-dividas.md`. **A
decisão de virar passo do script é do ARQUITECT.**
