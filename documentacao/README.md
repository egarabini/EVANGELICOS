# Documentação do Didasko

> Governança do projeto: **visão**, **método**, **decisões (ADRs)** e **demandas (DEMs)**.
> O método adotado é INTENT + SDD, copiado autocontido em [`metodo/`](metodo/README.md).

## Por onde começar

| Quero… | Leia |
|---|---|
| entender o produto | [`visao/projeto.md`](visao/projeto.md) |
| saber a stack e as regras do projeto | [`perfil-do-projeto.md`](perfil-do-projeto.md) |
| saber **por que** algo é assim | [`adr/`](adr/README.md) — 11 decisões registradas |
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
| DEM-202610-001 | Estudo: capítulos próprios + mapa de origem (Fase 2 das bibliotecas) | **planejada** | Fase A |

> A fonte é esta tabela. Não hardcode a "DEM atual" nos arquivos de guarda.

## Fase A (em andamento)

- [x] estrutura `documentacao/` + método copiado
- [x] perfil do projeto
- [x] guardas (raiz + código)
- [x] ADRs 001–011
- [ ] GitFlow (`develop` + tags)
- [ ] CI/CD (`gh` autenticado + workflows + secrets) — **bloqueado**: precisa do `gh auth login`
