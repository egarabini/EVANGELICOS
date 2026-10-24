# DEM-202610-017 — relatório da fatia 1

- **Branch:** `feature/DEM-202610-017-fatia1-painel`, a partir da `develop` `0d86a25`. Commits `9efe747` (fatia 1) + `a18fcb1` (fix das 4 ressalvas).
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

`rota:/admin` = `(ADMIN,)`; `rota:/revisor` = `(REVISOR,)`. Chaves **compartilhadas**.
Casas **por versão**: v0 `HOME_DO_PAPEL[REVISOR] = /admin` (congelada); v1 `HOME_DO_PAPEL_V1[REVISOR] = /revisor`.
O POST não tem handler: 405 (ou 403 se o CSRF recusar antes).

## Correção das 4 ressalvas do EVAL (antes do merge)

A 1ª rodada do EVAL (head `9efe747`) deu PASS nos 7 critérios e 4 ressalvas. A ressalva 1
**bloqueava o merge**: o mapa único mandava o REVISOR da v0 a `/revisor` (404; o teste da v0
tinha sido relaxado).

| # | Ressalva | Correção |
|---|---|---|
| 1 | casas por versão | `HOME_DO_PAPEL` da v0 volta a REVISOR → `/admin`; a v1 usa `HOME_DO_PAPEL_V1` (REVISOR → `/revisor`); o `guarda_rota` da v0 deixa o papel entrar na própria casa; o teste `revisor entra: 9.2a` revertido; invariante da casa em **cada** mapa |
| 2 | `VinculoObra` calculado e não renderizado | renderizado em `admin/painel.html` (`Obras vinculadas`) |
| 3 | cobertura | `test_painel_admin` exercita obra disponível (`versao_liberada_id` + `aberta`), `completed=True` (`Estudo feito`) e `recusada` no histórico do Revisor |
| 4 | Alterar senha / Sair | `ITENS_MENU` inclui Alterar senha (`rota:/perfil/alterar-senha`, todos os papéis); Sair permanece no template para qualquer autenticado; teste por papel |

Conferência rápida do ARQUITECT (não é nova rodada do EVAL): suíte da v0 intacta (sem o teste relaxado); menu por papel com Alterar senha e Sair; casa por versão (`/admin` na v0, `/revisor` na v1).

## Testes

| # | Prova | Onde |
|---|---|---|
| 1 | `/admin` → 200 com obras disponíveis/em estudo, `VinculoObra`, feitos (`completed=True`) e a fazer | `test_painel_admin_200_com_os_dados` |
| 2 | `/revisor` → 200 com fila; histórico com `recusada`, `vista` e `liberada` | `test_painel_revisor_200_com_fila_e_historico` |
| 3 | 10 células (2 rotas × 5 papéis) com permitido 200 **e** negado 403 | `test_matriz_paineis_celula_permitido_e_negado` |
| 4 | monkeypatch remove as duas chaves → 403 nas 4 combinações ADMIN/REVISOR × `/admin`/`/revisor` | `test_matriz_paineis_falha_sem_as_duas_chaves` |
| 5 | HTML do ADMIN tem os links do ADMIN; o do REVISOR não tem os do ADMIN; anônimo sem `nav`; cada papel tem Alterar senha e Sair | `test_menu_admin_revisor_e_anonimo` + `test_menu_deriva_da_matriz` + `test_menu_alterar_senha_e_sair_em_todos_os_papeis` |
| 6 | POST `/admin` e `/revisor` → 403 ou 405 | `test_paineis_sao_so_leitura` |

Inventário RF-02 inclui GET `/admin` e GET `/revisor`. Destino RF-01 usa o mapa da v1: ADMIN → `/admin`, REVISOR → `/revisor`, COORDENADOR → `/`. A v0 continua REVISOR → `/admin`.

## Suíte local (após o fix)

| Suíte | Resultado |
|---|---|
| `pytest tests -q` na raiz do app | **277 passaram** |
| `pytest tests -q` a partir de `v1/` | **172 passaram** |

Python local 3.14.6; CI roda 3.12. Conferência rápida do ARQUITECT. Sem `subir.sh`, sem merge.
