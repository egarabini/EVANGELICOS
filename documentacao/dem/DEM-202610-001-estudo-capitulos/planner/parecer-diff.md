# Parecer do PLANNER sobre o diff real — DEM-202610-001

Data: 2026-10-16 · Branch: `feature/DEM-202610-001-estudo-capitulos` · Base: `develop` (`a6c5b80`)
Parecer sobre o **diff**, não sobre o relato de quem codificou.

## O que o diff contém

`git diff --stat develop...HEAD` → **8 arquivos, +714 / −2**.

| Tipo | Arquivo | Linhas |
|---|---|---|
| novo | `gsi_ebd/models/estudo.py` | +77 |
| novo | `gsi_ebd/scripts/importar_estudo_aplicado.py` | +413 |
| novo | `tests/test_estudo_aplicado.py` | +63 |
| modificado | `gsi_ebd/models/__init__.py` | +3 |
| modificado | `gsi_ebd/states/admin.py` | +72 |
| modificado | `gsi_ebd/pages/admin.py` | +80 |
| modificado | `gsi_ebd/components/sidebar.py` | +1 |
| modificado | `gsi_ebd/scripts/importar_obra.py` | +5 / −2 |

Corresponde ao List aprovado, **mais** o `importar_obra.py` — ver "Desvio" abaixo.

## Cobertura da spec pelo diff

| RF | Onde está | Situação |
|---|---|---|
| RF01 | `Estudo.obra_id` + `resolver_obra()` | coberto |
| RF02 | `EstudoCapitulo.ordem` + ordenação na leitura | coberto |
| RF03 | `EstudoCapituloOrigem` + `origem_label` com "sem origem declarada" | coberto |
| RF04 | `origem` sem unicidade por capítulo da obra (par é a chave) | coberto |
| RF05 | `gravar()` + autoteste (34/34, idempotente) | coberto |
| RF06 | `status=StudyStatus.RASCUNHO.value` na criação | coberto |
| RF07 | aba `_estudo_aplicado_tab` + item no menu, só leitura | coberto |
| RF08 | nenhum arquivo da lição no diff (**C-04**) | coberto |
| RF09 | importador só **lê** `Study`/`StudyVersion` no caminho de produção | coberto |
| RF10 | `origem_label` default "sem origem declarada" | coberto |

## Desvio em relação ao List aprovado

**1 commit fora do escopo declarado:** `6defd39 fix(obra)` — correção de 1 linha no
importador da obra (`select` do SQLModel em vez do SQLAlchemy).

Justificativa: defeito real, encontrado no caminho, que quebra a **re-execução** — e o
docstring da Fase 1 instrui o ARQUITECT a rodar de novo após corrigir a tradução. A DEM
depende da obra existir. Está em commit separado e é trivial de reverter.

## Conformidade com as ADRs

| ADR | Verificação |
|---|---|
| 001 stack | nenhuma dependência nova; nada de Node/TS |
| 002 corpus | nenhuma referência ao corpus; nenhuma escrita em `/conteudo` |
| 003 Escritura | o diff não toca `escritura_service` nem o caminho da Escritura |
| 005 modelo | materializa Obra → Estudo; não altera `Obra`/`ObraCapitulo` |
| 010 publicação | nenhum comando de deploy; entrega por branch + PR |
| 011 aprovação | capítulo nasce em rascunho; a assinatura+hash é da Ação 1, fora do escopo |

## Provas objetivas

- **C-04:** `git diff --stat develop...HEAD -- gsi_ebd/pages/lesson.py gsi_ebd/states/aluno.py gsi_ebd/models/study.py` → **vazio**.
- Suíte: **82 passed** (76 + 6 novos).
- Autoteste do importador: **PASS**, 10 checagens.

## Riscos que o diff deixa

1. **Ordem operacional:** as 3 tabelas nascem quando o ARQUITECT roda o importador
   (`create_all`). Entre o deploy e essa execução, a aba **Estudo Aplicável** consulta
   tabelas que ainda não existem e cai no estado vazio, com erro no log. É o preço de
   não ter migration formal; registrado como nota de operação, não como defeito.
2. `datetime.utcnow()` emite `DeprecationWarning` — **consistente com o resto do repo**
   (`importar_obra.py` faz igual). Não é regressão desta DEM.
3. O `_semear_estudos()` do autoteste cria `Study` em SQLite **descartável** — é fixture
   de teste, não caminho de produção. Registro aqui para evitar leitura equivocada do
   H-04 (que verifica que o caminho real não escreve em `Study`).

## Recomendação

**Liberar para o EVAL.** Nada no diff contraria a spec nem as ADRs; o único desvio está
isolado, justificado e revertível.
