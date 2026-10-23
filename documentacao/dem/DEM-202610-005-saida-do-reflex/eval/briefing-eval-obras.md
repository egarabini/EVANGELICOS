# Briefing do EVAL cego — DEM-011, fatia 2 (as obras)

> **O EVAL julga o PR #9** (o head `3f9246e`, o CI `40038005779`, a base `develop` `5c0bc3e`) — **não
> confia no relatório nem na jornada**. **O veredito é PASS/FAIL por critério, com o comando e a
> saída.** O **máximo de 2 rodadas** (o ADR-018).

## 1. O alvo

- o PR **#9** — `feature/DEM-202610-011-fatia2-obras` → `develop`;
- o head **`3f9246e`**; o CI **`40038005779`** (`success`);
- a branch **a partir da `develop`** (`5c0bc3e`) — **não o #5** (o #5 duplicava o esqueleto do marco 1);
- os arquivos: o `v1/rbac.py`, o `v1/tests/test_obras_matriz.py`, o `v1/tests/test_obras_adr020.py`,
  o `v1/seed_homolog_estudo.py`, o `v1/tests/test_estudo_fake.py`, o `v1/tests/test_seed_homolog.py`,
  o `v1/tests/test_fluxo_http.py`.

## 2. O que ler (a régua)

1. `documentacao/dem/DEM-202610-005-saida-do-reflex/dev/despacho-obras-fatia2.md` — o contrato, o
   ADR-020, o modo fake;
2. `.../dev/plano-testes-obras.md` — a matriz 5×3, a vacuidade, o ADR-020, o modo fake;
3. o **ADR-020** (o `documentacao/adr/ADR-020-*`) — as regras de autoridade;
4. o `v1/rbac.py` e os testes — o código é a prova.

## 3. O que julgar (os critérios)

| # | O critério | A prova |
|---|---|---|
| 1 | **O `rbac`: as 3 chaves** — `/admin/obras` = ADMIN; `/revisor/obras` = REVISOR; `/obras` = os dois (o `GET /obras` incluso) | o `v1/rbac.py` + o `test_obras_matriz.py` |
| 2 | **A matriz de 15 células** — cada célula com o **permitido E o negado** (não vacuosa) | o `test_obras_matriz.py` (as 2 asserções por célula) |
| 3 | **A prova da vacuidade** — o monkeypatch remove as 3 chaves e o **permitido vira 403** | o teste da vacuidade |
| 4 | **O ADR-020** — só o Admin muda a publicação/disponibilidade; o Revisor assina o parecer e move o editorial; a **liberação exige os dois**; a **N imutável** (o ciclo cria a N+1); o **hash LF+NFC**; a disponibilidade `aberta \| suspensa_para_novos` | o `test_obras_adr020.py` |
| 5 | **Os alunos fake** — só no `v1/seed_homolog_estudo.py` (o banco **`didasko_v1` de homologação**); o **seed de produção NÃO os recebe** | o `seed_homolog_estudo.py` + o `test_seed_homolog.py` |
| 6 | **Os testes** — a **v1 130** + a **v0 272** | o `pytest` |
| 7 | **O CI** — o run `40038005779` (`success`) no head `3f9246e` | a API |
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
- inventar valores.
