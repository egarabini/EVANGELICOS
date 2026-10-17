# `templates/` — Modelos copiáveis

Copie estes arquivos para dentro da pasta de cada DEM. Todos são **neutros** — nenhum cita stack; o específico do seu projeto vem do [perfil](../perfil-do-projeto/perfil-do-projeto.template.md).

| Template | Vira, na DEM | Dono | Quando |
|---|---|---|---|
| [intent.md](intent.md) | `planner/intent.md` | PLANNER escreve / ARQUITECT assina | **Antes** de tudo |
| [prd.md](prd.md) | `planner/prd.md` | PLANNER | Após intent `signed` |
| [spec.md](spec.md) | `planner/spec.md` | PLANNER | Após o PRD |
| [design.md](design.md) | `planner/design.md` | PLANNER | Após a spec |
| [plano-testes.md](plano-testes.md) | `planner/plano-testes.md` | PLANNER escreve / EVAL executa | Ao fechar a spec |
| [briefing.md](briefing.md) | `<agente>/briefing.md` | PLANNER | No handoff de cada agente |
| [jornada.md](jornada.md) | `<agente>/jornada.md` | o próprio agente | Durante a execução (vivo) |
| [changelog.md](changelog.md) | `changelog.md` (raiz da DEM) | PLANNER | No fechamento |
| [README-dem.md](README-dem.md) | `README.md` (raiz da DEM) | PLANNER | Ao abrir a DEM |

## Regras

- **Um `intent.md` por DEM.** Curto (≤ 1 página). Sem stack.
- O `plano-testes.md` só é aceito se **cada caso rastreia** a uma origem: `F-*`→capacidade da spec, `H-*`→§6 do intent, `C-*`→§5, `N-*`→§4 Out, `G-*`→gate humano.
- **Nunca apague seções** de um template: se não se aplica, escreva "N/A" e o motivo.
- Cada arquivo tem **um dono único** (ver [estrutura-da-dem.md](../04-estrutura-dem/estrutura-da-dem.md)).
