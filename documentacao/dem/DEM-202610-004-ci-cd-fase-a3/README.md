# DEM-202610-004 — CI/CD (Fase A3)

## Finalidade

Fazer o PR **mostrar, antes do merge, se a suíte passa e as páginas compilam**; e publicar em
produção **pelo pipeline**, sem agente com acesso à produção (ADR-010).

É a DEM que **desbloqueia o aceite de release da DEM-001** — entregue e aceita, mas parada
porque a publicação depende de CI.

## Relação com a governança

- Intent: [`planner/intent.md`](planner/intent.md) — **rascunho** (lapidado do rascunho do AUXILIAR-ARCHITECT)
- ADRs: **009** (GitFlow + Copilot Enterprise) · **010** (publicação por CI) · **008** (segredos) · **001/002** (intocáveis)
- Bloqueia: aceite de release da **DEM-202610-001**
- Origem: ADR-009 + ADR-010 + bloqueio do release da DEM-001

## Estado

- [x] **Intent assinado** — 5 decisões no §9 (`GATE: intent` vencido)
- [x] Spec + design da Etapa 1
- [x] **Etapa 1 (CI) entregue**: workflow verde (82 testes, 50 s) e **proteção** em `develop` e `main` exigindo o check `testes (pytest)`
- [ ] **Etapa 2 (CD)** — aguarda a **chave de deploy** (decisão 9.3): pública no `authorized_keys` da VPS, privada em secret
- [ ] EVAL da Etapa 1 + aceite

## O que a lapidação mudou no rascunho do AUXILIAR

| Mudança | Por quê |
|---|---|
| Encurtado para ~1 página | o intent do método não passa de uma página; passou disso já está especificando |
| **8.1 Copilot Enterprise** e **8.2 runner** viraram **decisões registradas** | o ARQUITECT já as respondeu em 17/10 (Copilot ativado; aceitou runner GitHub-hosted + SSH e descartou runner na VPS por ser repositório público) |
| **H-04** reescrito | o rascunho dizia "a medir no 1º deploy" — baseline inexistente não passa no teste de admissão do método. Virou **200 hoje** (medido) e **≤ 2 min após o deploy** |
| Perguntas: **7 → 5** | as duas respondidas saíram da lista, sem serem respondidas pelo PLANNER |

## Histórico (data, não relógio)

| Data | Evento |
|---|---|
| 2026-10-17 | Rascunho do AUXILIAR-ARCHITECT (CI/CD, 7 perguntas) |
| 2026-10-17 | PLANNER lapida: encurta, registra 8.1/8.2 como decididas, corrige H-04, reduz a 5 perguntas |
