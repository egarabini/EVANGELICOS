# Perfil do Projeto — Didasko

> Fonte da verdade técnica. O método é neutro e não repete nada daqui.

## 1. Identidade

- **Nome:** Didasko — Estudos Bíblicos Dirigidos
- **Objetivo em uma frase:** conduzir estudos bíblicos dirigidos com trilha por capítulo, correção humana e IA de apoio, sem nunca inventar Escritura.
- **Contexto:** projeto do Eduardo, para igrejas/escolas (multi-tenant por instituição).
- **Idioma:** documentação **pt-BR com acentuação**; código e comentários **sem acento** (padrão histórico do repo).

## 2. Papéis (instâncias)

| Papel | Instância |
|---|---|
| ARQUITECT | Eduardo (humano) |
| PLANNER | IA condutora (esta) |
| DEVS | IA, em contexto próprio ou subagente |
| EVAL | subagente cego (não lê a jornada do DEVS) |
| VISION | Eduardo (não há navegador automatizado disponível) |
| DEPLOY | GitHub Actions; o agente só abre PR e lê o resultado |
| KNOW / ORCHESTRATOR | não usados |

## 3. Stack e tecnologias

- **Linguagem/runtime:** Python 3.12
- **Framework de aplicação:** Reflex 0.9.5 (front e back na mesma linguagem)
- **Persistência:** PostgreSQL 16 (SQLModel/SQLAlchemy)
- **Busca semântica:** ChromaDB (corpus bíblico, 31.102 versículos)
- **IA local:** Ollama, modelo `gemma2:9b` (VPS sem GPU)
- **Infra:** Docker Compose + Traefik (HTTPS/Let's Encrypt) na VPS Contabo
- **Testes:** pytest
- **Restrição de stack ("não trocar"):** nada de Node/TS na **aplicação**. Node existe apenas dentro da imagem, para o build do frontend do Reflex.

## 4. Segurança e dados sensíveis

- **Requisito legal:** LGPD.
- **Segredos:** `.env` na VPS (nunca no repositório) e GitHub Secrets para o CI.
- **Dados que não podem vazar:** senhas (bcrypt), CPF, endereço e telefone de usuários.
- **Restrição de IA:** o LLM local recebe a Escritura já recuperada do corpus, nunca dados pessoais.
- **Sistemas intocáveis:** o corpus bíblico (montado `:ro`) e o backup do banco.

## 5. Ambientes e GitFlow

- **Produção:** `main` (tags SemVer) → VPS `didasko.app.br`
- **Integração:** `develop`
- **Homologação:** **não existe** (pergunta aberta do perfil)
- **Estado limpo:** `docker compose down -v` + seed + importadores
- **Backup pré-release:** `pg_dump` + volume do Postgres, pareados com checksum

## 6. Rastreio e commits

- **Sistema de rastreio:** nenhum tracker externo (ADR-009). O slot `<tracker>` do id fica reservado.
- **Formato do id:** `DEM-AAAAMM-<seq>-<slug>`
- **Trailers de commit:** `DEM-AAAAMM-<seq>`
- **Commits:** Conventional Commits

## 7. Testes

- **Framework:** pytest (76 testes na adoção do método)
- **Rastreabilidade:** o nome do teste referencia o requisito (`test_rf03_...`)
- **Critério de conclusão:** todo RF da spec com teste correspondente; página compila (`tests/test_paginas.py`)

## 8. Observabilidade

- **Hoje:** logs do `docker compose`; verificação HTTP no fim do `subir.sh`.
- **Lacuna conhecida:** ninguém é avisado quando o site cai. Candidata a DEM futura.

## 9. Custo / métricas

- **Tokens:** não medidos.
- **Tempo:** não medido — a jornada registra apenas **data**, para histórico.
- **Painel de DEMs:** `documentacao/README.md`

## 10. ADRs vigentes

| ADR | Assunto | Status |
|---|---|---|
| ADR-001 | Stack fixa (Python/Reflex) | Accepted |
| ADR-002 | Corpus bíblico local, não redistribuído | Accepted |
| ADR-003 | Escritura por igualdade, não por similaridade | Accepted |
| ADR-004 | Referências cruzadas do OpenBible e sua curadoria | Accepted |
| ADR-005 | Modelo Obra + Adendos → Estudo | Accepted |
| ADR-006 | Guard-rails de agente + TLC + arquivos de guarda | Accepted |
| ADR-007 | Estrutura de DEM + gate INTENT | Accepted |
| ADR-008 | Segredos e a pendência das senhas de demonstração | Accepted |
| ADR-009 | GitFlow e revisão por Copilot Enterprise | Accepted |
| ADR-010 | Publicação por CI/CD, nunca por agente | Accepted |
| ADR-011 | Aprovação de conteúdo assinada e amarrada ao hash | Accepted |

## 11. Perguntas abertas do perfil

- [ ] Homologação: criar ambiente? Onde?
- [ ] Runner do Actions: GitHub-hosted + SSH (recomendado) ou self-hosted na VPS (descartado por repo público)?
- [ ] `gh` autenticado: quem autentica e com qual escopo?
- [ ] E-mail transacional: domínio próprio?
- [ ] Senhas de demonstração: quando são trocadas? (ADR-008)
