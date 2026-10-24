# DEM-202610-011 — o fluxo de obras e estudos

## Finalidade

O fluxo de aprovação de **obras e estudos** com os estados, as assinaturas e os gates — implementando
a **ADR-011** (a aprovação assinada) com a **emenda da ADR-019** (a assinatura como intervalo) e a
**ADR-020** (a autoridade e a disponibilidade). Fecha a **D-07**.

## As fatias

| Fatia | O quê | Estado |
|---|---|---|
| **1** | **O domínio**: as 12 operações, os hashes (normalização LF+NFC + JSON canônico), os gates de licença, a trilha append-only, a disponibilidade e o `VinculoObra` | **PASS** (269 testes; 39/39 casos; 9/9 mutações) e **mergeada** no `develop` (`7670aec`, o PR #4) |
| **2** | **As telas do fluxo** (na v1): inclusão, desenvolvimento, aprovação e estudo com alunos fake | **PR #9** a partir da develop `5c0bc3e`; 1ª rodada EVAL FAIL no critério 5 (fluxo vacuoso); fix do HTTP do aluno fake + fail-open do seed; **não** o PR #5; aguarda 2ª rodada do EVAL |
| **3** | **A coordenação**: o `desvincular`, o CRUD do **adendo do ambiente** e o `planejar` (a 9.5) | a fatia da coordenação |

## O PASS — e o que o EVAL registrou

O EVAL cego **validou a nova semântica da ADR-020**: o `revisar`/`recusar` movem só o estado
**editorial** e nunca a publicação nem a disponibilidade; a N+1 é um registro novo; a N fica
`liberada` intacta e depois `substituida`; o `vincular` fixa a versão; a suspensão bloqueia só os
novos; e o `contestar` **não existe** mais (é a `solicitar_revisao`).

**Os 11 avisos não bloqueantes** (o registro para as fatias seguintes):

1. O `vincular` não emite `ObraVersaoEvento` — o `VinculoObra` é a trilha própria (a ressalva do F-10).
2. **A spec aprovada (o RF06/§10) cita o `desvincular` e o adendo do ambiente; a fatia 1 só tem o `vincular` + o `Adendo.ambiente_id`** → a fatia 3.
3. A solicitação pendente sobrevive ao `alterar`/`cancelar`; um `aceitar` posterior pode abrir a N+2 → a fatia 2/3 (o ciclo da solicitação).
4. O `conteudo_hash` do `importar` é o da base vazia até o primeiro `revisar` (a base é anexada depois).
5. O `recusar` atualiza o `hash_visto` sem criar um novo `visto`.
6. A prévia do `diferenca(atual=True)` usa o texto cru (o CRLF/NFD pode aparecer).
7. Sem a migração Alembic e com a FK circular `obra.versao_liberada_id` ↔ `obraversao.obra_id` → a v1 (o banco próprio + o baseline).
8. O `importar` não valida a base duplicada; o cache de exibição não é atualizado pelo `recarregar`; o F-06 compara sem `order_by`; o CI em 3.12 × o local 3.14.6.

## Os registros

- **Intent** (signed), **spec** (aprovada), **design v7**, **plano v4**: [`planner/`](planner/)
- A **ADR-020** (a autoridade e a disponibilidade), a **ADR-019** (emendada), a **ADR-011**
- O **despacho** e o **briefing** do Codex, o **relatório**, a **jornada**, as **evidências de mutação**: [`dev/`](dev/)
- O **EVAL**: [`eval/jornada.md`](eval/jornada.md) — o PASS da verificação


## Entrega da fatia 2

Branch **nova** a partir da `develop` `5c0bc3e` (`feature/DEM-202610-011-fatia2-obras`). O PR #5 (`fatia2-telas`) **não** é o veículo: duplicava o esqueleto do marco 1. Esta fatia traz **só as telas** para a v1 que já está na develop.

Contrato: `rbac.py` com as 3 chaves (`/admin/obras` = ADMIN; `/revisor/obras` = REVISOR; `/obras` = os dois). Matriz de 15 células com permitido **e** negado; prova de vacuidade (monkeypatch remove as 3 chaves). ADR-020 nas telas. Alunos fake só no seed de homologação (`v1/seed_homolog_estudo.py`); o seed de produção não os recebe.

Suíte local após o fix do critério 5: **138 testes v1 + 273 regressão**. 1ª rodada: [CI `pull_request` 40038006423](https://github.com/egarabini/gsi_ebd/actions/runs/40038006423) (`3f9246e`) e [40038703819](https://github.com/egarabini/gsi_ebd/actions/runs/40038703819) (`8ae1a3c`, opção A). Fix: [CI `pull_request` 40043436945](https://github.com/egarabini/gsi_ebd/actions/runs/40043436945) (`48f97f8`). Check `testes (pytest)` no [PR #9](https://github.com/egarabini/gsi_ebd/pull/9). **2ª rodada do EVAL** (máximo do ADR-018) pendente.

[Despacho](../DEM-202610-005-saida-do-reflex/dev/despacho-obras-fatia2.md) · [plano de testes](../DEM-202610-005-saida-do-reflex/dev/plano-testes-obras.md) · [jornada](dev/jornada-fatia-2.md)
