# Intent: DEM-202610-002 / guarda-de-papel-admin

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: achado do EVAL da DEM-202610-001 (jornada, 2026-10-16) + carta do ARQUITECT de 2026-10-18 (§5 e §6)
signed_at:
supersedes: —
open_questions_open: 3
spec_citations: — (preenchido ao fechar a spec)

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
- **H-06** · aluno logado em `/admin` recebe **403** · baseline hoje **200** · porteiro **EVAL**

## 7. Sinal de sucesso

O ARQUITECT entra como **aluno**, digita `/admin` e **não entra**. Entra como admin e **nada mudou**.
O teste da matriz falha se alguém remover a guarda de uma rota.

## 8. Decisões já registradas (não são perguntas)

| # | Questão | Decisão |
|---|---|---|
| 8.1 | Momento | **Antes do deploy por pipeline** (carta do ARQUITECT, 18/10) e antes da migração do admin (ADR-014) |
| 8.2 | Onde | No **Reflex**, agora — a base nova só herda a matriz |
| 8.3 | Resposta | **403** na rota; na navegação, devolver ao painel do papel |

## 9. Perguntas abertas — só o ARQUITECT fecha

- [ ] **9.1** A **matriz papel × rota** é levantada **agora** (H-04, baseline) ou a guarda entra
  primeiro e a matriz vem depois? *Recomendação: levantar antes — sem o baseline, o teste não sabe
  o que afirmar.*
- [ ] **9.2** O **coordenador** alcança `/admin` hoje? Se não deve alcançar, qual é o recorte
  (admin tem tudo; coordenador tem o quê)? *Recomendação: admin = tudo; coordenador = o painel
  próprio, sem as telas de usuários/estudos.*
- [ ] **9.3** Existe **rota que hoje é pública** e deveria continuar? (ex.: confirmação de conta)
  *Recomendação: manter como está; a matriz registra o "público".*

## 10. Fora de julgamento

A implementação da dependência, nomes de funções, formato do teste da matriz, e a ordem interna das
rotas. O design decide o como.
