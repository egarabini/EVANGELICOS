# Estrutura da DEM — ownership por pasta

> **A estrutura do processo é arquitetura.** O controle de "quem escreve o quê" não é textual — é **estrutural**: cada arquivo tem um dono único, garantido pela organização das pastas. Isso elimina a classe de erro em que um papel escreve o registro de outro.

## Regra única

Toda DEM — grande ou pequena — usa o **mesmo pacote de pastas**. Em DEMs pequenas, várias seções ficam enxutas ou "N/A": o arquivo existe, mas não vira burocracia.

```
DEM-AAAAMM-<tracker>-<seq>-<slug>/
├── README.md            ← índice da DEM (+ rollup de tempo/tokens)
├── changelog.md         ← resultado consolidado + veredito dos gates (PLANNER)
├── planner/             ← o PLANO (PLANNER): intent · prd · spec · design · plano-testes
├── dev/                 ← DEVS:   briefing.md (PLANNER) + jornada.md (DEVS)
├── eval/                ← EVAL:   jornada.md   (o briefing dele é o planner/plano-testes)
├── deploy/              ← DEPLOY: briefing.md (runbook, PLANNER) + jornada.md (DEPLOY)
├── vision/              ← VISION: briefing.md? + jornada.md   (só se há tela)
└── know/                ← KNOW:   jornada.md   (quando participa)
```

| Pasta | Dono | Conteúdo |
|---|---|---|
| `planner/` | PLANNER | `intent` · `prd` · `spec` · `design` · `plano-testes` (o plano) |
| `dev/` | DEVS | `briefing.md` (PLANNER) + `jornada.md` (DEVS) |
| `eval/` | EVAL | `jornada.md` (briefing = `planner/plano-testes`) |
| `deploy/` | DEPLOY | `briefing.md` (runbook, PLANNER) + `jornada.md` (DEPLOY) |
| `vision/`, `know/` | VISION / KNOW | idem — **só se o agente participou** |
| `changelog.md` (raiz) | PLANNER | resultados consolidados + veredito dos gates |

## Princípios estruturais

- **Pasta por agente que atua.** A **ausência** de uma pasta indica que o agente **não participou** (ex.: sem `vision/` = VISION N/A).
- **Dois arquivos de dono único** dentro da pasta de cada agente: `briefing.md` (escrito pelo **PLANNER** — o handoff/runbook) e `jornada.md` (escrita **pelo próprio agente**). O PLANNER **nunca** escreve a `jornada.md`.
- **PLANNER e ARQUITECT não têm pasta de diário.** O registro do PLANNER é a pasta `planner/` + o `changelog`; o controle de toda a DEM é dele.
- **Cada pasta tem seu `README.md`** (convenção do pacote).

## Nomenclatura

```
DEM-AAAAMM-<tracker>-<seq>-<slug-kebab>
    └ mês ┘ └ id(s) do seu rastreador ┘ └seq┘ └─ descrição curta ─┘
```

- `<tracker>` são os identificadores do(s) seu(s) sistema(s) de rastreio (ticket, work item). Defina o formato no [perfil do projeto](../perfil-do-projeto/perfil-do-projeto.template.md).
- `<seq>` é o número sequencial da DEM no projeto.
- A **branch** de feature espelha a pasta (ver [gitflow.md](gitflow.md)).

## Cartão de ponto e rollup (tempo + tokens)

`briefing.md` e `jornada.md` são **livros-razão vivos**: cada tarefa é uma entrada titulada com `Início`/`Término`. No topo, um cabeçalho de ponto:

```
Agente: <NOME> (<PAPEL>)
Início:  AAAA-MM-DD HH:MM   (1ª tarefa)
Término: AAAA-MM-DD HH:MM   (última tarefa)
SPAN: Xh Ym
Tempo ativo: Xh Ym          ← Σ das durações das tarefas (A MÉTRICA)
Tokens: in <N> / out <N>    (derivado de fonte real | "não medido")
```

Regras:

1. **A métrica é o `Tempo ativo` = Σ(término − início) das tarefas**, **não** o SPAN — o SPAN engloba o tempo de despacho do ARQUITECT (que trabalha em vários projetos), e esse gap **não conta para ninguém**.
2. Cada agente carimba o **próprio** ponto no **próprio** arquivo: `briefing.md` mede o **PLANNER** (overhead de orquestração); `jornada.md` mede a **execução do agente** (o custo que justifica melhorias).
3. Tarefas do `briefing.md` e da `jornada.md` se **espelham** pelo título (`Tarefa N ↔ Tarefa N`), incluindo entradas de erro/correção.
4. Formato **ISO** (`AAAA-MM-DD HH:MM`) para agregação futura.
5. **Rollup por DEM:** o `README.md` da DEM traz um quadro derivado somando `Tempo ativo` e `Tokens` por agente (fonte = os cabeçalhos das jornadas; consolidado pelo PLANNER no fechamento).

Mecânica completa da jornada em [`../templates/jornada.md`](../templates/jornada.md).

## Definition of Ready / Done por fase

| Para entrar em… | Precisa ter… |
|---|---|
| **Intent** | problema em linguagem crua do ARQUITECT |
| **Spec** | `intent.md` `signed`; `prd.md` sem ambiguidade pendente |
| **Design** | `spec.md` aprovada, requisitos verificáveis, contratos se houver |
| **Implementação** | documentos anteriores aprovados; ADRs relevantes citadas |
| **Fechamento** | testes verdes cobrindo os requisitos; hash do commit; checklist de regressão arquitetural OK |

**Done de fase** = documento completo (sem `[placeholder]`) + ARQUITECT aprovou + conflitos com ADRs sinalizados + itens em aberto registrados.

## Um painel de DEMs (recomendado)

Mantenha um `_dashboard.md` (ou equivalente) listando todas as DEMs, seu estado, dependências e a última release. É a **fonte** do que está em andamento — não hardcode a "DEM atual" nos arquivos de guarda, que envelhecem a cada ciclo.
