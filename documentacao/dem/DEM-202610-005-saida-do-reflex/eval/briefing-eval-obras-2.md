# Briefing do EVAL cego — DEM-011, fatia 2 — a **2ª (e última) rodada** (ADR-018)

> **O EVAL julga o PR #9** (o head **`48f97f8`**, o CI `pull_request` **`40043436945`**) — a **2ª
> rodada**; o **ADR-018 dá no máximo 2**. **O foco: o critério 5 (o fluxo do aluno fake) — o FAIL da
> 1ª rodada.**

## 1. O alvo

- o PR **#9**, o head **`48f97f8`** (o CI `pull_request` **`40043436945`**, `success`);
- o **fix**: o **`v1/routers/aluno.py`** (o `GET /aluno` e o `/aluno/licao/{id}`; o `POST` da resposta
  → 303); o **`test_estudo_fake.py`** (o `entrar_como(aluno.fake.a)`); o **seed** com o
  `DIDASKO_AMBIENTE` obrigatório; o relatório/o briefing.

## 2. O foco (o critério 5 — o FAIL da 1ª rodada)

**O teste REAL do aluno:**

- o **`entrar_como(aluno.fake.a)`**;
- o **GET `/aluno`** e o **`/aluno/licao/{id}`** da obra liberada → **200**;
- o **POST da resposta** → **303**;
- o **`UserResponse`/`Progress` gravados pelo handler** (não inseridos direto);
- o **`aluno.fake.b`** na obra **não liberada** → a **lista vazia** e o **403 na lição**.

**O seed:**

- o **`DIDASKO_AMBIENTE=homologacao`** **obrigatório**; o **`ambiente=""`** e o **desconhecido**
  **recusam** (o **fail-open** fechado);
- o **`popular()`/`run()`** exercitados num **SQLite `didasko_v1.db`**.

**A documentação:**

- o **`relatorio-fatia-2.md`** com o **#9/`3f9246e`/130+272** (não o #5/`3b5f56c`/157+269);
- o **briefing** da 2ª rodada com o head **`48f97f8`** e o CI **`40043436945`**.

## 3. O resto (re-conferir, sem refazer)

- o **rbac** (as 3 chaves: `/admin/obras` = ADMIN; `/revisor/obras` = REVISOR; `/obras` = os dois) —
  a matriz real é o **`gsi_ebd/utils/rbac.py`** (o `v1/rbac.py` **não** existe);
- a **matriz 15** (o permitido E o negado); a **vacuidade**; o **ADR-020**;
- o **CI**; os **138 da v1 + 273 da v0** (a contagem nova).

## 4. A régua

- **PASS/FAIL por critério**, com a **evidência** (o comando e a saída);
- **o ADR-018: no máximo 2 rodadas — ESTA É A ÚLTIMA.** Um FAIL consome a rodada.

## 5. O que **não** fazer

- alterar o código do PR;
- tocar na **produção**/no **Traefik**/na **v0**;
- o **merge**; o **`subir.sh`**;
- inventar valores.
