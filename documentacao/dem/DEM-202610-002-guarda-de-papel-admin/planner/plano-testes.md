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
| **F-12** | **Varredura da classe**: todo método público de `AdminState`, `CoordenadorState` e `RevisaoState` tem o marcador `__exige__` — exceto os `@rx.var` | nenhum evento sem guarda | RF07 (ajuste 2) |
| **F-13** | `load_coordenadores` com ALUNO/INSTRUTOR/COORDENADOR/REVISOR | **não consulta nada** (sai antes de abrir sessão) | RF02 |
| **F-14** | `update_lead_status` com ALUNO/INSTRUTOR/COORDENADOR/REVISOR | **não escreve** | RF08 |
| **F-15** | `activate_user`/`suspend_user`/`cancel_user` com **REVISOR** (que o `can_manage` deixaria passar, nível 1 × 2) | **barrado** | RF08 · achado do AUXILIAR |
| **F-16** | `assign_study` com REVISOR e ALUNO | **não escreve** | RF08 |
| **F-17** | `abrir_resposta`/`fechar_resposta`/`usar_sugestao`/`descartar_sugestao` com ALUNO e COORDENADOR | **barrado** | RF08 |
| **F-18** | cada handler com um **papel permitido** (`acao:usuarios` → ADMIN; `acao:catalogo` → ADMIN/REVISOR) | executa | RF07 |
| **F-19** | `aprovar_estudo`/`aprovar_todos`/`rejeitar_estudo` com **REVISOR** | **executa** (é o catálogo, a casa dele) | 9.2a |
| **F-20** | `exige(chave)` grava `__exige__` no wrapper | marcador presente e igual à chave | RF07 |
| **F-21** | `pode("acao:usuarios", REVISOR)` = **False**; `pode("acao:usuarios", ADMIN)` = True | matriz | RF01 |
| **F-22** | `pode` de **chave desconhecida** (rota ou ação) | **False** (fecha para o desconhecido) | N-01 |
| **F-23** | **Auto setters desligados**: `AuthState` **não** expõe `set_current_user_role`, `set_current_user_id`, `set_current_user_name`, `set_current_user_status`, `set_current_user_ambiente`, `set_is_authenticated`, `set_must_change_password` | **nenhum existe** (medido do diretório do app) | RF09 · item 1 do List 2.1 |
| **F-24** | Cada setter **explícito** usado pelas páginas existe (`login_email`, `tab_atual`, `user_answer`, `parecer_texto`, `senha_atual`, `form_nome`…) | as 9 páginas compilam | RF09 · rede de segurança |
| **F-25** | `aprovar_estudo`/`aprovar_todos`/`rejeitar_estudo` com **REVISOR** | **barrado** (`acao:catalogo_aprovar` = ADMIN) | RF10 |
| **F-26** | `load_estudos_pendentes`/`load_obras` com **REVISOR** | **executa** (`acao:catalogo_ler`) | RF10 · 9.2a |
| **F-27** | Handler decorado com argumentos: continua **síncrono** e com a assinatura original (`__wrapped__`) | `inspect.iscoroutinefunction` = False; `inspect.signature` = original | item 3 do List 2.1 |
| **F-28** | A suíte roda **do diretório do app** (`ESTUDOS_BIBLICOS/GSI_EBD`) | **82+ passed** (do diretório errado dá falha de setter) | H-01 · lição medida |

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
- **N-06** · evento público **novo** sem `@exige` → a varredura **F-12 reprova** (é o teste que
  impede o furo voltar por descuido).
- **N-07** · `can_manage` continua existindo, mas **não** é a guarda de evento nenhum (o decorator
  barra antes); se alguém voltar a usá-lo como única guarda, F-15 reprova.
- **N-08** · nenhum `@rx.var` é decorado — a varredura da F-12 ignora `ComputedVar` e não exige
  marcador deles.

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
