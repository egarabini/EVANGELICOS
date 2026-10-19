# Briefing do EVAL — DEM-202610-011, fatia 1 (o domínio)

> **Para:** EVAL (subagente cego) · **De:** PLANNER · **Data:** 2026-10-19
> **Você não sabe quem implementou e não deve procurar saber.** Julgue pelo plano. Este briefing
> segue o template [`metodo/templates/briefing-eval.md`](../../../metodo/templates/briefing-eval.md).

## 1. O que ler

1. `planner/intent.md` (signed), `planner/spec.md` (**aprovada**), `planner/design.md` (**v4** — as
   snapshots com `momento`, os eventos, a normalização) e `planner/plano-testes.md` (**v3** — o F,
   N, C, H + a mutação).
2. O **diff**: `git -C ESTUDOS_BIBLICOS/GSI_EBD diff origin/develop...8f6608a` (a branch
   `feature/DEM-202610-011-fatia1-dominio`, commit `8f6608a`; o checkout local está nela).
3. O código: `gsi_ebd/services/flow.py`, `gsi_ebd/services/fontes.py`, `gsi_ebd/models/obra.py`,
   os testes `tests/test_flow.py` e `tests/test_fontes.py`.

## 2. O que fazer

- Rodar a suíte **do diretório do app** (`ESTUDOS_BIBLICOS/GSI_EBD`) com `python -m pytest`
  (`--basetemp` fora do app, se o `tmp_path` falhar).
- Executar os casos: **F-01..F-16** (a **ADR-020** mudou a semântica: o **F-06 foi reescrito** — a
  versão NOVA, a liberada intacta, só o Admin abre ciclo; o **F-06b** e o **F-12..F-16** são novos:
  a disponibilidade, a solicitação, o `versao_id` fixado, o cancelamento, a posição), **N-01..N-08**,
  **C-01..C-10**, os H.
- **A distinção editorial × publicação (a ADR-020)**: o `revisar`/`recusar` movem o estado
  **editorial** da versão (o Revisor) e **nunca** a `versao_liberada_id` nem a `disponibilidade`
  (só o Admin). Prove isso: o `revisar` não muda a publicação.
- Verificar os **invariantes no código**: as transições validadas no serviço (não no template); o
  `revisar`/`recusar` recusam com `hash_esperado` diferente; o `liberar` cria o instantâneo
  **liberado** e o `revisar` cria o **visto**; o `alterar` não remove; cada operação acrescenta um
  `ObraVersaoEvento`; o `liberar` usa `recarregar=True`; a normalização (LF + NFC); o `flow.py`
  **não importa `reflex`** (o C-07).
- **Prova de mutação** (em cópia fiel, restaurando com `git checkout --`): sem o gate do
  `nao_entra` → N-01; sem a checagem do `hash_esperado` → N-08; sem o instantâneo visto → F-08;
  **sem a normalização → C-10**; **sem o evento → F-10**; sem o `revisor_id` → N-03.

## 3. O ambiente (o que já sabemos)

`python -m pytest` (não o `pytest.exe`); o `tmp_path` 0o700 no sandbox exige `--basetemp` fora do
app; a escrita na árvore do app pode ser negada por ACL → a mutação em **cópia fiel**; se o HEAD
mudar durante o julgamento, **não faça checkout** (verifique o diff e siga).

## 4. O que reportar

- **PASS/FAIL por caso** (F, N, C, H), com o comando e a saída;
- cada **FAIL**: o defeito, a causa e o caso que ele viola;
- os **avisos não bloqueantes** separados;
- o **veredito** (PASS/FAIL) com a justificativa;
- os resíduos e o ambiente que precisou de contorno.

Grave em `eval/jornada.md`. **Não leia** o `dev/jornada.md` nem o `dev/relatorio.md` (a cegueira).
Não conserte nada — julgue.

