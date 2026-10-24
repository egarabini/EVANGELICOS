# Briefing do EVAL cego — DEM-011, fatia 2 (as obras) — 2ª rodada

> **O EVAL julga o PR #9** (a 2ª rodada, o máximo do ADR-018) — **não confia no relatório nem na
> jornada**. **O veredito é PASS/FAIL por critério, com o comando e a saída.**

A 1ª rodada julgou o head **`8ae1a3c`**. O CI a citar dessa rodada é o **`pull_request` `40038006423`**
(head `3f9246e`) — **não** o `workflow_dispatch` `40038005779`. A opção A no mesmo head: `pull_request`
`40038703819`. FAIL só no critério 5 (fluxo do aluno fake vacuoso; `recusar_producao` fail-open).

## 1. O alvo

- o PR **#9** — `feature/DEM-202610-011-fatia2-obras` → `develop`;
- o head **`48f97f8`** (o fix acima de `8ae1a3c`); o CI do evento **`pull_request`** nesse head
  (não o `workflow_dispatch`);
- a branch **a partir da `develop`** (`5c0bc3e`) — **não o #5**;
- os arquivos: o `gsi_ebd/utils/rbac.py` (não existe `v1/rbac.py`), o `v1/tests/test_obras_matriz.py`,
  o `v1/tests/test_obras_adr020.py`, o `v1/seed_homolog_estudo.py`, o `v1/tests/test_estudo_fake.py`,
  o `v1/tests/test_seed_homolog.py`, o `v1/routers/aluno.py`, o `v1/tests/test_fluxo_http.py`.

## 2. O que ler (a régua)

1. `documentacao/dem/DEM-202610-005-saida-do-reflex/dev/despacho-obras-fatia2.md` — o contrato, o
   ADR-020, o modo fake;
2. `.../dev/plano-testes-obras.md` — a matriz 5×3, a vacuidade, o ADR-020, o modo fake (§3);
3. `.../dev/despacho-fatia2-fix.md` — o DoD desta 2ª rodada;
4. o **ADR-020** (o `documentacao/adr/ADR-020-*`) — as regras de autoridade;
5. o `gsi_ebd/utils/rbac.py` e os testes — o código é a prova.

## 3. O que julgar (os critérios)

| # | O critério | A prova |
|---|---|---|
| 1 | **O `rbac`: as 3 chaves** — `/admin/obras` = ADMIN; `/revisor/obras` = REVISOR; `/obras` = os dois (o `GET /obras` incluso) | o `gsi_ebd/utils/rbac.py` + o `test_obras_matriz.py` |
| 2 | **A matriz de 15 células** — cada célula com o **permitido E o negado** (não vacuosa) | o `test_obras_matriz.py` (as 2 asserções por célula) |
| 3 | **A prova da vacuidade** — o monkeypatch remove as 3 chaves e o **permitido vira 403** | o teste da vacuidade |
| 4 | **O ADR-020** — só o Admin muda a publicação/disponibilidade; o Revisor assina o parecer e move o editorial; a **liberação exige os dois**; a **N imutável** (o ciclo cria a N+1); o **hash LF+NFC**; a disponibilidade `aberta \| suspensa_para_novos` | o `test_obras_adr020.py` |
| 5 | **Os alunos fake (o fluxo, não o esquema)** — `entrar(aluno.fake.a)`; GET da obra/estudo **liberado** → 200; POST da resposta → 201/303; `UserResponse`/`Progress` no banco **gravados pelo POST**; `aluno.fake.b` na obra **não liberada** → 403/vazio. O teste **falha** se a rota do aluno não existir. Seed só em `v1/seed_homolog_estudo.py` (banco **`didasko_v1`**); `DIDASKO_AMBIENTE=homologacao` **obrigatório** (`ambiente=""` recusa); `popular()`/`run()` exercitados num teste; o seed de produção **não** os recebe | o `test_estudo_fake.py` + o `test_seed_homolog.py` + o `seed_homolog_estudo.py` |
| 6 | **Os testes** — a **v1 138** + a **v0 273** (local, após o fix) | o `pytest` |
| 7 | **O CI** — o run **`pull_request` `40043436945`** no head `48f97f8` (`success`); check `testes (pytest)` | a API |
| 8 | **A branch** — a partir da `develop` (`5c0bc3e`), **sem** o esqueleto do marco 1 duplicado | o `git log`/o `git diff` contra o `develop` |

## 4. A régua do veredito

- **PASS/FAIL por critério**, com a **evidência** (o comando e a saída);
- no FAIL, **o que falta** e **o que faria passar**;
- o que **não deu** para testar, dito com todas as letras;
- **não confie** no relatório nem na jornada — **o comando é a prova**.

## 5. O que **não** fazer

- tocar na **produção**/no **Traefik**/na **v0**;
- o `subir.sh`, o merge do PR;
- alterar o código do PR;
- inventar valores;
- inflar as telas completas do aluno (o Architect deixou isso fora desta fatia).
