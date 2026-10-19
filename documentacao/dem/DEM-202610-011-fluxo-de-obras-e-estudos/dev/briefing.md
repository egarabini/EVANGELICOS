# Briefing do DEVS — DEM-202610-011, fatia 1 (Codex)

> **Para:** Codex (DEVS) · **De:** PLANNER · **Data:** 2026-10-19
> A DEM está assinada; a spec foi **aprovada** em 19/10 e a ADR-019 **aceita**. Esta é a **fatia 1 —
> o domínio**: sem tela, sem deploy.

## 1. O que ler, nesta ordem

1. `ESTUDOS_BIBLICOS/GSI_EBD/AGENTS.md` — o guarda do código.
2. `planner/intent.md` (as decisões 8.x e a 9.5), `planner/spec.md` (aprovada; os RFs e o §9 do
   fatiamento), `planner/design.md` (**o alvo**), `planner/plano-testes.md` (os casos F/N/C/H).
3. `documentacao/adr/ADR-011` (a aprovação assinada) e `ADR-019` (a emenda — a assinatura como
   intervalo, os dois hashes).

## 2. A tarefa

- Os modelos do design: `ObraVersao` (nova), os campos novos em `Obra` e `Adendo`
  (`ambiente_id`).
- O `flow.py` (as seis operações: `importar`, `revisar`, `recusar`, `liberar`, `alterar`,
  `contestar`) — **as transições validadas no serviço**, não na tela.
- O **hash canônico** (`v1|...`, sha256) e a **diferença** (`hash_visto` × `hash_liberado`).
- A `fonte_decisao()` (o inventário, lida uma vez; o caminho configurável).
- **Os testes do plano** — inclusive a **prova de mutação** (remover o gate/checagem e ver falhar).

**NÃO faça**: as telas (fatia 2), o `Study` (a fatia seguinte), o `planejar` (a 9.5 é posterior),
o Compose, o deploy, o `.env`, os segredos. Não altere o inventário nem o `verificar_inventario.py`.

## 3. As regras

- Branch `feature/DEM-202610-011-fatia1-dominio` a partir do `develop`; PR → develop; commits pt-BR.
- Rodar a suíte **do diretório do app** com `python -m pytest` (o `pytest.exe` do venv falha).
- Sem acento em código; com acento nos docs. Não "melhorar" o adjacente.
- A migração: o projeto usa o `create_all` (sem alembic) — um modelo novo/coluna nova com
  `create_all` não altera a tabela existente; registre no relatório o que a v1 precisa (a
  migração de dados fica com o deploy da v1).

## 4. Definition of Done

- os casos F-01..F-06, N-01..N-06, C-01..C-03 passando; a suíte do app **verde** (128 + os novos);
- a prova de mutação registrada no relatório;
- o relatório final no formato da DEM-012 (o que, onde, os testes, o que ficou fora).

> O EVAL cego julga pelo plano. A fatia 2 (as telas) só depois do PASS desta.
