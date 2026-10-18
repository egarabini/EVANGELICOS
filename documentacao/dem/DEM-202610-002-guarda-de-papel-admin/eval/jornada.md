# Jornada — EVAL da DEM-202610-002 (guarda de papel)

| | |
|---|---|
| Agente | **EVAL** — cego e adversarial |
| Data | **2026-10-18** |
| DEM | **DEM-202610-002 / guarda-de-papel-admin** |
| Repositório | `C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD` |
| Commit avaliado | **`65fbf7a`** (`feat(dem-002): guarda de papel por rota e por evento + estado imutavel pelo cliente`) |
| Worktree | limpo (`git status --porcelain` vazio); `HEAD == 65fbf7a` |
| Runtime | Python do venv do app · Reflex **0.9.5.post2** |
| Contrato lido | `planner/{intent,spec,design,plano-testes}.md` (design v3 = List 2.1; plano F-01..F-28 / N-01..N-08) |
| Não lido (regra) | `dev/`, `README.md` e `changelog.md` da DEM, jornadas |

Todos os comandos rodaram **do diretório do app** (`ESTUDOS_BIBLICOS/GSI_EBD`), como o CI
(`.github/workflows/ci.yml` → `python -m pytest tests -q` na raiz do repo do app).

## 0. Veredito

**Veredito agregado: FAIL (de teste/DoD). Segurança dos três alvos: PASS.**

- Nenhum caminho **explorável** foi encontrado para os três furos que a DEM diz ter fechado:
  identidade, rota e evento estão barrados **no código** (evidência na §3).
- Mas o **teste que a DEM declara como prova de regressão não prova**:
  `test_todo_evento_tem_marcador_exige` examina **zero** métodos (Reflex troca o método por
  `EventHandler` antes do teste rodar), e **nenhum teste toca o `on_load`** nem a guarda real
  `AuthState.guarda_*`. Apagar todos os `@exige` ou neutralizar a guarda de rota mantém a suíte
  **105 passed** (evidência na §6).
- O DoD do repositório exige "testes verdes **cobrindo** os requisitos da DEM"; RF02 e RF07 não
  estão cobertos. Por isso o veredito é FAIL — com escopo declarado, não com furo de produção.

| Categoria | Resultado | Leitura |
|---|---|---|
| **F** (F-01..F-28) | **22 PASS · 1 PASS com ressalva · 2 PARCIAL · 3 FAIL** | F-06 (rotas públicas), F-12 (varredura vazia) e F-19 (contradiz F-25) falham |
| **H** | **H-01 PASS · H-04 PASS · H-06 PARCIAL** | H-06 prova o redirecionamento/ausência de dados; não há 403 e não há browser |
| **C** | **4 PASS** | sem dependência, sem schema, 9 páginas, usa `Role` |
| **N** | **6 PASS · 1 PARCIAL · 1 FAIL** | N-06 falha (a varredura que impediria o furo voltar é vazia); N-03 parcial (só os 3 estados admin) |
| **G** (geral) | **FAIL de teste / PASS de segurança** | os 3 furos fechados no código; a prova automatizada não sustenta a afirmação da DEM |

## 1. Suíte e CI (H-01, C-03, F-28)

```
pytest tests -q                     -> 105 passed  (7.34 s, do diretório do app)
pytest tests/test_rbac.py -q        -> 23 passed   (23 casos coletados)
pytest tests/test_paginas.py -q     -> 9 passed    (as 9 páginas compilam)
```

Baseline do intent: 82. `105 = 82 + 23` — bate. `test_paginas` 9/9. CI roda o mesmo comando
no mesmo `cwd`. `saida_pytest.txt`, `saida_rbac.txt`, `saida_rbac_collect.txt`,
`saida_paginas.txt`.

## 2. Identidade — o cliente escreve o próprio papel? (RF09)

**Fechado.**

- `get_config().state_auto_setters is False` — lido do `rxconfig.py` real, com o `cwd` do app.
- Nos **7 estados** (`AuthState`, `AdminState`, `CoordenadorState`, `RevisaoState`, `AlunoState`,
  `PerfilState`, `CommonState`): `event_handlers` **não contém** nenhum `set_current_user_*`,
  `set_is_authenticated` ou `set_must_change_password`; e `getattr(estado, "set_<campo>")` é
  `None` para os 7 campos (`current_user_id/name/role/status/ambiente`, `is_authenticated`,
  `must_change_password`).
- `AuthState` tem 13 handlers; só 2 setters de formulário (`set_login_email`,
  `set_login_password`). `AdminState` 18; `CoordenadorState` 10; `RevisaoState` 10;
  `AlunoState` 8; `PerfilState` 6; `CommonState` 2.
- **`setvar` não alcança a identidade.** O handler registrado é
  `EventHandlerSetVar.setvar` (`reflex/state.py:201-210`), e ele faz
  `getattr(self, "set_" + var_name)`. Chamado direto nos 7 estados com
  `("current_user_role", 1)`, `("is_authenticated", True)` e `("must_change_password", 1)`:
  **`AttributeError: 'X' object has no attribute 'set_current_user_role'`** em todos.
- **Contrafactual (memória):** ligando `state_auto_setters=True` antes de importar os estados,
  `AuthState` volta a **28 handlers**, com os **7 setters de identidade**, e
  `setvar("current_user_role", 1)` + `setvar("is_authenticated", True)` deixa o estado com
  `role=1 / autenticado=True`. O flag é load-bearing; o furo era real. (`counterfactual.py`)
- O teste de identidade **é real**: nesse contrafactual,
  `test_state_auto_setters_desligado` e `test_nenhum_setter_de_identidade` **reprovam**.
- Ressalva: **nenhum dos 23 casos testa o `setvar`**. A prova do `setvar` é por mecanismo
  (código do Reflex + chamada direta), não por teste da DEM.

## 3. Rota (RF01–RF04) e matriz

`PERMISSOES` (`utils/rbac.py:19-31`) — rotas e ações:

| Chave | Papéis | Medido |
|---|---|---|
| `rota:/admin` | ADMIN, REVISOR | ✓ (`ALUNO/COORDENADOR/INSTRUTOR` negados) |
| `rota:/coordenador` | ADMIN, COORDENADOR | ✓ |
| `rota:/revisao` | ADMIN, INSTRUTOR | ✓ |
| `acao:catalogo_ler` | ADMIN, REVISOR | ✓ |
| `acao:catalogo_aprovar` | ADMIN | ✓ |
| `acao:usuarios` · `acao:leads` | ADMIN | ✓ |
| `acao:coordenacao` | ADMIN, COORDENADOR | ✓ |
| `acao:revisao` | ADMIN, INSTRUTOR | ✓ |

`on_load` **real** do `gsi_ebd/gsi_ebd.py` (lido do objeto `app` em memória):

```
/admin        -> ['AuthState.guarda_admin', 'AdminState.load_coordenadores']
/coordenador  -> ['AuthState.guarda_coordenador', 'CoordenadorState.load_all']
/revisao      -> ['AuthState.guarda_revisao', 'RevisaoState.load_fila']
```

Guarda real (`AuthState.guarda_*`, `auth.py:216-229`) medida em estado de memória:

| Rota | ADMIN | REVISOR | COORDENADOR | INSTRUTOR | ALUNO | ANÔNIMO |
|---|---|---|---|---|---|---|
| `/admin` | segue | **segue** | `/coordenador` | `/revisao` | `/aluno` | `/login` |
| `/coordenador` | segue | `/admin` | **segue** | `/revisao` | `/aluno` | `/login` |
| `/revisao` | segue | `/admin` | `/coordenador` | **segue** | `/aluno` | `/login` |

- **Sem loop**: a casa de cada papel é permitida. `rbac.home_do_papel` ==
  `AuthService.redirect_for_role` == `/admin`(ADMIN,REVISOR), `/coordenador`(COORDENADOR),
  `/revisao`(INSTRUTOR), `/aluno`(ALUNO); todas as casas guardadas passam em `pode`.
- **Papel inválido** (99) em `/admin` → `/login` (N-02), e `/login` é pública (sem guarda).
- **Defesa em profundidade**: `AdminState.load_coordenadores` (no `on_load` de `/admin`) tem
  `@exige("acao:usuarios")`; com ALUNO nem abre sessão (sondado com `rx.session` armado para
  explodir).
- **Ressalvas**: (a) o redirect é **client-side** — não há **403 HTTP**, ao contrário do que o
  `intent §2/H-06` diz literalmente; a `spec §5/CA01` escolheu redirecionar, e é o que o código
  faz. (b) `rbac.guarda_rota` **não é usado no app** (só no teste sintético); a guarda real é
  `AuthState._guarda`, uma segunda cópia da mesma regra. (c) o teste da invariante usa
  `rbac.home_do_papel`, **não** `AuthService.redirect_for_role` — hoje são iguais, mas uma
  mudança no login não seria pega.

## 4. Evento (RF07/RF08/RF10)

Os **28** eventos não-setter dos 3 estados têm marcador `__exige__` no wrapper real
(`handler.fn.__exige__`, não no `EventHandler` da classe):

- `AdminState` (13): `acao:usuarios` em `activate/suspend/cancel/create_gestor/load_coordenadores`;
  `acao:leads` em `load_leads/update_lead_status`; `acao:catalogo_ler` em
  `load_estudos_pendentes/load_obras/load_estudos_aplicados`; `acao:catalogo_aprovar` em
  `aprovar_estudo/aprovar_todos/rejeitar_estudo`.
- `CoordenadorState` (8): todos `acao:coordenacao` (`assign_study`, `load_all`, `load_alunos`,
  `load_estudos`, `load_turmas`, `toggle_aluno`, `select_all_alunos`, `clear_selection`).
- `RevisaoState` (7): todos `acao:revisao` (`load_fila`, `abrir/fechar_resposta`, `pedir/usar/
  descartar_sugestao`, `salvar_parecer`).

Comportamento dos handlers **reais** (sem banco; `rx.session` armado para explodir):

| Chamada | Resultado |
|---|---|
| `load_coordenadores` ALUNO | `None`, sem sessão |
| `load_leads` REVISOR | `None`, sem sessão |
| `update_lead_status` COORDENADOR | `None`, sem sessão |
| `aprovar_estudo` **REVISOR** e COORDENADOR | `None`, sem sessão (**F-25**: revisor não aprova) |
| `assign_study` ALUNO/REVISOR | `None`, sem sessão |
| `abrir_resposta` COORDENADOR · `salvar_parecer` ALUNO | `None`, sem sessão |
| `activate/suspend/cancel_user` **REVISOR** | `None`, sem sessão (F-15) |

`exige` preserva o tipo: `iscoroutinefunction=False` e `inspect.signature` original
(`__wrapped__`), medido em `aprovar_estudo`, `assign_study`, `abrir_resposta` (F-27; não testado
na suíte). `can_manage` continua existindo, mas **não** é guarda única de nenhum evento (N-07):
ele só refina a hierarquia depois do `@exige`.

## 5. Teste — o que ele realmente prova

### 5.1 O achado central: a varredura de `__exige__` é **vazia**

`tests/test_rbac.py:162-172` faz:

```python
for nome, fn in vars(estado).items():
    if nome.startswith("_") or nome == "setvar" or not inspect.isfunction(fn): continue
    ...
    if not hasattr(fn, "__exige__"): sem_marcador.append(nome)
```

O Reflex **substitui cada método público por um `EventHandler`** em `state.py:693-696`
(`setattr(cls, name, handler)`). Logo `inspect.isfunction(fn)` é **False** para todos e o laço
examina **0** entradas nos 3 estados. Medido:

```
AdminState         entradas que o scan do teste examina: 0
CoordenadorState   entradas que o scan do teste examina: 0
RevisaoState       entradas que o scan do teste examina: 0
```

Consequência: **removendo os 28 marcadores `__exige__` em memória, o teste continua verde**
(`mutacao.py`, seção B). O teste não distingue "tem `@exige`" de "não tem".

Correção possível (não aplicada — EVAL não corrige): varrer `E.event_handlers[nome].fn` e checar
`hasattr(..., "__exige__")`, ou `inspect.isfunction(handler.fn)`.

### 5.2 O que **realmente** reprova

| Mutação (em memória) | Suíte reprova? |
|---|---|
| Tirar um papel de `PERMISSOES` (ex.: REVISOR de `rota:/admin`) | **Sim** — `test_matriz_de_rotas` (`REVISOR deveria poder /admin`) |
| Dar `acao:catalogo_aprovar` ao REVISOR | **Sim** — `test_matriz_de_acoes` |
| Novo evento em `AdminState` | **Sim** — `test_lista_de_eventos_congelada` (lista congelada, real) |
| Ligar `state_auto_setters=True` | **Sim** — `test_state_auto_setters_desligado` + `test_nenhum_setter_de_identidade` |
| Remover **todos** os `@exige` | **Não** — 105 passed (varredura vazia) |
| Neutralizar `AuthState._guarda` / `guarda_*` | **Não** — 105 passed (`mutacao.py`, seção D) |
| Trocar/remover a guarda do `on_load` de `/admin` | **Não** — nenhum teste importa `gsi_ebd.gsi_ebd`; o único `on_load` em `tests/` é a função sintética de `test_guarda_rota_redireciona_e_libera`, que testa o `rbac.guarda_rota` **não usado** pelo app |

### 5.3 Os 23 casos, por cobertura real

- Matriz de rotas/ações, chave desconhecida, identidade, lista congelada, decorador isolado:
  **reais** (o contrafactual e as mutações acima confirmam).
- `test_guarda_rota_redireciona_e_libera` (F-09/F-10/F-11): testa `rbac.guarda_rota`, não
  `AuthState.guarda_*`; o `guarda_rota` do `rbac` não tem uso no app.
- Nenhum caso **executa** um handler real barrado (F-13..F-17, F-25, F-26) — só a presença do
  marcador seria o proxy, e o proxy está vazio.
- F-18 e F-26 (papel permitido **executa**) não têm teste (exigiria banco).
- F-27 (síncrono/assinatura) não tem teste, embora o código preserve.
- F-06 (rotas públicas) não tem teste e o `pode` **nega** as rotas públicas (ver §7).

## 6. Adversarial — o que o autor não fechou

Nenhum caminho de escalada de papel foi encontrado. Ainda assim:

1. **`CoordenadorState.toggle_aluno` / `assign_study` — id de aluno do cliente sem pertença.**
   `toggle_aluno` (`coordenador.py:242-252`) só converte `int(aluno_id)` e guarda; não confere se o
   aluno é da turma/ambiente do coordenador. Sondado: `toggle_aluno("999999")` →
   `selected_aluno_ids == [999999]`. `assign_study` (`:269-335`) grava `StudyAssignment` para
   **esses ids**, sem checar o ambiente do aluno. É a **mesma classe** (autorização), mas o RF08
   pede só exclusividade de papel; a pertença fina/tenant está declarada fora do escopo
   (DEM-202610-010). Não é furo novo do `/admin`, é resíduo do modelo.
2. **`AlunoState` inteiro sem guarda** (`aluno.py`): `load_assigned_studies`, `load_pareceres`,
   `select_study`, `start_study`, `submit_answer` não têm `@exige`, não checam
   `is_authenticated` nem posse do estudo. `start_study(study_id, version_id)` carrega
   `StudyService.load_version_payload(version_id)` **direto do id do cliente** (`:147`);
   `submit_answer` grava `UserResponse` com `current_user_id` (que pode ser `None` num cliente
   anônimo) e `_finish_study` grava `Progress` com `study_id` escolhido pelo cliente
   (`:223-231`). Conteúdo de qualquer versão + escrita com id arbitrário. RF07 cobre só os **3
   estados administrativos**, então está fora do contrato — mas é o mesmo tipo de furo que o
   commit diz ter fechado.
3. **`RevisaoState.abrir_resposta`** aceita qualquer `response_id` do cliente, mas a página
   renderiza a partir de `pendentes` (filtrado por `_alunos_do_avaliador`) e a **escrita**
   (`salvar_parecer`) e a sugestão (`sugerir_parecer`) conferem posse no service
   ("Você não acompanha este aluno"). **Sem exploração encontrada**; o teste de pertença está no
   service, não no handler.
4. **Mudança de `current_user_role` fora do login**: só `auth.py:138` (login, do banco) e
   `auth.py:190` (logout → ALUNO). Nenhum `getattr("set_"+...)`, nenhum `add_var`, nenhum
   `_add_event_handler` no app. `setvar` bloqueado (§2).
5. **`is_instrutor` é event handler público** (não é `@rx.var`, ao contrário dos irmãos
   `is_admin`/`is_revisor`/…). Devolve `bool`; inofensivo, mas é uma inconsistência.
6. **`AdminState._reload_all` chama `load_coordenadores()` duas vezes** (bug de duplicação, sem
   impacto de segurança).

## 7. Divergências contrato × código (documentação)

1. **F-06 / spec §2**: `pode("rota:/login", X)` e das demais públicas (`/`, `/confirmar/[token]`,
   `/homenagens`) devolve **False** para todo papel. A matriz só tem rotas **protegidas**; a
   função pura não representa as públicas como a F-06 pede. Sem impacto funcional (as páginas
   públicas não chamam a guarda), mas F-06 **reprova** se for executada.
2. **F-19 × F-25**: o plano se contradiz — F-19 diz que REVISOR **aprova**; F-25/RF10 diz que é
   **barrado**. O código segue F-25 (`acao:catalogo_aprovar` = ADMIN). F-19 está errada no plano.
3. **Spec §5 × design §4**: a spec nomeia `ROTAS_PROTEGIDAS`/`pode_acessar`; o design v3 e o
   código usam `PERMISSOES`/`pode`. O design venceu; a spec ficou desatualizada.
4. **Commit message**: diz "`guarda_rota` nos `on_load`" — o código usa `AuthState.guarda_admin/
   coordenador/revisao`; `rbac.guarda_rota` é dead code.
5. **Intent §2/§6 (403)** × **spec §5/CA01 (redirect)**: o código redireciona (client-side), não
   responde 403. O comportamento entregue é o da spec; o 403 literal do intent não existe.
6. **F-08**: a invariante é testada contra `rbac.home_do_papel`, não contra
   `AuthService.redirect_for_role` (a fonte que o login usa). Hoje idênticos; risco de drift.
7. **F-12/F-13..F-19/F-25/F-26/F-27** estão no plano, mas o `test_rbac.py` não os implementa
   (proxy de marcador, e o proxy é vazio).

## 8. Escopo e higiene (C-01/C-02)

`git show --stat 65fbf7a` — **11 arquivos**, todos da DEM:

```
rxconfig.py · gsi_ebd/gsi_ebd.py · gsi_ebd/utils/rbac.py
gsi_ebd/states/{auth,admin,coordenador,revisao,aluno,perfil}.py
gsi_ebd/landing_content/controller.py · tests/test_rbac.py
470 insertions(+), 7 deletions(-)
```

- **Nenhuma dependência nova**: `requirements.txt`, `requirements-dev.txt`, `pyproject.toml`,
  `uv.lock` intocados no commit.
- **Nenhum schema/modelo**: `gsi_ebd/models/` e `alembic/` intocados.
- **Nenhum deploy**: `deploy/` e `.github/` intocados.
- **Nenhum segredo**: nada em `.env`.
- 20 setters explícitos: Auth 2 + Admin 4 + Coordenador 1 + Revisão 2 + Aluno 1 + Perfil 3 +
  Landing 7 = **20** (19 de formulário + `set_selected_study_option` validado). Confere.

## 9. Limites (o que não deu para provar sem browser/banco)

- **H-06**: provei que a guarda devolve `rx.redirect` correto e que os loaders barram sem abrir
  sessão. **Não** provei, sem browser, que o SPA executa o redirect antes de pintar o painel, nem
  que um GET direto a `/admin` devolve 403 (não devolve: é SPA).
- Não executei handler com papel **permitido** que grava no banco (F-18/F-26): exigiria escrita no
  banco do app; a evidência é o marcador + a leitura do código.
- Não abri conexão websocket para forjar o evento `setvar` no barramento real; a prova é a chamada
  direta do handler registrado (`EventHandlerSetVar.setvar`) e o código do Reflex.

## 10. Evidências (nesta pasta)

| Arquivo | O que contém |
|---|---|
| `saida_pytest.txt` | `pytest tests -q` → 105 passed |
| `saida_rbac.txt` / `saida_rbac_collect.txt` | 23 passed / 23 coletados |
| `saida_paginas.txt` | 9 passed |
| `saida_verificacao.txt` | config, 7 estados, `setvar`, matriz, guarda real, on_load, 28 marcadores, handlers reais barrados, adversarial |
| `saida_mutacao.txt` | varredura vazia; marcadores removidos = verde; lista congelada = vermelho; guarda neutralizada = 105 passed |
| `saida_counterfactual.txt` | `state_auto_setters=True` recria os 7 setters e o `setvar` vira ADMIN; testes de identidade reprovam |
| `saida_git.txt` | `git show --stat`, arquivos do commit, worktree limpo |
| `verificacao.py` · `mutacao.py` · `counterfactual.py` · `probe_scan.py` | scripts das sondas (memória, sem editar o app) |
