# Briefing do EVAL cego — DEM-017, fatia 1 (o painel do Admin e do Revisor)

> **O EVAL julga o PR #11** (o head `9efe747`, o CI `40097452147`, a base `develop` `0d86a25`) — **não
> confia no relatório nem na jornada**. **O veredito é PASS/FAIL por critério, com o comando e a
> saída.** O **máximo de 2 rodadas** (o ADR-018).

## 1. O alvo

- o PR **#11** — a branch `feature/DEM-202610-017-fatia1-painel`, a partir do **`0d86a25`**;
- o head **`9efe747`**; o CI **`40097452147`** (`success`);
- a suíte local: o **166 da v1 + 274 da v0**.

## 2. O que julgar

| # | O critério | A prova |
|---|---|---|
| 1 | **O painel do ADMIN** (`GET /admin`, só leitura) | as **obras disponíveis e em estudo**; os **coordenadores com os estudos escolhidos**; os **instrutores com os alunos**; a **lista de todos os alunos** com os **feitos/a fazer e os resultados** |
| 2 | **O painel do REVISOR** (`GET /revisor`) | a **fila** e o **histórico** (`vista`/`recusada`/`liberada`) |
| 3 | **Só leitura** | o **POST** nessas rotas → **405/403** (nenhuma escrita) |
| 4 | **O menu derivado do `rbac.py`** | o **`base.html`** só renderiza o que o **`itens_do_menu(papel)`** libera; o **ADMIN** vê **Painel/Obras/Estudos/Alunos/Sair**; o **REVISOR** vê **Painel/Revisão/Sair**; o **anônimo não vê o menu** |
| 5 | **A matriz** | o **`rota:/admin` = ADMIN**; o **`rota:/revisor` = REVISOR**; **as 4 combinações** com o **permitido (200) E o negado (403)** |
| 6 | **A vacuidade** | o **monkeypatch** remove as chaves → **as 4 → 403** |
| 7 | **A invariante da casa** | o **`test_rf02`** com o **`/revisor`** (a casa do Revisor passou a `/revisor`) |
| 8 | **Os testes/o CI** | a **v1 166**; a **v0 274**; o CI `40097452147` |
| 9 | **A branch/docs** | a partir do **`0d86a25`**; a **documentação** da DEM-017 atualizada |

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
