# DEM-202610-017 — relatório da fatia 1

- **Branch:** `feature/DEM-202610-017-fatia1-painel`, a partir da `develop` `0d86a25`. Commit `9efe747`.
- **PR:** https://github.com/egarabini/gsi_ebd/pull/11 → `develop`, sem merge.
- **CI:** [40097452147](https://github.com/egarabini/gsi_ebd/actions/runs/40097452147) — check `testes (pytest)` verde.
- **Worktree:** `.worktrees/DEM-017-painel` (GSI_EBD).
- **Alvo:** despacho `dev/despacho-fatia1-painel.md`; menu derivado do `rbac.py`; matriz não vacuosa.
- **Escopo:** painéis só leitura + menu + duas chaves na matriz. Sem criação de estudo, sem banco da v0, sem Traefik.

## O que entrou

| Superfície | Papel | Conteúdo |
|---|---|---|
| GET `/admin` | ADMIN | obras disponíveis (`versao_liberada_id` + `disponibilidade=aberta`) e em estudo (`Estudo`); coordenadores com `Ambiente`/`AmbienteEstudo`/`VinculoObra`; instrutores (`EquipeInstrutor`) e alunos (`TurmaMembro`); lista de alunos com `StudyAssignment` (feitos/a fazer) e `Progress` |
| GET `/revisor` | REVISOR | fila (`em_revisao`/`aguardando_admin`); histórico (`ObraVersaoEvento` tipos `vista`/`recusada`/`liberada`) |
| Menu | o papel autenticado | `ITENS_MENU` filtrado por `pode(chave, papel)` |

`rota:/admin` = `(ADMIN,)`; `rota:/revisor` = `(REVISOR,)`; `HOME_DO_PAPEL[REVISOR] = /revisor`.
O POST não tem handler: 405 (ou 403 se o CSRF recusar antes).

## Testes

| # | Prova | Onde |
|---|---|---|
| 1 | `/admin` → 200 com obras/coordenadores/instrutores/alunos | `test_painel_admin_200_com_os_dados` |
| 2 | `/revisor` → 200 com fila; depois `vista` e `liberada` no histórico | `test_painel_revisor_200_com_fila_e_historico` |
| 3 | 10 células (2 rotas × 5 papéis) com permitido 200 **e** negado 403 | `test_matriz_paineis_celula_permitido_e_negado` |
| 4 | monkeypatch remove as duas chaves → 403 nas 4 combinações ADMIN/REVISOR × `/admin`/`/revisor` | `test_matriz_paineis_falha_sem_as_duas_chaves` |
| 5 | HTML do ADMIN tem os links do ADMIN; o do REVISOR não tem os do ADMIN; anônimo sem `nav` | `test_menu_admin_revisor_e_anonimo` + `test_menu_deriva_da_matriz` |
| 6 | POST `/admin` e `/revisor` → 403 ou 405 | `test_paineis_sao_so_leitura` |

Inventário RF-02 inclui GET `/admin` e GET `/revisor`. Destino RF-01: ADMIN → `/admin`, REVISOR → `/revisor`, COORDENADOR → `/` (casa ainda não existe na v1).

## Suíte local

| Suíte | Resultado |
|---|---|
| `pytest tests -q` na raiz do app | **274 passaram** |
| `pytest tests -q` a partir de `v1/` | **166 passaram** |

Python local 3.14.6; CI roda 3.12. `git diff --check` limpo. EVAL cego pendente (máximo de 2, ADR-018). Sem `subir.sh`, sem merge.
