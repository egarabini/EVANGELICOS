# `arquivos-de-guarda/` — Manifestos para a raiz do repo

Copie estes arquivos para a **raiz do repositório de código** do novo projeto. Todo agente de código os lê antes de escrever (guard-rail estrutural: [ADR-005 equivalente](../02-guard-rails/guard-rails-e-tlc.md)).

| Arquivo | Lido por | O que faz |
|---|---|---|
| [AGENTS.md](AGENTS.md) | agentes de código (nativo) | Manifesto do DEVS: guard-rails, TLC, restrições, estrutura da DEM. |
| [CLAUDE.md](CLAUDE.md) | agentes Claude | Comportamento e papéis; aponta para os demais. |
| [CONVENTIONS.md](CONVENTIONS.md) | todos | Padrões de código/teste/segurança, commits, DoR/DoD. |

## Como adotar

1. Copie os três para a raiz do repo (e crie um `PROJECT_CONTEXT.md` com o stack + "o que NÃO mudar").
2. Substitua todo `[preencher: …]` com os valores do [perfil do projeto](../perfil-do-projeto/perfil-do-projeto.template.md).
3. Não duplique conteúdo entre eles: cada um aponta para a fonte única (o método vive em `documentacao/metodo/`, o técnico no perfil/`PROJECT_CONTEXT.md`).

> Estes arquivos são **behaviorais e curtos** de propósito. O detalhe do processo mora no pacote `metodo/`; aqui fica só o que o agente precisa no início de cada sessão.
