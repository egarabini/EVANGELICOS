# Tasks — Fase 0: Fundação da Plataforma DAVID Pastoral

**Data:** 2026-07-15
**Status:** Aguardando aprovação do PRD e Spec
**Sprint estimado:** 2 semanas

---

## Pré-condições para iniciar

- [ ] PRD da Fase 0 aprovado
- [ ] Spec da Fase 0 aprovada
- [ ] Pontos em aberto P01-P04 da spec respondidos

---

## BLOCO A — Ambiente e Infraestrutura

### A1 — Verificar ambiente de desenvolvimento

- [ ] **A1.1** Confirmar se Hermes Agent roda nativo no Windows ou exige WSL2
  - Verificar aviso do site: "Native Windows support is experimental"
  - Decidir: usar WSL2 ou desenvolvimento na VPS diretamente
- [ ] **A1.2** Confirmar disponibilidade de GPU na VPS Contabo
  - Se sem GPU: ajustar Docker Compose (remover seção `devices`)
  - Se sem GPU: testar velocidade do Ollama com `mistral-nemo` em CPU
- [ ] **A1.3** Verificar requisitos de hardware do `marker-pdf`
  - Rodar em CPU-only? Quanto de RAM mínimo?

### A2 — Setup Docker Compose

- [ ] **A2.1** Criar `docker-compose.yml` conforme spec
- [ ] **A2.2** Criar `.env.example` com todas as variáveis necessárias
- [ ] **A2.3** Executar `docker-compose up` e validar saúde dos 3 serviços
  - PostgreSQL: `pg_isready` retorna OK
  - ChromaDB: `GET /api/v1/heartbeat` retorna 200
  - Ollama: `GET /api/tags` retorna 200
- [ ] **A2.4** Pull do modelo Ollama: `ollama pull mistral-nemo`
- [ ] **A2.5** Teste rápido Ollama: `ollama run mistral-nemo "Diga olá em português"`

**Critério de conclusão do Bloco A:** `docker-compose up` sobe tudo, todos os healthchecks passam, Ollama responde em PT-BR.

---

## BLOCO B — Pipeline de Conteúdo

### B1 — Instalar dependências do pipeline

- [ ] **B1.1** Criar `requirements.txt` com:
  - `marker-pdf`
  - `pymupdf`
  - `pypandoc`
  - `chromadb`
  - `sentence-transformers`
  - `openai` (cliente compatível com Ollama)
  - `jsonschema`
  - `python-dotenv`
- [ ] **B1.2** Criar ambiente virtual: `python -m venv .venv`
- [ ] **B1.3** Instalar: `pip install -r requirements.txt`

### B2 — Implementar `pdf_to_md.py`

- [ ] **B2.1** Implementar conversão com `marker-pdf` como primário
- [ ] **B2.2** Implementar fallback para `PyMuPDF` se marker falhar
- [ ] **B2.3** Testar com PDF de livro real (ex: um dos PDFs em `F:\ESTUDOS_BIBLICOS\`)
- [ ] **B2.4** Validar: output `.md` tem pelo menos 5 cabeçalhos `#` ou `##`
- [ ] **B2.5** Validar: texto perdido < 2% (comparar contagem de palavras PDF vs MD)

### B3 — Criar schema JSON do estudo

- [ ] **B3.1** Criar `schemas/estudo_estruturado.schema.json` (JSON Schema completo)
- [ ] **B3.2** Testar validação com `jsonschema` em Python

### B4 — Implementar `md_to_estudo.py`

- [ ] **B4.1** Implementar chamada ao Ollama com o prompt da spec
- [ ] **B4.2** Implementar parsing e validação do JSON gerado
- [ ] **B4.3** Testar com o MD gerado no B2.3
- [ ] **B4.4** Validar: JSON tem pelo menos 3 capítulos
- [ ] **B4.5** Validar: perguntas estão em PT-BR
- [ ] **B4.6** Validar: nenhum versículo inventado (verificação manual inicial)

**Critério de conclusão do Bloco B:** Pipeline completo processa `livro.pdf` → `livro.md` → `estudo_estruturado.json` com qualidade aceitável para revisão humana.

---

## BLOCO C — RAG Bíblico

### C1 — Obter corpus bíblico

- [ ] **C1.1** Localizar fonte JSON da Bíblia ARC (verificar licença — deve ser aberta)
  - Opções: `thiagobodruk/bíblia` no GitHub, `scrollmapper` ou similar
- [ ] **C1.2** Localizar fonte JSON da Bíblia NVI (verificar licença)
- [ ] **C1.3** Padronizar formato: `{"livro": str, "capitulo": int, "versiculo": int, "texto": str, "traducao": str}`
- [ ] **C1.4** Salvar em `rag/biblia/sources/biblia_arc.json` e `biblia_nvi.json`

### C2 — Implementar `load_biblia.py`

- [ ] **C2.1** Implementar carregamento por batches de 500 versículos
- [ ] **C2.2** Implementar geração de embeddings com `paraphrase-multilingual-MiniLM-L12-v2`
- [ ] **C2.3** Implementar inserção no ChromaDB na coleção `biblia_pt_br`
- [ ] **C2.4** Executar carga completa (ARC + NVI — ~62.000 versículos total)
- [ ] **C2.5** Validar: coleção `biblia_pt_br` tem os documentos esperados

### C3 — Implementar `embeddings.py` (para estudos)

- [ ] **C3.1** Implementar geração de embeddings para capítulos de estudos
- [ ] **C3.2** Implementar inserção em coleção isolada `org_{id}__estudo_{id}`
- [ ] **C3.3** Testar com o estudo estruturado gerado no Bloco B

**Critério de conclusão do Bloco C:** ChromaDB indexado com Bíblia completa. Query "O que João 3:16 diz?" retorna o versículo correto.

---

## BLOCO D — Hermes Agent Base

### D1 — Instalar Hermes Agent

- [ ] **D1.1** Clonar repositório: `git clone https://github.com/NousResearch/hermes-agent`
- [ ] **D1.2** Executar instalador: `./scripts/install.sh` (ou equivalente Windows/WSL2)
- [ ] **D1.3** Executar `hermes setup` — configurar com Ollama como provider
  - Provider: Custom API
  - Base URL: `http://localhost:11434/v1`
  - Model: `mistral-nemo`

### D2 — Configurar DAVID

- [ ] **D2.1** Criar `david_agent/config.yaml` conforme spec
- [ ] **D2.2** Criar `david_agent/system_prompt.py` com system prompt da spec
- [ ] **D2.3** Iniciar Hermes com config do DAVID
- [ ] **D2.4** Teste 1: Digitar "Bom dia" — DAVID responde de forma calorosa e pastoral
- [ ] **D2.5** Teste 2: Digitar "O que a Bíblia diz sobre amor?" — DAVID cita versículo real
- [ ] **D2.6** Teste 3: Digitar "Qual o resultado do Flamengo?" — DAVID recusa e redireciona

**Critério de conclusão do Bloco D:** Hermes + Ollama + DAVID system prompt funcionando via CLI.

---

## BLOCO E — Benchmark e Validação Final

- [ ] **E1** Executar `test_rag_qualidade.py` — todos os casos passam
- [ ] **E2** Documentar resultados no `diario.md`
- [ ] **E3** Registrar qualquer desvio da spec no `diario.md`
- [ ] **E4** Atualizar `changelog.md` com o que foi entregue

---

## Sequência recomendada

```
A1 (verificar ambiente)
  └── A2 (Docker up)
        └── B1 (instalar deps)
              ├── B2 → B3 → B4 (pipeline)
              └── C1 → C2 → C3 (RAG bíblico)
                    └── D1 → D2 (Hermes Agent)
                          └── E (benchmark final)
```

---

## Estimativa de tempo

| Bloco | Estimativa |
|---|---|
| A — Ambiente | 2-4h |
| B — Pipeline | 4-8h |
| C — RAG Bíblico | 4-6h |
| D — Hermes Agent | 2-4h |
| E — Benchmark | 1-2h |
| **Total** | **~1,5 semana** |
