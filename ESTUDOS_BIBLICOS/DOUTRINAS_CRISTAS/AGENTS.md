# {NOME DO ESTUDO} — Configuração para Outros Agentes de IA

> **Configurações para Gemini, Copilot, e outros agentes**

---

## Instruções Gerais para Todos os Agentes

### Linguagem e Tom

- **Idioma**: Português brasileiro (pt-BR)
- **Acentuação**: 100% correta
- **Tom**: Acadêmico, respeitoso, acessível
- **Nome do usuário**: Eduardo

### Estrutura do Projeto

Este projeto segue o TEMPLATE_ESTUDO:

```
{NOME_DO_PROJETO}/
├── estudo/              ← Conteúdo principal (capítulos)
├── decks/               ← Slides animados do Mira
├── estudo_dirigido/     ← Planos de estudo dirigido
├── docs/                ← Documentação e referências
├── mira-templates/      ← Templates do Mira
└── plano-template-estudo/ ← Templates de planejamento
```

---

## Configurações Específicas

### Gemini (Google)

#### Prompt de Sistema

```
Você está assistindo Eduardo em um projeto de estudo teológico chamado {NOME_DO_ESTUDO}.

REGRAS IMPORTANTES:
1. Sempre responda em português brasileiro com acentuação 100% correta
2. NUNCA edite arquivos *_EN.md (originais em inglês)
3. NUNCA edite arquivos *_PT.md (traduções preservadas)
4. EDITE apenas arquivos *_PT_v1.md (versões corrigidas)

ESTRUTURA DE CAPÍTULOS:
- Cada capítulo está em estudo/capitulo_XX/
- Formato: # Título, > **Capítulo N**, ## Perguntas centrais, ## I. Explicação e Base Bíblica
- Use abreviações bíblicas em português: Gn, Êx, Lv, Mt, Mc, Lc, Jo, At, Rm, 1Co, Ef, Hb, Ap, etc.

MIRA (SLIDES ANIMADOS):
- Pipeline: /mira-extract → /mira-planner → /mira-copywriter → /mira-builder → /mira-animator → /mira-validator
- TODA animação deve entrar com coreografia e DEPOIS continuar em loop interno
- Use CSS variables do tema: var(--mira-primary), etc.
- Tema padrão: mira-dark

PLANOS DE ESTUDO DIRIGIDO:
- 6 etapas: Aquecimento → Leitura guiada → Conceitos-chave → Teste → Reflexão → Consolidação
- Use caixas de seleção - [ ] e espaços > _Resposta:_
- Farol final: 🟢 dominado · 🟡 revisar · 🔴 reler

NOMENCLATURA:
- Capítulos: capitulo_XX/
- Arquivos: XX_Titulo_EN.md, XX_Titulo_PT.md, XX_Titulo_PT_v1.md
- Decks: xx-nome-do-capitulo/

Priorize qualidade, clareza e consistência.
```

### Copilot (GitHub)

#### Prompt de Sistema

```
Context: You are assisting Eduardo with a theological study project called {NOME_DO_ESTUDO}.

LANGUAGE: Portuguese (Brazil) with perfect accentuation.

CRITICAL RULES:
1. NEVER edit *_EN.md files (original English)
2. NEVER edit *_PT.md files (preserved translations)
3. ONLY edit *_PT_v1.md files (corrected versions)

CHAPTER FORMAT:
- Each chapter in estudo/capitulo_XX/
- Structure: # Title, > **Chapter N**, ## Central Questions, ## I. Explanation and Biblical Basis
- Bible abbreviations in Portuguese: Gn, Êx, Lv, Mt, Mc, Lc, Jo, At, Rm, 1Co, Ef, Hb, Ap

MIRA (ANIMATED SLIDES):
- Pipeline: extract → plan → copywrite → build → animate → validate
- ALL animations must enter with choreography AND THEN continue in internal loop
- Use CSS theme variables: var(--mira-primary), etc.
- Default theme: mira-dark

STUDY PLANS:
- 6 stages: Warm-up → Guided reading → Key concepts → Test → Reflection → Consolidation
- Use checkboxes - [ ] and spaces > _Answer:_
- Final traffic light: 🟢 mastered · 🟡 review · 🔴 reread

NAMING:
- Chapters: capitulo_XX/
- Files: XX_Title_EN.md, XX_Title_PT.md, XX_Title_PT_v1.md
- Decks: xx-chapter-name/

Prioritize quality, clarity, and consistency.
```

### Cursor (Editor)

#### .cursorrules

```
You are assisting Eduardo with a theological study project called {NOME_DO_ESTUDO}.

LANGUAGE: Portuguese (Brazil) with perfect accentuation.

CRITICAL RULES:
1. NEVER edit *_EN.md files (original English)
2. NEVER edit *_PT.md files (preserved translations)
3. ONLY edit *_PT_v1.md files (corrected versions)

CHAPTER FORMAT:
- Each chapter in estudo/capitulo_XX/
- Structure: # Title, > **Chapter N**, ## Central Questions, ## I. Explanation and Biblical Basis
- Bible abbreviations in Portuguese: Gn, Êx, Lv, Mt, Mc, Lc, Jo, At, Rm, 1Co, Ef, Hb, Ap

MIRA (ANIMATED SLIDES):
- Pipeline: extract → plan → copywrite → build → animate → validate
- ALL animations must enter with choreography AND THEN continue in internal loop
- Use CSS theme variables: var(--mira-primary), etc.
- Default theme: mira-dark

STUDY PLANS:
- 6 stages: Warm-up → Guided reading → Key concepts → Test → Reflection → Consolidation
- Use checkboxes - [ ] and spaces > _Answer:_
- Final traffic light: 🟢 mastered · 🟡 review · 🔴 reread

NAMING:
- Chapters: capitulo_XX/
- Files: XX_Title_EN.md, XX_Title_PT.md, XX_Title_PT_v1.md
- Decks: xx-chapter-name/

Prioritize quality, clarity, and consistency.
```

---

## Abreviações Bíblicas (Português)

### Antigo Testamento

- Gn = Gênesis
- Êx = Êxodo
- Lv = Levítico
- Nm = Números
- Dt = Deuteronômio
- Js = Josué
- Jz = Juízes
- Rt = Rute
- 1Sm = 1 Samuel
- 2Sm = 2 Samuel
- 1Rs = 1 Reis
- 2Rs = 2 Reis
- 1Cr = 1 Crônicas
- 2Cr = 2 Crônicas
- Ed = Esdras
- Ne = Neemias
- Et = Ester
- Jó = Jó
- Sl = Salmos
- Pv = Provérbios
- Ec = Eclesiastes
- Ct = Cântico dos Cânticos
- Is = Isaías
- Jr = Jeremias
- Lm = Lamentações
- Ez = Ezequiel
- Dn = Daniel
- Os = Oséias
- Jl = Joel
- Am = Amós
- Ob = Obadias
- Jn = Jonas
- Mq = Miquéias
- Na = Naum
- Hc = Habacuque
- Sf = Sofonias
- Ag = Ageu
- Zc = Zacarias
- Ml = Malaquias

### Novo Testamento

- Mt = Mateus
- Mc = Marcos
- Lc = Lucas
- Jo = João
- At = Atos
- Rm = Romanos
- 1Co = 1 Coríntios
- 2Co = 2 Coríntios
- Gl = Gálatas
- Ef = Efésios
- Fp = Filipenses
- Cl = Colossenses
- 1Ts = 1 Tessalonicenses
- 2Ts = 2 Tessalonicenses
- 1Tm = 1 Timóteo
- 2Tm = 2 Timóteo
- Tt = Tito
- Fm = Filemom
- Hb = Hebreus
- Tg = Tiago
- 1Pe = 1 Pedro
- 2Pe = 2 Pedro
- 1Jo = 1 João
- 2Jo = 2 João
- 3Jo = 3 João
- Jd = Judas
- Ap = Apocalipse

---

## Checklist para Qualidade

Antes de finalizar qualquer tarefa:

- [ ] Acentuação 100% correta
- [ ] Seguiu convenções de nomenclatura
- [ ] Não editou arquivos _EN.md ou _PT.md
- [ ] Usou formato correto para _PT_v1.md
- [ ] Animações têm loop interno (se aplicável)
- [ ] Plano de estudo tem 6 etapas completas
- [ ] Documentação está em docs/

---

> *"Toda a Escritura é soprada por Deus e útil para o ensino, para a repreensão, para a correção e para a instrução na justiça."* — 2 Timóteo 3.16
