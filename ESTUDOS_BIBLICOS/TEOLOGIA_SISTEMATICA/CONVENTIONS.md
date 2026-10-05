# CONVENTIONS — Convenções do Projeto

> **Regras e padrões para manter consistência em todo o projeto Teologia Sistemática**

---

## 1. Convenções de Nomenclatura

### 1.1. Capítulos

- **Formato**: `Cap_XX_Titulo_Do_Capitulo.md`
- **Exemplo**: `Cap_06_A_Trindade.md`, `Cap_22_A_Justificacao_e_a_Adocao.md`
- **Regra**: Use prefixo `Cap_` com número de dois dígitos
- **Organização**: Mantenha a estrutura por Partes (I-VII)

### 1.2. Partes do Livro

- **Parte I**: A Doutrina da Palavra de Deus
- **Parte II**: A Doutrina de Deus
- **Parte III**: A Doutrina do Homem
- **Parte IV**: A Doutrina de Cristo
- **Parte V**: A Doutrina da Aplicação da Redenção
- **Parte VI**: A Doutrina da Igreja
- **Parte VII**: A Doutrina do Futuro

### 1.3. Decks do Mira

- **Formato da pasta**: `xx-nome-do-capitulo/` (kebab-case)
- **Exemplo**: `06-a-trindade/`, `22-a-justificacao-e-a-adocao/`
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
- **Exemplo**: `estudo_dirigido/capitulo_06/plano-de-estudo.md`

---

## 2. Convenções de Formatação

### 2.1. Abreviações Bíblicas

Use SEMPRE abreviações em português:

**Antigo Testamento**:
Gn, Êx, Lv, Nm, Dt, Js, Jz, Rt, 1Sm, 2Sm, 1Rs, 2Rs, 1Cr, 2Cr, Ed, Ne, Et, Jó, Sl, Pv, Ec, Ct, Is, Jr, Lm, Ez, Dn, Os, Jl, Am, Ob, Jn, Mq, Na, Hc, Sf, Ag, Zc, Ml

**Novo Testamento**:
Mt, Mc, Lc, Jo, At, Rm, 1Co, 2Co, Gl, Ef, Fp, Cl, 1Ts, 2Ts, 1Tm, 2Tm, Tt, Fm, Hb, Tg, 1Pe, 2Pe, 1Jo, 2Jo, 3Jo, Jd, Ap

### 2.2. Referências Bíblicas

**Formato**: `Livro Capítulo:Versículo`

**Exemplos**:
- `Rm 3.23` — Romanos 3:23
- `1Co 13.4-7` — 1 Coríntios 13:4-7
- `Sl 23.1-6` — Salmos 23:1-6
- `Mt 5.3-12` — Mateus 5:3-12

### 2.3. Citações de Definições

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
var(--mira-bg-primary)   /* Fundo principal */
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
- [ ] Preservou estrutura de partes e capítulos
- [ ] Animações têm loop interno (se aplicável)
- [ ] Plano de estudo tem 6 etapas completas
- [ ] Documentação está em docs/
- [ ] Usou CSS variables do tema (Mira)
- [ ] Referências bíblicas seguem formato padrão

---

## 8. Exemplos de Uso

### 8.1. Criar Novo Deck

```bash
# Criar pasta do deck
mkdir decks/06-a-trindade

# Criar arquivos
touch decks/06-a-trindade/briefing.md
touch decks/06-a-trindade/plano-refinado.md
touch decks/06-a-trindade/validacao.md

# Criar pasta de assets
mkdir decks/06-a-trindade/assets
```

### 8.2. Criar Plano de Estudo

```bash
# Criar pasta
mkdir estudo_dirigido/capitulo_06

# Criar plano baseado no template
cp plano-template-estudo/template_capitulo.md estudo_dirigido/capitulo_06/plano-de-estudo.md
```

---

> *"A excelência não é um ato, mas um hábito."* — Aristóteles

**Manter consistência é chave para um projeto bem-sucedido.**
