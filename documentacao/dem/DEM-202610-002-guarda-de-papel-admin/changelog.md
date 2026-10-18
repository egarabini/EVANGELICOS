# Changelog — DEM-202610-002 / guarda de papel no `/admin`

## Resumo

| Item | Estado |
|---|---|
| Intent | **signed** 2026-10-18 ("DEM-002 já") |
| Spec + design + plano | aprovados (List 2.1) |
| Implementação | **`65fbf7a`** (repositório de código, `develop`) |
| CI | **verde** — run `39130776109`, 105 testes |
| EVAL cego | aguardando |
| Aceite | pendente |

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
