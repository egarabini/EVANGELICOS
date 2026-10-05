# docs/ — Documentação do Projeto

> **Documentos e materiais coletados sobre Wayne Grudem e Teologia Sistemática**

---

## Propósito

Esta pasta contém documentos e materiais coletados que servem de **base** para o conteúdo das pastas:
- `estudo/` — Conteúdo dos capítulos
- `decks/` — Slides animados
- `estudo_dirigido/` — Planos de estudo

---

## Estrutura da Pasta

```
docs/
├── diversos/          ← Documentos gerais sobre o projeto
├── referencias/       ← Referências bibliográficas
├── videos/           ← Links e metadados de vídeos
├── imagens/          ← Figuras e diagramas
├── audios/           ← Áudios de apoio
└── README.md         ← Este arquivo
```

---

## Como Usar

### Adicionar Documento Geral

Coloque documentos gerais sobre o projeto em `docs/diversos/`:

- Contexto histórico
- Notas sobre tradução
- Decisões de design
- Metadados do projeto

### Adicionar Referência Bibliográfica

Coloque referências em `docs/referencias/`:

- Livros
- Artigos acadêmicos
- Ensaios
- Comentários

Use formato padrão de citação.

### Adicionar Vídeo

Coloque metadados de vídeos em `docs/videos/`:

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

### Adicionar Imagem

Coloque figuras em `docs/imagens/`:

- Diagramas
- Gráficos
- Ilustrações
- Capturas de tela

### Adicionar Áudio

Coloque áudios em `docs/audios/`:

- Palestras
- Podcasts
- Audiobooks
- Músicas

---

## Convenções

### Nomenclatura de Arquivos

Use kebab-case com data:

```
YYYY-MM-DD-titulo-descritivo.extensao
```

**Exemplos**:
- `2026-06-17-introducao-teologia-sistematica.md`
- `2026-06-17-diagrama-trindade.svg`
- `2026-06-17-palestra-justificacao.mp3`

### Metadados Obrigatórios

Cada arquivo deve ter metadados no cabeçalho:

```markdown
---
titulo: "Título do Documento"
tipo: "diversos|referencia|video|imagem|audio"
data: "YYYY-MM-DD"
autor: "Nome do autor"
tags: ["tag1", "tag2", "tag3"]
---

Conteúdo...
```

---

## Notas

- Esta é uma pasta de **documentação e materiais de apoio**
- O conteúdo principal está em `estudo/`
- Slides animados ficam em `decks/`
- Planos de estudo ficam em `estudo_dirigido/`

---

## Fonte dos Documentos

Estes documentos são coletados de diversas fontes:

- Livros e artigos sobre Wayne Grudem
- Vídeos e palestras sobre teologia sistemática
- Diagramas e ilustrações sobre doutrinas cristãs
- Documentos históricos sobre contextos

---

> *"Documentação é amor. Documentação é futuro. Documentação é para sempre."* — Anônimo

---

**Projeto**: Teologia Sistemática — Wayne Grudem
**Data de criação**: 17 de Junho de 2026
