# Design — DEM-202610-001 / Estudo com capítulos próprios e mapa de origem

> Dono: PLANNER. O **como** técnico, dentro do stack do perfil. Não reabre o *porquê*
> (intent) nem o *quê* (spec).

## 1. Referência

Spec: [`spec.md`](spec.md) — aprovada em 2026-10-16 · ADRs: 001 (stack), 002 (corpus),
005 (modelo), 011 (rascunho/assinatura), 010 (publicação).

## 2. Componentes a criar ou modificar

- **Modelos** — `gsi_ebd/models/estudo.py` *(novo)*: `Estudo`, `EstudoCapitulo`,
  `EstudoCapituloOrigem`; registrar em `gsi_ebd/models/__init__.py`.
- **Importador** — `gsi_ebd/scripts/importar_estudo_aplicado.py` *(novo)*, no padrão de
  `importar_obra.py`: `--apply`, `--autoteste`, funções puras testáveis.
- **Estado** — `gsi_ebd/states/admin.py`: `estudos_aplicados` e `capitulos_estudo`
  (listas **planas**) + `load_estudos_aplicados()`.
- **Tela** — `gsi_ebd/pages/admin.py`: aba **Estudos**; `gsi_ebd/components/sidebar.py`: item.
- **Testes** — `tests/test_estudo_aplicado.py` *(novo)*; `tests/test_paginas.py` já cobre a página.
- **Persistência** — 3 tabelas novas via `SQLModel.metadata.create_all` no importador
  (mesmo padrão da Fase 1). **Nenhuma tabela existente é alterada.**

## 3. Fluxo principal

1. O **ARQUITECT** roda `python -m gsi_ebd.scripts.importar_estudo_aplicado --apply`
   (ver §4, "Quem executa a carga").
2. **Pré-condição verificada antes de escrever:** a obra da Fase 1 tem de existir no
   banco. Se não existir, o importador **aborta com mensagem clara e não cria nada** —
   falhar é melhor do que criar capítulos sem origem (coberto pelo caso F-11).
3. O importador resolve o estudo de destino (cria se não existir, ligado à obra).
4. Lê os **34 `Study` existentes** e, de cada um, a `StudyVersion` de maior `version`.
5. Deriva a ordem do título (`Cap. NN`) e cria/atualiza o `EstudoCapitulo` com
   `status = RASCUNHO`, copiando `content_md` e `questions_json`.
6. Cria/atualiza a origem 1:1 com o `ObraCapitulo` de ordem equivalente.
7. A tela lê as 3 tabelas + `ObraCapitulo`/`Adendo` e exibe em modo leitura.

## 4. Decisões técnicas

- **A fonte da carga é o banco, não o markdown.** Os 34 `Study` + `StudyVersion` já têm o
  conteúdo e as questões que o aluno consome; reler o markdown duplicaria a lógica e
  poderia divergir. O importador **só lê** essas tabelas (RF09).
- **Quem executa a carga, onde e quando:** o **ARQUITECT**, manualmente, **depois** do
  `pg_dump` (rotina de backup do perfil) e **depois** do merge/release. Nunca o agente —
  a ADR-010 proíbe IA de escrever em produção. O agente entrega código, a instrução e a
  evidência; a escrita em produção é humana.
- **Pré-condição dura, verificada antes de escrever:** obra ausente → **aborta sem criar
  nada**. O caminho é exercitado no autoteste (F-11).
- **Ordem derivada do título** com `^Cap\.\s*(\d+)`, e **fallback** para a ordem de
  criação quando o título não seguir o padrão. Função pura e testável.
- **`questions_json` copiado como texto opaco** — não é parseado nem revalidado aqui.
- **Status = `StudyStatus.RASCUNHO`** (já existe no enum; `Study` não é modificado).
  A ADR-011 (assinatura + hash) **não** é implementada nesta DEM — só o estado inicial.
- **Strings montadas em Python, nunca no componente.** O estado entrega `origem_label` já
  formatado (`"Doutrinas Cristãs · Cap. 07 + ADO-07"` ou `"sem origem declarada"`).
  É a lição do incidente de 16/10, em que `Var + str` dentro de `rx.foreach` derrubou o app.
- **Listas planas, sem `foreach` aninhado** — dois `rx.foreach` independentes.
- **Idempotência** por `(estudo, ordem)` e por `(capítulo_do_estudo, capítulo_da_obra)`.

## 5. Migrations / mudanças de dados

- [x] **Sim** — 3 tabelas novas (`estudo`, `estudocapitulo`, `estudocapituloorigem`),
  criadas por `create_all` no importador. Nenhuma coluna existente é alterada ou removida.

## 6. Impacto em features/módulos existentes

- O menu do admin ganha **Estudos**; a página `admin` ganha uma aba.
- Nada mais. Lição, progresso, revisão, atribuições e catálogo não são tocados.

## 7. O que não muda

- A lição (`pages/lesson.py`, `states/aluno.py`) e o caminho
  `Study` / `StudyVersion` / `StudyAssignment` (RF08).
- O caminho da Escritura, o corpus e o importador da obra.
- Nada é publicado ao aluno: todo capítulo nasce **rascunho**.

## 8. Ordem de implementação

1. `models/estudo.py` + registro em `models/__init__.py`
2. `scripts/importar_estudo_aplicado.py` (funções puras + `--autoteste`, com aborto na pré-condição)
3. `tests/test_estudo_aplicado.py`
4. `states/admin.py` — `estudos_aplicados`, `capitulos_estudo`, `load_estudos_aplicados`
5. `pages/admin.py` (aba) + `components/sidebar.py` (item)
6. Suíte completa + `tests/test_paginas.py`

## 9. Riscos

- **Obra ausente no banco** → o importador aborta sem criar (F-11). Sem isso, o pior
  cenário seria criar capítulos órfãos e descobrir depois.
- **Título fora do padrão** `Cap. NN` → fallback por ordem de criação (coberto por teste).
- **Mais de uma `StudyVersion`** por estudo → escolher a de maior `version`; empate resolve
  por `created_at` mais recente.
- **Volume:** ~1,4 MB duplicados no banco. Aceitável; é o preço de separar fonte de aplicação.
- **`create_all` em banco de produção** cria só tabelas ausentes; como são novas, não há
  conflito com o que existe.
