# Jornada do DEVS — DEM-202610-001

```
Agente: DEVS (IA)
Papel:  DEVS
DEM:    DEM-202610-001-estudo-capitulos
Registro: **data** (decisão do ARQUITECT — sem relógio e sem tokens)
```

## Tarefa 0 — TLC (Think + List) · 2026-10-16

Status: **List aguardando aprovação do ARQUITECT.** Nenhum arquivo de código criado;
nenhuma branch criada.

### Think — assunções declaradas

1. A fonte da carga é o **banco**: os 34 `Study` + a `StudyVersion` de maior `version`.
   Não releio o markdown (design §4).
2. A ordem vem do título do `Study` (`^Cap\.\s*(\d+)`), com fallback para a ordem de
   criação. Função pura, testável isoladamente.
3. `questions_json` é **opaco**: copio a string, não parseio, não valido.
4. `StudyStatus.RASCUNHO` serve; **não** crio enum novo.
5. A aba nova segue o padrão de `_obras_tab`: listas planas, rótulos montados no estado.
6. `create_all` no importador cria as 3 tabelas (o projeto não usa Alembic).
7. O importador **aborta** se a obra não existir, antes de criar qualquer coisa (design §4).

### Ambiguidades e conflitos

- **Nenhum conflito** com as ADRs 001–011.
- Uma decisão que estava ambígua foi fechada pelo ARQUITECT nesta rodada: **quem roda a
  carga em produção**. Registrado no design §4: o ARQUITECT, manualmente, após `pg_dump`
  e após o merge — nunca o agente (ADR-010).
- Dois ajustes do ARQUITECT foram incorporados antes deste List: a **pré-condição da obra**
  (F-11) e a **prova objetiva de não tocar na lição** (C-04, `git diff` vazio).

### List — arquivos, riscos e ordem

**Criar (3)**

| # | Arquivo | Conteúdo |
|---|---|---|
| 1 | `gsi_ebd/models/estudo.py` | `Estudo`, `EstudoCapitulo`, `EstudoCapituloOrigem` |
| 2 | `gsi_ebd/scripts/importar_estudo_aplicado.py` | importador idempotente, `--apply`/`--autoteste`, aborto na pré-condição, funções puras |
| 3 | `tests/test_estudo_aplicado.py` | ordem pelo título, fallback, idempotência, pré-condição |

**Modificar (4)**

| # | Arquivo | Mudança |
|---|---|---|
| 4 | `gsi_ebd/models/__init__.py` | registro das 3 entidades (~2 linhas) |
| 5 | `gsi_ebd/states/admin.py` | 2 listas planas + `load_estudos_aplicados()` |
| 6 | `gsi_ebd/pages/admin.py` | aba **Estudos** (~40 linhas) |
| 7 | `gsi_ebd/components/sidebar.py` | 1 item de menu |

**Não tocar (declarado e verificável por C-04):**
`gsi_ebd/pages/lesson.py` · `gsi_ebd/states/aluno.py` · `gsi_ebd/models/study.py` ·
`gsi_ebd/scripts/importar_obra.py` · todo `gsi_ebd/services/` · o corpus.

**Riscos**

| Risco | Mitigação |
|---|---|
| Obra ausente no banco | aborta antes de criar nada (F-11) |
| Título fora do padrão `Cap. NN` | fallback por ordem de criação, unitário |
| Mais de uma `StudyVersion` | maior `version`; empate por `created_at` |
| A aba quebrar a compilação da página (incidente de 16/10) | rótulos prontos no estado, sem `Var + str`; `test_paginas.py` roda antes do commit |
| `create_all` no banco de produção | só cria tabelas ausentes; contagens conferidas antes/depois (H-04) |

**Ordem dos passos**

1. `models/estudo.py` + registro → suíte verde
2. `scripts/importar_estudo_aplicado.py` (com `--autoteste`)
3. `tests/test_estudo_aplicado.py` → verde
4. `states/admin.py`
5. `pages/admin.py` + `components/sidebar.py` → `test_paginas.py` verde
6. suíte completa

**Branch:** `feature/DEM-202610-001-estudo-capitulos`, criada de `develop` no passo 1.

### Estado

- [x] Think
- [x] List
- [ ] **List aprovado pelo ARQUITECT** ← aguardando
- [ ] Code (passo 1 em diante)
