# Plano de testes — DEM-202610-002 / guarda de papel no `/admin`

> Dono: PLANNER. O EVAL é cego: **este plano é o contrato**, e os scripts de verificação ficam em
> `eval/`. Suíte: `pytest tests -q` em `ESTUDOS_BIBLICOS/GSI_EBD/.venv` (hoje **82** testes).

## 1. Casos funcionais (F)

| ID | Caso | Esperado | Cobre |
|---|---|---|---|
| **F-01** | `pode_acessar("/admin", ADMIN)` | `True` | RF01 |
| **F-02** | `pode_acessar("/admin", REVISOR)` | `True` | RF01 · 9.2a |
| **F-03** | `pode_acessar("/admin", ALUNO)` | `False` | RF01 |
| **F-04** | `pode_acessar("/coordenador", {ADMIN, COORDENADOR})` = True; `{REVISOR, INSTRUTOR, ALUNO}` = False | idem | RF01 |
| **F-05** | `pode_acessar("/revisao", {ADMIN, INSTRUTOR})` = True; `{REVISOR, COORDENADOR, ALUNO}` = False | idem | RF01 |
| **F-06** | `pode_acessar` das rotas **públicas** para qualquer papel **e para anônimo** | `True` | RF01 |
| **F-07** | **Matriz completa**: laço `ROTAS_PROTEGIDAS × Role` confere a tabela inteira da spec §2 | igual à spec | RF05 · H-04 |
| **F-08** | **Invariante da casa**: para cada papel, `pode_acessar(redirect_for_role(papel), papel)` | `True` (sem loop) | RF04 |
| **F-09** | `guarda_admin` com `is_authenticated=False` | `rx.redirect("/login")` | RF03 |
| **F-10** | `guarda_admin` com papel ALUNO e logado | redirect para a **casa** do aluno (`/aluno`) | RF04 |
| **F-11** | `guarda_admin` com papel ADMIN | `None` (segue) | RF02 |
| **F-12** | los três loaders (`load_coordenadores`, `load_all`, `load_fila`) chamam `pode_acessar` **antes** de abrir sessão | inspeção de código + teste do caminho cedo | RF02 (defesa em profundidade) |

## 2. Casos de saúde (H)

- **H-01** · suíte verde: **82 + novos** · porteiro **EVAL** (roda `pytest tests -q`).
- **H-04** · a matriz papel × rota **existe e é testada** · baseline: a tabela da spec §2 · porteiro **EVAL**.
- **H-06** · aluno logado **não permanece** em `/admin` e **não vê dado administrativo** · baseline hoje: entra · porteiro **ARQUITECT** (navegador) + **EVAL** (o que der para provar sem browser).

## 3. Casos de contrato (C)

- **C-01** · nenhuma dependência nova (`requirements.txt` e `requirements-dev.txt` intactos).
- **C-02** · nenhum modelo/schema alterado (`git diff` em `gsi_ebd/models/` vazio).
- **C-03** · `tests/test_paginas.py` passa (as 9 páginas compilam).
- **C-04** · nenhuma ADR contrariada: a guarda usa o `Role` da ADR-005; o PR segue a ADR-009.

## 4. Casos negativos (N) — o que **não** pode acontecer

- **N-01** · `rota` desconhecida em `pode_acessar` → **False** (fecha para o desconhecido, não abre).
- **N-02** · papel inválido/inesperado → `redirect_for_role` devolve `/login` (sem loop).
- **N-03** · loader chamado direto (sem `on_load`) não carrega dado para quem não pode.
- **N-04** · nenhum `is_admin` usado como guarda de `/admin` (bloquearia o REVISOR — 9.2a).
- **N-05** · nenhum segredo/credencial tocado (ADR-008).

## 5. Verificação manual (ARQUITECT)

1. Entrar como **ALUNO** → digitar `/admin` → **cai em `/aluno`**, sem dados administrativos.
2. Entrar como **COORDENADOR** → `/coordenador` abre; `/admin` não.
3. Entrar como **REVISOR** → `/admin` **abre** (é a casa dele — 9.2a).
4. Entrar como **INSTRUTOR** → `/revisao` abre; `/admin` não.
5. Entrar como **ADMIN** → tudo como antes.

## 6. Baseline de referência

| Métrica | Hoje | Esperado |
|---|---|---|
| testes | 82 | 82 + F-01..F-12 |
| aluno em `/admin` | **200 e vê o painel** | **redirecionado, sem dados** |
| páginas compilando | 9/9 | 9/9 |
