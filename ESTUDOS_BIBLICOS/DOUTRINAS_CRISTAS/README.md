# Teologia Sistemática — Wayne Grudem

> **Manual de Doutrinas Cristãs | Teologia ao Alcance de Todos**

---

## ⚠️ Nota sobre Arquitetura

Este projeto segue a arquitetura centralizada do **TEMPLATE_ESTUDO**:

- **TEMPLATE_ESTUDO** (`f:/ESTUDOS_BIBLICOS/TEMPLATE_ESTUDO/`) — Fonte de verdade, consultado como referência
- **DOUTRINAS_CRISTAS** — Este projeto contém apenas o conteúdo específico do estudo

---

## Sobre a Obra

Este TEMPLATE_ESTUDO é um framework completo para organizar estudos bíblicos e teológicos, desenvolvido a partir da experiência de criação do projeto *Teologia Sistemática — Wayne Grudem*. Ele fornece uma estrutura padronizada para:

1. **Organização de conteúdo** — Capítulos, textos originais, traduções e revisões
2. **Produção visual** — Slides animados via Mira (D3.js)
3. **Aprendizado dirigido** — Planos de estudo estruturados
4. **Documentação** — Referências, vídeos, imagens e materiais de apoio
5. **Trabalho com IAs** — Arquivos de configuração para direcionar agentes de IA

---

## Data de Criação

**17 de Junho de 2026**

---

## Estrutura do Template

```
TEMPLATE_ESTUDO/
│
├── README.md                          ← Este arquivo — resumo do estudo
├── CLAUDE.md                          ← Configuração para agente Claude
├── AGENTS.md                          ← Configuração para outros agentes
├── CONVENTIONS.md                     ← Convenções de formatação
├── .cursorrules                       ← Regras para o Cursor (copilot)
├── mira.config.json                   ← Configuração do Mira (slides)
│
├── docs/                              ← Documentação do projeto
│   ├── diversos/                      ← Documentos gerais
│   ├── referencias/                   ← Referências bibliográficas
│   ├── videos/                        ← Links e metadados de vídeos
│   ├── imagens/                       ← Figuras e diagramas
│   └── audios/                        ← Áudios de apoio
│
├── estudo/                            ← Conteúdo principal do estudo
│   ├── capitulo_01/                   ← Capítulo 1
│   │   ├── 01_Titulo_EN.md            ← Original em inglês (intocado)
│   │   ├── 01_Titulo_PT.md            ← Tradução preservada
│   │   └── 01_Titulo_PT_v1.md         ← Versão corrigida e formatada
│   ├── capitulo_02/                   ← Capítulo 2
│   └── ...                            ← Demais capítulos
│
├── decks/                             ← Slides animados do Mira
│   ├── 01-capitulo-1/                 ← Deck do capítulo 1
│   │   ├── index.html                 ← Apresentação final
│   │   ├── briefing.md                ← Briefing inicial
│   │   ├── plano-refinado.md          ← Plano de slides
│   │   ├── validacao.md               ← Validação do deck
│   │   └── assets/                    ← Imagens e recursos
│   └── 02-capitulo-2/                 ← Deck do capítulo 2
│
├── estudo_dirigido/                   ← Planos de estudo dirigido
│   ├── README.md                      ← Guia do estudante
│   ├── _template_plano-de-estudo.md   ← Template de plano
│   ├── capitulo_01/                   ← Plano do capítulo 1
│   │   └── plano-de-estudo.md         ← Plano completo
│   └── capitulo_02/                   ← Plano do capítulo 2
│
├── mira-templates/                    ← Templates do Mira
│   ├── themes/                         ← Temas visuais
│   │   ├── mira-dark.css              ← Tema principal
│   │   ├── corporate-blue.css
│   │   └── light-minimal.css
│   └── slides/                        ← Templates de slides
│       ├── card_capa.html
│       ├── card_encerramento.html
│       └── ...
│
└── plano-template-estudo/             ← Templates de planejamento
    ├── template_capitulo.md           ← Template de capítulo
    ├── template_slide.md              ← Template de slide
    └── template_reflexao.md           ← Template de reflexão
```

---

## Como Usar Este Template

### 1. Criar um novo estudo

Para iniciar um novo estudo baseado neste template:

1. **Copie a pasta TEMPLATE_ESTUDO** inteira
2. **Renomeie** para o nome do seu estudo (ex: `Teologia_Biblica`, `Historia_da_Igreja`, etc.)
3. **Edite o README.md** principal com as informações do seu estudo
4. **Personalize o CLAUDE.md** e **AGENTS.md** conforme necessário
5. **Ajuste o mira.config.json** com o tema e configurações desejadas

### 2. Adicionar conteúdo

- **estudo/**: Adicione os capítulos do estudo nas subpastas `capitulo_XX/`
- **docs/**: Organize documentação, referências e mídias
- **decks/**: Use o Mira para criar slides animados

### 3. Criar slides com Mira

Siga o pipeline padrão do Mira:

1. `/mira-extract` — Extrair contexto do conteúdo
2. `/mira-planner` — Planejar a estrutura dos slides
3. `/mira-copywriter` — Refinar os textos
4. `/mira-builder` + `/mira-animator` — Construir slides animados
5. `/mira-validator` — Validar o resultado

### 4. Criar plano de estudo dirigido

Use o template `_template_plano-de-estudo.md` para criar planos estruturados em 6 etapas.

---

## Convenções de Nomenclatura

### Capítulos

- `capitulo_XX/` — Pasta do capítulo (XX = número com zero à esquerda)
- `XX_Titulo_EN.md` — Original em inglês
- `XX_Titulo_PT.md` — Tradução preservada
- `XX_Titulo_PT_v1.md` — Versão corrigida

### Decks

- `xx-nome-do-capitulo/` — Pasta do deck (kebab-case, número com zero)
- `index.html` — Apresentação final
- `briefing.md` — Briefing inicial
- `plano-refinado.md` — Plano de slides

### Estudo Dirigido

- `capitulo_XX/` — Pasta do capítulo
- `plano-de-estudo.md` — Plano completo do capítulo

---

## Arquivos de Configuração para IAs

### CLAUDE.md

Configura o agente Claude Code com:
- Instruções do projeto
- Regras de formatação
- Convenções de nomenclatura
- Estrutura de pastas

### AGENTS.md

Configura outros agentes (Gemini, etc.) com informações similares.

### .cursorrules

Regras para o editor Cursor (GitHub Copilot) auxiliar na edição.

### CONVENTIONS.md

Documenta todas as convenções usadas no projeto para manter consistência.

---

## Integração com Mira

Este template já vem configurado para usar o Mira — sistema de criação de slides animados com D3.js.

### mira.config.json

Arquivo de configuração do Mira que define:
- **sources[]**: Fontes de conteúdo vinculadas
- **defaultTheme**: Tema visual padrão (ex: `mira-dark`)
- **decks[]**: Decks criados

### Temas disponíveis

- `mira-dark` — Tema principal (glassmorphism escuro)
- `corporate-blue` — Azul corporativo
- `light-minimal` — Claro minimalista
- `neon-emerald` — Neon verde

---

## Fluxo de Trabalho Recomendado

```
1. Definir tema e escopo do estudo
2. Coletar materiais (livros, PDFs, vídeos)
3. Organizar em estudo/capitulo_XX/
4. Criar documentação em docs/
5. Gerar slides com Mira (decks/)
6. Criar plano de estudo dirigido (estudo_dirigido/)
7. Revisar e refinar
```

---

## Referências

Este template foi desenvolvido a partir da experiência com:

- **Teologia Sistemática** — Wayne Grudem
- **Mira** — Sistema de criação de slides animados
- **Claude Code** — Agente de IA para desenvolvimento

---

## Notas

- Este é um **template inicial** — adapte conforme suas necessidades
- Mantenha a **consistência de nomenclatura** em todos os projetos
- Documente suas **decisões de design** em docs/diversos/
- Use os **planos de estudo dirigido** para maximizar o aprendizado

---

> *"Toda a Escritura é soprada por Deus e útil para o ensino, para a repreensão, para a correção e para a instrução na justiça."* — 2 Timóteo 3.16

---

**Versão do Template:** 1.0
**Data de Criação:** 17 de Junho de 2026
**Baseado em:** Grudem_Doutrina_Biblica
