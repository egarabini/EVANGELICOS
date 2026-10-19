# Definição da v1

> Proposta do PLANNER ao ARQUITECT (2026-10-19), ligada à [ADR-018](../adr/ADR-018-modo-agil-ate-a-v1.md).
> **Sem isto, "a v1" não tem fim** — e o modo ágil, que termina na v1, ficaria sem gatilho.

## 1. O que é a v1

**Um estudo bíblico dirigido funcionando de ponta a ponta, com as proteções fechadas, dados reais
limpos e o pipeline publicando.** Não é "o produto pronto": é o **primeiro marco com segurança de
produção**.

## 2. Escopo da v1 (o que entra)

| # | Item | Estado hoje |
|---|---|---|
| 1 | Login, papéis (admin, coordenador, instrutor, aluno) e a matriz de acesso | **pronto** (DEM-002 aceita) |
| 2 | Estudo aplicável com capítulos próprios e mapa de origem | **pronto e no ar** (DEM-001, v0.1.0) |
| 3 | Catálogo de estudos (as 34 lições) e a atribuição a alunos | pronto no código; **conteúdo em produção a confirmar** |
| 4 | Registro e aprovação de estudos (catálogo do admin) | pronto (uma assinatura — dívida D-07) |
| 5 | Deploy pelo pipeline, com backup verificado e HTTP 200 | **pronto** (DEM-004, v0.1.0) |
| 6 | Inventário de fontes e licenças | EVAL PASS; **aguarda o aceite** (DEM-003) |
| 7 | Segurança fechada: D-01, D-02, D-03, D-04, D-05, D-08, D-09 | **a executar na virada** |

## 3. Fora da v1 (explicitamente)

- **DEM-B/C/D** (registro de fontes, grafo, busca por assunto) — pós-v1.
- **DEM-E (DAVID)** — pós-v1.
- **DEM-005 (saída do Reflex)** — pós-v1, e **só depois do aceite da ADR-014** + o spike de sessão.
- **DEM-010 (tenant)**, **DEM-011 (dupla aprovação)** — ficam com gatilho próprio (D-06/D-07).
- **DEM-013 (publicação como serviço MCP)** — **adiada**; reavaliar na virada.

## 4. Critério de pronto (o que o ARQUITECT verifica)

1. O fluxo completo numa sessão: **login → estudo atribuído → lição → resposta → correção → parecer**.
2. **Nenhuma dívida crítica aberta**: D-01, D-02, D-05, D-09 fechadas; D-03, D-04 revisadas; D-06, D-07, D-08 com gatilho novo escrito.
3. **Dados de teste limpos** e **dados reais** entrando com procedimento (o D-09).
4. **Release `v1.0.0`** taggeada, publicada pelo pipeline, com o backup verificado e o HTTP 200.
5. **Documentação**: o painel refletindo a realidade; a ADR-018 e as dívidas com o fechamento registrado.

## 5. Checklist de fechamento (na virada)

- [ ] D-01 — senha de seed fora do código; admin e demos com troca obrigatória; a senha do admin de produção trocada
- [ ] D-02 — `diag` no script de entrada + chave com `restrict`; a operacional revogada
- [ ] D-03 — ruleset de tags `v*`; revisar a conta única
- [ ] D-04 — Environment `producao` com aprovador (ou decisão escrita de manter sem)
- [ ] D-05 — cópia do dump **fora da VPS** (com checksum)
- [ ] D-06/D-07/D-08 — reclassificar com novo gatilho (ou implementar)
- [ ] D-09 — limpar `eval/tmp-*`, usuários demo e o histórico de teste
- [ ] **declarar o fim do modo ágil** (ADR-018) e voltar as ADR-006/007 ao processo cheio

## 6. Candidatas de produto pós-piloto (ordem recomendada, não decisão)

| Ordem | Candidata | Nível (ADR-018) | Dependência |
|---|---|---|---|
| **a** | **Novos estudos a partir de Sire, Clark e Edwards** — piloto no **Clark** (8 arquivos), usando **plano próprio**, não o texto do livro | 2 | o inventário (DEM-003) aceito; a doutrina revisada |
| **b** | **DEM-B → C → D** (registro de fontes, ingestão do grafo, busca por assunto) | 2 (B) · 3 (C, ingestão) · 2 (D) | o aceite da DEM-003; o grafo do atlas (F-082) |
| **c** | **DEM-005 (saída do Reflex)**, por rotas, admin primeiro | 3 | o aceite da **ADR-014** + o **spike de sessão compartilhada** |

**Por que o Clark primeiro**: é o menor acervo (8 arquivos), tem plano de estudo dirigido como
formato — que é exatamente o que a plataforma consome — e está na base editorial reformada. O
Sire e o Edwards exigem mais material por capítulo. E **não** usa o texto integral do livro: o
estudo é **derivado** (o mesmo regime da F-084), não reprodução.

## 7. Como se declara a v1

O ARQUITECT declara, com o checklist acima fechado. O PLANNER registra a data, o hash do release
e o fechamento das dívidas no painel; a ADR-018 ganha o status `Superseded by processo pleno`
(na prática, volta o nível 3 como padrão) e o modo ágil encerra.
