# EVAL cego — DEM-202610-002 / guarda de papel — rodada 3

- **Data:** 2026-10-18
- **DEM:** DEM-202610-002-guarda-de-papel-admin
- **Commit avaliado:** `7cb2ee2` — *fix(dem-002): cobre a CHAVE de cada evento e o destino do redirect (EVAL rodada 2)*
- **Diretório de execução:** `ESTUDOS_BIBLICOS/GSI_EBD` (cwd do app)
- **Python:** `.venv\Scripts\python.exe`
- **Contrato usado:** `planner/{intent,spec,design,plano-testes}.md`. Não li `dev/`, README da DEM nem jornadas anteriores. O `changelog.md` foi aberto **apenas** para o item 8 (registro do WARN do `logout`), como o próprio checklist pede.
- **Natureza:** cega e adversarial; nada foi corrigido. As mutações foram feitas **em memória**, em processo separado do `pytest`, e restauradas ao final.

## Veredito por categoria

| # | Categoria | Veredito | Resumo |
|---|---|---|---|
| 1 | **m7** — chave errada por evento | **PASS** | `load_leads` decorado com `acao:catalogo_ler` **reprova**; mapa cobre 13/13, 8/8 e 7/7 eventos não-setter |
| 2 | **m6** — destino do redirect | **PASS** | `home_do_papel → /login` **reprova**; oráculo das casas é hardcoded no teste |
| 3 | **Contrato (403)** | **PASS** | Nenhuma afirmação de 403 como resposta; §2/§4 sem a palavra, §5/§8.3 só a negam, §6 é a nota histórica |
| 4 | **Regressão dos 3 furos** | **PASS** | Identidade: 7/7 estados sem setter e `setvar` → `AttributeError`; rota: 3 `on_load` com guarda; evento: 28 `@exige` com as chaves certas |
| 5 | **Negativo dos handlers reais** | **PASS com WARN** | O teste chama `.fn` e 7/8 casos são não-vacuosos; `abrir_resposta` sozinho não prova o barramento (F-12/F-18 suprem) |
| 6 | **Suíte** | **PASS** | `113 passed`; `test_rbac` **31**; `test_paginas` **9/9** |
| 7 | **Escopo** | **PASS** | `git show --stat 7cb2ee2` = só `tests/test_rbac.py`; diff da DEM sem schema/dependência/deploy |
| 8 | **Adversarial** | **PASS com observações** | 28 chaves coerentes com design §4; nenhuma rota com `pode` incoerente; WARN do `logout` registrado |
| — | **AGREGADO** | **PASS** | Os dois bloqueios da rodada 2 estão fechados; restam WARNs não bloqueantes |

---

## 1. m7 — a chave de cada evento

**Mutação:** em memória, `AdminState.event_handlers["load_leads"].fn.__exige__ = "acao:catalogo_ler"` (equivale a trocar o decorador na fonte) e chamada direta de `test_chave_de_cada_evento("AdminState")`.

```
M7 REPROVOU -> AdminState: chave errada em {'load_leads': ('acao:catalogo_ler', 'acao:leads')} (real, esperado)
```

**Cobertura do mapa** (`CHAVES_ESPERADAS` × eventos não-setter reais, medido em memória):

| Estado | Eventos não-setter | Entradas no mapa | Faltando | Sobrando |
|---|---|---|---|---|
| `AdminState` | 13 | 13 | — | — |
| `CoordenadorState` | 8 | 8 | — | — |
| `RevisaoState` | 7 | 7 | — | — |

**Evento sem chave no mapa:** removendo `load_leads` do mapa (em memória), o teste também reprova:

```
M7b REPROVOU -> AdminState: chave errada em {'load_leads': ('acao:leads', None)} (real, esperado)
```

O `diff` do teste percorre a **união** das chaves reais e esperadas; portanto evento novo sem classificação e chave trocada caem os dois. Confirmado.

## 2. m6 — o destino do redirect

**Mutação:** em memória, `rbac.home_do_papel = lambda papel: "/login"` (equivale a trocar a casa do papel na fonte, já que `AuthService.redirect_for_role` delega para ela) e chamada de `test_guarda_real_bloqueia_e_libera`.

```
M6 REPROVOU -> /admin: COORDENADOR deveria ir para /coordenador, foi /login
```

O oráculo é **hardcoded**: o teste tem `casas = {ADMIN: "/admin", REVISOR: "/admin", COORDENADOR: "/coordenador", INSTRUTOR: "/revisao", ALUNO: "/aluno"}` e **não** chama `home_do_papel` para decidir o esperado. As únicas menções a `home_do_papel` no arquivo são em outro teste (invariante/consistência com `AuthService`, linhas 123 e 199), não no teste de destino. O caminho é extraído do `EventSpec` de `rx.redirect` por `_destino`. Restaurado o original, os dois testes voltam a passar.

## 3. Contrato — o 403

Busca por `403` em `planner/*.md`:

| Arquivo:linha | Texto | Afirma 403? |
|---|---|---|
| `intent.md:57` (§5) | “**Não há 403**: a rota é servida pelo SPA…” | **Não** — nega |
| `intent.md:65` (§6, nota H-06) | “a formulação original dizia ‘recebe 403’. Não há 403…” | **Não** — citação histórica permitida |
| `intent.md:78` (§8.3) | “**Redirect para a casa do papel**, sem 403 HTTP” | **Não** — nega |

- **§2** e **§4 (In)** não contêm a palavra `403`; dizem “devolvido ao seu painel / loader não executa” e “redirect para a casa do papel e loader que não carrega”.
- **§5** e **§8.3** dizem redirect/casa do papel e usam `403` apenas para negá-lo.
- **§6/H-06** é a nota que o próprio checklist autoriza citar a formulação antiga.

**Spec §4/CA01 × código:** spec §4 diz “a resposta de acesso negado é redirecionar”; CA01 diz que o aluno “não permanece; volta a `/aluno`”. No código, `guarda_rota` devolve `rx.redirect(home_do_papel(ALUNO))` = `/aluno`, e o loader é barrado pelo `@exige`. Concordam. Nenhuma menção afirmativa de 403 sobrou.

## 4. Regressão dos 3 furos

### 4.1 Identidade — 7 estados, nenhum setter, `setvar` fecha

Medido nos 7 estados (`AuthState`, `AdminState`, `CoordenadorState`, `RevisaoState`, `AlunoState`, `PerfilState`, `CommonState`):

- eventos de identidade (`set_current_user*`, `set_is_authenticated`, `set_must_change_password`): **[] em todos**;
- atributos `set_<campo>`: **nenhum** em todos;
- `estado.setvar("current_user_role", 1)`: **`AttributeError` nos 7** (“Variable `current_user_role` cannot be set on …”). O `setvar` não reabre a porta porque o Reflex o resolve para `set_<var>`, que não existe.

### 4.2 Rota — 3 `on_load` com guarda

`gsi_ebd/gsi_ebd.py`: `/admin` → `[AuthState.guarda_admin, …]`; `/coordenador` → `[AuthState.guarda_coordenador, …]`; `/revisao` → `[AuthState.guarda_revisao, …]`. `test_fiacao_on_load_das_rotas_guardadas` importa o app e confere o `on_load` real (não só a existência do decorador). Passa.

### 4.3 Evento — 28 `@exige` com as chaves certas

Contagem na fonte: **28** (13 em `admin.py`, 8 em `coordenador.py`, 7 em `revisao.py`). Chaves reais por evento, comparadas com `design.md` §4/spec §3a:

| Chave | Eventos | Papéis (matriz) | Coerente com §4/§3a |
|---|---|---|---|
| `acao:catalogo_ler` | `load_estudos_pendentes`, `load_obras`, `load_estudos_aplicados` | ADMIN, REVISOR | sim |
| `acao:catalogo_aprovar` | `aprovar_estudo`, `aprovar_todos`, `rejeitar_estudo` | ADMIN | sim |
| `acao:usuarios` | `load_coordenadores`, `create_gestor`, `activate_user`, `suspend_user`, `cancel_user` | ADMIN | sim (mutadores; o loader de usuários também é só ADMIN) |
| `acao:leads` | `load_leads`, `update_lead_status` | ADMIN | sim |
| `acao:coordenacao` | os 8 eventos de `CoordenadorState` | ADMIN, COORDENADOR | sim |
| `acao:revisao` | os 7 eventos de `RevisaoState` | ADMIN, INSTRUTOR | sim |

Nenhuma chave do mapa diverge da matriz do design §4.

## 5. Mutação dos handlers reais — `test_handlers_reais_barrados_nao_executam`

- O teste chama **`handler.fn`** (o wrapper real), não `vars(cls)` nem uma função sintética.
- Os 8 casos devolvem `None` com o papel negado.
- Prova de que não é vácuo por “sempre-permite”: trocando `rbac.pode` por `lambda *_: True` em memória, o teste **reprova** (`AttributeError: 'types.SimpleNamespace' object has no attribute 'is_admin'`), ou seja, o corpo seria executado se a guarda não barrasse.

**WARN — um caso fraco:** `abrir_resposta` **sem** `@exige` devolve `None` com um `SimpleNamespace` (o corpo só mexe em campos de estado). Simulei a remoção só desse decorador e `test_handlers_reais_barrados_nao_executam` **passou**. Ou seja, esse caso isolado não distingue “wrapper barrou” de “corpo rodou e retornou `None`”. O buraco **não** chega à suíte: com o decorador removido de `abrir_resposta`, `test_todo_evento_tem_marcador_exige` reprova (`RevisaoState sem @exige: ['abrir_resposta']`) e `test_chave_de_cada_evento` reprova (`(None, 'acao:revisao')`). Portanto é fraqueza de um caso, não da cobertura. Dos outros 7, seis levantam erro no corpo cru (`aprovar_estudo`, `aprovar_todos`, `rejeitar_estudo`, `activate_user`, `update_lead_status`, `assign_study`) e `load_leads` levantaria `TypeError` na chamada do teste com argumento extra (a assinatura não aceita `1`), então a remoção seria percebida.

## 6. Suíte

```
.venv\Scripts\python.exe -m pytest tests -q
113 passed, 2 warnings in 5.83s
```

| Arquivo | Casos | Resultado |
|---|---|---|
| `tests/test_rbac.py` | **31** | 31 passed |
| `tests/test_paginas.py` | **9** | 9/9 passed |
| Demais | 73 | passed |

`test_rbac` = 31: 3 rotas + 6 ações + desconhecida + invariante + auto setters + identidade + 7 congeladas + marcador + públicas + home consistente + fiação + 3 chaves + handlers reais + guarda real + `exige` barra + `guarda_rota` = 31. `state_auto_setters` foi lido do diretório do app (`False`), como o teste exige.

## 7. Escopo

```
git show --stat 7cb2ee2
 tests/test_rbac.py | 97 ++++++++++++++++++++++++++++++++++++++++++++++++++++--
 1 file changed, 94 insertions(+), 3 deletions(-)
```

- Só teste no commit avaliado. Sem `gsi_ebd/models/`, `alembic/`, `requirements*.txt`, `pyproject.toml`, `uv.lock`, `deploy/`, `docker-compose.yml`, `.github/`.
- Diff acumulado da DEM (`9a27dd3..7cb2ee2`): `gsi_ebd/*`, `rxconfig.py`, `tests/test_rbac.py` — nenhum schema, nenhuma dependência, nenhum deploy. (`deploy/didasko-deploy-entry.sh` aparece em `7cafeaa..7cb2ee2` por causa do commit **anterior** `9a27dd3`, que não é da DEM.)
- `git status --porcelain` do repositório do app: limpo. O único arquivo novo desta rodada é este `jornada-rodada3.md`, no guarda-chuva.

## 8. Adversarial

- **Chave × design §4:** todas as 28 conferem (tabela do item 4.3). Não há evento com chave “de outra família”.
- **Rota × `pode`:** `/admin` = ADMIN+REVISOR; `/coordenador` = ADMIN+COORDENADOR; `/revisao` = ADMIN+INSTRUTOR; casas iguais (`ADMIN/REVISOR→/admin`, `COORDENADOR→/coordenador`, `INSTRUTOR→/revisao`, `ALUNO→/aluno`). Nenhum papel é mandado para rota que ele não pode abrir; a invariante é testada.
- **Observação (não bloqueante):** `AdminState.load_coordenadores` está com `acao:usuarios` (ADMIN). Como `/admin` é permitido ao REVISOR e esse loader está no `on_load` da rota, o REVISOR entra em `/admin` mas não carrega a lista de gestores. Não é bypass (nega, não vaza); é escolha de matriz coerente com “usuários = ADMIN”.
- **`logout`:** confirmado no código: `AuthState.logout` limpa os campos de identidade, mas não zera `AdminState.leads`, `estudos_pendentes` etc. O WARN está **registrado** no `changelog.md` (“Pendência registrada (WARN do EVAL, fora do escopo)”, linhas 83–85), com a hipótese de REVISOR ver dado carregado pelo ADMIN anterior. Fora do escopo desta DEM, como declarado.

## 9. O que ainda falta (não bloqueia esta rodada)

1. **Fortalecer o caso `abrir_resposta`** (ou removê-lo) em `test_handlers_reais_barrados_nao_executam`: ele passa com o decorador removido porque o corpo cru devolve `None`. Enquanto o teste de marcador e o de chave existirem, a suíte ainda pega a remoção; o caso, sozinho, não prova nada.
2. **Marcador “falso”:** a suíte confia em `__exige__` como prova do decorador. Um `__exige__` atribuído à mão num handler fora dos 8 casos exercitados passaria F-12/F-18 (é sabotagem deliberada, não o erro acidental que os testes visam; F-12/F-18 pegam remoção sem marcador).
3. **F-06 e “anônimo”:** `pode("rota:/login", -1)` é `False`; o plano fala em “qualquer papel **e anônimo** → True”. Na prática as rotas públicas não têm guarda, então o comportamento está correto; o caso literal de F-06 para anônimo não é asserido.
4. **Nomes do contrato:** spec §5 cita `ROTAS_PROTEGIDAS`/`pode_acessar`; o código usa `PERMISSOES`/`pode`. O intent §10 declara nomes fora de julgamento — não é falha, mas o texto da spec não foi atualizado.
5. **Higiene:** `gsi_ebd/states/auth.py` importa `home_do_papel` e `pode` sem usá-los (o `guarda_rota` já os resolve em `rbac.py`). Sem efeito funcional.
6. **WARN do `logout`** continua aberto por decisão de escopo; precisa de DEM própria (ou DEM-010).
