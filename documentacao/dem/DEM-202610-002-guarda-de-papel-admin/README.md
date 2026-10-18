# DEM-202610-002 — Guarda de papel nas rotas `/admin`

## Finalidade

Fechar o furo de **autorização** apontado pelo EVAL da DEM-001: hoje **qualquer usuário logado**
alcança a área administrativa, porque as páginas não conferem o papel. A correção é pequena — e
por isso **vai antes do deploy por pipeline**.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — **rascunho**, 3 perguntas abertas (9.1–9.3)
- Originado do **achado do EVAL da DEM-001** (changelog) e da **carta do ARQUITECT de 18/10**
- **Antes da Etapa 2 do CI/CD** (não publicar versão com o furo) e **antes da migração do admin**
  (a matriz papel × rota daqui é reaproveitada pela DEM-005)
- **ADR-007** (guard-rails + TLC) e **ADR-005** (papéis já existem em `Role`)

## Estado

- [x] Intent escrito (rascunho)
- [ ] **Intent assinado** — fecha 9.1 (matriz antes ou depois) e 9.2 (o que o coordenador alcança)
- [ ] Spec + design + **baseline H-04** (matriz papel × rota)
- [ ] Implementação (TLC)
- [ ] EVAL + aceite

## O furo é maior que o `/admin`

O levantamento dos eventos (List 2.0) mostrou que o furo **não para nas rotas**:

- `AdminState.update_lead_status` — **escrita** em dados de leads, **sem verificação nenhuma**;
- `AdminState.activate_user/suspend_user/cancel_user` — só `can_manage`, e pela hierarquia do
  `utils/rbac.py` o **REVISOR (nível 1) gerencia coordenador, instrutor e aluno** — contra o próprio
  `Role`, que o descreve como "função editorial, fora da cadeia de comando";
- `CoordenadorState.assign_study` — **escrita** (atribui estudo), sem verificação;
- `RevisaoState.abrir_resposta/fechar_resposta/usar_sugestao/descartar_sugestao` — sem verificação;
- os `load_*` dos três estados — leitura direta por evento.

Daí a DEM ter passado de "guarda de rota" para **guarda de rota + de evento**, com um decorator
único e um teste que varre a classe. O `require_role` que existia em `utils/rbac.py` nunca foi
usado por nenhum arquivo.

## O segundo furo (bloqueante): o cliente escreve o próprio papel

`rxconfig.py` tem `state_auto_setters=True`. Medido **do diretório do app**, o `AuthState` expõe
**25 eventos / 17 setters**, entre eles `set_current_user_role`, `set_current_user_id`,
`set_current_user_ambiente`, `set_is_authenticated` e `set_must_change_password`.

Como a guarda inteira lê `self.current_user_role`, um cliente que dispara `set_current_user_role(1)`
**vira ADMIN para o servidor** — e a matriz e o `@exige` passariam a proteger um estado controlado
pelo atacante. Por isso a DEM começa por desligar os auto setters e escrever os setters explícitos
(RF09): **a guarda só vale se o estado for imutável pelo cliente**.

> **Lição medida:** o Reflex descobre o `rxconfig.py` a partir do **diretório atual**. Rodando a
> suíte do diretório errado, os setters não existem e `test_paginas` falha 9/9; do diretório do app,
> **82 passed**. A suíte roda sempre de `ESTUDOS_BIBLICOS/GSI_EBD`.

## Achados que saem desta DEM

- **`can_manage` não confere o ambiente (tenant)**: um COORDENADOR pode agir sobre usuário de
  **outro** ambiente por evento direto. É isolamento de dados, não só de papel → **DEM-202610-010**
  (proposta no painel).
- **Aprovação em dupla**: a regra de negócio confirmada em 18/10 é que o estudo só fica disponível
  quando **REVISOR e ADMIN** aprovam. Hoje não existe: há uma única aprovação (`aprovado_por`, só
  ADMIN), e a **ADR-011** (assinatura + data + hash do conteúdo) **também não está implementada**.
  Antes disso, o admin sozinho libera os estudos — inclusive os 34 capítulos já importados.
  → **DEM-202610-011** (proposta no painel). Esta DEM (002) **não** antecipa: o revisor **lê** o
  catálogo e **não** aprova.

## Por que é urgente

O furo existe **hoje, em produção**: uma conta de aluno abre `/admin`. Não é hipótese — está no
changelog da DEM-001 como achado do EVAL. Esperar a migração para a base nova (DEM-005) deixaria o
furo aberto por semanas, e a troca de framework não é motivo para manter uma porta destrancada.
