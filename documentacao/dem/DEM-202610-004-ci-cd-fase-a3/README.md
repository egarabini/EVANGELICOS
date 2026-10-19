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
- [x] **Etapa 1 (CI) entregue**: workflow verde e **proteção** em `develop` e `main` exigindo o check `testes (pytest)`
- [x] **Etapa 2 (CD) entregue e usada**: o deploy da **`v0.1.0`** passou pelo pipeline (run `39175867118`, job `118049517557`), todas as etapas verdes, com HTTP externo 200
- [x] **ADR-016 aceita** (2026-10-19): o **perfil DEPLOY** executa a publicação pelo procedimento, sem aprovação por passo; **Environment `producao` sem required reviewer**, secrets e policies (`main` + `v*`) mantidos
- [x] **Artifact do backup**: o run guarda o **manifesto** (log com caminho, tamanho e sha256); o dump fica na VPS
- [x] **GitFlow encerrado**: `release/0.1.0` mergeada, tag `v0.1.0` e **back-merge `main` → `develop`**
- [ ] **Rotação/revogação das chaves** (dívida): a chave operacional não tem `restrict`; a antiga será revogada — depois do fluxo verde, conforme o runbook
- [ ] **Transferir o DUMP como artifact** (hoje só o manifesto) — follow-up
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
