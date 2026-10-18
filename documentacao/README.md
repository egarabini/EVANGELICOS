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

## Painel de DEMs

| DEM | Assunto | Estado | Depende de |
|---|---|---|---|
| [DEM-202610-001](dem/DEM-202610-001-estudo-capitulos/README.md) | Estudo: capítulos próprios + mapa de origem | **aceito** — entrega aprovada; aguarda publicação (CI) | — |
| [DEM-202610-002](dem/DEM-202610-002-guarda-de-papel-admin/README.md) | Guarda de papel nas rotas `/admin` (achado do EVAL) | **intent em rascunho** — urgente: o furo está aberto | — |
| [DEM-202610-003](dem/DEM-202610-003-inventario-de-fontes/README.md) | DEM-A: inventário de fontes e licenças | **EVAL PASS** (rodada 5) — aguarda aceite do ARQUITECT | DEM-001 entregue |
| [DEM-202610-004](dem/DEM-202610-004-ci-cd-fase-a3/README.md) | CI/CD (Fase A3) | **Etapa 1 entregue** — CI verde + proteção em `develop`/`main`; Etapa 2 aguarda a chave | — |
| [DEM-202610-005](dem/DEM-202610-005-saida-do-reflex/README.md) | **Saída do Reflex** (FastAPI + Jinja2 + HTMX), por rotas | **intent em rascunho** — aguarda ADR-014 + DEM-004 | DEM-004 |
| DEM-202610-006 *(proposta)* | DEM-B: registro de fontes e proveniência | proposta | DEM-003 |
| DEM-202610-007 *(proposta)* | DEM-C: ingestão do grafo (lugares, pessoas, eventos, jornadas) | proposta | DEM-006 |
| DEM-202610-008 *(proposta)* | DEM-D: busca por assunto (coordenador e instrutor) | proposta | DEM-007 |
| DEM-202610-009 *(futura)* | DEM-E: o agente **DAVID** no atendimento ao aluno (texto e voz) | futura | DEM-008 |
| DEM-202610-010 *(proposta)* | Isolamento por ambiente (tenant) no RBAC — `can_manage` não confere o ambiente | proposta (achado da DEM-002) | DEM-002 |

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
