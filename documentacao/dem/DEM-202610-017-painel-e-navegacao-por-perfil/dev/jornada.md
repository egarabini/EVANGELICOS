# Jornada — DEM-202610-017, fatia 1

## 2026-10-24 — Fix das 4 ressalvas do EVAL (PR #11)

Despacho `dev/despacho-fatia1-fix.md`. As 4 ressalvas no mesmo commit, no #11, **antes** do merge.
Não é nova rodada do EVAL — conferência rápida do ARQUITECT.

1. **Casas por versão.** `HOME_DO_PAPEL` da v0 volta exatamente ao que era (REVISOR → `/admin`).
   A v1 ganha `HOME_DO_PAPEL_V1` (REVISOR → `/revisor`); o `destino()` da v1 consulta esse mapa,
   não o `AuthService.redirect_for_role`. As chaves `rota:/admin` e `rota:/revisor` continuam
   compartilhadas. O `guarda_rota` da v0 deixa o papel entrar na própria casa, para o REVISOR
   não cair em 404 nem em loop. O teste `revisor entra: 9.2a` foi revertido. A invariante da
   casa vale para cada mapa (`test_invariante_casa_do_papel` na v0; `test_rf02_invariante_casa_v1`
   na v1).

2–3. **Cobertura e VinculoObra.** O painel do Admin renderiza `bloco.obras`. A fixture libera a
   obra (`versao_liberada_id` + `aberta`), cria `VinculoObra`, um assignment `completed=True` e o
   fluxo do Revisor passa por `recusar` antes de reenviar/revisar/liberar.

4. **Alterar senha e Sair.** `ITENS_MENU` ganha Alterar senha com a chave `_TODOS`
   `rota:/perfil/alterar-senha`. O Sair permanece no `base.html` para qualquer autenticado. O
   restante do menu dos demais papéis fica na fatia 3.

Suíte: 172 v1 + 277 v0. [CI verde](https://github.com/egarabini/gsi_ebd/actions/runs/40100843953) (`testes (pytest)`). Sem `subir.sh`, sem merge.

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

Suíte local: 166 v1 + 274 v0. [PR #11](https://github.com/egarabini/gsi_ebd/pull/11).
[CI verde](https://github.com/egarabini/gsi_ebd/actions/runs/40097452147) (`testes (pytest)`).
Sem `subir.sh`, sem EVAL (quem dispara é o Architect), sem merge.
