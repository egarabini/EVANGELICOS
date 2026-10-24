# DEM-202610-017 — o painel e a navegação por perfil na v1

## Finalidade

Depois do login, cada perfil cai no **seu painel** e vê **só o menu que a matriz
permite**. A fonte única é `gsi_ebd/utils/rbac.py`. A fatia 1 é **só leitura**.

## As fatias

| Fatia | O quê | Estado |
|---|---|---|
| **1** | Painel do Admin (`/admin`) e do Revisor (`/revisor`), menu derivado da matriz, rotas novas sem teste vacuoso | **PR #11** — fix das 4 ressalvas do EVAL; conferência rápida do ARQUITECT; sem merge |
| **2** | Criação do Estudo (`/admin/estudos`) + visão das avaliações/liberações + testes dos alunos fake no painel | proposta |
| **3** | Painéis do Coordenador, do Instrutor e do Aluno | proposta |
| **4** | Navegação hierárquica coordenador → instrutor → aluno | proposta |

## A fatia 1

- **GET `/admin`** (ADMIN): obras disponíveis e em estudo; coordenadores com estudos escolhidos; instrutores (`EquipeInstrutor`) com alunos (`TurmaMembro`); lista de alunos com feitos/a fazer e resultados (`StudyAssignment`/`Progress`).
- **GET `/revisor`** (REVISOR): fila de revisão; histórico de `ObraVersaoEvento` (`vista`/`recusada`/`liberada`).
- **Menu**: `ITENS_MENU` + `itens_do_menu(papel)` no `rbac.py`; o `base.html` só itera o que o papel pode. ADMIN: Painel / Obras / Estudos / Alunos / Alterar senha / Sair. REVISOR: Painel / Revisão / Alterar senha / Sair. Demais papéis: Alterar senha / Sair (o restante na fatia 3). Anônimo: sem menu.
- **Matriz**: `rota:/admin` = ADMIN; `rota:/revisor` = REVISOR. Casa **por versão**: v0 REVISOR → `/admin`; v1 REVISOR → `/revisor`. Cada célula tem o permitido (200) **e** o negado (403); monkeypatch remove as chaves → 403 nas 4 combinações. POST nas rotas novas → 405/403.

**Não entra**: criação de obras/estudos; banco da v0; roteamento de produção (Traefik/compose da v0).

## Os registros

- Intent (respostas do ARQUITECT em 24/10): [`planner/intent.md`](planner/intent.md)
- Despacho da fatia 1 (não reescrever): [`dev/despacho-fatia1-painel.md`](dev/despacho-fatia1-painel.md)
- Jornada, changelog e relatório: [`dev/`](dev/)
