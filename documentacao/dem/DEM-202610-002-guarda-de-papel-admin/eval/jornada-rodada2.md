# Jornada do EVAL — rodada 2 (cega e adversarial)

**DEM:** DEM-202610-002 / guarda-de-papel-admin
**Repositório:** `C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD`
**Commit avaliado:** `6768ea9` — `fix(dem-002): testes que realmente testam (EVAL rodada 1: FAIL de teste)`
**Data:** 2026-10-18 (America/Sao_Paulo)
**Ambiente:** Windows; `.venv\Scripts\python.exe`; todos os comandos executados **do diretório do app**; Reflex 0.9.5.post2.
**Leitura:** `planner/{intent,spec,design,plano-testes}.md` e o código do app. Não li `dev/`, o README/changelog da DEM nem as jornadas anteriores em `eval/`.

## 0. Resumo executivo

- O defeito central da rodada 1 (varredura que examinava **zero** métodos e passava com os 28 `@exige` removidos) **está corrigido**: a varredura agora itera `event_handlers` e examina **28** eventos.
- **As 5 mutações pedidas reprovam** (com uma ressalva no item 3: a matriz reprova, o teste do guarda real não).
- `guarda_rota` **não é mais dead code**: os 3 guardas do app usam o decorador, e o teste toca o handler real.
- **F-06/F-08 passam**; **F-19** está corrigido no plano (ADMIN positivo, REVISOR negativo), mas **não há teste que execute o handler**; o EVAL o exercitou por sonda e o código passa.
- **H-06:** o comportamento está certo (redirect para a casa, sem dado administrativo), mas o `intent.md` **ainda diz 403 em quatro lugares** (§2, §4 In, §5 e §8.3). O `spec.md` não diz 403 (RNF “redirecionar”, CA01 “volta a /aluno”). Contrato internamente incoerente.
- **Nenhum bypass de guarda atual** foi encontrado. A sonda exercitou os **28 handlers × 5 papéis** (140 células) em instâncias reais: todos batem com a matriz; papel negado não abre sessão nem muda estado.
- **Cobertura incompleta:** uma mutação de **chave errada** (`load_leads` com `acao:catalogo_ler`) passa pela suíte e deixa o REVISOR carregar leads (F-18/F-26 não existem como teste). Uma mutação do **destino do redirect** (`home_do_papel -> /login`) também passa. Ambas são regressões futuras, não furos atuais.
- **Escopo:** `6768ea9` toca só 4 arquivos, todos da DEM; o range da DEM não toca schema, dependências nem deploy.

**Agregado: FAIL — 2 bloqueios (cobertura de evento por chave e incoerência do intent). O comportamento atual da guarda está correto; o que reprova é o contrato e a cobertura, não um furo explorável hoje.** Detalhe por categoria no §9.

## 1. Método

1. `pytest tests -q` no diretório do app → **109 passed**.
2. `eval/auditoria_rodada2.py` → matriz, identidade, `setvar`, `on_load`, os 28 marcadores e os destinos reais dos guardas.
3. `eval/mutacoes_rodada2.py m1..m7` → mutações **em memória**, cada uma em processo novo, sem tocar em arquivo do app.
4. `eval/sonda_handlers_rodada2.py` → instâncias reais de `AuthState` + substates, `reflex.session` trocado por sentinela que **levanta** ao ser aberta: papel negado não abre sessão; papel permitido delega. 28 handlers × 5 papéis.
5. `git show --stat 6768ea9` e `git diff --stat 9a27dd3..6768ea9`.
6. `git status` do app limpo; `HEAD = 6768ea9`.

Nada foi alterado no app. As saídas brutas estão em `eval/saida_rodada2_auditoria.txt`, `saida_rodada2_mutacoes.txt`, `saida_rodada2_sonda_handlers.txt` e `saida_rodada2_pytest.txt`.

## 2. Regressão dos 3 furos (o que já estava aprovado)

| Furo | Verificação feita | Resultado |
|---|---|---|
| **Identidade** | 7 estados (`AuthState`, `AdminState`, `CoordenadorState`, `RevisaoState`, `AlunoState`, `PerfilState`, `CommonState`) sem `set_current_user_*`, `set_is_authenticated` e `set_must_change_password` — nem como atributo, nem em `event_handlers`. `state_auto_setters=False` lido pelo Reflex. | **PASS** |
| **Identidade / `setvar`** | `setvar("current_user_role", 1)`, `("current_user_id", 999)`, `("is_authenticated", True)` e `("must_change_password", False)` em `AuthState` e em `AdminState` → `AttributeError: Variable ... cannot be set`. `setvar` só chama `set_<var>`, e esses setters não existem. | **PASS** |
| **Rota** | `on_load` real do app: `/admin` = `[AuthState.guarda_admin, AdminState.load_coordenadores]`; `/coordenador` = `[guarda_coordenador, load_all]`; `/revisao` = `[guarda_revisao, load_fila]`. | **PASS** |
| **Evento** | **28** `@exige`: `AdminState` 13 (`load_coordenadores`, `load_leads`, `load_estudos_pendentes`, `load_obras`, `load_estudos_aplicados`, `create_gestor`, `activate_user`, `suspend_user`, `cancel_user`, `update_lead_status`, `aprovar_estudo`, `aprovar_todos`, `rejeitar_estudo`), `CoordenadorState` 8, `RevisaoState` 7. A varredura examina **28**, não zero. | **PASS** |

Observação: há **9** classes de estado no app; `LandingState` e `HomenagensState` herdam `rx.State` e não têm var de identidade. Os “7 estados” do teste cobrem todos os que herdam `AuthState` (ou `rx.State` com vars próprias). Não é furo hoje; se uma delas passar a herdar `AuthState`, o teste não a cobre.

## 3. Mutações em memória — uma por uma

Todas em processo novo, do diretório do app, sem tocar em arquivo.

| # | Mutação | Teste que deveria acusar | Reprovou? | Evidência |
|---|---|---|---|---|
| **1** | Trocar o `fn` de `AdminState.load_coordenadores` pelo `__wrapped__` (equivale a remover o `@exige`) | `test_todo_evento_tem_marcador_exige` | **SIM** | `AdminState sem @exige: ['load_coordenadores']` |
| **1b** | Mesma mutação em `RevisaoState.abrir_resposta` | idem | **SIM** | `RevisaoState sem @exige: ['abrir_resposta']` |
| **2** | Remover `AuthState.guarda_admin` do `on_load` de `/admin` | `test_fiacao_on_load_das_rotas_guardadas` | **SIM** | `/admin sem o guarda no on_load: [<function AdminState.load_coordenadores>]` |
| **3** | `PERMISSOES["rota:/admin"] = (Role.ADMIN,)` (tirar o REVISOR) | `test_matriz_de_rotas("/admin", ...)` | **SIM** | `REVISOR deveria poder /admin` |
| **3b** | A mesma mutação do item 3 | `test_guarda_real_bloqueia_e_libera` | **NÃO** | O teste lê `rbac.PERMISSOES["rota:"+rota]` como oráculo; com a matriz mutada ele “espera” o REVISOR barrado e passa. O guarda real **barra** o REVISOR, mas o teste não é independente. |
| **4** | `PERMISSOES["acao:catalogo_aprovar"] = (Role.ADMIN, Role.REVISOR)` | `test_matriz_de_acoes("acao:catalogo_aprovar", ...)` | **SIM** | `REVISOR NAO deveria poder acao:catalogo_aprovar` |
| **5** | `get_config().state_auto_setters = True` **antes** de importar os estados (contrafactual) | `test_nenhum_setter_de_identidade` | **SIM** | `AuthState expoe ['set_current_user_id', 'set_current_user_name', 'set_current_user_role', 'set_current_user_status', 'set_current_user_ambiente', 'set_is_authenticated', 'set_must_change_password']`; `setvar("current_user_role", 1)` vira `EventSpec` — o cliente escreveria a identidade. `test_state_auto_setters_desligado` também reprova. |
| **m6** (extra) | `rbac.home_do_papel = lambda papel: "/login"` | `test_invariante_casa_do_papel`, `test_home_consistente_com_authservice`, `test_guarda_real_bloqueia_e_libera`, `test_guarda_rota_redireciona_e_libera` | **NÃO** | Os quatro passam: ninguém afirma o **destino** do redirect (só “não é None”). O código atual acerta (`/aluno`, `/coordenador`, `/revisao`, `/admin`, `/login`), mas a regressão não seria pega. |
| **m7** (extra) | `AdminState.load_leads` decorado com `acao:catalogo_ler` (chave errada; marcador presente) | suíte relevante (`test_todo_evento...`, `test_lista_de_eventos_congelada`) | **NÃO** | Os testes passam; o REVISOR passa a **delegar** em `load_leads` (sessão aberta) — vazamento de leads que a suíte não acusa. É o furo de cobertura F-18/F-26. |

**Leitura:** as 5 mutações pedidas reprovam. O defeito da rodada 1 (varredura vazia) não existe mais. As duas mutações extras (m6/m7) mostram que a suíte ainda não é **completa**: ela prova que *há* um `@exige`, não que a **chave** é a da matriz, e não prova o **destino** do redirect.

## 4. F-06, F-08, F-19 e H-06

### F-06 — rotas públicas

- As 8 rotas públicas/abertas (`/`, `/login`, `/confirmar/[token]`, `/homenagens`, `/aluno`, `/aluno/licao`, `/aluno/pareceres`, `/perfil/alterar-senha`) respondem `pode=True` para os **5 papéis** (40 células; `test_rotas_publicas_abertas_a_todos`).
- **Anônimo:** `pode("rota:/", -1) = False`. O anônimo não tem assento na matriz (`pode` recebe `int`), e as rotas públicas não têm guarda de papel — o acesso anônimo é preservado pela **ausência** de guarda, não por `pode`. O plano F-06 pede “e para anônimo”; literalmente, isso não é testado nem representável no `pode`. Comportamento correto, cobertura literal incompleta (**WARN**).
- O `_TODOS` nas rotas públicas é só para `pode` ser total; não cria poder novo.

### F-08 — casa do papel

- `AuthService.redirect_for_role` **delega** para `rbac.home_do_papel` (fonte única). Para os 5 papéis a igualdade é verdadeira e `pode("rota:"+casa, papel)` é `True`; papel inválido (99) → `/login` nos dois.
- `test_home_consistente_com_authservice` e `test_invariante_casa_do_papel` passam. **PASS.**
- Nuance: o teste da invariante **pula** `/login` (`if casa == "/login": continue`), então “casa inválida → /login” não é afirmado por ele; é afirmado pela sonda/auditoria (papel 99 → `/login`). Cobertura N-02 mínima.

### F-19 — caso positivo com ADMIN

- O **plano** foi corrigido: F-19 é o positivo com ADMIN; F-25 é o negativo com REVISOR; RF10 separa `catalogo_ler` (ADMIN+REVISOR) de `catalogo_aprovar` (ADMIN). A contradição da rodada 1 não está mais no plano.
- No **código**, `aprovar_estudo`/`aprovar_todos`/`rejeitar_estudo` têm `@exige("acao:catalogo_aprovar")`; `pode(..., ADMIN)=True`, `pode(..., REVISOR)=False`.
- Na **suíte**, não há teste que **execute** `aprovar_estudo`/`aprovar_todos`/`rejeitar_estudo` com ADMIN (nem com REVISOR). O que existe é a matriz (`test_matriz_de_acoes`) e o marcador. O EVAL executou os três por sonda: com ADMIN **delegam** (abrem sessão), com REVISOR **não abrem** e não mudam estado. O código passa; a suíte não protege a regressão F-19/F-25 (**WARN/cobertura**).

### H-06 — intent, spec e código

- **Código:** correto. Anônimo → `/login`; ALUNO → `/aluno`; COORDENADOR → `/coordenador`; INSTRUTOR → `/revisao`; REVISOR e ADMIN → seguem em `/admin`. Nenhum 403. Os loaders de dado administrativo (`acao:usuarios`, `acao:leads`) não abrem sessão para ALUNO/COORDENADOR/INSTRUTOR/REVISOR (sonda).
- **`spec.md`:** não contém 403. O RNF do §4 diz “A resposta de acesso negado é **redirecionar**”; CA01 diz “não permanece; volta a `/aluno`”. Coerente com o código.
- **`intent.md`:** a nota do H-06 (linha 63) diz “não há 403... a métrica passa a ser essa”, **mas o resto do intent continua prometendo 403**:
  - §2 (linha 26): “recebe **403** na rota”;
  - §4 In (linha 41): “teste ... que prova o **403**”;
  - §5 Constraints duras (linha 56): “A resposta de acesso negado é **403**”;
  - §8.3 (linha 76): “**403** na rota; na navegação, devolver ao painel do papel”.
- O intent está `status: signed` e a nota é posterior. Uma nota de métrica não revoga uma constraint dura; o correto seria reabrir/re-assinar o intent e remover o 403 de §2/§4/§5/§8.3. **Intent/spec/código NÃO estão coerentes entre si: spec e código sim; o intent não.** Isto é **FAIL de contrato (documentação)**, não de comportamento. Se o PLANNER re-assinar o intent sem o 403, o bloqueio cai.

## 5. `guarda_rota`: usado pelo app ou dead code?

- **Usado.** `gsi_ebd/states/auth.py` aplica `@guarda_rota("/admin")`, `("/coordenador")`, `("/revisao")` em `guarda_admin`, `guarda_coordenador`, `guarda_revisao`; os três handlers estão no `on_load` das três páginas; `__guarda_rota__` está gravado nos três wrappers.
- O teste `test_guarda_real_bloqueia_e_libera` chama `AuthState.guarda_* .fn` — **o mesmo objeto** que o `test_fiacao_on_load_das_rotas_guardadas` encontra no `on_load`. A cadeia é real, não uma cópia sintética.
- `rbac.require_role` continua existindo e **sem uso** (legado declarado no design). Não é guarda de evento nenhum; não é o `guarda_rota`.
- Higiene: `auth.py` importa `home_do_papel` e `pode` e não os usa mais (o `_guarda` antigo foi removido); `tests/test_rbac.py` importa `inspect` e não usa. Não afeta segurança.

## 6. Suíte

| Medida | Resultado |
|---|---|
| `pytest tests -q` no diretório do app | **109 passed**, 2 warnings (cache do pytest sem permissão de escrita) |
| `tests/test_rbac.py` | **27** (11 testes simples + 3 parametrizações de rota + 6 de ação + 7 de lista congelada) |
| `tests/test_paginas.py` | **9/9** |
| `test_paginas.py` alterado no 6768ea9? | Não (intocado) |

Os 27 de `test_rbac` cobrem: matriz de rotas/ações, chave desconhecida, invariante, identidade/auto setters, lista congelada, varredura de marcador, rotas públicas, consistência da casa, fiação do `on_load`, guarda real, decorador `exige` e decorador `guarda_rota`.

## 7. Adversarial — o que ainda não está coberto

### 7.1 Não há furo de guarda atual

- **`current_user_role`:** as únicas escritas no app são `login` (role do usuário lido do banco) e `logout` (reset para ALUNO), em `gsi_ebd/states/auth.py:135-141` e `185-191`. Nenhum evento de página escreve papel. `setvar` não alcança (AttributeError nos 4 vars de identidade, em `AuthState` e `AdminState`).
- **Sonda dos 28 handlers × 5 papéis:** em instância real (substate com o papel injetado no pai), papel negado **não abre sessão** e **não muda estado**; papel permitido delega. As 140 células batem com `PERMISSOES`. Isso cobre na prática F-13, F-14, F-16, F-17, F-18, F-19 e F-26.
- **`ReviewService`:** `registrar_parecer` e `sugerir_parecer` conferem `r.user_id in permitidos` (pertença). `abrir_resposta(response_id)` só grava o id na UI; sem o parecer/sugestão, não vaza conteúdo. `salvar_parecer`/`pedir_sugestao` são barrados para resposta de aluno fora do escopo do instrutor.
- **`AdminState.create_gestor`** cria apenas COORDENADOR (não cria ADMIN); `activate/suspend/cancel` exigem `acao:usuarios` (ADMIN) e usam `can_manage` como segunda checagem. `can_manage` não confere ambiente, mas só o ADMIN chega nele (o REVISOR é barrado antes pelo `@exige`).

### 7.2 Fora do escopo (mesma classe, para a DEM-010)

O autor já registrou; confirmo o mecanismo:

- `CoordenadorState.toggle_aluno(aluno_id)` aceita qualquer id para a seleção; `assign_study` grava `StudyAssignment` para **qualquer** `selected_aluno_ids`, sem conferir se o aluno é da turma/ambiente do coordenador. Um COORDENADOR pode atribuir estudo a aluno de outro tenant (escrita cross-tenant). Não é acesso administrativo; é posse/tenant → **DEM-010**.
- `AlunoState.start_study(study_id, version_id)` carrega o payload de **qualquer** `version_id`, sem conferir se a versão foi atribuída ao aluno; `submit_answer` grava resposta em cima do `current_version_id` escolhido. Também `select_study(study_id)` aceita id arbitrário (mas só carrega conteúdo se estiver em `assigned_studies`). **DEM-010**.
- `AdminState.update_lead_status`/`aprovar_estudo`/`rejeitar_estudo` recebem id, mas são ADMIN-only e operam catálogo/leads globais — o ADMIN é global por definição (`EscopoService`). Não há pertença a conferir nesse nível.

### 7.3 Achados novos (não registrados)

1. **Chave errada do `@exige` não é testada (F-18/F-26 ausentes).** `test_todo_evento_tem_marcador_exige` só verifica que `__exige__` existe, não que ele é a chave da matriz. Mutação m7: `load_leads` com `acao:catalogo_ler` passa pela suíte e o REVISOR passa a carregar leads (dado administrativo). **É o furo de cobertura mais sério da rodada.** O código atual está correto (auditoria e sonda confirmam as 28 chaves), mas a suíte não o protege.
2. **Destino do redirect não é asserido (m6).** Os testes só checam “não é None”. `home_do_papel -> /login` passa nos quatro testes de casa/guarda. O H-06 (“devolvido ao painel dele”) não é provado pela suíte; a auditoria do EVAL prova que o código atual acerta.
3. **Resíduo de estado no logout.** `AuthState.logout` reseta a identidade, mas **não limpa** os vars do substate `AdminState` (`coordenadores`, `leads`, `estudos_*`). No mesmo navegador/token, um REVISOR que entra depois de um ADMIN (que fez logout) pode ver os dados administrativos que o ADMIN já carregou, embora `load_coordenadores`/`load_leads` estejam barrados para ele. Não é bypass de guarda (o REVISOR é autorizado em `/admin`; os dados ficam no estado), é **higiene de estado/sessão**. Sugiro DEM própria (limpar substates no logout ou rotacionar token). **WARN, fora do escopo estrito da DEM-002.**
4. **Casos do plano sem teste executável na suíte:** F-13, F-14, F-15, F-16, F-17, F-18, F-19, F-26 (execução por papel) e F-27 (handler decorado continua síncrono e com assinatura original) e F-28 (suíte do diretório do app). O EVAL cobriu F-13..F-19/F-26 por sonda e F-27 pela inspeção de assinatura; o código passa. Mas o plano é o contrato e a suíte não os contém. F-27: as assinaturas impressas pela auditoria são as originais (`activate_user(self, user_id: int)`, etc.), `functools.wraps` preserva; não há `inspect.iscoroutinefunction` em teste.
5. **Varredura pula todo nome `set_*`.** Um mutador perigoso chamado `set_...` (que não seja de identidade) não é examinado por F-12; a lista congelada é a única rede. Se um dev atualizar `FROZEN` e adicionar um `set_...`, a varredura não acusa. Hoje todos os `set_*` dos 3 estados são setters de formulário/UI legítimos (4 no Admin, 1 no Coordenador, 2 na Revisão), e os de identidade são pegos por F-23.
6. **`permitidos` como oráculo no teste do guarda real (m3b).** O teste acompanha a matriz; só `test_matriz_de_rotas`/`test_matriz_de_acoes` são oráculos independentes (parâmetros hardcoded). Funciona hoje porque os dois existem, mas o teste do guarda real não é independente.
7. **Anônimo no F-06** (já no §4) e **N-02** (papel inválido) não têm teste na suíte; a auditoria confirma o comportamento.

## 8. Escopo

- `git show --stat 6768ea9`: **4 arquivos**, todos da DEM — `gsi_ebd/services/auth_service.py`, `gsi_ebd/states/auth.py`, `gsi_ebd/utils/rbac.py`, `tests/test_rbac.py`.
- Range da DEM (`9a27dd3..6768ea9`): 12 arquivos — `gsi_ebd.py`, `landing_content/controller.py`, `services/auth_service.py`, `states/{admin,aluno,auth,coordenador,perfil,revisao}.py`, `utils/rbac.py`, `rxconfig.py`, `tests/test_rbac.py`.
- **Sem** `gsi_ebd/models/` (schema), **sem** `requirements*.txt` (dependência), **sem** scripts/workflows de deploy, **sem** `tests/test_paginas.py` (intocado).
- Não há segredo/credencial nova. `create_gestor` continua com senha inicial fixa (“senha123”) e `must_change_password=True` — pré-existente, fora do escopo desta DEM, mas é dívida de segurança para outra DEM.

## 9. Veredito

| Categoria | Veredito | Base |
|---|---|---|
| Regressão dos 3 furos | **PASS** | identidade (7 estados + `setvar`), rota (3 `on_load`), evento (28 marcadores) |
| 5 mutações pedidas | **PASS 5/5** | m1, m1b, m2, m3 (matriz), m4, m5 — todas reprovam |
| Segurança atual da guarda | **PASS** | sonda 140 células; nenhum papel negado abre sessão/muda estado; nenhum caminho de escrita de `current_user_role` fora de login/logout |
| F-06 / F-08 | **PASS** (F-06 com ressalva do anônimo) | 40/40 papéis×rotas públicas; casa única e invariante |
| F-19 / F-25 | **PASS no comportamento; FAIL de cobertura** | matriz + marcador; sem teste que execute os handlers com ADMIN/REVISOR na suíte (a sonda do EVAL passa) |
| `guarda_rota` | **PASS** | usado pelos 3 guardas e testado no handler real |
| Suíte | **PASS** | 109; `test_rbac` 27; `test_paginas` 9/9 |
| H-06 / contrato | **FAIL (documentação)** | código redireciona e a spec também; `intent.md` §2/§4/§5/§8.3 ainda dizem 403 |
| Cobertura adversarial | **FAIL** | m7 (chave errada) e m6 (destino) não reprovam; F-13..F-19/F-26/F-27/F-28 sem teste na suíte; resíduo de estado no logout |
| Escopo | **PASS** | 4 arquivos no commit; sem schema/dependência/deploy |

**Agregado: FAIL.**

Dois bloqueios, nenhum deles um furo de guarda atual:

1. **Cobertura de evento por chave (F-18/F-26):** a suíte prova presença de `@exige`, não a chave certa; a mutação m7 deixa o REVISOR carregar leads e passa em tudo. O código está correto hoje; falta o teste que mapeia handler → chave (a sonda deste EVAL é o roteiro).
2. **Contrato H-06:** o `intent.md` assinado ainda promete 403 em §2/§4/§5/§8.3, enquanto spec e código entregam redirect. Precisa de re-assinatura/emenda do intent, não de nota de métrica.

Ressalvas não bloqueantes: destino do redirect não asserido (m6), resíduo de estado no logout, F-27/F-28 sem teste, anônimo do F-06 não representado, `set_*` pulado pela varredura.

**O defeito da rodada 1 está corrigido:** a varredura examina 28 eventos, as 5 mutações pedidas reprovam, `guarda_rota` é o guarda real e o teste toca o handler que o app usa.
