# DEM-202610-014 — O Codex como DEVS (piloto)

## Finalidade

**Medir** o Codex como executor do papel **DEVS** numa DEM real, com o **EVAL cego** julgando — e
comparar com o histórico do DEVS anterior (o subagente DeepSeek). O resultado vira **dado**, não
opinião.

## O piloto

- **A DEM escolhida: a [DEM-202610-012](../DEM-202610-012-credencial-de-seed/planner/intent.md)**
  (credencial de seed) — pequena, de segurança, com teste binário. O EVAL tem como julgar sem
  ambiguidade, e o escopo cabe num contexto.
- **O que o Codex recebe**: os guardas (`ESTUDOS_BIBLICOS/GSI_EBD/AGENTS.md` + `CONVENTIONS.md`),
  o pacote da DEM-012 (`intent`, `spec`, `plano-testes`) e o acesso ao repositório.
- **O que o Codex NÃO faz**: publicar (ADR-016); alterar os guardas, o CI ou o deploy; tocar em
  segredo ou VPS. Ele **commita numa branch e abre o PR** — o gate da ADR-009.
- **O EVAL julga sem saber quem implementou** (o mesmo EVAL cego de sempre).

## As métricas (o dado do piloto)

| Métrica | Como se mede | Onde se registra |
|---|---|---|
| **Rodadas de EVAL** | quantas rodadas até o PASS | `eval/jornada.md` da DEM-012 |
| **Defeitos** | cada FAIL, por categoria | a mesma jornada |
| **Tempo** | início/fim da execução (data) | `dev/jornada.md` da DEM-012 |
| **Aderência aos guardas** | violou alguma regra (escopo, acento no código, `subir.sh`, segredo)? | o parecer do PLANNER sobre o diff |
| **Qualidade do diff** | o que mudou **além** do escopo | o mesmo parecer |

## A comparação (honesta)

A DEM-012 é a **primeira** execução — não existe um par "subagente × Codex na mesma DEM". A
comparação é contra o **histórico** do subagente nas DEMs de porte e risco comparáveis:

| DEM | Executor | Rodadas de EVAL | O que os FAILs pegaram |
|---|---|---|---|
| DEM-001 | subagente | 1 | — (PASS de primeira) |
| DEM-002 | subagente | **3** | teste vacuoso, cobertura por chave, destino do redirect |
| DEM-003 | subagente | **5** | forma, identidade (com a auditoria), conteúdo, rastreabilidade |
| **DEM-012** | **Codex** | **?** | **?** |

## Regras do piloto

1. O **mesmo** EVAL, o **mesmo** plano de testes, a **mesma** DEM.
2. O Codex **não** altera os guardas, o CI, o deploy nem os segredos.
3. Se violar um guarda, o parecer registra — **é o dado**.
4. O PLANNER escreve o parecer do diff e compara; o ARQUITECT lê o resultado.

## Estado

- [x] Piloto aprovado pelo ARQUITECT (19/10)
- [x] O pacote da DEM-012 escrito (`intent`, `spec`, `plano-testes`)
- [ ] A DEM-012 assinada (falta a pergunta 9.1)
- [ ] O Codex configurado (auth/modelo) e o despacho definido
- [ ] A execução + o EVAL + o parecer comparativo
