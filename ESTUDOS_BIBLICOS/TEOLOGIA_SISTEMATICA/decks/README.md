# Decks — Slides Animados do Mira

> **Apresentações animadas criadas com Mira (D3.js)**

---

## Sobre Esta Pasta

Esta pasta contém os decks (apresentações) de slides animados criados com o sistema Mira para cada capítulo da Teologia Sistemática.

---

## Estrutura

```
decks/
├── 01-introducao-a-teologia-sistematica/
│   ├── index.html           ← Apresentação final
│   ├── briefing.md          ← Briefing inicial
│   ├── plano-refinado.md    ← Plano de slides refinado
│   ├── validacao.md         ← Validação do deck
│   └── assets/              ← Imagens e recursos
├── 02-a-autoridade-e-a-inerrancia-da-biblia/
└── ...
```

---

## Como Criar um Novo Deck

Use o pipeline padrão do Mira:

```
1. /mira-new         → Criar estrutura do deck
2. /mira-extract     → Extrair conteúdo do capítulo
3. /mira-planner     → Planejar estrutura dos slides
4. /mira-copywriter  → Refinar textos
5. /mira-builder     → Construir slides HTML
6. /mira-animator    → Adicionar animações D3.js
7. /mira-validator   → Validar resultado
```

---

## Nomenclatura

- **Formato da pasta**: `xx-nome-do-capitulo/` (kebab-case)
- **Exemplo**: `06-a-trindade/`, `22-a-justificacao-e-a-adocao/`

---

## Regras de Animação

- **TODA animação** deve entrar com coreografia
- **DEPOIS** continuar em loop interno perpétuo
- Animação estática é **PROIBIDA**
- Use CSS variables do tema: `var(--mira-primary)`, etc.
- Tema padrão: `mira-dark`

---

> *"A visão amplia o entendimento."*
