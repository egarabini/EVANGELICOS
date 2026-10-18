# Changelog — DEM-202610-001 / estudo-capitulos

## Veredito dos gates

| Gate | Quem assina | Resultado | Evidência |
|---|---|---|---|
| **intent** | ARQUITECT | ✅ signed 2026-10-16 | `planner/intent.md` §8 — 5 decisões fechadas |
| **spec** | ARQUITECT | ✅ aprovada 2026-10-16 | `planner/spec.md` — 10 RF, 6 CA |
| **TLC-List** | ARQUITECT | ✅ aprovado 2026-10-16 | `dev/jornada.md` — arquivos, riscos e ordem |
| **eval** | EVAL (cego) | ✅ **PASS** — hash `ac712dd`, estado limpo | `eval/jornada.md` — C 4/4 · N 6/6 · F 11/11 · H PASS |
| **vision / aceite de entrega** | ARQUITECT | ✅ **aceito 2026-10-17** | conferência da aba **Estudo Aplicável** em `/admin` |
| **aceite de release** | ARQUITECT | ⏳ **pendente** | depende do CI (Fase A3) — bloqueado no `gh` |

## Resultado

- **2 commits** em `feature/DEM-202610-001-estudo-capitulos` (publicada):
  `6defd39` `fix(obra)` e `ac712dd` `feat(estudo)`.
- **8 arquivos, +714/−2** — 3 novos (modelo, importador, testes), 4 modificados
  (registro, estado, página, sidebar) e 1 linha de correção no importador da obra.
- **82 testes** verdes (76 + 6).
- Autoteste do importador: **PASS** (10 checagens), incluindo F-11 (aborta sem a obra)
  e idempotência.
- **C-04 provado**: `git diff` vazio em `lesson.py`, `aluno.py` e `study.py`.

## O que NÃO foi feito, e por quê

| Item | Motivo |
|---|---|
| Publicação e merge do PR | **Bloqueados**: sem `gh` autenticado não há PR, e sem CI (ADR-010) não há publicação |
| Rodar o importador em produção | É o **ARQUITECT**, após `pg_dump` e após o merge (design §4) |
| H-02/H-03/H-04 em produção | Só fazem sentido **após** o deploy; o EVAL os marcou N-A com justificativa |
| Guarda de papel em `/admin` (RNF de segurança) | Virou **DEM-202610-002** — fora do escopo desta DEM |

## Ganhos colaterais

- **`fix(obra)`** — defeito de re-execução no importador da obra, encontrado no caminho:
  a segunda execução estourava `AttributeError`. Sem isso, o ARQUITECT travaria ao rodar
  de novo depois de corrigir uma tradução.
- **EVAL cego inaugurado** — o primeiro da história do projeto, com fixture própria, CLI
  real e sha256 das tabelas. A verificação deixou de ser relato.
- **Scripts de prova versionados** em `eval/` — a verificação fica reproduzível.

## Merge em `develop` e CI (2026-10-18)

O **PR #1** foi mergeado pelo ARQUITECT em `develop` — commit de merge **`ba165d9`**,
00:56 UTC — e a **CI rodou no push do merge e passou** (run `39083755739`, 82 testes, 50 s).
A branch `feature/DEM-202610-001-estudo-capitulos` foi removida depois do merge.

O merge aconteceu **antes** de a proteção de branch existir: o portão nasceu depois. A CI
validou o resultado, mas o registro é honesto — este foi o último merge sem check obrigatório.

**Continua pendente:** aceite de **release** (depende da Etapa 2 do CD, DEM-004) e a execução
do importador em produção (tarefa do ARQUITECT, após `pg_dump`).

## Pendências que saem desta DEM

1. **DEM-202610-002** — guarda de papel nas rotas `/admin` (segurança; qualquer usuário
   logado alcança a área administrativa).
2. **Fase A3 (CI/CD)** — bloqueia publicação e a última perna do GitFlow.
3. **Importador em produção** — tarefa do ARQUITECT, depois do merge.
4. **H-02/H-03/H-04** — verificação em produção, no momento do deploy.
5. **Mover `Diagnostico/*.md`** para `documentacao/historico/` — adiado porque há
   comentários de código apontando para eles.
