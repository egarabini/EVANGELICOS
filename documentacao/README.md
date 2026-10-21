# Documentação do Didasko

> Governança do projeto: **visão**, **método**, **decisões (ADRs)** e **demandas (DEMs)**.
> O método adotado é INTENT + SDD, copiado autocontido em [`metodo/`](metodo/README.md).

## Por onde começar

| Quero… | Leia |
|---|---|
| entender o produto | [`visao/projeto.md`](visao/projeto.md) |
| ver a frente em preparação | [`visao/OLPF-base-de-conhecimento-e-busca.md`](visao/OLPF-base-de-conhecimento-e-busca.md) |
| saber a stack e as regras do projeto | [`perfil-do-projeto.md`](perfil-do-projeto.md) |
| saber **por que** algo é assim | [`adr/`](adr/README.md) — 13 decisões registradas |
| trabalhar numa demanda | [`dem/`](dem/) — uma pasta por DEM |
| ver o que veio antes do método | [`historico/`](historico/README.md) |

## O método em uma linha

**INTENT** (o porquê, assinado pelo ARQUITECT) → **SPEC** (o quê) → **DEM** (o como) → **código** (a evidência).
Nenhuma spec abre sem `intent.md` com `status: signed`. Detalhe em [`metodo/00-visao-geral/filosofia.md`](metodo/00-visao-geral/filosofia.md).

## Papéis

| Papel | Instância |
|---|---|
| ARQUITECT | Eduardo — assina intent, spec, aceite e release |
| PLANNER | IA condutora — intent/spec/plano-testes/briefings/fechamento |
| DEVS | IA (ou subagente) — implementa via TLC, escopo da DEM |
| EVAL | subagente **cego** — PASS/FAIL sobre hash, em estado limpo |
| VISION | Eduardo — validação visual (não há navegador automatizado) |
| DEPLOY | GitHub Actions — o agente **não** publica (ADR-010) |

> **A v0 (o Reflex) está congelada na tag `v0.1.0`** (decisão de 2026-10-19): a `develop` pertence à v1; a
> correção urgente da v0 sai de um hotfix sobre a tag, e as mudanças da `develop` vão ao ar **com a v1**.

## Painel de DEMs

| DEM | Assunto | Estado | Depende de |
|---|---|---|---|
| [DEM-202610-001](dem/DEM-202610-001-estudo-capitulos/README.md) | Estudo: capítulos próprios + mapa de origem | **aceita e publicada** na v0.1.0 (deploy verde); o importador em produção é do ARQUITECT | — |
| [DEM-202610-002](dem/DEM-202610-002-guarda-de-papel-admin/README.md) | Guarda de papel nas rotas `/admin` | **aceita** (2026-10-18) e **publicada** na v0.1.0 | — |
| [DEM-202610-003](dem/DEM-202610-003-inventario-de-fontes/README.md) | DEM-A: inventário de fontes e licenças | **aceita** (2026-10-19) — inventário + **revisão doutrinária** (22 linhas, opção A; a FAJOPA `depende`) | DEM-001 entregue |
| [DEM-202610-004](dem/DEM-202610-004-ci-cd-fase-a3/README.md) | CI/CD (Fase A3) | **entregue** — CI + CD no ar; a **v0.1.0 publicada pelo pipeline**; ADR-016 aceita | — |
| [DEM-202610-005](dem/DEM-202610-005-saida-do-reflex/planner/spec.md) | **A v1 na base nova** (FastAPI + Jinja2 + HTMX, construída ao lado, virada única) | **o marco 1 PASS no 2º EVAL cego** (o `3d28934`; 40 testes da v1 + 269 da v0; a homologação no ar; a v0 intocada) — o **1b** (a identidade) e os marcos 2–6 na fila | — |
| DEM-202610-006 *(proposta)* | DEM-B: registro de fontes e proveniência | proposta | DEM-003 |
| DEM-202610-007 *(proposta)* | DEM-C: ingestão do grafo (lugares, pessoas, eventos, jornadas) | proposta | DEM-006 |
| DEM-202610-008 *(proposta)* | DEM-D: busca por assunto (coordenador e instrutor) | proposta | DEM-007 |
| DEM-202610-009 *(futura)* | DEM-E: o agente **DAVID** no atendimento ao aluno (texto e voz) | futura | DEM-008 |
| DEM-202610-010 *(proposta)* | Isolamento por ambiente (tenant) no RBAC — `can_manage` não confere o ambiente | proposta — **D-06** (gatilho: mais de um ambiente real) | DEM-002 |
| [DEM-202610-011](dem/DEM-202610-011-fluxo-de-obras-e-estudos/README.md) | **O fluxo de obras e estudos** (admin → revisor → admin → liberada; adendos do coordenador) | **fatia 1 (o domínio) PASS** (269 testes; 39 casos; 9 mutações) e **mergeada** (`7670aec`); a fatia 2 (as telas, na v1) é a próxima | DEM-005 |
| [DEM-202610-012](dem/DEM-202610-012-credencial-de-seed/README.md) | **Credencial de seed**: sem senha no código, troca obrigatória para todos | **EVAL PASS** (128 testes; RF01-RF07) e **mergeada no `develop`** (`dbbfc09`) — aguarda o aceite; a D-01/D-10/D-11 seguem abertas | — |
| DEM-202610-013 *(adiada)* | Publicação como serviço MCP | **adiada até a v1** (decisão de 19/10; ADR-017 Deferred) | — |
| [DEM-202610-014](dem/DEM-202610-014-codex-como-devs/README.md) | **O Codex acumula DEVS e DEPLOY** (os gates preservam a independência) | **decidido** (uma página) — a DEM-012 é a próxima, executada por ele | DEM-012 |
| [DEM-202610-016](dem/DEM-202610-016-zitadel-experimento/dev/relatorio.md) | **O experimento do provedor de identidade** (o Zitadel) | **concluído**: o E-01..E-07 (o E-05 no critério original), o E-06 de 5–9 dias; a decisão **A** (a ADR-021) — o experimento **reaproveitado**, sem desmonte | — |
| [DEM-202610-013](dem/DEM-202610-013-publicacao-como-servico/planner/intent.md) | **Publicação como serviço MCP** (o DEPLOY vira API; os agentes são clientes) | **intent em rascunho** — aguarda ADR-017 + 3 decisões | DEM-004 |
| DEM-202610-014 *(proposta)* | **Piloto do Codex como DEVS** (segundo modelo, julgado pelo EVAL) | proposta | DEM-013 |

> A fonte é esta tabela. Não hardcode a "DEM atual" nos arquivos de guarda.

## Frente em preparação — base de conhecimento e busca

Proposta do AUXILIAR-ARCHITECT, com as **12 perguntas fechadas** pelo ARQUITECT em
2026-10-17: [`visao/OLPF-base-de-conhecimento-e-busca.md`](visao/OLPF-base-de-conhecimento-e-busca.md).

- Política que rege a frente: **[ADR-012](adr/ADR-012-politica-de-fontes-e-licencas.md)** (fontes, licenças, cânon, citação, riscos com gatilho).
- Exceção de stack pendente: **[ADR-013](adr/ADR-013-componente-de-mapa-em-javascript.md)** (mapa em JS) — **Proposed**, aguarda aceite.
- A decisão **10.9** (original grego/hebraico no primeiro corte) **amplia** o primeiro corte em relação ao que a OLPF sugeria.
- Sequência: **começa depois do fechamento da DEM-001** (a OLPF §8 impõe a dependência).

## Fase A (em andamento)

- [x] estrutura `documentacao/` + método copiado
- [x] perfil do projeto
- [x] guardas (raiz + código)
- [x] ADRs 001–011
- [x] GitFlow (`develop` nos dois repos; tags virão com o primeiro release)
- [ ] CI/CD (`gh` autenticado + workflows + secrets) — **bloqueado**: precisa do `gh auth login`











