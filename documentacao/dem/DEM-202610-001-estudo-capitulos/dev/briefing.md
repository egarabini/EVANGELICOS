# Briefing — DEM-202610-001 (DEVS)

```
PARA: DEVS
DEM: DEM-202610-001-estudo-capitulos
GATE: TLC-List   ← produza o List e AGUARDE aprovação do ARQUITECT
```

## Caminhos absolutos

- intent: `C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-001-estudo-capitulos\planner\intent.md`
- prd: `C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-001-estudo-capitulos\planner\prd.md`
- spec: `C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-001-estudo-capitulos\planner\spec.md`
- design: `C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-001-estudo-capitulos\planner\design.md`
- plano de testes: `C:\Projetos\EM_ESTUDO\EVANGELICOS\documentacao\dem\DEM-202610-001-estudo-capitulos\planner\plano-testes.md`
- código: `C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD`
- guardas: `AGENTS.md` · `CONVENTIONS.md` · `PROJECT_CONTEXT.md` (na raiz do código)

## Contexto em uma linha

Hoje cada capítulo é um `Study` isolado. Esta DEM cria o **estudo aplicável** com capítulos
próprios e o **mapa de origem** para a obra, sem tocar na lição do aluno (RF08).

## Tarefas

| # | Tarefa | Arquivo |
|---|---|---|
| 1 | Modelos `Estudo`, `EstudoCapitulo`, `EstudoCapituloOrigem` + registro | `gsi_ebd/models/estudo.py`, `gsi_ebd/models/__init__.py` |
| 2 | Importador idempotente com `--apply`/`--autoteste` e funções puras | `gsi_ebd/scripts/importar_estudo_aplicado.py` |
| 3 | Testes das funções puras (ordem pelo título, fallback, idempotência) | `tests/test_estudo_aplicado.py` |
| 4 | Estado do admin (listas planas + rótulos montados em Python) | `gsi_ebd/states/admin.py` |
| 5 | Aba **Estudos** e item no menu | `gsi_ebd/pages/admin.py`, `gsi_ebd/components/sidebar.py` |
| 6 | Suíte completa + compilação das páginas | `pytest tests` |

## Restrições (não negociáveis)

- **Não tocar** em `pages/lesson.py`, `states/aluno.py`, `models/study.py`,
  `scripts/importar_obra.py` nem em nenhum serviço existente — esta DEM é paralela (RF08).
- **Não criar enum novo**: usar `StudyStatus.RASCUNHO` (`models/study.py`).
- **Nunca** concatenar `Var` com `+` no componente: montar o texto no estado (incidente de 16/10).
- **Nenhuma** escrita no corpus; **nenhum** comando de deploy.
- Sem `--apply` o importador **não grava nada**.
- Comentários **sem acento**, respondendo *por que*.

## Antes de codificar

Produza o **List** — arquivos a criar/modificar, riscos e ordem dos passos — e aguarde a
aprovação do ARQUITECT. Registre a `dev/jornada.md` a partir da Tarefa 1.
