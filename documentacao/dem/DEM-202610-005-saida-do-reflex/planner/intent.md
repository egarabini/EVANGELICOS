# Intent: DEM-202610-005 / v1-na-base-nova

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: decisão do ARQUITECT (19/10) — a v1 é a base nova; não há migração por rotas
signed_at:
supersedes: —
open_questions_open: 3
nivel_agil: 3 — muda a base de toda a plataforma
nota: a DEM-005 deixou de ser "a saída do Reflex" e passou a ser **a v1** (ADR-014 v3). O
domínio é reaproveitado; as telas e o auth são novos; a virada é única.

## 1. Problema

O Reflex (a v0) foi a base de teste e cumpriu o papel — mas a v1 não deve nascer sobre ele: os
três incidentes (o `Var` derrubando produção, a colisão de nomes na DEM-001 e as regras
compensatórias) mostram que o custo de mantê-lo supera o ganho. E **construir a v1 na base nova,
ao lado, é mais simples do que migrar por rotas** — porque os dados são de teste e serão limpos
na virada.

## 2. Outcome

**A v1 é uma aplicação FastAPI + Jinja2 + HTMX**, com o **domínio reaproveitado**, telas novas,
autenticação própria, publicada pelo pipeline — e a v0 segue rodando para teste até a **virada
única** pelo Traefik. Ao fim, o Reflex não é dependência do produto.

## 3. Afetados

Todos os papéis (o login e as telas são novos), o domínio (as adaptações de `rx.session`), o
CI/CD (o `deploy.yml` e a imagem), e as DEMs seguintes (a busca, o DAVID — nascem na base nova).

## 4. Escopo

**In**
- a aplicação FastAPI + Jinja2 + HTMX: **login e sessão de servidor**, o layout, a matriz
  papel × rota (o que a DEM-002 fez, **inteiro**, na base nova);
- as telas da v1: **admin, coordenador, instrutor, aluno, lição, pareceres, perfil**;
- o **domínio reaproveitado**: `models/`, `services/`, `scripts/`, `ai/` (troca de `rx.session`
  pela sessão do SQLModel; sem reescrita de regra);
- o **fluxo de obras/estudos** (DEM-011) construído **direto na v1**;
- o **pipeline**: o `deploy.yml` aponta para a imagem nova; a verificação HTTP;
- a **virada**: o Traefik aponta o domínio para a v1; a v0 fica de pé para retorno.

**Out (non-goals)**
- **migração de dados** — os de teste são limpos na virada (ADR-018);
- **convivência por rotas** e **sessão compartilhada** — removidas pela ADR-014 v3;
- **tela nova no Reflex** — a v0 só recebe correção, até a virada;
- reescrever o domínio.

## 5. Constraints

- **O domínio não se reescreve**: `models/`, `services/`, `scripts/`, `ai/` são reaproveitados;
  a alteração é a sessão.
- **A v0 fica de pé** até a virada; a virada é **um evento** e tem **retorno** (voltar o Traefik).
- **Os gates da DEM-002 migram inteiros**: a matriz papel × rota e o `@exige` viram dependências
  da v1, com teste que renderiza todas as rotas por papel.
- **Testes desde o dia 1**: `StrictUndefined`, CSRF, cookie de sessão, a matriz — a spec exige.
- **Níveis de risco** (ADR-018): as telas de segurança são **nível 3**; as de conteúdo, 2.

## 6. Health metrics

- **H-01** · a suíte da v1 verde (o número novo, com o baseline escrito)
- **H-04/H-05** · a **matriz papel × rota** e o **inventário de rotas** existem e são testados
- **H-06** · a lição do aluno (a última tela) funcional na v1: HTTP 200 + "João 3:16" e as relacionadas
- **H-13** · o **retorno** da virada funciona (o Traefik volta ao v0 em ≤ 5 min)

## 7. Sinal de sucesso

O ARQUITECT percorre a v1 como cada papel, faz o estudo completo, e **não encontra função que
sumiu** da v0. A v0 é desligada sem perda — e o Reflex deixa de ser dependência.

## 8. Decisões já registradas

| # | Questão | Decisão |
|---|---|---|
| 8.1 | A base | **FastAPI + Jinja2 + HTMX** (ADR-014 v3) |
| 8.2 | A estratégia | **v1 ao lado**, com **uma única virada** (sem rotas, sem sessão compartilhada) |
| 8.3 | O domínio | **reaproveitado**; a alteração é a sessão |
| 8.4 | A v0 | fica de pé, só com correção, até a virada |
| 8.5 | Os dados | **teste**, limpos na virada — nada a migrar |

## 9. Perguntas abertas — só o ARQUITECT fecha

- [ ] **9.1** A **ordem das telas**: admin/segurança primeiro (a matriz migra cedo) ou o fluxo do aluno primeiro? *Recomendação: admin + o fluxo de obras/estudos primeiro (são o núcleo de conteúdo), a lição por último (H-06).*
- [ ] **9.2** A **virada**: junto com a DEM-011 (o fluxo novo) ou antes dela? *Recomendação: depois — o fluxo é o motivo da v1 ser nova.*
- [ ] **9.3** O **retorno**: basta o Traefik voltar para a v0, ou há dados criados na v1 que precisam de atenção? *Recomendação: basta; os dados são de teste.*

## 10. Fora de julgamento

O framework HTTP, o motor de templates, o CSS, a organização das pastas.
