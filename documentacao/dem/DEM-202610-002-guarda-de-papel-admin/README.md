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

## Achados que saem desta DEM

- **`can_manage` não confere o ambiente (tenant)**: um COORDENADOR pode agir sobre usuário de
  **outro** ambiente por evento direto. É isolamento de dados, não só de papel → **DEM própria**
  (DEM-202610-010, proposta no painel).

## Por que é urgente

O furo existe **hoje, em produção**: uma conta de aluno abre `/admin`. Não é hipótese — está no
changelog da DEM-001 como achado do EVAL. Esperar a migração para a base nova (DEM-005) deixaria o
furo aberto por semanas, e a troca de framework não é motivo para manter uma porta destrancada.
