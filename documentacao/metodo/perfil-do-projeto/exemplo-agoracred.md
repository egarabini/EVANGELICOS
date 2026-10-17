# Perfil do Projeto — AgoraCred / AI Sustentação Hub (exemplo preenchido)

> **Exemplo real** do projeto de origem deste método, para servir de referência de preenchimento. Não é normativo para o seu projeto — é o perfil **de outro** projeto. Copie a **estrutura**, não os valores.

## 1. Identidade

- **Nome do projeto:** AC_SUSTENTACAO — AI Sustentação Hub
- **Objetivo em uma frase:** orquestrador de IA que automatiza a sustentação (triagem de tickets, base de conhecimento), com processamento 100% local.
- **Empresa / contexto:** AgoraCred (financeira).
- **Idioma de documentação e código:** pt-BR.

## 2. Papéis (instâncias)

| Papel | Instância |
|---|---|
| ARQUITECT | Eduardo (humano) |
| PLANNER | IA condutora (assistente de código) |
| DEVS | agente de código (ex.: CODEX) ou humano |
| EVAL | IA (execução de testes/runtime) |
| VISION | IA com navegador real |
| DEPLOY | IA (GitFlow no Azure DevOps) |
| KNOW | latente (base consultável via MCP — fase futura) |
| ORCHESTRATOR | latente (roteador — adiado) |

## 3. Stack e tecnologias

- **Linguagem / runtime:** .NET 10 (C#). Exceção: Python, exclusivamente para orquestração governada de IA, atrás de contrato.
- **Framework de aplicação:** .NET Aspire.
- **UI / front:** Blazor Web App (Interactive Server) + MudBlazor; gráficos em ApexCharts.
- **Persistência / banco:** PostgreSQL + pgvector (`vector(1024)`); Oracle read-only (bases corporativas).
- **Orquestração / infra:** Aspire (AppHost); Kestra para workflows.
- **IA / modelos:** Ollama local (`llama3.1`, `mxbai-embed-large`); MCP entre serviços.
- **Restrição de stack ("não trocar"):** .NET 10 + Aspire. Python só para IA governada, sem regra de negócio.

## 4. Segurança e dados sensíveis

- **Requisitos legais:** LGPD.
- **Onde vivem os segredos:** user-secrets / variáveis de ambiente. **Nunca** em `appsettings.json` ou no repo.
- **Dados que nunca podem vazar:** connection strings, tokens, payload cifrado, material de chave — nem em log, exceção, cookie ou UI.
- **Restrições de IA:** sem LLM em cloud para dado sensível — só Ollama local. Não persistir/logar conteúdo bruto de ticket.
- **Fontes read-only / intocáveis:** GLPI (leitura); a `api` existente, `AppDbContext`/migrations e a coluna `vector(1024)` fora de spec aprovada.

## 5. Ambientes e GitFlow

- **Branch de produção:** `master` (cumpre o papel de `main`, por ser o default do Azure DevOps).
- **Branch de integração:** `develop`.
- **Ambientes:** dev (notebook) / homologação (VM exclusiva) / produção (rede interna).
- **Homologação em estado limpo:** script de limpeza que zera volumes/dados do stack antes de validar.
- **Backup pré-release:** banco + key-ring pareados com checksum SHA256, antes de promover.

## 6. Rastreio e commits

- **Sistemas de rastreio:** Azure DevOps (Boards) + GLPI (tickets).
- **Trailers de commit:** `AB#<workitem>` (link nativo Azure) e `GLPI#<ticket>` (ou `000000`), mais o id da DEM.
- **Formato do id da DEM:** `DEM-AAAAMM-VSTS<nº>-GLPI<nº>-<seq>-<slug>`.

## 7. Testes

- **Framework:** testes .NET (xUnit).
- **Rastreabilidade requisito ↔ teste:** o nome do teste referencia o RF (`Test_RF03_...`).
- **Critério de conclusão:** todo RF implementado tem teste; caminho feliz + erro/edge por endpoint novo.

## 8. Observabilidade

- **Instrumentação:** OpenTelemetry via Aspire ServiceDefaults (logs/traces/métricas).
- **Onde se lê:** dashboard do Aspire (traces `POST /mcp`, health checks).

## 9. Custo / métricas

- **Fonte de tokens/custo:** gateway de custo LLM (quando disponível) — derivado, não estimado.
- **Painel de DEMs:** `documentacao/arquiteturaV1/demandas/_dashboard.md`.

## 10. ADRs registradas (extrato)

| ADR | Assunto | Status |
|---|---|---|
| ADR-001 | Stack de IA e modelo de embedding | Accepted |
| ADR-002 | Estratégia de branches (GitFlow) | Accepted |
| ADR-005 | Guard-rails de agentes | Accepted |
| ADR-008 | Estrutura única de DEM | Accepted |
| ADR-014 | Orquestração de IA governada (LangGraph) | Accepted |
| ADR-015 | Camada INTENT como gate de objetivo | Accepted |

> No projeto de origem, o método vive em duas camadas históricas: `arquiteturaV1/` (papéis, ADRs, estrutura) e `arquiteturaV2/` (camada INTENT). Este pacote `metodo/` é a **fusão neutralizada** das duas.
