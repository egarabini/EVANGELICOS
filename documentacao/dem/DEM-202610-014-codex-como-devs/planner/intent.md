# Intent: DEM-202610-014 / codex-como-devs

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: decisão do ARQUITECT de 2026-10-19 (o Codex como DEVS, piloto na DEM-012)
signed_at:
supersedes: —
open_questions_open: 2
nivel_agil: 1 — é um experimento de processo, não código de produto

## 1. Problema

O papel **DEVS** é executado por **um único runtime** (o subagente DeepSeek). Não há dado de que
ele seja o melhor executor — nem de que um modelo diferente cometeria menos defeitos, levaria menos
rodadas de EVAL ou entregaria um diff mais limpo.

## 2. Outcome

**Um dado comparável**: o **Codex** implementa a **DEM-012** como DEVS, o **EVAL cego** julga pelo
mesmo plano de testes, e o resultado (rodadas, defeitos, tempo, aderência aos guardas) fica
registrado e comparável ao histórico do subagente.

## 3. Afetados

O PLANNER (escreve o parecer e compara), o ARQUITECT (lê o resultado e decide o futuro do papel
DEVS), e as DEMs seguintes (que podem usar o executor escolhido).

## 4. Escopo

**In**
- o **despacho** do Codex: o que ele recebe (os guardas + o pacote da DEM-012 + o repositório);
- a **execução** da DEM-012 por ele (branch + PR, sem publicar);
- o **julgamento** pelo EVAL cego, com o plano da DEM-012;
- o **parecer comparativo** do PLANNER (as métricas da tabela);
- o **registro** no `README.md` desta DEM.

**Out (non-goals)**
- trocar o DEVS oficialmente (é decisão posterior, com o dado na mão);
- o Codex como **DEPLOY** (a publicação é do serviço/pipeline — ADR-016/017);
- deixar o Codex publicar, mexer em chave, segredo, VPS ou CI.

## 5. Constraints

- O **mesmo** EVAL, o **mesmo** plano, a **mesma** DEM — a comparação só vale assim.
- O Codex **não** altera os guardas, o CI, o deploy nem os segredos.
- O resultado é **registrado**, inclusive se for ruim.
- O piloto é de **processo** (nível 1): não muda a arquitetura.

## 6. Health metrics

- **H-12** · as 5 métricas do piloto registradas (rodadas, defeitos, tempo, aderência, diff) · baseline: o histórico da 001/002/003 · porteiro **ARQUITECT**
- **H-01** · a suíte da DEM-012 (a mesma exigência de antes)

## 7. Sinal de sucesso

O parecer responde, com número: **o Codex precisou de mais ou menos rodadas de EVAL que o
subagente nas DEMs comparáveis?** Qualquer resposta é sucesso — a ausência de resposta é fracasso.

## 8. Decisões já registradas

| # | Questão | Decisão |
|---|---|---|
| 8.1 | A DEM do piloto | **DEM-012** (credencial de seed) |
| 8.2 | Quem julga | o **EVAL cego** de sempre, pelo plano da 012 |
| 8.3 | O que o Codex pode | branch + PR; **não** publica, **não** toca em segredo/VPS/CI |

## 9. Perguntas abertas — só o ARQUITECT fecha

- [ ] **9.1** O **despacho**: o Codex roda na **sua máquina** (a sessão, com o `codex exec`) ou há um ambiente próprio? *Recomendação: na máquina, com o repositório local, sem credencial de deploy.*
- [ ] **9.2** O **modelo/auth** do Codex: usa a conta/modelo que você já tem configurado? *Preciso saber para não prometer um piloto que não roda.*

## 10. Fora de julgamento

O prompt do despacho, o formato do parecer, as ferramentas que o Codex usa.
