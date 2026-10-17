# Perfil do Projeto — [Nome do Projeto]

> Preencha cada campo. Este documento é a fonte da verdade técnica do projeto; o método (o resto do pacote) é neutro e não repete nada daqui. Campo desconhecido → pergunta aberta → vira ADR.

## 1. Identidade

- **Nome do projeto:**
- **Objetivo em uma frase:**
- **Empresa / contexto:**
- **Idioma de documentação e código:** [ex.: pt-BR]

## 2. Papéis (instâncias)

Quem/qual ferramenta ocupa cada papel neste projeto (o método define os papéis; aqui você diz **quem**):

| Papel | Instância (humano / modelo / agente) |
|---|---|
| ARQUITECT | |
| PLANNER | |
| DEVS | |
| EVAL | |
| VISION | |
| DEPLOY | |
| KNOW | (opcional) |
| ORCHESTRATOR | (opcional) |

## 3. Stack e tecnologias

- **Linguagem(ns) / runtime:**
- **Framework de aplicação:**
- **UI / framework de front:**
- **Persistência / banco:**
- **Orquestração / infra:**
- **IA / modelos (se houver):**
- **Restrição de stack ("não trocar"):**

## 4. Segurança e dados sensíveis

- **Requisitos legais/regulatórios aplicáveis:** [ex.: LGPD/GDPR/HIPAA]
- **Onde vivem os segredos:** [ex.: user-secrets / cofre / variáveis de ambiente — NUNCA no repo]
- **Dados que nunca podem vazar (log/UI/URL):**
- **Restrições de IA (ex.: sem LLM em cloud para dado sensível):**
- **Fontes read-only / sistemas intocáveis:**

## 5. Ambientes e GitFlow

- **Branch de produção:** [main | master]
- **Branch de integração:** [develop]
- **Ambientes:** dev / homologação / produção — onde ficam?
- **Homologação em estado limpo:** como se zera o estado?
- **Backup pré-release:** o que é copiado e como (checksum)?

## 6. Rastreio e commits

- **Sistema(s) de rastreio:** [ex.: Azure DevOps / Jira / GitHub Issues / GLPI]
- **Trailers de commit:** [ex.: `AB#<id>`, `GLPI#<id>`]
- **Formato do id da DEM:** `DEM-AAAAMM-<...>-<seq>-<slug>`

## 7. Testes

- **Framework de teste:**
- **Rastreabilidade requisito ↔ teste:** [ex.: nome do teste referencia o RF]
- **Cobertura mínima / critério de conclusão:**

## 8. Observabilidade

- **Como se instrumenta (logs/traces/métricas):**
- **Onde se lê o comportamento em runtime:**

## 9. Custo / métricas

- **Fonte real de tokens/custo por tarefa (se houver):**
- **Painel de DEMs:** onde vive?

## 10. ADRs já registradas

| ADR | Assunto | Status |
|---|---|---|
| ADR-001 | | |
| ADR-002 | | |

## 11. Perguntas abertas do perfil

- [ ]
