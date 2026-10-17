# Plano de testes — DEM-202610-001 / estudo-capitulos

status: draft
owner: PLANNER
executor: EVAL
intent: `planner/intent.md` — signed em 2026-10-16
spec: `planner/spec.md` — aprovada em 2026-10-16
design: `planner/design.md`
signed_by: ARQUITECT
signed_at:

## Âncora

- **branch:** `feature/DEM-202610-001-estudo-capitulos`
- **hash_alvo:** `<preenchido no despacho PARA: EVAL — o hash que existe no git>`
- **ambiente:** `local-autoteste` (SQLite descartável) + **produção somente leitura**
- **dados:** o autoteste usa SQLite novo a cada execução; a produção só é **lida**
  (HTTP 200 e conteúdo da lição), nunca escrita.

## Estado limpo (obrigatório)

Antes de QUALQUER caso:

- [ ] o SQLite do autoteste é apagado no início de cada execução (o script faz)
- [ ] nenhum resíduo de rodada anterior (arquivo temporário inexistente antes do reset)
- [ ] comando de reset rodado e a saída colada na jornada

```
cd ESTUDOS_BIBLICOS/GSI_EBD
.venv/Scripts/python -m gsi_ebd.scripts.importar_estudo_aplicado --apply --autoteste
```

Se o reset falhar → EVAL **não testa**. Veredito: `BLOCKED` (não `FAIL`).

## Rastreio

| ID | Tipo | Origem | Critério (1 linha) | Automatizável | Porteiro |
|----|------|--------|--------------------|---------------|----------|
| F-01 | funcional | spec RF01 | Existe Estudo ligado à obra, com título/descrição/doutrina/status | sim | EVAL |
| F-02 | funcional | spec RF02 | Capítulos com ordem única e contínua no estudo | sim | EVAL |
| F-03 | funcional | spec RF03 | Origem por capítulo (obra + adendo opcional) e origem ausente permitida | sim | EVAL |
| F-04 | funcional | spec RF04 | Um capítulo da obra alimenta vários do estudo (mapa N:N) | sim | EVAL |
| F-05 | funcional | spec RF05 | Carga cria 1 estudo com 34 capítulos e 34 origens | sim | EVAL |
| F-06 | funcional | spec RF06 | Todo capítulo criado nasce `rascunho` | sim | EVAL |
| F-07 | funcional | spec RF07 | Tela lista estudo, capítulos e origem, somente leitura | sim | EVAL |
| F-08 | funcional | spec RF08 | A lição continua servida por `StudyVersion` | sim | EVAL |
| F-09 | funcional | spec RF09 | `Study`/`StudyVersion` intactos após a carga | sim | EVAL |
| F-10 | funcional | spec RF10 | Capítulo sem origem exibe "sem origem declarada" | sim | EVAL |
| F-11 | funcional | spec RF05 + design §4 | **Obra ausente no banco → importador ABORTA sem criar nada** | sim | EVAL |
| H-01 | health | intent §6.H-01 | **76** testes passando (`pytest tests`) | sim | EVAL |
| H-02 | health | intent §6.H-02 | Lição do Cap. 21 com "João 3:16" e 5 passagens relacionadas | sim | EVAL |
| H-03 | health | intent §6.H-03 | Cap. 21 com **4 citações e 10 questões** | sim | EVAL |
| H-04 | health | intent §6.H-04 | **39** estudos · **31.102** versículos · **344.799** referências | sim | EVAL |
| C-01 | constraint | intent §5 (ADR-002) | O corpus **não** é escrito nesta DEM | sim | EVAL |
| C-02 | constraint | intent §5 (ADR-011) | Nenhum capítulo criado fica disponível ao aluno | sim | EVAL |
| C-03 | constraint | intent §5 (ADR-010) | O agente **não** executa deploy (sem `subir.sh`, sem SSH) | sim | EVAL |
| C-04 | constraint | design §4 · intent §5 | `lesson.py`, `aluno.py` e `study.py` com **`git diff` VAZIO** | sim | EVAL |
| N-01 | non-goal | intent §4 Out | Fluxo da Ação 1 (agendamento/ressalvas) **não existe** | sim | EVAL |
| N-02 | non-goal | intent §4 Out | Bibliotecas, níveis e treinamento **não existem** | sim | EVAL |
| N-03 | non-goal | intent §4 Out | Liberação/classificação de alunos **não existe** | sim | EVAL |
| N-04 | non-goal | intent §4 Out | A lição **não foi repontada** (segue em `StudyVersion`) | sim | EVAL |
| N-05 | non-goal | intent §8.1 | A tela **não** cria nem edita capítulo | sim | EVAL |
| N-06 | non-goal | intent §8.2 | Os 5 estudos de exemplo **não** viraram estudo | sim | EVAL |
| G-01 | gate humano | intent §7 | Aceite visual da tela pelo ARQUITECT | não | ARQUITECT |

**0 casos órfãos · 0 capacidades da spec sem `F-*` · todo §6 do intent virou `H-*`.**

## Casos

### F-05 — a carga (o caso central)
- origem: spec RF05
- precondição: estado limpo; banco com a obra importada (1 obra, 34 capítulos)
- passos: 1. rodar o importador com `--apply --autoteste` 2. conferir contagens
- esperado: 1 estudo · 34 capítulos · 34 origens · 0 fora de rascunho
- evidência: saída do importador + query no SQLite do autoteste
- FAIL se: contagem ≠ 34, ou algum capítulo fora de rascunho

### F-03 / F-04 — mapa de origem
- origem: spec RF03, RF04
- passos: 1. inserir no autoteste um segundo capítulo do estudo ligado ao mesmo capítulo
  da obra 2. inserir um capítulo sem origem 3. ler a tela
- esperado: o capítulo da obra lista 2 origens; o capítulo sem origem mostra
  "sem origem declarada"; nenhum erro
- evidência: saída da query + captura da tela
- FAIL se: erro, contagem errada ou texto ausente

### F-09 / H-04 — nada existente é perdido
- origem: spec RF09 · intent §6.H-04
- passos: 1. contar antes (`study`, `studyversion`, `studyassignment`, `progress`,
  `userresponse`) 2. rodar a carga 3. contar depois
- esperado: contagens idênticas; versículos e referências inalterados
- evidência: as duas contagens coladas
- FAIL se: qualquer contagem mudar

### F-06 / C-02 — nada nasce disponível
- origem: spec RF06 · intent §5 · ADR-011
- passos: 1. rodar a carga 2. procurar qualquer capítulo com status ≠ `rascunho`
  3. conferir que o aluno não vê nenhum estudo novo
- esperado: 0 capítulos fora de rascunho; listagem do aluno inalterada
- evidência: query + tela do aluno
- FAIL se: existir capítulo disponível

### H-02 / H-03 / F-08 — a lição não regride
- origem: intent §6 · spec RF08
- passos: 1. abrir `/aluno/licao` do Cap. 21 em produção 2. conferir Escritura e
  passagens relacionadas 3. conferir citações/questões
- esperado: "João 3:16" presente, 5 passagens, 4 citações, 10 questões
- evidência: captura de tela + resposta HTTP 200
- FAIL se: bloco ausente, contagem diferente ou erro

### F-11 — pré-condição: obra ausente aborta
- origem: spec RF05 · design §4
- precondição: SQLite do autoteste **sem** a obra (não rodar antes o importador da obra)
- passos: 1. rodar o importador com `--apply --autoteste` 2. conferir contagens
- esperado: **mensagem de erro clara** e **0 estudos, 0 capítulos, 0 origens** criados
- evidência: saída do comando + contagens consultadas no SQLite
- FAIL se: criar qualquer registro sem a obra, ou falhar em silêncio sem mensagem

### N-01..N-06 — non-goals (provam AUSÊNCIA)
- passos: busca no código e nas rotas
- esperado: não existe rota/tabela/tela de agendamento, biblioteca, níveis, liberação de
  aluno ou edição de capítulo; `pages/lesson.py` e `states/aluno.py` **sem** referência a
  `EstudoCapitulo`
- evidência: `grep` no código + schema do banco
- FAIL se: qualquer item aparecer — significa que a spec inflou

### C-01 / C-03 / C-04 — constraints
- C-01: `grep` por escrita no corpus / ausência de caminho de escrita para `/conteudo`
- C-03: ausência de execução de `subir.sh`/SSH na jornada
- C-04: `git diff --stat develop...HEAD -- gsi_ebd/pages/lesson.py gsi_ebd/states/aluno.py gsi_ebd/models/study.py`
  deve sair **vazio** (nenhuma linha) — prova objetiva de que a lição não foi tocada
- FAIL se: houver qualquer escrita no corpus, comando de deploy registrado, ou uma linha de
  diff nos três arquivos intocáveis

### G-01 — aceite humano (não é FAIL de EVAL)
- EVAL registra **N-A** e o que foi preparado; o ARQUITECT abre a tela e dá o aceite.

## Ordem de execução

1. Reset + prova de estado limpo (log no disco)
2. `C-*` — se falhar, pare
3. `N-*` — provas de ausência
4. `F-*` — capacidades
5. `H-*` — health, no mesmo hash
6. `G-*` — anotar N-A

## Veredito (preenche o EVAL, não o PLANNER)

```
hash: <40 chars> · estado_limpo: sim|não
C: PASS|FAIL|N-A · N: PASS|FAIL · F: PASS|FAIL · H: PASS|FAIL · G: N-A (ARQUITECT)
agregado: PASS só se C+N+F+H = PASS e estado_limpo = sim
# BLOCKED se o reset falhou, o hash não existe ou a fixture falta
```

## Fora deste plano

- UI/UX, layout, viewport → **VISION** (o ARQUITECT neste projeto).
- Deploy, backup, tag → **DEPLOY** (GitHub Actions).
- "Ficou melhor que X" → não é caso.
- Correção de código → **DEVS**, via PLANNER, depois de FAIL triado.

## Despacho (PARA: EVAL)

```
PARA: EVAL
DEM: DEM-202610-001
GATE: eval
intent: C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-001-estudo-capitulos\planner\intent.md
spec:   C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-001-estudo-capitulos\planner\spec.md
plano:  C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-001-estudo-capitulos\planner\plano-testes.md
código: C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD
        branch: feature/DEM-202610-001-estudo-capitulos   hash: <40 chars>
NÃO LER: dev/jornada.md
NÃO FAZER: corrigir código, mudar critério, validar estado residual
```
