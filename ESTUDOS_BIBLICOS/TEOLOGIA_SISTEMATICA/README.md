# Teologia Sistemática — Wayne Grudem

> **Estudo completo da Teologia Sistemática de Wayne Grudem**

---

## Sobre o Estudo

Este projeto contém o estudo completo da **Teologia Sistemática** de **Wayne Grudem**, uma das obras mais influentes da teologia cristã contemporânea. O material está organizado em **7 partes principais**, cobrindo todas as doutrinas fundamentais da fé cristã.

---

## Estrutura do Estudo

### Partes

- **Parte I**: A Doutrina da Palavra de Deus
  - Capítulo 2: A Autoridade e a Inerrância da Bíblia
  - Capítulo 3: A Clareza, a Necessidade e a Suficiência da Bíblia

- **Parte II**: A Doutrina de Deus
  - Capítulo 4: O Caráter de Deus — Atributos Incomunicáveis
  - Capítulo 5: Os Atributos Comunicáveis de Deus
  - Capítulo 6: A Trindade
  - Capítulo 7: A Criação
  - Capítulo 8: A Providência Divina
  - Capítulo 9: A Oração
  - Capítulo 10: Os Anjos, Satanás e os Demônios

- **Parte III**: A Doutrina do Homem
  - Capítulo 11: A Criação do Homem
  - Capítulo 12: O Ser Humano como Homem e Mulher
  - Capítulo 13: O Pecado

- **Parte IV**: A Doutrina de Cristo
  - Capítulo 14: A Pessoa de Cristo
  - Capítulo 15: A Expiação
  - Capítulo 16: A Ressurreição e a Ascensão

- **Parte V**: A Doutrina da Aplicação da Redenção
  - Capítulo 17: A Graça Comum
  - Capítulo 18: A Eleição
  - Capítulo 19: O Chamado do Evangelho
  - Capítulo 20: A Regeneração
  - Capítulo 21: A Conversão — Fé e Arrependimento
  - Capítulo 22: A Justificação e a Adoção
  - Capítulo 23: A Santificação
  - Capítulo 24: A Perseverança dos Santos
  - Capítulo 25: A Morte, o Estado Intermediário e a Glorificação

- **Parte VI**: A Doutrina da Igreja
  - Capítulo 26: A Natureza da Igreja
  - Capítulo 27: O Batismo
  - Capítulo 28: A Ceia do Senhor
  - Capítulo 29: Os Dons do Espírito Santo I — Perguntas Gerais
  - Capítulo 30: Os Dons do Espírito Santo II — Dons Específicos

- **Parte VII**: A Doutrina do Futuro
  - Capítulo 31: A Volta de Cristo — Quando e Como
  - Capítulo 32: O Milênio
  - Capítulo 33: O Juízo Final e a Punição Eterna
  - Capítulo 34: Os Novos Céus e a Nova Terra

---

## Estrutura do Projeto

```
TEOLOGIA_SISTEMATICA/
├── README.md              ← Este arquivo
├── CLAUDE.md              ← Configuração para Claude Code
├── AGENTS.md              ← Configuração para outros agentes
├── CONVENTIONS.md         ← Convenções do projeto
├── .cursorrules           ← Regras para Cursor/Copilot
├── mira.config.json       ← Configuração do Mira
│
├── docs/                  ← Documentação
│   ├── diversos/          ← Documentos gerais
│   ├── referencias/       ← Referências bibliográficas
│   ├── videos/            ← Links de vídeos
│   ├── imagens/           ← Figuras e diagramas
│   └── audios/            ← Áudios de apoio
│
├── docs/base/             ← Conteúdo original
│   ├── 00_Preliminares/   ← Prefácio, abreviações
│   ├── Introducao/        ← Capítulo 1
│   ├── Parte_01_.../      ← Partes I-VII
│   └── Apendices/         ← Apêndices
│
├── estudo/                ← Conteúdo processado
│   └── (a ser preenchido)
│
├── decks/                 ← Slides animados (Mira)
│   └── (a ser preenchido)
│
├── estudo_dirigido/       ← Planos de estudo
│   └── (a ser preenchido)
│
├── mira-templates/        ← Templates do Mira
│   ├── themes/            ← Temas visuais
│   └── slides/            ← Templates de slides
│
└── plano-template-estudo/ ← Templates de planejamento
```

---

## Recursos Disponíveis

### Mira — Slides Animados

Este projeto integra o **Mira** para criar apresentações animadas com D3.js.

**Pipeline padrão**:
1. `/mira-extract` — Extrair contexto do capítulo
2. `/mira-planner` — Planejar estrutura dos slides
3. `/mira-copywriter` — Refinar textos
4. `/mira-builder` + `/mira-animator` — Criar slides animados
5. `/mira-validator` — Validar resultado

### Planos de Estudo Dirigido

Cada capítulo terá um plano estruturado em 6 etapas:

1. 🔥 **Aquecimento** — Perguntas-gatilho
2. 📖 **Leitura guiada** — Leituras focadas
3. 🧠 **Conceitos-chave** — Definições essenciais
4. ✍️ **Teste de entendimento** — Questões de verificação
5. 💭 **Reflexão pessoal** — Aplicação à vida
6. 🏁 **Consolidação** — Síntese e autoavaliação

---

## Como Usar Este Estudo

### Para Estudar

1. Comece pelo **Capítulo 1** — Introdução à Teologia Sistemática
2. Leia o conteúdo em `docs/base/`
3. Use os planos em `estudo_dirigido/` para aprofundar
4. Revise os slides em `decks/` para revisão visual

### Para Criar Materiais

1. **Para novos slides**: Use o pipeline do Mira
2. **Para novos planos**: Siga o template em `plano-template-estudo/`
3. **Para documentação**: Adicione em `docs/`

---

## Convenções

### Idioma

- **Português brasileiro** (pt-BR)
- Acentuação 100% correta

### Abreviações Bíblicas

Use sempre abreviações em português:
- Gn, Êx, Lv, Nm, Dt, Sl, Pv, Is, Mt, Mc, Lc, Jo, At, Rm, 1Co, 2Co, Ef, Hb, Tg, 1Pe, 2Pe, 1Jo, Ap, etc.

### Nomenclatura

- Capítulos: `Cap_XX_Titulo.md`
- Decks: `xx-nome-do-capitulo/`
- Planos: `estudo_dirigido/capitulo_XX/plano-de-estudo.md`

---

## Informações sobre a Obra

**Autor**: Wayne Grudem
**Título original**: Systematic Theology: An Introduction to Biblical Doctrine
**Editora original**: Zondervan (1994)
**Tradução**: Editora Vida Nova

---

## Data de Criação

**17 de Junho de 2026**

---

## Base

Este projeto foi criado com base no **TEMPLATE_ESTUDO v1.0**

---

> *"Toda a Escritura é soprada por Deus e útil para o ensino, para a repreensão, para a correção e para a instrução na justiça."* — 2 Timóteo 3.16

---

**Versão**: 1.0
**Status**: Em desenvolvimento
