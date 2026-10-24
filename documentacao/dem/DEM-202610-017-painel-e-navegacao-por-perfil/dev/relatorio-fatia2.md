# DEM-202610-017 — relatório da fatia 2

- **Branch:** `feature/DEM-202610-017-fatia2-estudo`, a partir da `develop` `b5573bd` (merge do PR #11). Commit `3e0e48f`. **Não reusa o #11.**
- **PR:** https://github.com/egarabini/gsi_ebd/pull/12 → `develop`, sem merge.
- **Worktree:** `.worktrees/DEM-017-fatia2` (GSI_EBD).
- **Alvo:** despacho `dev/despacho-fatia2-estudo.md`. ADR-020. Matriz não vacuosa.
- **Escopo:** criação do Estudo; avaliações/liberações; fake na lista do painel. Sem UI fina dos demais papéis, sem banco da v0, sem Traefik, sem `subir.sh`.

## O que entrou

| Superfície | Papel | Conteúdo |
|---|---|---|
| GET/POST `/admin/estudos` e `/admin/estudos/nova` | ADMIN | lista; formulário (obra de origem, capítulos, questões); POST cria `Estudo` + `EstudoCapitulo` + `EstudoVersao` N=1 em `em_revisao` |
| GET/POST `/revisor/avaliacoes` | REVISOR | fila; parecer (`revisar`/`recusar`) |
| POST `/admin/estudos/{id}/liberar` e `/alterar` | ADMIN | liberação (exige assinatura); N imutável (ciclo cria N+1) |
| GET `/admin` | ADMIN | "Aluno Fake A/B" com `Progress` e `UserResponse` |

`rota:/admin/estudos` = ADMIN; `rota:/admin/estudos/nova` = ADMIN; `rota:/revisor/avaliacoes` = REVISOR.

A versão editorial vive em tabelas novas (`EstudoVersao`, `EstudoVersaoCapitulo`) — `create_all` da v1 cria tabela nova em homologação; não altera colunas da `estudo` existente.

## Testes

| # | Prova | Onde |
|---|---|---|
| 1 | POST `/admin/estudos/nova` → 303; `Estudo` + `EstudoCapitulo` | `test_criar_estudo_post_303_e_grava` |
| 2 | GET `/admin/estudos` → 200 com o estudo | `test_lista_estudos_200_com_os_criados` |
| 3 | GET `/revisor/avaliacoes` → 200 com a fila | `test_fila_revisor_200_com_o_estudo_em_revisao` |
| 4 | POST parecer Revisor → 303; Admin no parecer → 403 | `test_parecer_revisor_303_admin_403` |
| 5 | Admin sozinho na liberação → 409; os dois → 303 | `test_liberacao_exige_os_dois_admin_sozinho_409` |
| 6 | N imutável; alterar cria N+1 | `test_n_imutavel_ciclo_cria_n_mais_1` |
| 7 | Hash LF+NFC (CRLF/LF e NFC/NFD) | `test_hash_estudo_lf_nfc` |
| 8 | `/admin` com Aluno Fake A/B, `1/1` e `q1` | `test_fake_na_lista_do_painel` |
| 9 | Matriz 15 células + vacuidade (3 chaves) + menu | `test_matriz_estudos_*` + `test_menu_estudos_e_avaliacoes` |

Inventário RF-02 inclui as rotas novas. Menu: ADMIN vê Estudos (`/admin/estudos`); REVISOR vê Avaliações (`/revisor/avaliacoes`).

## Suíte local

| Suíte | Resultado |
|---|---|
| `pytest tests -q` na raiz do app | **277 passaram** |
| `pytest tests -q` a partir de `v1/` | **213 passaram** |

Python local 3.14.6; CI roda 3.12. EVAL cego: ordem do ARQUITECT (máximo de 2, ADR-018). Sem `subir.sh`, sem merge.
