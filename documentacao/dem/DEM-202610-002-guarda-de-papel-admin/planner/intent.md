# Intent: DEM-202610-002 / guarda-de-papel-admin

status: signed
owner: PLANNER
signed_by: ARQUITECT
origin: achado do EVAL da DEM-202610-001 (jornada, 2026-10-16) + carta do ARQUITECT de 2026-10-18 (§5 e §6)
signed_at: 2026-10-18
supersedes: —
open_questions_open: 0
spec_citations: 100% — todo RF de `spec.md` cita §2, §4 In, §5 ou uma decisão do §9
nota_de_assinatura: o ARQUITECT determinou "DEM-002 já" (2026-10-18) após "é pequena e é segurança";
as três perguntas foram fechadas com as recomendações do PLANNER, registradas no §9.

## 1. Problema

**Hoje, qualquer usuário autenticado alcança a área administrativa.** Quem está logado como aluno
e digita `/admin` vê as telas de administração — não por falha de um botão, mas porque as páginas
`pages/admin.py` (e as rotas irmãs) **não conferem o papel** antes de renderizar.

O achado é do EVAL da DEM-001 e está registrado no changelog dela. O ARQUITECT concordou em
corrigir **antes** do deploy por pipeline: não se publica uma versão que ainda tem o furo.

## 2. Outcome

**Nenhuma rota administrativa responde a quem não é admin.** Um aluno logado que tenta `/admin`
recebe **403** na rota (e é devolvido ao seu painel na navegação); um coordenador também não
alcança o que é exclusivo do admin. E a **matriz papel × rota** deixa de ser promessa: passa a ser
teste.

## 3. Afetados

Alunos e instrutores/coordenadores (que hoje conseguem abrir o admin), o admin (nada muda na
operação), e a **DEM-005** (a migração do admin reaproveita a mesma matriz; a coluna "base que
serve a rota" é da spec de lá).

## 4. Escopo

**In**
- guarda de papel em **todas** as rotas administrativas (`/admin` e subrotas)
- a **matriz papel × rota** como baseline: qual papel pode qual rota
- teste automatizado que percorre a matriz e prova o 403 (o `test_paginas.py` atual só compila)
- registro do achado no changelog da DEM-002

**Out (non-goals)**
- RBAC completo de todos os papéis em todas as telas (a matriz nasce com o que existe hoje)
- mudança de UI, de menu ou de fluxo de login
- mudança de schema: os papéis já existem (`Role`)
- migrar o admin (é a DEM-005)

## 5. Constraints (duras)

- **Não quebrar o admin atual**: o admin continua operando as telas como hoje.
- **Nenhuma mudança de schema ou de dado.**
- **Antes do deploy por pipeline** (ordem do ARQUITECT, 18/10) e **antes da migração do admin**.
- Guarda **central**, não copiada por página: uma função/dependência única, testada.
- A resposta de acesso negado é **403**, não tela em branco nem erro 500.

## 6. Health metrics

- **H-01** · a suíte continua verde · baseline **82 testes** · porteiro **EVAL**
- **H-04** · a **matriz papel × rota** passa a existir e é testada · baseline **a levantar (inventário das rotas e dos papéis)** · porteiro **EVAL**
- **H-06** · aluno logado em `/admin` é **devolvido ao painel dele e não vê dado administrativo** · baseline hoje: entra e vê · porteiro **EVAL** + verificação manual do ARQUITECT.
  *Nota (2026-10-18, após o EVAL): a formulação original dizia "recebe 403". Não há 403 — a rota é servida pelo SPA, que responde 200 e redireciona no cliente. A garantia verificável é mais forte: o **estado não carrega** dado administrativo para quem não tem papel (loader com `@exige`). A métrica passa a ser essa, não o código HTTP.*

## 7. Sinal de sucesso

O ARQUITECT entra como **aluno**, digita `/admin` e **não entra**. Entra como admin e **nada mudou**.
O teste da matriz falha se alguém remover a guarda de uma rota.

## 8. Decisões já registradas (não são perguntas)

| # | Questão | Decisão |
|---|---|---|
| 8.1 | Momento | **Antes do deploy por pipeline** (carta do ARQUITECT, 18/10) e antes da migração do admin (ADR-014) |
| 8.2 | Onde | No **Reflex**, agora — a base nova só herda a matriz |
| 8.3 | Resposta | **403** na rota; na navegação, devolver ao painel do papel |

## 9. Perguntas abertas — fechadas pelo ARQUITECT em 2026-10-18

| # | Pergunta | Decisão |
|---|---|---|
| 9.1 | Matriz antes ou depois da guarda? | **Antes.** A matriz é o baseline (H-04) e o próprio teste — sem ela, o teste não sabe o que afirmar |
| 9.2 | O que o COORDENADOR alcança? | **`/coordenador`** (e mais nada da área administrativa). `/revisao` é do INSTRUTOR (+ADMIN) |
| 9.2a | **Correção depois de ler o código** | A decisão 9.2 dizia "`/admin` exclusivo do ADMIN". O código (`AuthService.redirect_for_role`) manda o **REVISOR** para `/admin` ("valida o catálogo na tela do admin"). Fechar `/admin` só para ADMIN faria o login do revisor **entrar em loop** (redireciona para /admin → guarda recusa → redireciona para /admin). Matriz corrigida: **`/admin` = ADMIN + REVISOR** |
| 9.3 | Rota pública que continua pública? | **`/`, `/login`, `/confirmar/[token]` e `/homenagens`** — conferidas no código, não mudam |

## 10. Fora de julgamento

A implementação da dependência, nomes de funções, formato do teste da matriz, e a ordem interna das
rotas. O design decide o como.
