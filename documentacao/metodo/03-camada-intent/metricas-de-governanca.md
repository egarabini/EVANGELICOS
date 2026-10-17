# Métricas de governança — o gate INTENT está funcionando?

> **Isto NÃO vai dentro de nenhum intent.** São métricas da **prática** (governança), não do produto. Vivem no painel de DEMs / rollup por DEM. Instrumente só o que **git + a regra de ouro 9** já dão. Nada de survey.

## Três coisas diferentes — não confundir

A camada INTENT lida com três medições distintas. Misturá-las infla o `intent.md` e faz o PLANNER "medir" o que deveria só **recusar**:

1. **Invariantes do produto** → §6 do intent (health metrics). O que **não pode piorar**. Ver [camada-intent.md](camada-intent.md).
2. **Saúde do artefato** → checklist do PLANNER no `GATE: intent`. O intent está **assinável**? Ver [camada-intent.md](camada-intent.md).
3. **Saúde da prática** → **este documento**. O **gate** está sendo respeitado ao longo das DEMs?

## Métricas de prática

Alvos valem **depois da DEM piloto**.

| Métrica | Como medir | Alvo | Doença que denuncia |
|---|---|---|---|
| **Intent-before-spec** | % DEMs com commit `signed` de `intent.md` **antes** do 1º commit de spec | 100% | PLANNER pulou o gate |
| **Churn pós-spec** | commits em `intent.md` **depois** da spec signed | ~0 (1 = descoberta honesta → `superseded`) | intent era spec; ou a spec reabriu o porquê no silêncio |
| **Kill rate de non-goal** | itens do §4 Out que viraram tarefa DEVS | 0 | cerca de escopo furou |
| **Briefing cita intent** | % despachos com caminho absoluto do intent | 100% | regra 9 falhou no transporte |
| **Constraint → FAIL** | FAILs do EVAL cujo critério está no §5 (não numa capacidade) | **>0 é bom** | 0 eterno = §5 é enfeite |
| **Fechamento ilegal** | perguntas do §8 respondidas por PLANNER/DEVS | 0 | fronteira de papel furada |
| **Drift de outcome** | PRs cujo parecer do PLANNER cita "melhoria" fora do §2 | 0 | DEVS/VISION otimizando o prior, não o intent |
| **Tempo até signed** (leading) | 1ª conversa → commit `signed` | cai ao longo das DEMs | ritual demais, ou ARQUITECT ausente |
| **Survival draft→signed** | intents que morrem em `draft` | **não 100%** (morte é filtro) | 100% signed = ARQUITECT assina tudo; ~0% = template inútil |

## Ordem de adoção (não meça tudo de uma vez)

- **Na DEM piloto:** só as **4 primeiras** (intent-before-spec, churn, kill rate, briefing cita).
- **Depois de 3 DEMs:** o restante. Antes disso, você mede o **rito** em vez do **efeito**.

## O que NÃO medir no início

- "Qualidade percebida do intent" (gosto).
- Tokens do PLANNER na sessão de intent (barato demais; o custo está em DEVS/DEPLOY).
- Número de health metrics por arquivo (vira meta de preencher o §6).

## Dois números que vão no cabeçalho do intent

Estes **sim** ficam no artefato, no cabeçalho, colados pelo PLANNER:

- `open_questions_open` — tem de ser **0** no `signed` (ou explicitamente aceitas como risco pelo ARQUITECT).
- `spec_citations` — depois da spec, **100%** das capacidades apontam para §2 / §4 Out / §5. Capacidade órfã = spec inflou.
