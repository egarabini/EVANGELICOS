# mira-templates/ — Templates do Mira

> **Temas visuais e templates de slides para o Mira**

---

## Estrutura da Pasta

```
mira-templates/
├── themes/              ← Temas visuais (CSS)
│   ├── mira-dark.css        ← Tema principal
│   ├── corporate-blue.css
│   ├── light-minimal.css
│   └── neon-emerald.css
├── slides/              ← Templates de slides
│   ├── card_capa.html
│   ├── card_encerramento.html
│   ├── card_escada.html
│   └── ...
└── README.md            ← Este arquivo
```

---

## Temas Visuais

### mira-dark (Tema Principal)

Tema padrão do projeto. Características:

- Glassmorphism escuro
- Laranja primário (`--mira-primary`)
- Azul secundário (`--mira-secondary`)
- Verde de destaque (`--mira-accent`)

### Outros Temas

| Tema | Descrição |
|------|-----------|
| `corporate-blue` | Azul corporativo |
| `light-minimal` | Claro minimalista |
| `neon-emerald` | Neon verde |

---

## CSS Variables

Cada tema define as seguintes variáveis:

```css
/* Cores principais */
--mira-primary
--mira-secondary
--mira-accent

/* Fundos */
--mira-bg-primary
--mira-bg-card
--mira-bg-glass

/* Texto */
--mira-text-primary
--mira-text-muted

/* Efeitos */
--mira-glow
--mira-shadow
```

**Regra**: Sempre use variáveis, nunca cores hardcoded.

---

## Templates de Slides

### Estrutura de um Template

Cada template em `slides/` define um tipo de slide:

```html
<!-- Nome do Template -->
<div class="mira-card">
  <!-- Header -->
  <div class="card-header">
    <h2 class="card-title">Título do Slide</h2>
  </div>

  <!-- Canvas de animação -->
  <div class="card-canvas">
    <svg id="animacao"></svg>
  </div>

  <!-- Base -->
  <div class="card-base">
    <p class="card-description">Descrição ou legenda</p>
    <div class="card-pills">
      <span class="pill">Pílula 1</span>
      <span class="pill">Pílula 2</span>
    </div>
  </div>
</div>
```

### Templates Disponíveis

| Template | Propósito |
|----------|-----------|
| `card_capa.html` | Slide de capa |
| `card_encerramento.html` | Slide de encerramento |
| `card_escada.html` | Escada de progressão |
| `card_fluxo.html` | Fluxo de processos |
| `card_orbital.html` | Sistema orbital |
| `card_metricas.html` | Métricas e estatísticas |

---

## Como Criar Novo Template

### 1. Criar Arquivo

```bash
touch mira-templates/slides/card_novo-template.html
```

### 2. Definir Estrutura

```html
<!-- card_novo-template.html -->
<div class="mira-card mira-card--novo-template">
  <div class="card-header">
    <h2 class="card-title">{{TITULO}}</h2>
  </div>

  <div class="card-canvas">
    <svg id="animacao-{{ID}}"></svg>
  </div>

  <div class="card-base">
    <p class="card-description">{{DESCRICAO}}</p>
    <div class="card-pills">
      {{PILULAS}}
    </div>
  </div>
</div>
```

### 3. Adicionar CSS (se necessário)

```css
.mira-card--novo-template {
  /* Estilos específicos */
}
```

---

## Como Criar Novo Tema

### 1. Criar Arquivo CSS

```bash
touch mira-templates/themes/novo-tema.css
```

### 2. Definir Variáveis

```css
/* novo-tema.css */
:root {
  /* Cores principais */
  --mira-primary: #FF6B35;
  --mira-secondary: #004E89;
  --mira-accent: #00A896;

  /* Fundos */
  --mira-bg-primary: #1A1A2E;
  --mira-bg-card: #16213E;
  --mira-bg-glass: rgba(22, 33, 62, 0.8);

  /* Texto */
  --mira-text-primary: #FFFFFF;
  --mira-text-muted: #B0B0B0;

  /* Efeitos */
  --mira-glow: 0 0 20px rgba(255, 107, 53, 0.5);
  --mira-shadow: 0 10px 30px rgba(0, 0, 0, 0.3);
}
```

### 3. Atualizar mira.config.json

Adicione o novo tema à lista:

```json
{
  "themes": [
    "mira-dark",
    "novo-tema"
  ]
}
```

---

## Convenções

### Nomenclatura de Arquivos

- **Temas**: `nome-tema.css` (kebab-case)
- **Slides**: `card_nome-template.html` (kebab-case, prefixo `card_`)

### Nomenclatura de Classes

- **Card**: `.mira-card`
- **Modificador**: `.mira-card--nome-modificador`
- **Elemento**: `.card-header`, `.card-title`, etc.

---

## Exemplo de Uso

### Usar Template em um Deck

```html
<!-- Em decks/xx-capitulo/index.html -->
<div class="slide">
  <!-- Copiar estrutura do template -->
  <div class="mira-card">
    <div class="card-header">
      <h2 class="card-title">Meu Título</h2>
    </div>

    <div class="card-canvas">
      <svg id="animacao-1"></svg>
    </div>

    <div class="card-base">
      <p class="card-description">Minha descrição</p>
      <div class="card-pills">
        <span class="pill">Pílula 1</span>
        <span class="pill">Pílula 2</span>
      </div>
    </div>
  </div>
</div>
```

---

## Checklist de Qualidade

Antes de considerar um template ou tema completo:

- [ ] Usa CSS variables (sem cores hardcoded)
- [ ] Segue convenção de nomenclatura
- [ ] Tem estrutura padrão do Mira
- [ ] Funciona com animações D3.js
- [ ] Responsivo (se aplicável)
- [ ] Documentado (comentários)

---

> *"O design não é apenas o que parece e se sente. O design é como funciona."* — Steve Jobs

---

**Nota**: Este é o espaço para templates do Mira. Os decks finais estão em `decks/` e o conteúdo de estudo está em `estudo/`.
