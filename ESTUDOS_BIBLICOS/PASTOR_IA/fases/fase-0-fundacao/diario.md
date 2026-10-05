# Diario de Desenvolvimento -- Fase 0 Fundacao

## 2026-07-15 / 16 -- Marco: Pipeline RAG + Agente DAVID operacional

### O que foi feito

**Bloco A -- Ambiente**
- [x] Docker 29.6.1, Python 3.14, Git 2.53 verificados
- [x] `.venv` criado com todas as dependencias (torch, chromadb, sentence-transformers, openai, pymupdf, rich, typer)
- [x] Bug Pillow cp1252: resolvido fixando `Pillow>=11.0.0` (Python 3.14 requer Pillow 12.x)
- [x] Conflito de portas: PostgreSQL 5432 ocupada pelo intellicare -- ajustado para 5433
- [x] ChromaDB na porta 8001 (8000 ocupada)
- [x] Ollama reaproveitado: `intellicare-ollama` na porta 11434 (publica)

**Bloco B -- Modelo LLM**
- [x] `hermes3:8b` (NousResearch, 4.7GB) baixado no `intellicare-ollama`
- [x] Descoberta: `hermes-ollama` ja tinha hermes3:8b instalado (projeto Hermes ja existente)

**Bloco C -- RAG Biblico**
- [x] BibleMarkdown clonado em `rag/biblia/sources/BibleMarkdown`
- [x] Parser reescrito para formato real: `**N** \tTexto`
- [x] Bug corrigido: `43N-Joa` (nao `43N-Jo`), `31A-Ob` (nao `31A-Ab`)
- [x] **31.102 versiculos ACF 2007 indexados no ChromaDB**
- [x] Benchmark: Joao 3:16 score=0.837-0.932, Genesis 1:1 score=0.961, 1Ts 5:17 score=0.920

**Bloco D -- Agente DAVID**
- [x] `agent/david_agent.py`: pipeline RAG -> prompt -> hermes3:8b -> resposta
- [x] System prompt inspirado em David Livingstone
- [x] `agent/cli_david.py`: interface terminal rich
- [x] RAG validado: Joao 3:16 aparece em #1 com score=0.837

### Proximos passos (Fase 1)
1. [ ] Validar conversa completa DAVID (LLM response via Ollama)
2. [ ] Processar livro piloto Grudem (PDF -> MD -> estudo)
3. [ ] Modulo admin (upload, aprovacao, disponibilizacao)
4. [ ] Dashboard do gestor
5. [ ] Interface web do DAVID (chat UI)
