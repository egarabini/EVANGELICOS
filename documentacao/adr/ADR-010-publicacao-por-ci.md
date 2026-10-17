# ADR-010: Publicação por CI/CD, nunca por agente

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

Até hoje **o agente executava o deploy em produção**: SSH na VPS + `sudo docker`
rodando `deploy/subir.sh`. Isso já derrubou o site uma vez (erro de tipagem que só
aparecia na compilação da página) e dá ao agente poder que ele não deve ter.

## Decisão

Quem publica é o **GitHub Actions**, no merge. O agente **cria branch, commita,
abre PR e lê o resultado dos testes**; no máximo, aciona o workflow manualmente quando
autorizado. A chave de deploy sai da máquina do agente e vira **GitHub Secret**.

## Consequências

**Positivas:**
- IA sem acesso a produção; toda publicação fica auditada no Actions.
- Homologação em estado limpo deixa de ser boa vontade.

**Negativas / trade-offs:**
- Exige construir o pipeline (workflows + runner + secrets) e aposentar o deploy por SSH.
- O `subir.sh` deixa de ser executável à mão e passa a ser o runbook do workflow.

## Impacto nas DEMs

- Toda DEM com deploy.
- **Aposenta** o caminho SSH atual; a chave `didasko_deploy` deve ser revogada após a migração.
