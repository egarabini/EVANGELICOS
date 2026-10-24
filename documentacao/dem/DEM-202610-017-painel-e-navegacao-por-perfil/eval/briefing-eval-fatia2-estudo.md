# Briefing do EVAL cego — DEM-017, fatia 2 (a criação do Estudo + as avaliações)

> **O EVAL julga o PR #12** (o head `3e0e48f`, o CI `40106321822`, a base `develop` `b5573bd`) — **não
> confia no relatório nem na jornada**. **O veredito é PASS/FAIL por critério, com o comando e a
> saída.** O **máximo de 2 rodadas** (o ADR-018).

## 1. O alvo

- o PR **#12** — a branch nova a partir da **`b5573bd`** (não reusa o #11);
- o head **`3e0e48f`**; o CI **`40106321822`** (`success`);
- a suíte: **277 da v0 + 213 da v1**.

## 2. O que julgar

| # | O critério | A prova |
|---|---|---|
| 1 | **A criação do Estudo** | o `/admin/estudos` e o `/admin/estudos/nova` (o ADMIN) → 200; o **POST → 303**; o **`Estudo` + o `EstudoCapitulo` + o `EstudoVersao` N=1** criados |
| 2 | **A fila do Revisor** | o `/revisor/avaliacoes` (o REVISOR) → 200 com o que está em revisão |
| 3 | **O parecer** | o **`revisar`/o `recusar`** → 303 (o Revisor) |
| 4 | **A liberação pelos dois** | a **assinatura do Revisor + a liberação do Admin** → 303; o **Admin sozinho → 409** |
| 5 | **A N imutável** | a versão liberada **não é editável**; o ciclo cria a **N+1** |
| 6 | **O hash LF+NFC** | o mesmo conteúdo com o LF/NFC → o **mesmo hash** |
| 7 | **Os fake na lista** | o `GET /admin` → 200 com o **"Aluno Fake A/B"** + o `Progress` + o `UserResponse` |
| 8 | **O menu** | o **ADMIN vê o "Estudos"**; o **REVISOR vê as "Avaliações"** (derivado do `rbac.py`) |
| 9 | **A matriz (não vacuosa)** | as **3 rotas novas** com o **permitido 200 E o negado 403**; a **vacuidade** (o monkeypatch → 403) |
| 10 | **Os testes/o CI** | a **v0 277**; a **v1 213**; o CI `40106321822` |

## 3. A régua

- **PASS/FAIL por critério**, com a **evidência** (o comando e a saída);
- no FAIL, **o que falta** e **o que faria passar**;
- o que **não deu** para testar, dito com todas as letras;
- **não confie** no relatório nem na jornada — **o comando é a prova**.

## 4. O que **não** fazer

- tocar na **produção**/no **Traefik**/na **v0**;
- o **merge**; o **`subir.sh`**;
- alterar o código do PR;
- inventar valores.
