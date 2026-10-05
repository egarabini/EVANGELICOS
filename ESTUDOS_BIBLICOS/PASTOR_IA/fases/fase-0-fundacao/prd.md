# PRD — Fase 0: Fundação da Plataforma DAVID Pastoral

**Data:** 2026-07-15
**Status:** Aguardando aprovação
**Fase:** 0 de 6
**Predecessora:** OLPF aprovado

---

## 1. Problema

A Plataforma DAVID Pastoral não possui infraestrutura base para operar. Sem os componentes da Fase 0, nenhuma funcionalidade subsequente pode ser construída ou testada:

- Não há ambiente Docker configurado com PostgreSQL, ChromaDB e Ollama
- Não há pipeline que converta PDFs de livros em estudos estruturados para o RAG
- Não há base de conhecimento bíblico indexada (Bíblia ARC + NVI)
- Não há instância do Hermes Agent configurada e funcional

O resultado: o agente DAVID não tem onde rodar, não tem o que dizer e não tem onde guardar o que aprende.

---

## 2. Objetivo

Ao final da Fase 0, a plataforma deve ser capaz de:

1. **Processar um PDF** de livro bíblico e gerar um estudo estruturado em JSON (capítulos, versículos, perguntas de reflexão, sinais de compreensão) com qualidade aprovável por um administrador humano
2. **Responder perguntas bíblicas** com precisão a partir do RAG indexado (Bíblia ARC + NVI), sem alucinações — toda resposta deve citar o versículo exato do corpus
3. **Iniciar o Hermes Agent** com Ollama como LLM backend e interagir por linha de comando com o system prompt base do DAVID

---

## 3. Natureza desta fase

Esta fase é uma **infraestrutura base** — não entrega funcionalidade ao usuário final. Não há frontend, não há Telegram, não há dashboard. É o alicerce sobre o qual tudo será construído.

**Regra de governança:** O escopo da Fase 0 encerra-se quando os três objetivos acima forem demonstráveis via testes locais. Nenhuma funcionalidade de Fase 1+ deve ser implementada aqui.

---

## 4. Componentes da Fase 0

| Componente | Papel |
|---|---|
| **Docker Compose** | Orquestra PostgreSQL + ChromaDB + Ollama em ambiente local e VPS |
| **Pipeline `pdf_to_md.py`** | Converte PDF/DOCX em Markdown limpo |
| **Pipeline `md_to_estudo.py`** | Estrutura MD em JSON de estudo via Ollama LLM |
| **Pipeline `embeddings.py`** | Gera vetores para ChromaDB |
| **RAG Bíblico** | Carrega Bíblia completa (ARC + NVI) no ChromaDB |
| **Hermes Agent base** | Instância configurada com Ollama + system prompt do DAVID |
| **Teste de qualidade RAG** | Script de benchmark com perguntas bíblicas padrão |

---

## 5. Modelo de dados do Estudo Estruturado

### 5.1 Estrutura do arquivo `estudo_estruturado.json`

```json
{
  "id": "string — slug único do estudo",
  "titulo": "string",
  "autor": "string",
  "fonte": "string — editora ou ministério de origem",
  "nivel": "iniciante | intermediario | avancado",
  "idioma": "pt-BR",
  "temas": ["string"],
  "total_capitulos": "integer",
  "tempo_estimado_semanas": "integer",
  "capitulos": [
    {
      "ordem": "integer",
      "titulo": "string",
      "tempo_estimado_min": "integer",
      "versiculos_chave": ["string — formato: Livro cap:vers"],
      "perguntas_reflexao": ["string"],
      "sinais_compreensao": ["string"],
      "perguntas_aprofundamento": ["string"]
    }
  ]
}
```

### 5.2 Exemplo de registro gerado

```json
{
  "id": "fundamentos_da_fe_v1",
  "titulo": "Fundamentos da Fé",
  "nivel": "iniciante",
  "idioma": "pt-BR",
  "total_capitulos": 10,
  "capitulos": [
    {
      "ordem": 1,
      "titulo": "Quem é Deus",
      "versiculos_chave": ["João 1:1", "Gênesis 1:1"],
      "perguntas_reflexao": [
        "Como você descreveria Deus para alguém que nunca ouviu falar d'Ele?"
      ],
      "sinais_compreensao": [
        "Menciona ao menos um atributo divino",
        "Cita um versículo de memória"
      ]
    }
  ]
}
```

---

## 6. Regras de qualidade do Pipeline

- **R1 — Fidelidade ao original:** o pipeline não inventa conteúdo; extrai e estrutura o que está no PDF
- **R2 — Versículos verificáveis:** todos os versículos extraídos devem existir no corpus bíblico do RAG
- **R3 — Revisão humana obrigatória:** o JSON gerado é um rascunho; nenhum estudo entra em produção sem aprovação do Administrador
- **R4 — Isolamento por organização:** cada coleção ChromaDB é prefixada com `org_{org_id}__estudo_{estudo_id}`
- **R5 — Sem cross-schema:** o pipeline não acessa dados de membros ou sessões — apenas conteúdo do livro

---

## 7. Critérios de aceite

### DoD local (Definition of Done)

| CA | Critério |
|----|----------|
| CA01 | `docker-compose up` sobe PostgreSQL, ChromaDB e Ollama sem erros |
| CA02 | `python pdf_to_md.py livro.pdf` gera `markdown_bruto.md` com estrutura de capítulos identificável |
| CA03 | `python md_to_estudo.py markdown_bruto.md` gera `estudo_estruturado.json` válido com ao menos 3 capítulos estruturados |
| CA04 | ChromaDB indexa a Bíblia ARC e NVI completas sem erros |
| CA05 | Query de benchmark: "O que João 3:16 diz?" retorna o versículo correto e completo, sem alucinação |
| CA06 | Query de benchmark: "Cite 3 versículos sobre oração" retorna 3 versículos existentes e verificáveis |
| CA07 | Hermes Agent inicia com Ollama como backend e responde à primeira mensagem usando o system prompt do DAVID |
| CA08 | Hermes Agent recusa responder sobre futebol e redireciona para o escopo espiritual |

---

## 8. Escopo

### Incluído na Fase 0

- Setup Docker local (PostgreSQL + ChromaDB + Ollama)
- Scripts Python do pipeline (pdf_to_md, md_to_estudo, embeddings)
- Carga do corpus bíblico no ChromaDB
- Configuração base do Hermes Agent com Ollama
- System prompt inicial do DAVID
- Scripts de teste/benchmark de qualidade do RAG

### Fora do escopo da Fase 0

- Interface web (Admin, Pastor, Gestor, Membro)
- Gateway Telegram/WhatsApp
- Autenticação / Keycloak
- Multi-tenant (PostgreSQL com isolamento por org_id)
- Skills do DAVID (buscar_capitulo_rag, reportar_evento, etc.)
- Dashboard
- Deploy na VPS Contabo (é feito na Fase 5)

---

## 9. Riscos

### R1 — Qualidade da conversão PDF → MD

**Descrição:** PDFs de livros religiosos frequentemente têm formatação complexa (notas de rodapé, citações bíblicas aninhadas, cabeçalhos irregulares) que pode confundir o parser.
**Mitigação:** Testar com 3 PDFs diferentes antes de fixar a solução. Usar `marker-pdf` como fallback se `PyMuPDF` falhar em qualidade.
**Impacto:** Médio — afeta qualidade do estudo estruturado, não bloqueia a fase.

### R2 — Qualidade do LLM em português para estruturação

**Descrição:** O modelo Ollama pode gerar perguntas de reflexão genéricas ou em inglês.
**Mitigação:** Testar `mistral-nemo` e `gemma2:9b`. Usar prompt de estruturação em PT-BR explícito. A revisão humana do Admin é a rede de segurança final.
**Impacto:** Baixo — admin revisa antes de publicar.

### R3 — Tamanho do corpus bíblico no ChromaDB

**Descrição:** A Bíblia completa tem ~31.000 versículos. Dependendo do modelo de embedding, a indexação pode ser lenta.
**Mitigação:** Usar `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2` (rápido, multilíngue). Indexar em batch de 500 versículos.
**Impacto:** Baixo — é operação única de setup.

---

## 10. Dependências

### Técnicas

- VPS Contabo com Docker e Docker Compose instalados (ou máquina local com WSL2)
- Modelo Ollama disponível: `mistral-nemo` ou `gemma2:9b`
- Hermes Agent clonado: `github.com/NousResearch/hermes-agent`
- Bíblia em formato JSON/XML (ARC + NVI) — fontes abertas disponíveis no GitHub

### Documentais

- `planejamento/DAVID-PASTORAL-PLATAFORMA.md` — estudo completo
- `fases/fase-0-fundacao/olpf.md` — justificativa aprovada
- Este PRD — aprovação pendente

---

## 11. Backlog para spec e design

| ID | Artefato | O que deve ser resolvido |
|----|----------|--------------------------|
| SPEC-01 | spec.md | Qual parser PDF usar como primário (PyMuPDF vs marker-pdf) e critério de fallback |
| SPEC-02 | spec.md | Prompt exato para estruturação MD → JSON (template e temperatura do LLM) |
| SPEC-03 | spec.md | Modelo de embedding escolhido e configuração do ChromaDB |
| SPEC-04 | spec.md | Configuração do Hermes Agent (config.yaml, variáveis de ambiente) |
| DESIGN-01 | design.md | Estrutura de diretórios do projeto `david_pastoral/` |
| DESIGN-02 | design.md | Docker Compose completo com volumes e networks |
| DESIGN-03 | design.md | Script de carga do corpus bíblico e estratégia de chunking por versículo |

---

## 12. Relação com o roadmap

A Fase 0 é **pré-requisito bloqueante** de todas as fases seguintes. Nenhuma fase pode ser iniciada sem os CAs desta fase verificados.

---

## 13. Referências

- `planejamento/DAVID-PASTORAL-PLATAFORMA.md`
- `fases/fase-0-fundacao/olpf.md`
- [Hermes Agent — NousResearch](https://github.com/NousResearch/hermes-agent)
- [hermes-agent.org](https://hermes-agent.org/)
- `pastor-hermes.md` — estudo inicial do projeto
