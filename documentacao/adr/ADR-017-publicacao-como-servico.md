# ADR-017: A publicação como serviço (MCP), com os agentes como clientes

- **Status:** **Proposed** — aguarda o aceite do ARQUITECT.
- **Data:** 2026-10-19
- **Decisores:** ARQUITECT (Eduardo) · redação do PLANNER
- **Gatilho:** Operação — a ADR-016 delegou a publicação a um "perfil com shell"; a lista fechada virou regra de conduta, não controle
- **Emenda:** [ADR-016](ADR-016-delegacao-de-publicacao-ao-deploy.md) (o executor passa a ser o **serviço**; os agentes são clientes)
- **Mantém:** ADR-008, ADR-009, o CI como caminho, o aceite de release

---

## Contexto

A ADR-016 delegou a publicação ao perfil DEPLOY. Hoje "perfil DEPLOY" significa **um agente
com shell, a chave e uma lista fechada** — e isso tem dois problemas:

1. **A lista é confiança, não controle.** O agente tem o shell; a proibição de `docker run`
   para ler arquivo, de `rm`, de restaurar banco é *política*. Um erro de julgamento do
   modelo, ou uma instrução mal interpretada, não encontra barreira técnica.
2. **O executor é acoplado ao processo.** Trocar o runtime (Codex, subagente, o PLANNER)
   reescreve o procedimento.

O experimento real (o deploy da `v0.1.0` pelo pipeline) mostrou o oposto do medo: quando o
processo é **determinístico**, um modelo no meio não agrega — só adiciona superfície.

## Decisão

**A publicação é um SERVIÇO** — um servidor MCP local que expõe **quatro ferramentas** — e os
agentes (PLANNER, DEVS, Codex, subagentes) são **clientes** dele.

| Ferramenta | Efeito | Gates que o **serviço** verifica antes |
|---|---|---|
| `publicar(tag)` | dispara/acompanha o pipeline e reporta | a tag está no `main` (release aceito); o backup veio com `sha256` válido; o HTTP final |
| `estado()` | o último run, a versão no ar, os backups | — |
| `rollback(tag)` | `publicar(tag-anterior)` | a tag existiu e foi publicada antes |
| `diagnostico()` | containers, logs, espaço — read-only | — |

**O que não existe como ferramenta não tem como ser feito pelo serviço.** Exclusão de
dados, restauração de banco, migração, seed/importação, infraestrutura, rotação de chave e
leitura de segredo **não são ferramentas** — a lista fechada da ADR-016 deixa de ser regra de
conduta e passa a ser **superfície de API**.

## Consequências

**Positivas**
- O shell do agente **deixa de ser necessário** para publicar; a chave fica com o serviço.
- **Auditoria em um ponto**: cada chamada (autor, argumentos, resultado) vai para a jornada.
- **Executor intercambiável**: o serviço não sabe nem precisa saber quem chamou. Codex, o
  PLANNER ou um subagente usam a mesma interface.
- A allowlist é **executável** — e testável (um teste que prova que a ferramenta proibida
  não existe).

**Negativas / trade-offs**
- **Superfície nova**: transporte MCP, plugin do harness, um processo a manter.
- **Ponto único** de abuso e de falha → mitigado pela jornada, pelos gates e pela chave
  restrita ao `didasko-deploy-entry`.
- O modo `diagnostico` expõe logs: o serviço **filtra** o que devolve (nada de `.env`,
  nada de segredo).

**Neutras**
- O caminho de publicação continua o mesmo (o CI + o script de entrada); muda **quem tem a
  chave**: o serviço, não o agente.
- O aceite de release continua do ARQUITECT; a tag continua nascendo do release.

## O que muda na ADR-016

O "perfil DEPLOY" passa a significar **quem opera o serviço** (a conta que o executa). A
autorização de publicação pertence ao **serviço**; os agentes **chamam**. A ADR-016 permanece
no que importa: o CI publica, o aceite é do ARQUITECT, a lista fechada continua fechada —
agora na API.

## Segurança e confiança

- o serviço roda com a **chave operacional restrita** ao `didasko-deploy-entry` (ADR-015);
- os agentes **nunca** veem a chave — eles chamam uma ferramenta;
- o serviço registra **quem** chamou (o cliente), para a auditoria ser rastreável;
- o serviço **não** expõe `exec`, `shell` nem comando arbitrário — por construção.

## Referências

- [ADR-015](ADR-015-acesso-operacional-do-agente.md) · [ADR-016](ADR-016-delegacao-de-publicacao-ao-deploy.md)
- Runbook de deploy/rollback · DEM-202610-013 (a construção do serviço)
