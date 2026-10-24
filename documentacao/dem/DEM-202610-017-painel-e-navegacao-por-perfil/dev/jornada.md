# Jornada — DEM-202610-017, fatia 1

## 2026-10-24 — Painéis só leitura e menu derivado

Despacho `dev/despacho-fatia1-painel.md` (já na develop, `e7afc82`). Worktree isolado
`.worktrees/DEM-017-painel`, branch `feature/DEM-202610-017-fatia1-painel` a partir de
`origin/develop` (`0d86a25`, merge do PR #10). Não reusa o PR #5 nem o worktree da fatia 2
de obras.

A matriz da v0 tinha `/admin` = ADMIN+REVISOR (decisão 9.2a da DEM-002, porque a casa do
Revisor era `/admin`). A fatia pede `/admin` = ADMIN e `/revisor` = REVISOR como chaves
únicas. A casa do Revisor passou a `/revisor` para a invariante da casa continuar válida
(sem loop). A v0 Reflex não ganha página em `/revisor`; o despacho exclui o roteamento de
produção (Traefik/compose), não o ajuste das chaves da fonte única.

Implementado: consultas agregadas (`v1/paineis.py`) sem N+1 por linha; routers GET-only;
templates `admin/painel.html` e `revisor/painel.html`; `base.html` itera `menu`;
`views.render` preenche `itens_do_menu(papel)`. Estudos/Alunos no menu são âncoras
`/admin#estudos` e `/admin#alunos` (a criação é a fatia 2). Catálogo e Trocar senha saíram
do nav para o menu bater com a lista do despacho.

Testes em `v1/tests/test_paineis.py` (plano §5): painel 200+dados; fila/histórico; 10
células com permitido e negado; vacuidade nas 4; menu ADMIN/REVISOR/anônimo; menu deriva
da matriz; POST 405/403. Inventário RF-02 e destino RF-01 atualizados: login do ADMIN vai
a `/admin`, o do REVISOR a `/revisor`; Coordenador ainda cai na raiz (casa ainda não
existe na v1).

Suíte local: 166 v1 + 274 v0. Sem `subir.sh`, sem EVAL (quem dispara é o Architect), sem
merge.
