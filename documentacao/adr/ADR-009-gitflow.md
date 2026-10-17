# ADR-009: GitFlow e revisão por Copilot Enterprise

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

Os dois repositórios têm **um único branch (`main`), zero tags e push direto**.
Não existe portão de merge, nem histórico de release.

## Decisão

Adotar **GitFlow** (`main` produção com tags SemVer, `develop` integração,
`feature/DEM-*`, `release/*`, `hotfix/*`), PR como portão, e **Copilot Enterprise**
como revisor de segurança/qualidade no PR. O agente usa `gh` para branch, commit
semântico, PR e leitura de resultado — **não** para publicar (ADR-010).

## Consequências

**Positivas:**
- Histórico de release por tag; portão de merge com dois revisores automáticos.
- Rastreio DEM ↔ branch ↔ PR ↔ tag.

**Negativas / trade-offs:**
- Cerimônia; exige `gh` autenticado e branch protection configurada.

## Impacto nas DEMs

- Fase A do método.
- O id da DEM entra no nome da branch e nos trailers.
