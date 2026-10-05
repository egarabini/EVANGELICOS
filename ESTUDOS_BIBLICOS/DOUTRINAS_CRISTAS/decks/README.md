# decks/ — Slides Animados do Mira

> **Apresentações HTML animadas com D3.js geradas pelo Mira**

---

## Estrutura da Pasta

```
decks/
├── 01-introducao-teologia-sistematica/    ← Deck do capítulo 1
│   ├── index.html                             ← Apresentação final
│   ├── briefing.md                            ← Briefing inicial
│   ├── plano-refinado.md                      ← Plano de slides
│   ├── validacao.md                           ← Validação do deck
│   └── assets/                                ← Imagens e recursos
├── 02-autoridade-inerrancia-biblia/      ← Deck do capítulo 2
└── README.md                              ← Este arquivo
```

---

## Pipeline do Mira

Para criar slides de um capítulo, siga o pipeline padrão:

```
1. /mira-extract      → Extrair contexto do capítulo
2. /mira-planner      → Planejar estrutura dos slides
3. /mira-copywriter   → Refinar textos dos slides
4. /mira-builder      → Construir slides HTML
5. /mira-animator     → Adicionar animações D3.js
6. /mira-validator    → Validar slides gerados
```

---

## Regras de Animação

### Regra Zero

- **TODA animação** deve entrar com coreografia
- **DEPOIS** continuar em loop interno perpétuo
- Animação estática é **PROIBIDA**

### CSS Variables

Use SEMPRE variáveis do tema, nunca cores hardcoded:

```css
var(--mira-primary)      /* Laranja primário */
var(--mira-secondary)    /* Azul secundário */
var(--mira-accent)       /* Verde de destaque */
var(--mira-bg-primary)   /* Fundo principal */
var(--mira-bg-card)     /* Fundo dos cards */
var(--mira-text-primary) /* Texto principal */
```

### Tema Padrão

O tema padrão é `mira-dark`. Outros temas disponíveis:

- `corporate-blue` — Azul corporativo
- `light-minimal` — Claro minimalista
- `neon-emerald` — Neon verde

---

## Estrutura de um Deck

### Pasta do Deck

```bash
# Criar pasta do deck
mkdir decks/xx-nome-do-capitulo

# Criar arquivos
touch decks/xx-nome-do-capitulo/briefing.md
touch decks/xx-nome-do-capitulo/plano-refinado.md
touch decks/xx-nome-do-capitulo/validacao.md

# Criar pasta de assets
mkdir decks/xx-nome-do-capitulo/assets
```

### Arquivo index.html

O arquivo `index.html` é a apresentação final. Ele deve:

- Ter todos os slides embutidos
- Ser navegável por scroll ou setas
- Ter animações com loop interno
- Usar CSS variables do tema
- Funcionar por `file://` (sem servidor)

---

## Como Criar Novo Deck

### Método 1: Usando /mira-new

```bash
# Invocar a skill
/mira-new

# Seguir as instruções:
# - Nome do tema
# - Template do deck
# - Tema base
# - Cor principal
# - Referências
```

### Método 2: Manualmente

```bash
# 1. Criar pasta
mkdir decks/xx-nome-do-capitulo

# 2. Criar briefing.md
# Preencher com o contexto do capítulo

# 3. Criar plano-refinado.md
# Usar /mira-planner para gerar plano

# 4. Criar index.html
# Usar /mira-builder + /mira-animator

# 5. Validar
# Usar /mira-validator
```

---

## Convenções de Nomenclatura

### Pastas de Decks

- **Formato**: `xx-nome-do-capitulo/` (kebab-case)
- **Exemplo**: `01-introducao-teologia-sistematica/`
- **Regra**: Número com zero à esquerda, seguido de hífen e nome em kebab-case

### Arquivos

| Arquivo | Propósito |
|---------|-----------|
| `index.html` | Apresentação final |
| `briefing.md` | Briefing inicial |
| `plano-refinado.md` | Plano de slides |
| `validacao.md` | Validação |

---

## Skills do Mira Disponíveis

| Skill | Propósito |
|-------|-----------|
| `/mira-new` | Criar novo deck |
| `/mira-extract` | Extrair contexto |
| `/mira-planner` | Planejar slides |
| `/mira-copywriter` | Refinar textos |
| `/mira-builder` | Construir HTML |
| `/mira-animator` | Adicionar animações |
| `/mira-validator` | Validar deck |
| `/mira-chart` | Criar gráficos |
| `/mira-visuals` | Gerar imagens |
| `/mira-3d` | Adicionar elementos 3D |
| `/mira-qrcode` | Inserir QR code |
| `/mira-image` | Posicionar imagem |
| `/mira-img-animator` | Animar imagem |
| `/mira-animated-metaphor` | Criar metáfora animada |
| `/mira-squared` | Versão quadrada (1:1) |
| `/mira-vertical` | Versão vertical (9:16) |
| `/mira-thirds` | Composição em terços |
| `/mira-transition-dissolve` | Transição dissolve |
| `/mira-size-animator` | Ajustar tamanho das animações |

---

## Checklist de Qualidade

Antes de considerar um deck completo:

- [ ] Todas as animações têm loop interno
- [ ] Usou CSS variables do tema
- [ ] Textos em português com acentuação correta
- [ ] Navegação funciona corretamente
- [ ] Funciona por file:// (sem servidor)
- [ ] Validação passou (/mira-validator)
- [ ] Assets estão na pasta assets/

---

## Exemplo de Uso

### Criar Deck para Capítulo 1

```bash
# 1. Extrair contexto
/mira-extract capitulo_01

# 2. Planejar slides
/mira-planner

# 3. Refinar textos
/mira-copywriter

# 4. Construir slides
/mira-builder

# 5. Adicionar animações
/mira-animator

# 6. Validar
/mira-validator
```

---

> *"Uma imagem vale mais que mil palavras. Uma animação vale mais que mil imagens."* — Adágio moderno

---

**Nota**: Este é o espaço para slides animados. O conteúdo de estudo está em `estudo/` e os planos de estudo dirigido estão em `estudo_dirigido/`.
