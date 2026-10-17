# Jornada de EVAL — DEM-202610-001 / estudo-capitulos

- **Agente:** EVAL (porteiro independente; não escreveu o código, não leu `dev/` nem o `README.md` da DEM)
- **Data:** 2026-10-17 10:44 (-03:00)
- **DEM:** DEM-202610-001 — estudo com capítulos próprios e mapa de origem
- **Contrato executado:** `planner/plano-testes.md` (lido após `intent.md` e `spec.md`)
- **branch:** `feature/DEM-202610-001-estudo-capitulos`
- **hash:** `ac712dd73dad14a95b2352bc59bae927f9ec8c74`
- **estado_limpo:** **sim**
- **ambiente:** local apenas. Produção **não** foi acessada (nenhum SSH, nenhum HTTP, nenhum deploy). Nenhum banco de produção foi aberto.
- **árvore de trabalho do código:** limpa antes e depois (`git status --porcelain` vazio nos dois momentos)

## Âncora

```
$ git rev-parse HEAD
ac712dd73dad14a95b2352bc59bae927f9ec8c74
$ git log -1 --format="%H %ci %s"
ac712dd73dad14a95b2352bc59bae927f9ec8c74 2026-10-17 10:37:08 -0300 feat(estudo): estudo aplicavel com capitulos proprios e mapa de origem
$ git status --porcelain      # (vazio)
$ git diff --stat develop...HEAD
 gsi_ebd/components/sidebar.py               |   1 +
 gsi_ebd/models/__init__.py                  |   3 +
 gsi_ebd/models/estudo.py                    |  77 ++++++
 gsi_ebd/pages/admin.py                      |  80 ++++++
 gsi_ebd/scripts/importar_estudo_aplicado.py | 413 ++++++++++++++++++++++++++++
 gsi_ebd/scripts/importar_obra.py            |   7 +-
 gsi_ebd/states/admin.py                     |  72 +++++
 tests/test_estudo_aplicado.py               |  63 +++++
 8 files changed, 714 insertions(+), 2 deletions(-)
$ git merge-base develop HEAD
a6c5b80a53e9eecdaab0b6d67102bd191932dc94
```

## 1. Reset / estado limpo (executado ANTES de qualquer caso)

```
$ cd ESTUDOS_BIBLICOS/GSI_EBD
$ .venv/Scripts/python -m gsi_ebd.scripts.importar_estudo_aplicado --apply --autoteste
OK    F-11 abortou sem a obra
OK    F-11 nada foi criado (estudos=0, capitulos=0)
OK    F-05 34 capitulos (=34)
OK    F-05 34 origens (=34)
OK    N-06 5 exemplos ignorados (=5)
OK    F-01 um estudo (=1)
OK    F-06 tudo em rascunho (fora=0)
OK    RNF idempotente (novos=0, origens=0)
OK    RNF nao duplicou (capitulos=34)
OK    dry-run seleciona 34 (=34)

AUTOTESTE: PASS
EXITCODE: 0
```

Resíduo: o SQLite descartável do autoteste é apagado pelo próprio script (`arquivo.unlink`).
Conferido depois da execução:

```
$ Get-ChildItem "$env:TEMP\estudo-aplicado-autoteste-*.db"
(vazio — nenhum resíduo)
```

`estado_limpo = sim`. O reset **não** falhou → nada é BLOCKED por reset.

### Como a evidência de banco foi produzida (sem tocar em produção)

O autoteste apaga o SQLite ao final, e não existe banco local (`*.db` ausente na raiz do
código). Para poder **consultar** o banco em vez de confiar na saída do script do autor, o
EVAL montou fixture própria e rodou o **CLI de produção do importador** apontando
`DATABASE_URL` para um SQLite descartável em `%TEMP%`:

```
$ .venv/Scripts/python <eval>/_eval_seed.py "$env:TEMP\eval-dem202610-001.db"
SEED OK db=...\eval-dem202610-001.db com_obra=True
  study=39 studyversion=39 studyassignment=39 progress=39 userresponse=39 obra=1 obracapitulo=34

$ $env:DATABASE_URL="sqlite:///.../eval-dem202610-001.db"
$ .venv/Scripts/python -m gsi_ebd.scripts.importar_estudo_aplicado --apply
banco: sqlite:///C:/Users/EDUARD~1.NET/AppData/Local/Temp/dsh-Xnlc8o/eval-dem202610-001.db
obra: Doutrinas Cristãs (34 capitulos)
capitulos do livro encontrados: 34
ignorados (sem 'Cap. NN'): 5
  - Exemplo 1 ... - Exemplo 5

estudo: Doutrinas Cristãs — Estudo Dirigido (id 1)
  capitulos:          34
  novos:              34
  atualizados:        0
  origens novas:      34
  sem origem:         0
  sem versao:         0
  total capitulos:    34
  total origens:      34
EXIT=0
```

Scripts de probe usados (ficam em `eval/`, nada foi escrito fora de `eval/`):
`_eval_seed.py`, `_eval_after.py`, `_eval_nn.py`, `_eval_hash.py`.

## 2. Tabela de evidência por caso

| ID | Veredito | Evidência curta |
|----|----------|-----------------|
| R-00 reset | PASS | `AUTOTESTE: PASS`, exit 0, sem resíduo em `%TEMP%` |
| C-01 | PASS | nenhuma linha adicionada pelo diff toca `corpus`/`/conteudo`/`open(`/`write_text`; único toque em disco do código novo é `arquivo.unlink()` do SQLite descartável (l. 259, 355) |
| C-02 | PASS | 34/34 capítulos `rascunho` (`por_status=[('rascunho', 34)]`, `fora_de_rascunho=0`); aluno continua vendo 39 estudos atribuídos (`StudyAssignment`), nenhum do modelo novo |
| C-03 | PASS | nenhum `subir.sh`/`ssh`/`scp`/deploy executado; `git grep` em `gsi_ebd` = 0 ocorrências; `deploy/` fora do diff |
| C-04 | PASS | `git diff --stat develop...HEAD -- gsi_ebd/pages/lesson.py gsi_ebd/states/aluno.py gsi_ebd/models/study.py` → **vazio** |
| N-01 | PASS | `git grep -i agendament\|ressalva` em `gsi_ebd` → só comentário (`models/obra.py:25`); nenhuma rota/tabela |
| N-02 | PASS | nenhuma tabela/rota nova de biblioteca/nível/treinamento; `StudyLevel` já existia em `develop` (arquivo `study.py` fora do diff) |
| N-03 | PASS | nenhuma tabela/rota de liberação/classificação de aluno; `grep` só acha o comentário "quando a liberacao por capitulo existir, em DEM futura" (`models/estudo.py:48`) |
| N-04 | PASS | `git diff --stat` vazio em `pages/lesson.py`, `states/aluno.py` **e** `services/study_service.py`; a lição ainda lê `StudyVersion` (`study_service.py:68`) |
| N-05 | PASS | aba "Estudo Aplicável" (`pages/admin.py:370-406`) não tem `button`/`on_click`/`on_change`, só `on_mount=load_estudos_aplicados`; no `AdminState` o único método novo é leitura |
| N-06 | PASS | carga: "ignorados (sem 'Cap. NN'): 5"; `estudo=1`; nenhum capítulo com título de exemplo |
| F-01 | PASS | `Estudo` id=1, `obra_id=1` (`Doutrinas Cristãs`), título/descrição/`status='rascunho'`/`is_active=True`, `doutrina_id=None` (opcional) |
| F-02 | PASS | 34 capítulos, ordens 1..34, `distintas=34`, `continua_1_a_34=True`, todos no estudo 1 |
| F-03 | PASS | capítulo 35 do estudo com 2 origens, uma com adendo: tela exibe `Doutrinas Cristãs · Cap. 03 + ADO-01.03 ; Doutrinas Cristãs · Cap. 04` |
| F-04 | PASS | obra cap 03 com **2** origens (2 capítulos do estudo); capítulo 35 do estudo puxa de **2** capítulos da obra (N:N nos dois sentidos) |
| F-05 | PASS | CLI: `estudos=1`, `capitulos=34`, `origens=34`; query: `estudo=1 estudocapitulo=34 estudocapituloorigem=34` |
| F-06 | PASS | `por_status=[('rascunho', 34)]`, `fora_de_rascunho=0` (ADR-011) |
| F-07 | PASS | `AdminState.load_estudos_aplicados()` lê a tela real: `estudos_aplicados=[{titulo, status='rascunho', '34 capítulos'}]` e 34 linhas com `ordem/titulo/origem_label/conteudo_label/status`; carregar a tela **não grava** (36→36 caps, 36→36 origens); página compila (`tests/test_paginas.py` inclui `admin_page`) |
| F-08 | PASS | `pages/lesson.py:33` → `AlunoState.study_content` → `StudyService.load_version_payload` → `select(StudyVersion)`; 3 arquivos do caminho com diff vazio |
| F-09 | PASS | impressão digital antes×depois da carga: `study` 39/`82b4c812…`, `studyversion` 39/`c800fda4…`, `studyassignment`, `progress`, `userresponse`, `obra`, `obracapitulo` — **idênticas** |
| F-10 | PASS | capítulo 36 (sem origem) na tela: `origem_label='sem origem declarada'`, sem erro |
| F-11 | PASS | CLI `--apply` em banco sem obra: `ABORTADO: obra 'Doutrinas Cristãs' nao encontrada. Obras no banco: (nenhuma). ... NADA foi criado.` exit **2**; contagens depois: `estudo=0 estudocapitulo=0 origem=0` |
| H-01 | PASS | `python -m pytest tests -q` → **82 passed**, 1 warning, 6.10s |
| H-02 | **N-A** | depende de produção (HTTP 200 + "João 3:16" + 5 passagens no Cap. 21). EVAL não tem acesso; nenhum número foi inventado |
| H-03 | **N-A** | depende de produção (4 citações e 10 questões no Cap. 21). EVAL não tem acesso |
| H-04 | PASS (local) / **N-A** (produção) | local: tabelas que guardam conteúdo com impressão digital idêntica antes×depois + inspeção de código (só LÊ `Study`/`StudyVersion`, nenhum `delete`/`DROP`); as contagens de produção (39 / 31.102 / 344.799) **não** foram verificadas |
| G-01 | **N-A** | aceite visual do ARQUITECT. Preparado: aba **Estudo Aplicável** em `/admin` (e item "Estudo Aplicável" no menu lateral) lendo 34 capítulos com origem |

## 3. Evidência colada — C-*

**C-01 · o corpus não é escrito.** Nenhuma linha adicionada pelo diff toca corpus/arquivo:

```
$ git diff develop...HEAD | Select-String "^\+" | Select-String "corpus|/conteudo|open\(|write_text|subir\.sh|ssh|scp|deploy"
+        o deploy de 16/10 derrubou o site em loop de restart.      <-- comentário, não ação
```

Único toque em disco do código novo (`importar_estudo_aplicado.py`):

```
$ grep -n "open(\|write_text\|write_bytes\|shutil\|unlink\|rmtree"
259:    arquivo.unlink(missing_ok=True)      # SQLite descartável do autoteste
355:        arquivo.unlink(missing_ok=True)  # limpeza do SQLite descartável
```

O importador lê **o banco**, não o markdown/corpus (docstring l. 3-5 e `conferir`/`gravar`
só usam `select(...)` de `Obra`/`ObraCapitulo`/`Study`/`StudyVersion`).

**C-02 · nada fica disponível ao aluno.**

```
-- F-06 / C-02: status dos capitulos criados --
  por_status=[('rascunho', 34)]
  fora_de_rascunho=0

$ StudyService.list_assigned_studies(1)
estudos que o aluno ve (StudyAssignment): 39
titulos: Cap. 01 — Estudo 1, Cap. 02 — Estudo 2, Cap. 03 — Estudo 3 ...
```

**C-03 · sem deploy.** Nenhum `subir.sh`/SSH/scp foi executado nesta jornada; grep no código:

```
$ git grep -n -i -E "subir\.sh|scp |ssh |paramiko|fabric" -- gsi_ebd
(no matches found)
```

`deploy/subir.sh` existe no repositório, mas está fora do diff (`git diff --stat` não o lista)
e não foi invocado.

**C-04 · os três arquivos intocáveis.**

```
$ git diff --stat develop...HEAD -- gsi_ebd/pages/lesson.py gsi_ebd/states/aluno.py gsi_ebd/models/study.py
VAZIO (0 linhas)
```

## 4. Evidência colada — N-*

```
$ git grep -n -i -E "agendament|ressalva|biblioteca|treinamento|liberacao|liberar_aluno|classificacao|classificar" -- gsi_ebd
gsi_ebd/models/estudo.py:48:  acontece quando a liberacao por capitulo existir, em DEM futura).   # comentário
gsi_ebd/models/obra.py:3:    ... (ver `Diagnostico/plano-bibliotecas.md`)                       # docstring
gsi_ebd/models/obra.py:25:   tradição e registrar as ressalvas nos comentários.                 # docstring
gsi_ebd/scripts/importar_obra.py:5: `Diagnostico/plano-bibliotecas.md`).                         # docstring
```

Achados = **0** estruturas (nenhuma rota, nenhuma tabela, nenhuma tela). Schema físico confere:

```
$ python -c "...sorted(SQLModel.metadata.tables)..."
26 tabelas:
adendo, ambiente, ambienteestudo, doutrina, equipe, equipeinstrutor, estudo, estudocapitulo,
estudocapituloorigem, lead, notification, obra, obracapitulo, paymenthistory, progress,
referenciacruzada, siteconfig, study, studyassignment, studyversion, subscription, testemunho,
turma, turmamembro, user, userresponse
```

As únicas tabelas novas são as 3 do RF05 (`estudo`, `estudocapitulo`, `estudocapituloorigem`).
`StudyLevel` (níveis básico/médio/avançado/master) é **pré-existente**: `git show develop:gsi_ebd/models/study.py`
já traz `class StudyLevel` e o arquivo está fora do diff — não foi esta DEM que o criou.

N-04 (a lição não foi repontada):

```
$ git grep -n "StudyVersion" -- gsi_ebd/services/study_service.py
gi:68:            select(StudyVersion).where(StudyVersion.id == version_id)
$ git diff --stat develop...HEAD -- gsi_ebd/services/study_service.py
VAZIO
$ git grep -c "EstudoCapitulo" -- gsi_ebd/pages/lesson.py gsi_ebd/states/aluno.py
(0 ocorrências nos dois)
```

N-05 (a tela não cria nem edita): a aba nova é

```
$ git diff develop...HEAD --unified=0 -- gsi_ebd/states/admin.py  (linhas adicionadas)
+    def load_estudos_aplicados(self):          <-- único método novo
+            EstudoCapitulo, EstudoCapituloOrigem  <-- só em select(...)
```

e os eventos de escrita de `pages/admin.py` (linhas 70, 77, 106, 112, 172, 250) estão todos em
abas pré-existentes (Usuários/Estudos), nenhum na aba `estudo_aplicado`.

## 5. Evidência colada — F-*

**F-05 / F-02 / F-01 / F-06 / N-06 (leitura do banco depois do CLI):**

```
TABELA                  CONTAGEM
  study                  39        studyversion      39
  studyassignment        39        progress          39
  userresponse           39        obra               1
  obracapitulo           34        estudo             1
  estudocapitulo         34        estudocapituloorigem 34

-- F-01: o Estudo --
  id=1 obra_id=1 obra='Doutrinas Cristãs' titulo='Doutrinas Cristãs — Estudo Dirigido'
  descricao='Estudo aplicavel gerado da obra Doutrinas Cristãs.' doutrina_id=None status='rascunho' is_active=True

-- F-02: ordem dos capitulos --
  capitulos=34 ordens_min=1 ordens_max=34
  distintas=34 continua_1_a_34=True
  estudo_ids=[1]

-- F-05 --
  estudos=1 capitulos=34 origens=34

-- conteudo propagado da origem real (StudyVersion) --
  cap1.titulo='Cap. 01 — Estudo 1' == study.title -> True
  cap1.conteudo_md == studyversion.content_md -> True (len=226)
  cap1.questions_json == studyversion.questions_json -> True ([{"q": "pergunta 1"}])

-- N-06: os 5 exemplos nao viraram estudo --
  algum titulo 'Exemplo': []   |  estudos=1  |  capitulos fora do padrao 'Cap. NN': []
```

**Idempotência (RNF do RF05) — segunda carga, mesmo banco:**

```
$ python -m gsi_ebd.scripts.importar_estudo_aplicado --apply     # 2a vez
  capitulos:          34
  novos:              0
  atualizados:        0
  origens novas:      0
  total capitulos:    34
  total origens:      34
EXIT=0
```

**F-03 / F-04 / F-07 / F-10 (mapa N:N e tela de verdade):**

```
-- F-04: quantas origens apontam para cada capitulo da obra (N:N) --
  obra cap 03: 2 origem(ns)  <== 2 capitulos do estudo
  obra cap 04: 2 origem(ns)  <== 2 capitulos do estudo
  (demais: 1 origem)

-- F-03: origens do capitulo 35 do estudo (obra + adendo opcional) --
  obra_cap=03 adendo=ADO-01.03
  obra_cap=04 adendo=None
  origens do capitulo 36 (sem origem) = 0

-- F-07: o que a tela mostra --
  estudos_aplicados = [{'titulo': 'Doutrinas Cristãs — Estudo Dirigido', 'status': 'rascunho', 'capitulos_label': '36 capítulos'}]
  capitulos listados = 36
  ordem 03: origem_label='Doutrinas Cristãs · Cap. 03'
  ordem 35: origem_label='Doutrinas Cristãs · Cap. 03 + ADO-01.03 ; Doutrinas Cristãs · Cap. 04'
  ordem 36: origem_label='sem origem declarada'   status='rascunho'

-- F-10: 'sem origem declarada' presente no capitulo 36 -> True
-- F-07 somente leitura: carregar a tela nao gravou nada (capitulos 36->36, origens 36->36)
```

**F-09 / H-04 (nada existente é perdido) — impressão digital das tabelas antes×depois:**

```
=== ANTES da carga ===                        === DEPOIS da carga ===
  study              linhas=39  sha256=82b4c81270d0d251…   →  82b4c81270d0d251…
  studyversion       linhas=39  sha256=c800fda44bf556bf…   →  c800fda44bf556bf…
  studyassignment    linhas=39  sha256=01b4a0f699456010…   →  01b4a0f699456010…
  progress           linhas=39  sha256=f42c3e959f7f4ac9…   →  f42c3e959f7f4ac9…
  userresponse       linhas=39  sha256=39d2ff8fed31fd27…   →  39d2ff8fed31fd27…
  obra               linhas=1   sha256=8c662098234a0895…   →  8c662098234a0895…
  obracapitulo       linhas=34  sha256=2d716ca7875c8488…   →  2d716ca7875c8488…
```

**F-11 (pré-condição dura, reproduzida isoladamente pelo CLI):**

```
$ python _eval_seed.py <tmp> --no-obra
SEED OK com_obra=False  study=39 ... obra=0 obracapitulo=0

$ DATABASE_URL=sqlite:///<tmp> python -m gsi_ebd.scripts.importar_estudo_aplicado --apply
banco: sqlite:///…/eval-f11-sem-obra.db
ABORTADO: obra 'Doutrinas Cristãs' nao encontrada. Obras no banco: (nenhuma).
Rode o importador da obra (Fase 1) antes — NADA foi criado.
EXIT=2

contagens depois: estudo=0 estudocapitulo=0 origem=0 | intactos: study=39 obra=0
```

Mensagem clara + 0 registros criados → PASS (não falha em silêncio, não cria capítulo sem origem).

## 6. Evidência colada — H-*

**H-01 · suíte:**

```
$ .venv/Scripts/python -m pytest tests -q
........................................................................ [ 87%]
..........                                                               [100%]
82 passed, 1 warning in 6.10s
```

Divergência de documento, registrada por transparência (não muda o veredito): o `intent §6`
e a tabela de rastreio do plano dizem **76**; o despacho diz **82**. A conta fecha:
76 (baseline em `develop`) **+ 6** testes novos de `tests/test_estudo_aplicado.py` = **82**.
`tests/test_estudo_aplicado.py` não existe em `develop` (`git show develop:...` → arquivo novo)
e tem exatamente 6 `def test_`. Nenhuma falha, nenhum skip.

**H-04 (parte local, por inspeção de código) — o importador só LÊ `Study`/`StudyVersion`:**

```
$ todas as escritas do importador
173:        session.add(estudo)                    <-- Estudo        (caminho de produção)
209:            session.add(cap)                   <-- EstudoCapitulo (caminho de produção)
222:                session.add(cap)               <-- EstudoCapitulo (caminho de produção)
236:            session.add(EstudoCapituloOrigem(  <-- Origem        (caminho de produção)
243:    session.commit()
273:    session.add(obra)                          <-- só em _semear_obra (autoteste)
276:        session.add(ObraCapitulo(              <-- só em _semear_obra (autoteste)
280:    session.commit()
287:        session.add(study)                     <-- só em _semear_estudos (autoteste)
289:        session.add(StudyVersion(...            <-- só em _semear_estudos (autoteste)
295:        session.add(study)                     <-- só em _semear_estudos (autoteste)
297:        session.add(StudyVersion(...            <-- só em _semear_estudos (autoteste)
300:    session.commit()

$ quem chama as funções de semeadura
317:        _semear_estudos(session)               <-- dentro de autoteste()
329:        _semear_obra(session, "Obra de Teste") <-- dentro de autoteste()
```

`autoteste()` usa `engine_de_teste()` (SQLite em `tempfile`), **separado** de
`engine_de_producao()`. Logo, as únicas escritas em `Study`/`StudyVersion` do arquivo vivem no
caminho descartável do autoteste e nunca no caminho `conferir`/`gravar`/CLI.

```
$ git grep -n -i -E "referenciacruzada|versiculo|versículo|update\(Study|delete\(Study" -- gsi_ebd/scripts/importar_estudo_aplicado.py
(vazio — não toca versículos nem referências cruzadas)

$ git grep -n -E "delete\(|session\.delete|DROP|TRUNCATE" -- gsi_ebd/models/estudo.py gsi_ebd/states/admin.py gsi_ebd/scripts/importar_estudo_aplicado.py gsi_ebd/pages/admin.py
(vazio — nenhum delete no código novo)
```

Mais o empírico: as contagens e impressões digitais de `study`, `studyversion`,
`studyassignment`, `progress`, `userresponse` antes e depois da carga são **idênticas**
(§5 acima) e o conteúdo copiado veio de `StudyVersion` sem alterá-lo.

## 7. N-A — o que não foi verificado e por quê

| Caso | Por que é N-A | O que ficou provado no lugar |
|------|---------------|------------------------------|
| **H-02** | exige abrir `/aluno/licao` do Cap. 21 **em produção** (HTTP 200 + bloco "João 3:16" + 5 passagens). EVAL só tem o repositório local; não há banco local com o conteúdo real e o EVAL não acessa produção. | o caminho que serve a lição (`pages/lesson.py` → `states/aluno.py` → `services/study_service.py`) tem **diff vazio** contra `develop` e continua lendo `StudyVersion`. É argumento estrutural, **não** a verificação de H-02. |
| **H-03** | idem (4 citações e 10 questões no Cap. 21, em produção). | idem. Nenhum número de produção foi copiado ou estimado. |
| **H-04 (contagens de produção)** | 39 estudos · 31.102 versículos · 344.799 referências cruzadas só existem no banco de produção. | parte local executada e PASS: impressão digital idêntica antes×depois + inspeção do importador (só lê, nunca apaga). |
| **G-01** | é gate humano (intent §7): o ARQUITECT abre a tela e dá o aceite. EVAL não substitui. | preparado e verificável: aba **Estudo Aplicável** em `/admin` + item no menu lateral; `load_estudos_aplicados()` devolve estudo, 34 capítulos, `origem_label` (com adendo) e `sem origem declarada`; a página compila (`tests/test_paginas.py` inclui `admin_page`). |

## 8. Notas fora do contrato (não afetam o veredito)

1. **RNF de segurança (spec §3: "tela e importador exigem papel ADMIN").** Não existe caso no
   plano para ele, então não vira FAIL aqui — mas registro o que achei: a rota `/admin` está
   registrada com `on_load=[AuthState.check_auth, ...]` e `check_auth` só faz
   `AuthService.require_login(...)`, sem checagem de papel; `load_estudos_aplicados` também não
   tem guarda `is_admin`. A rota é **pré-existente** (arquivo fora do diff), então não é
   regressão desta DEM, mas o RNF diz "ADMIN" e o que existe é "logado". Encaminho ao PLANNER
   para decidir se é caso novo.
2. **Divergência 76 × 82 no plano/despacho** (H-01) — resolvida aritmeticamente (76 + 6 novos),
   mas o número do `intent §6` ficou desatualizado.
3. `datetime.utcnow()` aparece nas linhas novas (3 no caminho de produção) e emite
   `DeprecationWarning`; é o padrão vigente em outros 6 arquivos de `gsi_ebd`, portanto
   consistente com o repositório — registrado, não pontuado.

## 9. Veredito

```
hash: ac712dd73dad14a95b2352bc59bae927f9ec8c74 · estado_limpo: sim
C: PASS · N: PASS · F: PASS · H: PASS · G: N-A (ARQUITECT)
agregado: PASS
ressalva_de_cobertura: H-02, H-03 e as contagens de producao do H-04 sao N-A
  (producao nao acessivel ao EVAL) — a metade local do H esta provada
C=4/4 · N=6/6 · F=11/11 · H=2 executados (H-01, parte local do H-04) + 2 N-A (H-02, H-03)
# BLOCKED se o reset falhou, o hash nao existe ou a fixture falta — nenhum dos tres ocorreu
```
