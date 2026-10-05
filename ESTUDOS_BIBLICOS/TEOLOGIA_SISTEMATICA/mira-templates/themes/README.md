# Themes — Temas Visuais do Mira

> **Temas CSS para apresentações animadas**

---

## Sobre Esta Pasta

Esta pasta contém os temas visuais do sistema Mira, usados para estilizar as apresentações animadas.

---

## Temas Disponíveis

### mira-dark.css

Tema principal com glassmorphism escuro:
- **Cores**: Laranja primário, azul secundário
- **Fundo**: Escuro com efeito de vidro
- **Uso**: Apresentações formais e acadêmicas

### corporate-blue.css

Tema corporativo em azul:
- **Cores**: Azul profundo, branco, cinza
- **Fundo**: Azul escuro
- **Uso**: Ambientes corporativos

### light-minimal.css

Tema claro minimalista:
- **Cores**: Preto, branco, cinza
- **Fundo**: Branco
- **Uso**: Impressão e ambientes claros

### neon-emerald.css

Tema neon em verde:
- **Cores**: Verde neon vibrante
- **Fundo**: Escuro
- **Uso**: Apresentações modernas

---

## CSS Variables

Cada tema define as seguintes variáveis:

```css
:root {
  /* Cores principais */
  --mira-primary: #FF6B35;
  --mira-secondary: #1E3A8A;
  --mira-accent: #10B981;

  /* Fundos */
  --mira-bg-primary: #0F172A;
  --mira-bg-card: rgba(30, 58, 138, 0.3);
  --mira-bg-glass: rgba(255, 255, 255, 0.05);

  /* Texto */
  --mira-text-primary: #F1F5F9;
  --mira-text-muted: #94A3B8;
}
```

---

## Como Usar

Sempre use variáveis do tema, nunca cores hardcoded:

```css
/* CORRETO */
color: var(--mira-primary);

/* ERRADO */
color: #FF6B35;
```

---

> *"A consistência visual é a chave para apresentações profissionais."*
