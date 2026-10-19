# Spec — DEM-202610-005 / a v1 na base nova (FastAPI + Jinja2 + HTMX)

> Dono: PLANNER. **Nível 3** (ADR-018). Intent **signed** em 2026-10-19 (as 9.1/9.2/9.3 fechadas).
> A ADR-014 v3 rege a base; a ADR-019 rege o fluxo (a fatia 1 da DEM-011 entrega o domínio).

## 1. Referência

Intent: [`intent.md`](intent.md) · [ADR-014 v3](../../../adr/ADR-014-saida-do-reflex.md) ·
ADR-018 · ADR-019 · DEM-011 (o fluxo) · DEM-010 (o ambiente) · DEM-012 (a credencial)

## 2. Os 6 marcos (cada um com resultado visível)

| # | Marco | O resultado visível | O que entra |
|---|---|---|---|
| **1** | **O esqueleto** | o login no **subdomínio de homologação** | a app FastAPI, o Jinja2, o HTMX, a **auth própria** (sessão, CSRF, cookie), a imagem, o pipeline, o **endereço de homologação** e o **banco próprio** (`didasko_v1`) com o **baseline de Alembic** |
| **2** | **O fluxo admin/revisor/obras** | importar → revisar → liberar na tela | as telas do admin e do revisor; a matriz papel × rota (a DEM-002) |
| **3** | **O coordenador** | vincular e adendar | a tela do coordenador + o `Adendo.ambiente_id` |
| **4** | **O instrutor e a correção** | ver a turma e corrigir | as telas do instrutor |
| **5** | **A lição do aluno** | o estudo completo | a lição (o H-06) |
| **6** | **A virada** | o domínio principal na v1 | o Traefik; o plano de virada e o retorno |

**A ordem é a decidida (9.1)**: admin e o fluxo de obras primeiro; a **lição por último**. A
**virada (9.2) é depois da DEM-011**.

## 3. Requisitos funcionais

- [ ] **RF01 — a autenticação própria**: login/logout com **sessão de servidor**, CSRF em
  formulários/HTMX, o cookie com flags e expiração. *(o achar A da revisão da ADR-014 fica
  resolvido por construção: não há nada a compartilhar com o Reflex)*
- [ ] **RF02 — a matriz papel × rota** (a DEM-002, migrada inteira): uma dependência única de
  autorização, testada pela matriz, **na base nova**.
- [ ] **RF03 — as telas por papel** (os marcos 2-5), com `StrictUndefined` no Jinja e um teste que
  **renderiza todas as rotas por papel**.
- [ ] **RF04 — o domínio reaproveitado**: `models/`, `services/`, `scripts/`, `ai/` — a troca de
  `rx.session` pela sessão do SQLModel; sem reescrever a regra.
- [ ] **RF05 — o fluxo de obras/estudos** (a DEM-011): as telas da fatia 1, com as transições
  **validadas no serviço** (não na tela).
- [ ] **RF06 — as dívidas de auth fechadas por construção**: **(D-11)** a flag
  `must_change_password` **bloqueia** rota/evento protegido até a troca (só a troca e o logout
  passam) — H-14; **(D-10)** o coordenador é criado **sem senha fixa** (token de uso único com
  expiração ou senha aleatória nunca exibida) — H-15.
- [ ] **RF07 — o deploy da v1**: a imagem da base nova, o pipeline apontando para ela, e o
  **`exec -e SEED_PASSWORD`** no script de deploy (a decisão A-2: o valor do **ambiente do
  script**, nunca da linha de comando; **não** no `environment:` do Compose).
- [ ] **RF08 — a homologação**: a v1 sobe num **subdomínio** ao lado da v0 (o DNS e o certificado
  são do ARQUITECT — avisar quando o marco 1 estiver pronto).
- [ ] **RF12 — a transação**: a camada de rotas da v1 abre e fecha a transação — **um `commit` por operação do fluxo**, com **`rollback`** em `FluxoBloqueado` (o domínio só faz `flush()`). Sem isso, um bloqueio no meio de uma operação deixa estado parcial.
- [ ] **RF11 — o inventário no contêiner**: o `inventario.csv` (o `documentacao/fontes/` do repositório de conteúdo) precisa estar **acessível no contêiner** da v1 — o Compose hoje só monta `conteudo/ESTUDOS_BIBLICOS`; a v1 monta ou copia o inventário e aponta o `CAMINHO_INVENTARIO` (o `services/fontes.py` da DEM-011 o lê).
- [ ] **RF10 — o banco da v1**: banco próprio (`didasko_v1`, no mesmo Postgres), schema do zero + o **baseline de Alembic**; a `DATABASE_URL` da v1 aponta para ele; a v0 fica no antigo. **Sem migração de schema no banco existente.**
- [ ] **RF09 — a virada**: o Traefik aponta o domínio principal para a v1; a v0 fica de pé para o
  **retorno** — que basta **enquanto só houver dados de teste**. **Dados reais só entram depois de
  um período estável** (o plano de virada define); **a partir daí "voltar à v0" perde dados**, e a
  correção é **para a frente**.

## 4. Requisitos não funcionais

- A base: Python 3.12, o SQLModel/Postgres (o mesmo domínio), o Jinja2/HTMX, **sem Node/TS na
  aplicação**; o corpus `:ro`.
- A segurança: o CSRF, o cookie, a matriz, o `StrictUndefined`, os testes que renderizam.
- O deploy: o CI verde; o backup verificado; o HTTP 200; a tag aceita (ADR-016).
- O **domínio não se reescreve**; a alteração é a sessão.

## 5. Os edge cases

- O login com a flag ativa → só a troca e o logout; rota/evento protegido recusa (H-14).
- O coordenador com o token expirado → recusa e reemissão (H-15).
- A v0 e a v1 no mesmo domínio? **Não**: a v0 no domínio, a v1 no subdomínio até a virada (RF08).
- A virada com a v0 de pé; o retorno pelo Traefik; os dados reais (a RF09).
- A sessão do Reflex e a da v1 são independentes (a RF01).

## 6. Critérios de aceitação

- [ ] **CA01** — o marco 1: login na homologação, a tela e a matriz (H-01, H-04/H-05).
- [ ] **CA02** — o marco 2: o fluxo admin/revisor/obras pela tela (H-14).
- [ ] **CA03** — o marco 5: a lição do aluno na v1 com o HTTP 200 e o "João 3:16" (H-06).
- [ ] **CA04** — as dívidas: H-14/H-15 fechadas (os testes dos dois).
- [ ] **CA05** — o deploy da v1: a imagem, o pipeline, o `exec -e`, o backup e o HTTP (RF07).
- [ ] **CA06** — a virada testada, com o **retorno** funcionando e o critério de dados reais escrito (RF09).
- [ ] **CA07** — o Reflex sem dependência: a v0 desligável sem perda (com os dados de teste).
- [ ] **CA08** — o banco da v1 criado com o **baseline de Alembic**; a `DATABASE_URL` correta; o banco da v0 **intocado**.

## 7. Fora da v1

A busca (DEM-B/C/D), o DAVID (DEM-E), o `planejar` (a 9.5, fatia posterior), o multi-ambiente real
(D-06), o serviço MCP (DEM-013, adiada).





