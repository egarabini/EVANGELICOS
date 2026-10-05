# DAVID Pastoral — Plataforma de Discipulado Digital

> *"Discipulado em escala. Com alma."*
> Batizado em honra de **David Livingstone** (1813–1873).

## O que é este projeto

Plataforma SaaS de discipulado digital para igrejas, composta por:

- **Agente DAVID** — IA com memória persistente que guia cada membro individualmente via Telegram/WhatsApp (powered by Hermes Agent + Ollama)
- **Pipeline de Conteúdo** — Admin converte PDFs de livros aprovados em estudos estruturados (RAG)
- **Dashboard Pastoral** — Pastores e gestores acompanham em tempo real o crescimento espiritual de cada membro

## Hierarquia de Papéis

```
Administrador (plataforma)
  └── Gestor (organização / igreja)
        └── Pastor / Líder (grupo / célula)
              └── Membro (interage com DAVID via chat)
```

## Documentação Principal

| Documento | Descrição |
|---|---|
| [DAVID-PASTORAL-PLATAFORMA.md](./planejamento/DAVID-PASTORAL-PLATAFORMA.md) | Estudo completo de implementação |
| [fase-0/prd.md](./fases/fase-0-fundacao/prd.md) | PRD da Fase 0 — Fundação |
| [fase-0/spec.md](./fases/fase-0-fundacao/spec.md) | Spec técnica da Fase 0 |
| [fase-0/tasks.md](./fases/fase-0-fundacao/tasks.md) | Tasks da Fase 0 |

## Roadmap de Fases

| Fase | Descrição | Status |
|---|---|---|
| **0** | Fundação — Docker + Ollama + Pipeline PDF→MD + RAG Bíblico | 🟡 Em planejamento |
| **1** | DAVID Conversacional — Telegram + System Prompt + Skills | ⏳ Aguardando Fase 0 |
| **2** | Dashboard Base — Pastor vê progresso em tempo real | ⏳ Aguardando Fase 1 |
| **3** | Módulo Admin — Interface de upload e aprovação | ⏳ Aguardando Fase 2 |
| **4** | Comportamentos Proativos — Check-ins, silêncio, marcos | ⏳ Aguardando Fase 3 |
| **5** | Multi-tenant + Multi-plataforma | ⏳ Aguardando Fase 4 |
| **6** | Hardening e Produção | ⏳ Aguardando Fase 5 |

## Stack Tecnológica

- **Agente:** Hermes Agent (NousResearch · MIT) + Ollama
- **LLM:** mistral-nemo ou gemma2:9b (PT-BR fluente, self-hosted)
- **RAG:** ChromaDB + sentence-transformers
- **Pipeline:** PyMuPDF + marker-pdf + pypandoc
- **Backend:** FastAPI (Python)
- **Dashboard:** Vue 3 + Vite
- **Banco:** PostgreSQL (multi-tenant)
- **Infra:** Docker + Traefik (VPS Contabo)
- **Gateway:** Hermes Gateway (Telegram / WhatsApp / Discord)

## Metodologia

Este projeto segue **Spec-Driven Development (SDD)**.

> Nenhuma linha de código sem `prd.md` + `spec.md` + `design.md` aprovados.

Sequência obrigatória por fase:
`olpf.md` → `prd.md` → `spec.md` → `design.md` → `tasks.md` → `plano-testes.md` → `diario.md` → `changelog.md`
