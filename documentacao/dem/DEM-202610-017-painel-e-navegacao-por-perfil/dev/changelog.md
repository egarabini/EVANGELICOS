# Changelog — DEM-202610-017

## 2026-10-24 — fatia 2 (criação do Estudo)

- Branch **nova** `feature/DEM-202610-017-fatia2-estudo` a partir da `develop` `b5573bd` (merge do PR #11). Worktree `.worktrees/DEM-017-fatia2`. **Não reusa o #11.**
- Criação: `/admin/estudos` + `/admin/estudos/nova` (ADMIN). Avaliações: `/revisor/avaliacoes` (REVISOR). ADR-020: assinatura + liberação; N imutável; hash LF+NFC.
- Commit GSI_EBD `3e0e48f`. [PR #12](https://github.com/egarabini/gsi_ebd/pull/12). [CI `pull_request` 40106321822](https://github.com/egarabini/gsi_ebd/actions/runs/40106321822) verde. Suíte: **213** v1 + **277** v0. EVAL cego pendente. Sem `subir.sh`, sem merge.

## 2026-10-24 — fix das 4 ressalvas do EVAL

- Casas por versão: `HOME_DO_PAPEL` da v0 (REVISOR → `/admin`); `HOME_DO_PAPEL_V1` (REVISOR → `/revisor`). Chaves de `PERMISSOES` inalteradas.
- Teste da v0 `revisor entra: 9.2a` revertido. `VinculoObra` renderizado. Cobertura: obra disponível, `completed=True`, `recusada`. Alterar senha + Sair no menu de todos os papéis.
- Commit GSI_EBD `a18fcb1`. Suíte: **172** v1 + **277** v0. [CI `pull_request` 40100843953](https://github.com/egarabini/gsi_ebd/actions/runs/40100843953) verde. Conferência rápida do ARQUITECT (não é nova rodada do EVAL). Sem merge.

## 2026-10-24

- Branch **nova** `feature/DEM-202610-017-fatia1-painel` a partir da `develop` `0d86a25` (merge do PR #10). Worktree `.worktrees/DEM-017-painel`.
- `rota:/admin` = ADMIN; `rota:/revisor` = REVISOR; `HOME_DO_PAPEL[REVISOR] = /revisor`. Menu derivado (`ITENS_MENU` / `itens_do_menu`) no `rbac.py`; `base.html` só renderiza o que o papel pode.
- GET `/admin` e GET `/revisor` só leitura (consultas agregadas em `v1/paineis.py`). POST → 405/403.
- Commit GSI_EBD `9efe747`. Suíte local: **166** v1 + **274** v0. [CI `pull_request` 40097452147](https://github.com/egarabini/gsi_ebd/actions/runs/40097452147) verde no [PR #11](https://github.com/egarabini/gsi_ebd/pull/11). EVAL cego pendente (máximo de 2 rodadas, ADR-018). Sem `subir.sh`, sem merge.
