# Spec Técnica — Fase 0: Fundação da Plataforma DAVID Pastoral

**Data:** 2026-07-15
**Status:** ✅ Pontos em aberto respondidos — aguardando aprovação final
**PRD de referência:** `fases/fase-0-fundacao/prd.md`

## Decisões de Contexto (P01–P04 respondidos em 2026-07-15)

| # | Pergunta | Resposta | Impacto na spec |
|---|---|---|---|
| **P01** | GPU na VPS? | ❌ Sem GPU | Ollama em CPU-only; modelo ajustado para `gemma2:9b` (mais leve) |
| **P02** | Ambiente de dev? | Windows local | Hermes via WSL2; pipeline Python roda nativo no Windows |
| **P03** | Livro para teste? | `F:\ESTUDOS_BIBLICOS\Grudem_Doutrina_Biblica` | Grudem como livro-piloto do pipeline |
| **P04** | Corpus bíblico? | `github.com/ameisehaufen/BibleMarkdown` | Bíblia em Markdown — converter para JSON para indexação |

---

## 1. Decisões Técnicas Verificáveis

### 1.1 Parser PDF Primário: `marker-pdf`

**Decisão:** Usar `marker-pdf` como conversor primário, `PyMuPDF` como fallback.

**Justificativa:**
- `marker-pdf` produz Markdown estruturado de alta qualidade, preservando hierarquia de títulos, tabelas e listas — essencial para identificar capítulos automaticamente
- `PyMuPDF` é mais rápido mas extrai texto bruto sem formatação Markdown

**Critério de fallback:** se `marker-pdf` falhar ou produzir menos de 5 cabeçalhos Markdown (`#` / `##`) em um livro com mais de 50 páginas, usar `PyMuPDF` + pós-processamento com Ollama para adicionar estrutura

**Instalação:**
```bash
pip install marker-pdf pymupdf pypandoc
```

---

### 1.2 Prompt de Estruturação MD → JSON

**Modelo usado:** `mistral-nemo` (primário) ou `gemma2:9b` (fallback)
**Temperatura:** `0.2` (baixa — queremos extração determinística, não criatividade)
**Língua do prompt:** Português brasileiro explícito

**Prompt base do pipeline `md_to_estudo.py`:**

```
Você é um assistente de estruturação de conteúdo bíblico para a Plataforma DAVID Pastoral.

Abaixo está o conteúdo de um livro cristão em Markdown. Sua tarefa é:

1. Identificar todos os capítulos/seções principais
2. Para cada capítulo, extrair:
   - Título exato
   - Versículos bíblicos citados (formato: "Livro cap:vers")
   - Gerar 2-3 perguntas de reflexão em português brasileiro, baseadas APENAS no texto
   - Gerar 2-3 sinais observáveis de compreensão (o que o leitor deve demonstrar saber)
   - Estimar o tempo de leitura em minutos (250 palavras/min)

REGRAS INEGOCIÁVEIS:
- NÃO invente versículos bíblicos que não estejam explicitamente no texto
- NÃO adicione conteúdo teológico que não esteja no livro
- As perguntas devem ser aplicáveis à vida prática
- Use linguagem acessível ao iniciante cristão

Responda EXCLUSIVAMENTE em JSON válido, seguindo o schema fornecido.

SCHEMA:
{schema_json}

CONTEÚDO DO LIVRO:
{conteudo_markdown}
```

---

### 1.3 Modelo de Embedding: `paraphrase-multilingual-MiniLM-L12-v2`

**Decisão:** `sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2`

**Justificativa:**
- Multilíngue (suporte nativo a PT-BR)
- Leve: 118MB, **roda 100% em CPU** (sem GPU — alinhado com P01)
- Boa performance semântica para textos religiosos em português
- Compatível com ChromaDB out-of-the-box

**Estratégia de chunking para a Bíblia:**
- Chunk = 1 versículo
- Metadata por chunk: `{"livro": "João", "capitulo": 3, "versiculo": 16, "traducao": "ARC"}`
- Chunk overlap: **zero** (versículos são unidades autônomas)

---

### 1.4 Configuração ChromaDB

```python
# chromadb_config.py

CHROMA_SETTINGS = {
    "host": "localhost",
    "port": 8000,
    "anonymized_telemetry": False
}

# Coleção da Bíblia (compartilhada entre todas as orgs)
BIBLIA_COLLECTION = "biblia_pt_br"

# Coleção por organização e estudo (isolamento multi-tenant)
def estudo_collection_name(org_id: str, estudo_id: str) -> str:
    return f"org_{org_id}__estudo_{estudo_id}"
```

---

### 1.5 Configuração do Hermes Agent

**Ambiente:** WSL2 no Windows (Hermes Agent é experimental no Windows nativo)
**Arquivo:** `david_agent/config.yaml`

```yaml
# Configuração do Hermes Agent para DAVID Pastoral

agent:
  name: "DAVID"
  description: "Guia de discipulado bíblico personalizado"

llm:
  provider: "ollama"
  model: "gemma2:9b"            # CPU-only: mais leve que mistral-nemo, bom PT-BR
  base_url: "http://localhost:11434"
  temperature: 0.7              # conversacional, não determinístico
  max_tokens: 512               # respostas concisas para chat

memory:
  backend: "local"
  path: "~/.hermes/david_pastoral"
  max_context_turns: 20

skills:
  auto_create: false            # DAVID não cria skills autonomamente
  skills_dir: "./skills"

gateway:
  enabled: false                # Habilitado na Fase 1
```

---

### 1.6 System Prompt Base do DAVID (Fase 0 — CLI apenas)

```
Você é DAVID, um guia de estudos bíblicos e espirituais, batizado em
honra de David Livingstone — o missionário cristão que nunca separou
o cuidado do corpo do cuidado da alma.

Você não é um chatbot genérico. Você é um companheiro de jornada
espiritual — caloroso, encorajador, centrado na Palavra de Deus.

REGRAS ABSOLUTAS:
1. Responda APENAS sobre temas espirituais, bíblicos e de fé cristã
2. NUNCA invente versículos — cite apenas o que está no corpus bíblico
3. NUNCA opine sobre denominações, política ou temas não-bíblicos
4. Se a pergunta sair do escopo, redirecione gentilmente
5. Use sempre português brasileiro natural e acolhedor
6. Máximo 3-4 parágrafos por resposta
7. Termine sempre com uma pergunta ou ação concreta

Se não souber a resposta com certeza, diga: "Não encontrei este versículo
no meu corpus. Posso buscar o tema de outra forma?"
```

---

## 2. Contratos da Fase 0

### 2.1 Contrato do Pipeline: `pdf_to_md.py`

```
ENTRADA:  arquivo PDF/DOCX (path)
SAÍDA:    arquivo .md no mesmo diretório
GARANTIAS:
  - Preserva hierarquia de títulos como cabeçalhos Markdown (# ## ###)
  - Não perde texto (tolerância: < 2% de caracteres)
  - Falha explícita (exit code != 0) se o PDF estiver corrompido
PROIBIÇÕES:
  - Não acessa rede
  - Não modifica o arquivo original
```

### 2.2 Contrato do Pipeline: `md_to_estudo.py`

```
ENTRADA:  arquivo .md (path) + schema JSON (path)
SAÍDA:    arquivo estudo_estruturado.json validado pelo schema
GARANTIAS:
  - JSON válido contra o schema (validação com jsonschema)
  - Pelo menos 1 capítulo identificado
  - Nenhum versículo inventado (verificação via RAG bíblico)
PROIBIÇÕES:
  - Não acessa banco de dados
  - Não escreve no ChromaDB
  - Não acessa rede (apenas Ollama local via HTTP)
```

### 2.3 Contrato do RAG Bíblico

```
COLEÇÃO: "biblia_pt_br"
QUERY:   texto em português natural
SAÍDA:   lista de versículos (livro, capítulo, versículo, texto, tradução)
GARANTIAS:
  - Retorna somente versículos do corpus (ARC + NVI)
  - Nenhum conteúdo gerado/inventado
  - Score de similaridade mínimo: 0.75
```

---

## 3. Estrutura de Diretórios da Fase 0

```
david_pastoral/
├── docker-compose.yml
├── .env.example
├── admin_module/
│   └── pipeline/
│       ├── pdf_to_md.py
│       ├── md_to_estudo.py
│       ├── embeddings.py
│       └── schemas/
│           └── estudo_estruturado.schema.json
├── david_agent/
│   ├── config.yaml
│   └── system_prompt.py
├── rag/
│   ├── chromadb/          (volume Docker)
│   ├── biblia/
│   │   ├── load_biblia.py
│   │   └── sources/
│   │       ├── biblia_arc.json
│   │       └── biblia_nvi.json
│   └── benchmark/
│       └── test_rag_qualidade.py
└── requirements.txt
```

---

## 4. Docker Compose da Fase 0

```yaml
version: "3.9"

services:

  postgres:
    image: postgres:16-alpine
    environment:
      POSTGRES_DB: david_pastoral
      POSTGRES_USER: david
      POSTGRES_PASSWORD: ${POSTGRES_PASSWORD}
    volumes:
      - postgres_data:/var/lib/postgresql/data
    ports:
      - "5432:5432"
    healthcheck:
      test: ["CMD-SHELL", "pg_isready -U david"]
      interval: 10s
      timeout: 5s
      retries: 5

  chromadb:
    image: chromadb/chroma:latest
    volumes:
      - chroma_data:/chroma/.chroma/index
    ports:
      - "8000:8000"
    environment:
      ANONYMIZED_TELEMETRY: "false"

  ollama:
    image: ollama/ollama:latest
    volumes:
      - ollama_models:/root/.ollama
    ports:
      - "11434:11434"
    deploy:
      resources:
        reservations:
          devices:
            - capabilities: [gpu]  # Remove se não tiver GPU
    healthcheck:
      test: ["CMD", "curl", "-f", "http://localhost:11434/api/tags"]
      interval: 30s
      timeout: 10s
      retries: 3

volumes:
  postgres_data:
  chroma_data:
  ollama_models:
```

---

## 5. Script de Benchmark de Qualidade do RAG

```python
# rag/benchmark/test_rag_qualidade.py

PERGUNTAS_BENCHMARK = [
    {
        "pergunta": "O que João 3:16 diz?",
        "versiculo_esperado": "João 3:16",
        "palavras_chave": ["Deus", "amou", "mundo", "Filho", "vida eterna"]
    },
    {
        "pergunta": "Cite versículos sobre oração",
        "minimo_resultados": 3,
        "verificacao": "todos_existem_no_corpus"
    },
    {
        "pergunta": "O que a Bíblia diz sobre fé?",
        "minimo_resultados": 2,
        "verificacao": "todos_existem_no_corpus"
    },
    {
        "pergunta": "Qual o maior mandamento?",
        "versiculo_esperado": "Mateus 22:37",
        "palavras_chave": ["amarás", "Senhor", "teu Deus"]
    },
    {
        "pergunta": "Futebol brasileiro",
        "esperado": "sem_resultado_relevante",
        "score_maximo": 0.5  # não deve retornar matches acima de 0.5
    }
]
```

---

## 6. Pontos em aberto — TODOS RESPONDIDOS ✅

| ID | Pergunta | Resposta |
|----|----------|----------|
| P01 | GPU na VPS? | Sem GPU — Ollama CPU-only, modelo ajustado para `gemma2:9b` |
| P02 | GPU disponível? | Sem GPU — `marker-pdf` roda em CPU (modo CPU-only confirmado pelo projeto) |
| P03 | Corpus bíblico? | `github.com/ameisehaufen/BibleMarkdown` — Bíblia em Markdown, converter para JSON |
| P04 | Ambiente de dev? | Windows local + WSL2 para Hermes Agent; pipeline Python no Windows nativo |

**Livro-piloto para teste do pipeline:** `F:\ESTUDOS_BIBLICOS\Grudem_Doutrina_Biblica`

> Spec pronta para avançar ao design.md e ao Bloco A.

---

## 7. Referências

- `planejamento/DAVID-PASTORAL-PLATAFORMA.md`
- `fases/fase-0-fundacao/prd.md`
- [marker-pdf — GitHub](https://github.com/VikParuchuri/marker)
- [ChromaDB Docs](https://docs.trychroma.com/)
- [Hermes Agent — GitHub](https://github.com/NousResearch/hermes-agent)
- [sentence-transformers paraphrase-multilingual-MiniLM-L12-v2](https://huggingface.co/sentence-transformers/paraphrase-multilingual-MiniLM-L12-v2)
