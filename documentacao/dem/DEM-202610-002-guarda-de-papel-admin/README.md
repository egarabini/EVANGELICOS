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

## Por que é urgente

O furo existe **hoje, em produção**: uma conta de aluno abre `/admin`. Não é hipótese — está no
changelog da DEM-001 como achado do EVAL. Esperar a migração para a base nova (DEM-005) deixaria o
furo aberto por semanas, e a troca de framework não é motivo para manter uma porta destrancada.
