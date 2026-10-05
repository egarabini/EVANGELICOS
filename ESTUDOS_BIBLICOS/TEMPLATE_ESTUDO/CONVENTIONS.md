# CONVENTIONS — Convenções do Projeto

> **Regras e padrões para manter consistência em todo o projeto**

---

## 1. Convenções de Nomenclatura

### 1.1. Pastas de Capítulos

- **Formato**: `capitulo_XX/`
- **Exemplo**: `capitulo_01/`, `capitulo_02/`, `capitulo_34/`
- **Regra**: Sempre dois dígitos, zero à esquerda para 01-09

### 1.2. Arquivos de Capítulos

| Tipo de Arquivo | Sufixo | Descrição | Pode Editar? |
|----------------|--------|----------|--------------|
| Original em inglês | `_EN.md` | Texto original em inglês | ❌ NUNCA |
| Tradução preservada | `_PT.md` | Tradução original preservada | ❌ NUNCA |
| Versão corrigida | `_PT_v1.md` | Versão corrigida e formatada | ✅ SIM |

**Exemplos**:
- `01_Introduction_to_Systematic_Theology_EN.md`
- `01_Introduction_to_Systematic_Theology_PT.md`
- `01_Introduction_to_Systematic_Theology_PT_v1.md`

### 1.3. Decks do Mira

- **Formato da pasta**: `xx-nome-do-capitulo/` (kebab-case)
- **Exemplo**: `01-introducao-teologia-sistematica/`
- **Regra**: Número com zero à esquerda, seguido de hífen e nome em kebab-case

### 1.4. Arquivos de Deck

| Arquivo | Propósito |
|---------|-----------|
| `index.html` | Apresentação final |
| `briefing.md` | Briefing inicial do deck |
| `plano-refinado.md` | Plano de slides refinado |
| `validacao.md` | Validação do deck gerado |
| `assets/` | Pasta para imagens e recursos |

### 1.5. Planos de Estudo Dirigido

- **Formato da pasta**: `capitulo_XX/`
- **Arquivo**: `plano-de-estudo.md`
- **Exemplo**: `estudo_dirigido/capitulo_01/plano-de-estudo.md`

---

## 2. Convenções de Formatação

### 2.1. Estrutura de Capítulo (_PT_v1.md)

```markdown
# Título do Capítulo em Português

> **Capítulo N** — Título Original em Inglês

## Perguntas centrais

- q1. Primeira pergunta?
- q2. Segunda pergunta?
- q3. Terceira pergunta?

## I. Explicação e Base Bíblica

### A. Primeira seção principal

#### 1. Subseção

Conteúdo...

> **Definição**: Termo teológico em blockquote

Texto de explicação...

## II. Outra seção principal

### A. Seção secundária

Conteúdo...

## Notas

[^1]: Primeira nota de rodapé
[^2]: Segunda nota de rodapé
```

### 2.2. Abreviações Bíblicas

Use SEMPRE abreviações em português:

- **Antigo Testamento**: Gn, Êx, Lv, Nm, Dt, Js, Jz, Rt, 1Sm, 2Sm, 1Rs, 2Rs, 1Cr, 2Cr, Ed, Ne, Et, Jó, Sl, Pv, Ec, Ct, Is, Jr, Lm, Ez, Dn, Os, Jl, Am, Ob, Jn, Mq, Na, Hc, Sf, Ag, Zc, Ml
- **Novo Testamento**: Mt, Mc, Lc, Jo, At, Rm, 1Co, 2Co, Gl, Ef, Fp, Cl, 1Ts, 2Ts, 1Tm, 2Tm, Tt, Fm, Hb, Tg, 1Pe, 2Pe, 1Jo, 2Jo, 3Jo, Jd, Ap

### 2.3. Referências Bíblicas

**Formato**: `Livro Capítulo:Versículo`

**Exemplos**:
- `Rm 3.23` — Romanos 3:23
- `1Co 13.4-7` — 1 Coríntios 13:4-7
- `Sl 23.1-6` — Salmos 23:1-6
- `Mt 5.3-12` — Mateus 5:3-12

### 2.4. Citações de Definições

Use blockquote para definições teológicas:

```markdown
> **Justificação**: Um ato legal de Deus pelo qual ele declara justos aqueles que colocaram sua fé em Jesus Cristo.
```

---

## 3. Convenções para Mira (Slides Animados)

### 3.1. Pipeline Padrão

```
1. /mira-extract    → Extrair contexto do capítulo
2. /mira-planner    → Planejar estrutura dos slides
3. /mira-copywriter → Refinar textos dos slides
4. /mira-builder    → Construir slides HTML
5. /mira-animator   → Adicionar animações D3.js
6. /mira-validator  → Validar slides gerados
```

### 3.2. Regras de Animação

- **TODA animação** deve entrar com coreografia
- **DEPOIS** continuar em loop interno perpétuo
- Animação estática é **PROIBIDA**
- Use SEMPRE CSS variables do tema: `var(--mira-primary)`, etc.
- Tema padrão: `mira-dark`

### 3.3. Estrutura de um Slide

```html
<!-- Card de slide com animação D3.js -->
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

### 3.4. CSS Variables do Tema

Sempre use variáveis do tema, nunca cores hardcoded:

```css
/* Cores principais */
var(--mira-primary)      /* Laranja primário */
var(--mira-secondary)    /* Azul secundário */
var(--mira-accent)       /* Verde de destaque */

/* Fundos */
var(--mira-bg-primary)    /* Fundo principal */
var(--mira-bg-card)      /* Fundo dos cards */
var(--mira-bg-glass)     /* Fundo glassmorphism */

/* Texto */
var(--mira-text-primary) /* Texto principal */
var(--mira-text-muted)   /* Texto secundário */
```

---

## 4. Convenções para Planos de Estudo Dirigido

### 4.1. Estrutura de 6 Etapas

Cada plano DEVE ter:

1. **🔥 Etapa 1 — Aquecimento** — 3 perguntas-gatilho (antes de ler)
2. **📖 Etapa 2 — Leitura guiada** — Leituras focadas do capítulo
3. **🧠 Etapa 3 — Conceitos-chave** — Definições a memorizar
4. **✍️ Etapa 4 — Teste de entendimento** — Questões objetivas e dissertativas
5. **💭 Etapa 5 — Reflexão pessoal** — Aplicação à vida
6. **🏁 Etapa 6 — Consolidação** — Síntese e farol final

### 4.2. Elementos Obrigatórios

| Elemento | Formato | Exemplo |
|----------|---------|---------|
| Caixa de seleção | `- [ ]` | `- [ ] Li a seção Perguntas centrais` |
| Espaço de resposta | `> _Resposta:_` | `> _Resposta:_` |
| Rubrica | Tabela Markdown | `| Critério \| Nota \|` |
| Farol final | Opções com emoji | `- [ ] 🟢 **Dominado**` |

### 4.3. Cabeçalho YAML

Cada plano deve começar com:

```yaml
---
capitulo: XX
parte: "{I-VII}"
titulo: "{TÍTULO DO CAPÍTULO}"
estudante: ""
status: nao_iniciado        # nao_iniciado | em_andamento | concluido
farol: ""                   # verde | amarelo | vermelho
nota_autoavaliacao: 0       # 0 a 20 (soma dos 4 critérios x 5)
data_inicio: ""
data_conclusao: ""
---
```

---

## 5. Convenções para Documentação (docs/)

### 5.1. Subpastas

| Pasta | Conteúdo |
|-------|----------|
| `docs/diversos/` | Documentos gerais sobre o projeto |
| `docs/referencias/` | Referências bibliográficas |
| `docs/videos/` | Links e metadados de vídeos |
| `docs/imagens/` | Figuras e diagramas |
| `docs/audios/` | Áudios de apoio |

### 5.2. Metadados de Vídeo

Ao adicionar um vídeo em `docs/videos/`, use este formato:

```markdown
# Título do Vídeo

- **Autor/Canal**: Nome do autor ou canal
- **Duração**: HH:MM:SS
- **Link**: https://url-do-video
- **Data de acesso**: DD/MM/AAAA
- **Tópicos abordados**:
  - Tópico 1
  - Tópico 2
  - Tópico 3
- **Notas**: Observações relevantes
```

---

## 6. Convenções de Linguagem

### 6.1. Idioma

- **Sempre**: Português brasileiro (pt-BR)
- **Acentuação**: 100% correta (á, é, í, ó, ú, ã, õ, â, ê, î, ô, û, à, ç)
- **Pontuação**: Seguir normas ABNT

### 6.2. Termos Teológicos

Mantenha termos teológicos originais quando apropriado:

- "Justificação" (não "Justifcação")
- "Santificação" (não "Santifcação")
- "Expiar" (não "Espiar")
- "Heresia" (não "Heregia")

---

## 7. Checklist de Qualidade

Antes de considerar qualquer tarefa como concluída:

- [ ] Acentuação 100% correta
- [ ] Seguiu convenções de nomenclatura
- [ ] Não editou arquivos _EN.md ou _PT.md
- [ ] Usou formato correto para _PT_v1.md
- [ ] Animações têm loop interno (se aplicável)
- [ ] Plano de estudo tem 6 etapas completas
- [ ] Documentação está em docs/
- [ ] Usou CSS variables do tema (Mira)
- [ ] Referências bíblicas seguem formato padrão

---

## 8. Exemplos de Uso

### 8.1. Criar Novo Capítulo

```bash
# Criar pasta
mkdir estudo/capitulo_35

# Criar arquivos
touch estudo/capitulo_35/35_Titulo_EN.md
touch estudo/capitulo_35/35_Titulo_PT.md
touch estudo/capitulo_35/35_Titulo_PT_v1.md
```

### 8.2. Criar Novo Deck

```bash
# Criar pasta do deck
mkdir decks/35-novo-capitulo

# Criar arquivos
touch decks/35-novo-capitulo/briefing.md
touch decks/35-novo-capitulo/plano-refinado.md
touch decks/35-novo-capitulo/validacao.md

# Criar pasta de assets
mkdir decks/35-novo-capitulo/assets
```

### 8.3. Criar Plano de Estudo

```bash
# Criar pasta
mkdir estudo_dirigido/capitulo_35

# Criar plano baseado no template
cp estudo_dirigido/_template_plano-de-estudo.md estudo_dirigido/capitulo_35/plano-de-estudo.md
```

---

> *"A excelência não é um ato, mas um hábito."* — Aristóteles

**Manter consistência é chave para um projeto bem-sucedido.**
