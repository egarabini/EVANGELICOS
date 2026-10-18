# Changelog — DEM-202610-002 / guarda de papel no `/admin`

## Fechamento (2026-10-18)

**Aceite do ARQUITECT: concedido em 2026-10-18**, no hash **`7cb2ee2`** — o head da
branch `release/0.1.0` (PR #2), que é exatamente o hash aprovado pelo EVAL na rodada 3.

| Gate | Evidência |
|---|---|
| `GATE: intent` | signed 2026-10-18 |
| `GATE: spec` + `GATE: TLC-List` | List 2.1 aprovado (com as 2 observações de implementação) |
| `GATE: EVAL` | **PASS** (rodada 3) — 113 testes; m6 e m7 reprovam |
| CI | **verde** — run `39146196858` |
| **Aceite** | **concedido 2026-10-18** |

**O que estava em jogo**: o furo do `/admin` (qualquer usuário logado alcançava a área
administrativa) **e** dois outros da mesma classe que a inspeção revelou — o cliente podia
escrever o próprio papel via `set_current_user_role`, e 28 eventos administrativos não
conferiam papel algum.

### Pendências que saem desta DEM (e para quem)

| Item | Para |
|---|---|
| **Release 0.1.0**: merge do PR #2, tag `v0.1.0`, deploy | ARQUITECT (depende da **chave de deploy**) |
| **DEM-202610-010** — isolamento por ambiente (tenant) e posse: `can_manage` sem ambiente; `toggle_aluno`/`assign_study` e `AlunoState.start_study`/`select_study`/`submit_answer` recebem id do cliente sem conferir pertença | DEM própria (proposta no painel) |
| **DEM-202610-011** — aprovação em dupla (ADR-011 não implementada; hoje o admin sozinho libera, inclusive os 34 capítulos) | DEM própria (proposta no painel) |
| **Higiene de sessão**: `logout` não limpa `AdminState` — um REVISOR no mesmo navegador/token, após logout de ADMIN, pode ver dados que o ADMIN carregou | WARN do EVAL; candidato a DEM própria |
| Limpeza dos WARNs da rodada 3 (imports sem uso, caso de teste vacuoso, nomes na spec) | já em `develop` (`d1dd132`), **fora da branch do release** para preservar o hash do aceite |

## Resumo

| Item | Estado |
|---|---|
| Intent | **signed** 2026-10-18 ("DEM-002 já") |
| Spec + design + plano | aprovados (List 2.1) |
| Implementação | `65fbf7a` → correções `6768ea9` e `7cb2ee2` (repositório de código) |
| CI | **verde** — 113 testes (run `39146196858`) |
| EVAL cego | **PASS** (rodada 3, `7cb2ee2`) |
| Aceite | **concedido 2026-10-18** |

## O que a DEM entregou

**1. O estado deixou de ser escrito pelo cliente (RF09 — bloqueante).**
`state_auto_setters=False` e 20 setters explícitos (19 de formulário + 1 validado).
Medição antes/depois no `AuthState`: **17 setters → 2** (`login_email`,
`login_password`). Os 7 de identidade (`current_user_*`, `is_authenticated`,
`must_change_password`) **deixaram de existir**. E o `setvar` — que faz
`getattr(self, "set_" + var)` — também não os alcança: é a mesma porta, fechada pela
mesma ausência.

**2. Guarda de rota (RF01–RF04).** Matriz `PERMISSOES` em `utils/rbac.py` (rotas **e**
ações), `guarda_rota` nos `on_load` de `/admin`, `/coordenador` e `/revisao`. Não
logado → `/login`; logado sem papel → **casa do próprio papel** (nunca a rota negada,
senão o redirect entra em loop — coberto por teste).

**3. Guarda de evento (RF07–RF08).** `@exige` em **28 eventos** dos três estados.
Antes: `assign_study` (escrita) e `update_lead_status` (escrita) não checavam nada, e
`activate/suspend/cancel_user` passavam só pelo `can_manage`, que deixava o **REVISOR
gerenciar COORDENADOR**. A matriz separa `catalogo_ler` (ADMIN, REVISOR) de
`catalogo_aprovar` (ADMIN): a DEM **não cria poder novo**.

**4. Teste.** `tests/test_rbac.py`, 23 casos: matriz completa por papel, invariante da
casa, ausência de setter de identidade nos 7 estados, **lista de eventos congelada**
(evento novo, inclusive setter, falha até ser classificado), marcador `__exige__` em
todo evento dos 3 estados, e o decorador barrando de verdade. **105 passed** (82 + 23).

## Rodada 1 do EVAL: FAIL de teste, PASS de segurança

O EVAL cego deu **FAIL** — e o defeito era exatamente o que eu cobro dos outros: **um teste que não testava nada**.

`test_todo_evento_tem_marcador_exige` varria `vars(estado)` com `inspect.isfunction(fn)`. O Reflex **substitui cada método por um `EventHandler`** ao compilar a classe — a varredura examinava **zero** métodos e passava com os 28 `@exige` removidos (o EVAL provou removendo-os em memória: **105 passed**).

O mesmo valia para a rota: `rbac.guarda_rota` era **dead code** (o app usava `AuthState._guarda`) e o único teste dela exercitava uma função sintética. E a casa do papel tinha **duas tabelas** (`rbac.home_do_papel` e `AuthService.redirect_for_role`).

### Corrigido nesta rodada (`6768ea9`)

| Defeito | Correção |
|---|---|
| Varredura cega | itera `event_handlers` e checa `handler.fn.__exige__` |
| `guarda_rota` morto | os 3 handlers usam `@guarda_rota(...)` — o decorador testado é o do app |
| Guarda sem teste de fiação | `test_fiacao_on_load_das_rotas_guardadas` importa o app e confere os `on_load` |
| `_guarda` sem teste real | `test_guarda_real_bloqueia_e_libera` chama o guarda do app, por papel |
| Casa em dois lugares | `AuthService.redirect_for_role` delega para `rbac.home_do_papel` + teste de consistência |
| F-06 (públicas) | rotas públicas entram na matriz com `_TODOS`; `pode` é total |
| F-19 × F-25 | F-19 corrigida (caso positivo é ADMIN) |

### Prova de que os testes estão vivos (mutações em memória)

| Mutação | Reprovou? |
|---|---|
| Remover `__exige__` de um handler | **sim** |
| Remover o guarda do `on_load` de `/admin` | **sim** |
| Tirar o REVISOR de `rota:/admin` | **sim** (matriz **e** guarda real barram) |
| Dar `catalogo_aprovar` ao REVISOR | **sim** |
| Ligar `state_auto_setters` | **sim** (contrafactual do EVAL) |

**Suíte: 109 passed** (82 + 27).

## Rodada 2 do EVAL: FAIL de cobertura e de contrato — corrigido (`7cb2ee2`)

Segurança **PASS** (regressão dos 3 furos, 5/5 mutações pedidas, sonda com 140 células). Dois bloqueios, ambos de **prova**:

1. **Cobertura por chave (m7):** a suíte provava que o evento tem `@exige`, não **qual** chave. Decorar `load_leads` com `catalogo_ler` passava — e o REVISOR carregava leads. Corrigido: `CHAVES_ESPERADAS` (mapa congelado evento → chave) + `test_chave_de_cada_evento`.
2. **Destino do redirect (m6):** ninguém asseria para onde o redirect ia; trocar `home_do_papel` por `/login` passava nos 4 testes. Corrigido: tabela **hardcoded** de casas (oráculo independente) + extração do path do `EventSpec`.

Também: `test_handlers_reais_barrados_nao_executam` cobre o negativo de F-13/F-16/F-19 chamando o **handler real** (o `@exige` retorna antes do corpo, sem abrir sessão).

**Contrato (H-06):** o intent dizia 403 em §2, §4, §5 e §8.3. Corrigido nos quatro — a garantia é *redirect para a casa + loader que não carrega*, sem 403 (a rota é SPA). **Suíte: 113 passed.**

### Pendência registrada (WARN do EVAL, fora do escopo)

`logout` não limpa `AdminState`: um REVISOR no mesmo navegador/token, após logout de um ADMIN, pode ver dados que o ADMIN carregou. É **higiene de sessão**, não bypass de guarda — candidato a DEM própria (ou à DEM-010, junto do tenant).

## Rodada 3 do EVAL: **PASS** — gate vencido (`7cb2ee2`)

| Categoria | Veredito |
|---|---|
| m7 (chave errada) | **PASS** — reprova agora, com o diff da chave |
| m6 (destino do redirect) | **PASS** — reprova agora, com o destino esperado |
| Contrato (403) | **PASS** — as 4 afirmações sumiram |
| Regressão dos 3 furos | **PASS** — 7/7 estados sem setter de identidade; `setvar` → `AttributeError` nos 7; 3 `on_load`; 28 `@exige` |
| Negativo dos handlers reais | **PASS** com WARN |
| Suíte | **PASS** — 113 |
| Escopo | **PASS** |

WARNs não bloqueantes, tratados: o caso `abrir_resposta` do teste de handlers reais era vacuoso (trocado por `salvar_parecer`, cujo corpo toca serviço/banco); imports sem uso em `auth.py` removidos; spec/plano alinhados aos nomes reais (`PERMISSOES`/`pode`); F-06 ajustado (anônimo não é papel).

**Essas limpezas foram para `develop` (`d1dd132`), não para a branch do release** — o PR #2 aponta o hash aprovado (`7cb2ee2`), e mover a branch invalidaria o hash do aceite por uma limpeza cosmética.

## Lição medida (registrada no teste e no README)

O Reflex descobre o `rxconfig.py` **pelo diretório atual**. Rodando a suíte de outro
diretório, a config não é lida, os setters não resolvem e `test_paginas` falha
**9/9** — o resultado se inverte. **A suíte roda sempre de `ESTUDOS_BIBLICOS/GSI_EBD`.**

## O que ficou de fora (e por quê)

- **DEM-202610-010 (tenant)** — `can_manage` não confere ambiente. O
  `set_selected_study_option` valida contra as opções carregadas, mas a pertença fina
  (o estudo é do *meu* ambiente?) é isolamento de dados, não de papel.
- **DEM-202610-011 (dupla aprovação)** — a ADR-011 (revisor + admin, com hash) não está
  implementada; hoje o admin sozinho libera, inclusive os 34 capítulos já importados.
- **Achado novo, para verificar na DEM-010** — eventos de `AlunoState`
  (`select_study`, `start_study`, `submit_answer`) recebem id do cliente e não
  conferem pertença: a lista vem de `assigned_studies`, mas um cliente pode mandar
  outro id por evento direto.
