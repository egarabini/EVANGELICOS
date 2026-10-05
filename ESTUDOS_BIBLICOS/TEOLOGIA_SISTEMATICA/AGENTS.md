# Teologia Sistemática — Configuração para Agentes de IA

> **Instruções para agentes de IA (Gemini, ChatGPT, etc.) trabalharem neste projeto**

---

## Identidade do Projeto

**Nome**: Teologia Sistemática — Wayne Grudem
**Tipo**: Estudo teológico sistemático
**Base**: TEMPLATE_ESTUDO v1.0
**Data de criação**: 17 de Junho de 2026

---

## Regras Fundamentais

### 1. NUNCA Edite o TEMPLATE

O TEMPLATE_ESTUDO em `f:/ESTUDOS_BIBLICOS/TEMPLATE_ESTUDO/` é IMUTÁVEL.

- ❌ **NUNCA** edite arquivos no TEMPLATE
- ✅ **SEMPRE** trabalhe apenas neste projeto
- ✅ **CONSULTE** o TEMPLATE como referência

### 2. Linguagem e Formatação

- **Idioma**: Português brasileiro (pt-BR)
- **Acentuação**: 100% correta (á, é, í, ó, ú, ã, õ, â, ê, î, ô, û, à, ç)
- **Tom**: Acadêmico, respeitoso, mas acessível
- **Nome do usuário**: Eduardo

### 3. Estrutura do Projeto

```
TEOLOGIA_SISTEMATICA/
├── docs/base/              ← Conteúdo original organizado por partes
│   ├── 00_Preliminares/
│   ├── Introducao/
│   ├── Parte_01_.../
│   ├── Parte_02_.../
│   └── Apendices/
├── estudo/                 ← Versões processadas dos capítulos
├── decks/                  ← Slides animados do Mira
├── estudo_dirigido/        ← Planos de estudo estruturados
├── docs/                   ← Documentação adicional
└── mira-templates/         ← Templates do Mira
```

---

## Convenções de Nomenclatura

### Capítulos

- **Formato**: `Cap_XX_Titulo.md`
- **Exemplo**: `Cap_06_A_Trindade.md`
- **Organização**: Por Partes (I-VII)

### Decks do Mira

- **Formato**: `xx-nome-do-capitulo/`
- **Exemplo**: `06-a-trindade/`
- **Arquivos**: `index.html`, `briefing.md`, `plano-refinado.md`

### Planos de Estudo

- **Pasta**: `estudo_dirigido/capitulo_XX/`
- **Arquivo**: `plano-de-estudo.md`

---

## Abreviações Bíblicas

Use SEMPRE abreviações em português:

**Antigo Testamento**:
Gn, Êx, Lv, Nm, Dt, Js, Jz, Rt, 1Sm, 2Sm, 1Rs, 2Rs, 1Cr, 2Cr, Ed, Ne, Et, Jó, Sl, Pv, Ec, Ct, Is, Jr, Lm, Ez, Dn, Os, Jl, Am, Ob, Jn, Mq, Na, Hc, Sf, Ag, Zc, Ml

**Novo Testamento**:
Mt, Mc, Lc, Jo, At, Rm, 1Co, 2Co, Gl, Ef, Fp, Cl, 1Ts, 2Ts, 1Tm, 2Tm, Tt, Fm, Hb, Tg, 1Pe, 2Pe, 1Jo, 2Jo, 3Jo, Jd, Ap

---

## Integração com Mira

### Pipeline Padrão

```
1. /mira-extract    → Extrair contexto do capítulo
2. /mira-planner    → Planejar estrutura dos slides
3. /mira-copywriter → Refinar textos dos slides
4. /mira-builder    → Construir slides HTML
5. /mira-animator   → Adicionar animações D3.js
6. /mira-validator  → Validar slides gerados
```

### Regras de Animação

- **TODA animação** entra com coreografia
- **DEPOIS** continua em loop interno perpétuo
- Animação estática é **PROIBIDA**
- Use CSS variables: `var(--mira-primary)`, etc.
- Tema padrão: `mira-dark`

---

## Planos de Estudo Dirigido

### Estrutura de 6 Etapas

Cada plano DEVE ter:

1. **🔥 Aquecimento** — 3 perguntas-gatilho (antes de ler)
2. **📖 Leitura guiada** — Leituras focadas
3. **🧠 Conceitos-chave** — Definições a memorizar
4. **✍️ Teste de entendimento** — Questões objetivas e dissertativas
5. **💭 Reflexão pessoal** — Aplicação à vida
6. **🏁 Consolidação** — Síntese e farol final

### Elementos Obrigatórios

- Caixas de seleção: `- [ ]`
- Espaços de resposta: `> _Resposta:_`
- Rubrica de autoavaliação (0–5)
- Farol final: 🟢 dominado · 🟡 revisar · 🔴 reler

---

## Checklist de Qualidade

Antes de considerar uma tarefa concluída:

- [ ] Acentuação 100% correta
- [ ] Seguiu convenções de nomenclatura
- [ ] Preservou estrutura de partes e capítulos
- [ ] Animações têm loop interno
- [ ] Plano de estudo tem 6 etapas
- [ ] Usou CSS variables do tema

---

## Prioridades

1. **Não perca dados** — Preserve arquivos originais
2. **Mantenha consistência** — Siga convenções
3. **Qualidade sobre quantidade** — Faça certo
4. **Comunique claramente** — Explique suas ações

---

> *"Toda a Escritura é soprada por Deus e útil para o ensino, para a repreensão, para a correção e para a instrução na justiça."* — 2 Timóteo 3.16
