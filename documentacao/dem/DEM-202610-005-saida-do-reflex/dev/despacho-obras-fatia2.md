# Despacho ao DEVS — as obras (DEM-011, fatia 2)

> **O quê / o porquê / o DoD / o risco.** O PR #5 (`feature/DEM-202610-011-fatia2-telas`) está em
> **rascunho** e **duplica o esqueleto do marco 1** (que já está na `develop`). **NÃO despachar o #5
> como está.**

## O quê

**Recriar a branch da fatia 2 a partir da `develop`** (o `8389630`, que já contém o marco 1) e trazer
**só as telas do fluxo de obras**:

1. a **inclusão** da obra (o `OS`/o texto de referência, o revisor);
2. o **desenvolvimento** (o estudo dirigido: os capítulos, as questões);
3. a **aprovação** (o parecer do Revisor, a liberação do Admin);
4. o **teste do estudo com os alunos fake** (a inclusão → o desenvolvimento → a aprovação → o estudo).

## O contrato do `rbac.py` (as 3 chaves)

| A rota | O papel |
|---|---|
| **`/admin/obras`** | **ADMIN** |
| **`/revisor/obras`** | **REVISOR** |
| **`/obras`** | **os dois** (o ADMIN e o REVISOR) |

**O teste da matriz (papel × rota) — NÃO vacuoso**: **cada célula** da matriz tem **duas asserções**:
- **o permitido** (o papel certo → 200);
- **o negado** (o outro papel → 403/404).

**A lição do marco 1**: um teste da matriz que só verifica o **permitido** passa com o `rbac` vazio.
**A matriz tem de falhar** se as 3 chaves forem removidas.

## As regras de autoridade (o ADR-020, Accepted)

- **só o Admin** muda o **estado de publicação/disponibilidade**;
- **o Revisor** é auxiliar de qualidade: move o **estado editorial**, **assina parecer**,
  **`solicitar_revisao`**;
- a **liberação** exige a **assinatura do Revisor + a liberação do Admin**;
- a **versão liberada é imutável** — o ciclo cria a **N+1**;
- o **hash canônico** com a normalização **LF + NFC**;
- a **disponibilidade**: `aberta | suspensa_para_novos`.

## O modo estudo com alunos fake

- **a inclusão da obra** → o **desenvolvimento** → a **aprovação** → o **teste do estudo**;
- **onde os dados fake vivem**: o banco **`didasko_v1` de HOMOLOGAÇÃO** — **nunca** a produção;
- **o dado fake** é seed/migração de homologação (o `v1/seed`? o documento), **não** dado de produção.

## O DoD

- a branch nova **a partir da `develop`**, sem o esqueleto duplicado (o diff contra o #5 mostra só as
  telas);
- o `rbac.py` com as **3 chaves**; o **teste da matriz** com as duas asserções por célula;
- as telas do fluxo (a inclusão, o desenvolvimento, a aprovação, o teste com os alunos fake);
- o **CI verde**; o **EVAL cego** (o máximo de 2 rodadas, ADR-018) antes do aceite;
- a **documentação** da DEM-011 atualizada (o plano, o status).

## O risco

| O risco | A mitigação |
|---|---|
| o #5 recriado a partir do **marco 1** (o esqueleto duplicado) | a branch **nova a partir da `develop`**; o diff avaliado **antes** do push |
| a matriz **vacuosa** (só o permitido) | as **duas** asserções por célula; a prova de que **falha** sem o `rbac` |
| o **dado fake** na produção | o seed de **homologação**; a produção **nunca** recebe o fake |
| o **Revisor** com autoridade demais | o **ADR-020**: só o Admin muda a publicação; a liberação **exige** os dois |
| o escopo inflar (o fluxo inteiro de uma vez) | a fatia 2 entrega o **fluxo mínimo** (a inclusão → o teste); o resto na fatia 3 |
