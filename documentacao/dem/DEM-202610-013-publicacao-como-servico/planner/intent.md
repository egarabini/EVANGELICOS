# Intent: DEM-202610-013 / publicacao-como-servico

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: ADR-017 (Proposed) + a experiência do deploy da v0.1.0 pelo pipeline
signed_at:
supersedes: —
open_questions_open: 3
spec_citations: — (preenchido ao fechar a spec)

## 1. Problema

A publicação depende de um agente com **shell** e de uma **regra de conduta** (ADR-016). A
lista fechada não tem barreira técnica: o shell pode `rm`, `docker run` com mount, `psql`.
E o executor está acoplado ao processo — trocar o runtime reescreve o procedimento.

## 2. Outcome

**A publicação é um serviço com quatro ferramentas; os agentes são clientes.** A lista
fechada vira **superfície de API**: o que não é ferramenta não existe. O serviço executa,
verifica os gates e registra; o agente (o PLANNER, o Codex, um subagente) só chama.

## 3. Afetados

O ARQUITECT (o aceite de release continua dele), os perfis PLANNER/DEVS/DEPLOY, o runbook e a
DEM-004 (o pipeline que o serviço aciona).

## 4. Escopo

**In**
- servidor **MCP local** com as ferramentas `publicar`, `estado`, `rollback`, `diagnostico`;
- **gates no serviço**: a tag em `main`, o backup com `sha256`, o HTTP, a idempotência;
- a **jornada** por chamada (autor, argumentos, resultado);
- a **chave do serviço** (restrita ao `didasko-deploy-entry`) e o comando `diag` no script
  de entrada (para o `diagnostico` não precisar de shell);
- a config do MCP no harness.

**Out (non-goals)**
- o **Codex como DEVS** — é a DEM-014 (piloto);
- transferir o **dump** como artifact (follow-up da DEM-004);
- qualquer operação destrutiva (segue exigindo autorização do ARQUITECT);
- substituir o CI: o serviço **aciona** o CI; não publica por fora dele.

## 5. Constraints

- **A chave fica com o serviço**, nunca com o agente (ADR-015).
- O serviço **não expõe** `exec`/`shell`/comando arbitrário.
- O CI continua sendo o caminho de publicação; o serviço o **dispara e lê**.
- Nenhum segredo no repositório (ADR-008); o `.env` não é lido pelo serviço.
- O aceite de release continua do ARQUITECT (a tag nasce do release).

## 6. Health metrics

- **H-01** · a suíte continua verde · baseline **113 testes** · porteiro **EVAL**
- **H-07** · `estado()` e `diagnostico()` respondem sem publicar · baseline **não existe** · porteiro **EVAL**
- **H-08** · `publicar(tag já publicada)` é seguro (não republica à toa) · baseline **não existe** · porteiro **EVAL**
- **H-09** · ferramenta proibida **não existe** (teste que prova a ausência) · porteiro **EVAL**

## 7. Sinal de sucesso

O ARQUITECT pede "publica a v0.1.1"; um **agente qualquer** chama a ferramenta e o serviço
faz o resto; a jornada mostra quem chamou, o que foi verificado e o resultado. Nenhum agente
teve acesso a shell na VPS.

## 8. Decisões já registradas

| # | Questão | Decisão |
|---|---|---|
| 8.1 | O executor | O **serviço** (ADR-017); os agentes são clientes |
| 8.2 | O caminho | O CI (o serviço aciona e lê), não publicação direta |

## 9. Perguntas abertas — só o ARQUITECT fecha

- [ ] **9.1** O transporte: MCP **local (stdio)** no harness — confirmar o caminho de configuração do plugin.
- [ ] **9.2** O serviço roda **como o seu usuário** (a sessão) ou como **serviço do sistema** (systemd/Windows Service)? *Recomendação: começar como processo local; virar serviço quando estabilizar.*
- [ ] **9.3** A chave do serviço: **reutilizar** a operacional (restrita ao `entry`) ou **criar uma nova** dedicada ao serviço? *Recomendação: nova, e a operacional é revogada — assim o agente não tem chave nenhuma.*

## 10. Fora de julgamento

O framework MCP, o idioma (Python stdio), o formato do log, a organização interna do código.
