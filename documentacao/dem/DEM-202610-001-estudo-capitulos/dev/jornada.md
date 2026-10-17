# Jornada do DEVS — DEM-202610-001

```
Agente: DEVS (IA)
Papel:  DEVS
DEM:    DEM-202610-001-estudo-capitulos
Branch: feature/DEM-202610-001-estudo-capitulos
Registro: **data** (decisão do ARQUITECT — sem relógio e sem tokens)
```

## Tarefa 0 — TLC (Think + List) · 2026-10-16

Think e List apresentados; **List aprovado pelo ARQUITECT em 2026-10-16**.

## Tarefa 1 — modelos · 2026-10-16

`models/estudo.py` com `Estudo`, `EstudoCapitulo`, `EstudoCapituloOrigem` + registro
em `models/__init__.py`.

Decisão: `status = StudyStatus.RASCUNHO` — o enum já existia com o mesmo ciclo de vida,
e criar outro só duplicaria taxonomia.

Verificação: as 3 tabelas aparecem no metadata com as FKs certas
(`obra.id`, `obracapitulo.id`, `adendo.id`, `estudocapitulo.id`); suíte 76 verde.

## Tarefa 2 — importador · 2026-10-16

`scripts/importar_estudo_aplicado.py` no padrão de `importar_obra.py`.

**Desvio 1 (erro meu).** Importei `select` do SQLAlchemy, que devolve `Row`; `obra.id`
estourou `AttributeError`. Corrigido para o `select` do SQLModel.

**Como descobri o defeito no importador da obra:** foi o mesmo erro, no mesmo lugar.
Ver "Descoberta" abaixo.

Verificação: `--apply --autoteste` → **PASS**, 10 checagens (F-11 aborta sem a obra e
não cria nada; 34 capítulos; 34 origens; 5 exemplos ignorados; tudo em rascunho;
idempotente; não duplicou; dry-run seleciona 34).

## Descoberta fora do escopo declarado — `importar_obra.py`

**Defeito:** `from sqlalchemy import func, select` → na **re-execução**, `obra.id`
estourava `AttributeError: id`. A primeira execução nunca lia o registro de volta
(criava a obra e seguia com a instância local), então o defeito nunca apareceu — e
contradiz o que o próprio docstring promete ("quando a correção for feita, basta rodar
de novo") e a premissa de idempotência da Fase 1.

**Ação:** corrigido em **commit separado** (`6defd39`), 1 linha, trivial de reverter.
Justificativa: esta DEM depende da obra existir, e é o ARQUITECT quem roda o importador
da obra depois de corrigir a tradução.

**Verificado:** 1ª execução 34 novos; 2ª execução 0 novos / 0 atualizados.

## Tarefa 3 — testes das funções puras · 2026-10-16

6 testes em `tests/test_estudo_aplicado.py`: ordem pelo título (padrão real dos 34 e os
5 exemplos), escolha de versão (maior, empate por data, vazio), seleção e ordenação.

## Tarefa 4 — estado do admin · 2026-10-16

Duas listas planas (`estudos_aplicados`, `capitulos_estudo`) + `load_estudos_aplicados()`.
Rótulos montados **em Python** (`origem_label`, `conteudo_label`) — nada concatenado no
componente, para não repetir o incidente de 16/10.

## Tarefa 5 — tela e menu · 2026-10-16

Aba **Estudo Aplicável** + item no menu (7 itens).

**Desvio 2 (erro meu, pego antes do commit).** Colidi o nome com a aba de Aprovação:
já existia `_estudos_tab()`. O Python não reclama — a segunda definição sobrescreve a
primeira, e a aba de **Aprovação de Estudos passaria a mostrar a tela nova**. Foi pego
ao conferir a fiação (6 triggers × 6 contents × funções distintas). Renomeada para
`_estudo_aplicado_tab`. Lição: compilar não basta; é preciso conferir **o que** está
ligado em **qual** aba.

## Tarefa 6 — verificação final · 2026-10-16

- suíte: **82 verdes** (76 + 6)
- autoteste do importador: **PASS** (10 checagens)
- `tests/test_paginas.py`: a página admin compila com a aba nova
- **C-04:** `git diff --stat develop...HEAD` em `lesson.py`, `aluno.py`, `study.py` → **vazio**

## Estado

Implementação concluída na branch, em 2 commits (`6defd39` fix, `ac712dd` feat).
Aguardando parecer do PLANNER sobre o diff real e o EVAL cego.
