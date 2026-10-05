# Mira Templates — Templates do Sistema Mira

> **Templates visuais e de slides para criação de apresentações animadas**

---

## Sobre Esta Pasta

Esta pasta contém os templates do sistema Mira, usados para criar apresentações animadas com D3.js.

---

## Estrutura

```
mira-templates/
├── themes/            ← Temas visuais
│   ├── mira-dark.css
│   ├── corporate-blue.css
│   ├── light-minimal.css
│   └── neon-emerald.css
└── slides/            ← Templates de slides
    ├── card_capa.html
    ├── card_encerramento.html
    └── ...
```

---

## Temas Disponíveis

### mira-dark

Tema principal com glassmorphism escuro:
- Fundo escuro com efeito de vidro
- Laranja como cor primária
- Azul como cor secundária
- Ideal para apresentações formais

### corporate-blue

Tema corporativo em azul:
- Azul profundo como cor primária
- Branco e cinza como neutros
- Ideal para ambientes corporativos

### light-minimal

Tema claro minimalista:
- Fundo branco
- Tipografia limpa
- Ideal para impressão ou ambientes claros

### neon-emerald

Tema neon em verde:
- Verde neon vibrante
- Fundo escuro
- Ideal para apresentações modernas

---

## CSS Variables do Tema

Sempre use variáveis do tema:

```css
/* Cores principais */
var(--mira-primary)      /* Laranja primário */
var(--mira-secondary)    /* Azul secundário */
var(--mira-accent)       /* Verde de destaque */

/* Fundos */
var(--mira-bg-primary)   /* Fundo principal */
var(--mira-bg-card)      /* Fundo dos cards */
var(--mira-bg-glass)     /* Fundo glassmorphism */

/* Texto */
var(--mira-text-primary) /* Texto principal */
var(--mira-text-muted)   /* Texto secundário */
```

---

> *"O design consistente facilita o reconhecimento e a memorização."*
