# `perfil-do-projeto/` — O seu projeto entra aqui

Este é o **único lugar** onde o método toca a tecnologia. Todo o resto do pacote é neutro; aqui você declara o stack, a segurança, os ambientes e as convenções do **seu** projeto.

| Documento | Para quê |
|---|---|
| [perfil-do-projeto.template.md](perfil-do-projeto.template.md) | O formulário a preencher. Copie, responda cada campo e mantenha versionado. |
| [exemplo-agoracred.md](exemplo-agoracred.md) | Um perfil **preenchido** de verdade (projeto de origem), como referência. |

## Como usar

1. Copie `perfil-do-projeto.template.md` para a documentação do seu projeto (ex.: `perfil-do-projeto.md`).
2. Preencha cada campo. O que você não souber ainda, marque como pergunta aberta — vira uma ADR.
3. Use este perfil para completar os [arquivos de guarda](../arquivos-de-guarda/README.md) (`AGENTS.md`, `CLAUDE.md`, `CONVENTIONS.md`, `PROJECT_CONTEXT.md`) que vão para a raiz do repo.
4. Registre as escolhas de fundo (stack, branches, segredos) como **ADRs** (ver [`../05-decisoes-adr/como-usar-adr.md`](../05-decisoes-adr/como-usar-adr.md)).

> **Regra de portabilidade:** se você precisar citar uma tecnologia em qualquer documento de método, é sinal de que ela deveria estar **aqui**. Mantenha o método limpo.
