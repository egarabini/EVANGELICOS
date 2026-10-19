# Briefing do DEVS — DEM-202610-011, **fatia 2** (as telas do fluxo, na v1)

> **Para:** Codex (DEVS) · **De:** PLANNER · **Data:** 2026-10-19
> A fatia 1 (o domínio) está **mergeada** (`7670aec`). Esta fatia faz a **primeira tela da v1**.

## 1. O que ler, nesta ordem

1. `ESTUDOS_BIBLICOS/GSI_EBD/AGENTS.md` (o guarda do código) e `CONVENTIONS.md`.
2. `documentacao/dem/DEM-202610-011-fluxo-de-obras-e-estudos/planner/design-fatia-2.md` — **o alvo**.
3. O design v7 e o plano v4 da fatia 1 (o domínio que as telas chamam) + o código
   `gsi_ebd/services/flow.py` (as 12 operações) e `gsi_ebd/models/obra.py`.
4. O design da DEM-005 (`documentacao/dem/DEM-202610-005-saida-do-reflex/planner/design.md`) — a
   estrutura da v1 e o marco 1.
5. A ADR-002 (o corpus `:ro`), a ADR-003 (a Escritura), a ADR-008 (os segredos) e a **ADR-020** (a
   autoridade e a disponibilidade — a semântica que as telas refletem).

## 2. A tarefa — duas etapas

**Etapa A — o esqueleto mínimo da v1** (o login funcionando local):
- a `v1/` com o `main.py`, o `auth.py` (a sessão, o CSRF, o `usuario_atual`, o `exige(papel)`), o
  `db.py` (a engine do SQLModel; o `DATABASE_URL`; o `create_all` no boot), o layout e os
  templates;
- a **matriz** do `gsi_ebd/utils/rbac.py` aplicada como as dependências;
- o `POST /login`, o `POST /logout`, o `/perfil/alterar-senha`, e o **H-14** (a flag bloqueia);
- **o teste**: cada rota × papel; o CSRF; o H-14; o render.

**Etapa B — as telas do fluxo** (o admin e o revisor):
- as rotas da §3 do design, chamando o `flow.py` — **nenhuma regra no template**;
- o admin: a lista, a importação, o detalhe com o histórico, a liberação, a alteração, a
  solicitação (o aceitar/a dispensar), o cancelamento;
- o revisor: a fila, o detalhe com o `hash_esperado`, o parecer, a recusa, a solicitação, a posição;
- a obra: o detalhe (o publicado × o em revisão);
- **a integração**: as ações mudam o estado (o F-06/F-12 da fatia 1 pela tela).

## 3. As regras

- Branch `feature/DEM-202610-011-fatia2-telas` a partir do `develop`; PR → develop; commits pt-BR.
- **A suíte da v1 roda do diretório da v1** (`v1/`) — e a da fatia 1 continua verde (a regressão).
- **O CSRF em todo POST**; **o `StrictUndefined`**; a autorização **no servidor** (a dependência),
  não no botão.
- **Sem segredo no repositório**: o `DATABASE_URL` local vem do ambiente/o `.env.example`.
- Sem deploy, sem imagem, sem DNS, sem a homologação (o marco 1 da DEM-005); sem as telas do
  instrutor/aluno; sem o `desvincular`/o adendo/o `planejar` (a fatia 3).
- Não alterar o `flow.py`/os models da fatia 1 sem registrar no relatório (se precisar de um
  campo novo, **pare e devolva ao PLANNER**).

## 4. O Definition of Done

- o login local com a matriz (a etapa A); as telas do admin e do revisor com o fluxo completo (a
  etapa B);
- a suíte da v1 verde + a matriz + o CSRF + o H-14 + o render; a **mutação** (remover a dependência
  de papel → a matriz falha; remover o CSRF → o teste falha);
- o CI verde; o relatório (o que, onde, os testes, o que ficou de fora).

> O EVAL cego julga depois, com o plano da v1 (a DEM-005) + o plano da fatia 2. A fatia 3
> (a coordenação) só depois do PASS desta.
