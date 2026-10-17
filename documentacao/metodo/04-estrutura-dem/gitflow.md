# GitFlow e as regras duras do DEPLOY

> Estratégia de branches neutra (GitFlow clássico), pensada para **controle de versão rigoroso** e para separar integração, homologação e produção. Ajuste os nomes de ambiente no [perfil do projeto](../perfil-do-projeto/perfil-do-projeto.template.md); registre a escolha como uma ADR.

## Branches de longa duração

| Branch | Papel | Ambiente |
|---|---|---|
| `main` | Releases de produção; cada merge recebe **tag SemVer** | Produção |
| `develop` | Linha de integração contínua das DEMs | Dev / integração |

> **Nota:** alguns repositórios usam `master` como default. Onde este método diz `main`, leia o nome que o seu repo adota — registre isso no perfil.

## Branches de apoio (curta duração)

| Prefixo | Uso | Origem | Destino |
|---|---|---|---|
| `feature/DEM-…` | Nova DEM (feature) | `develop` | `develop` (via PR) |
| `bugfix/DEM-…` | Correção durante o desenvolvimento | `develop` | `develop` |
| `release/x.y.z` | Estabilização para uma release | `develop` | `main` **e** `develop` (+ tag) |
| `hotfix/x.y.z` | Correção urgente em produção | `main` | `main` **e** `develop` (+ tag) |
| `experiment/<slug>` | Experimento descartável | qualquer | fora do fluxo de release |

## Nomenclatura de branch (espelha a pasta da DEM)

```
feature/DEM-AAAAMM-<tracker>-<seq>-<slug-kebab>
```

## Convenção de commit (Conventional Commits + rastreio)

```
tipo(escopo): descrição curta

<TRAILER-TRACKER>#<id>     # linka o work item / ticket do seu rastreador
DEM-AAAAMM-<tracker>-<seq>
```

- Tipos: `feat`, `fix`, `docs`, `refactor`, `test`, `chore`, `style`, `perf`, `build`, `ci`.
- Os **trailers de rastreio** dependem do seu tracker (defina no perfil). O **hash do commit** é registrado no `changelog.md` da DEM.

## Versionamento (SemVer)

- Tags anotadas `vMAJOR.MINOR.PATCH` em `main`.
- `release/*` nomeada pela versão alvo (ex.: `release/1.2.0`); `hotfix/*` incrementa o PATCH.

## Regras de proteção

- `main` e `develop` **protegidas**: proibido push direto, só via Pull Request.
- PR de `feature/*` → `develop` só avança com **EVAL=PASS** (+ **VISION** se houver tela).
- `release/*` parte de `develop` estável; a promoção `release/*` → `main` exige **aceite do ARQUITECT**.
- **1 PR por DEM**; a branch de feature é deletada após o merge.
- `release/*` e `hotfix/*` exigem **back-merge obrigatório em `develop`**.

## Regras DURAS do DEPLOY (abortar e reportar ao ARQUITECT se violar)

1. **Alvo de PR de feature/bugfix = SEMPRE a branch de integração** (`develop`). Nunca mesclar `feature/*` direto em produção. Alvo vindo como produção → **abortar** e corrigir.
2. **Produção só recebe PR de `release/*` (ou `hotfix/*`)**, após homologação + **aceite explícito do ARQUITECT**. **Homologar SEMPRE em estado limpo** (dados/volumes zerados) — estado residual gera **falso positivo**.
3. **Pré-flight antes de QUALQUER merge:** confirmar `source`/`target`; revisar `git diff --stat target...source`; **nenhum segredo no diff**.
4. **Recuperação de merge ruim — NUNCA "revert + re-merge".** Reverter um merge e re-mesclar a mesma branch **perde alterações** (o Git trata os commits como já presentes). Para desfazer: criar **branch nova** do estado correto e abrir PR limpo (ou `git revert` do revert). Sempre validar com `git diff --stat` que **nada sumiu**.
5. **Backup pareado antes de toda release.** Faça o backup dos dados e de qualquer material sensível (ex.: chaves) **pareados e com checksum**, antes de promover.
6. **Back-merge obrigatório** de `release/*`/`hotfix/*` em `develop`; confirmar que `develop ⊇ produção`.
7. **Pós-merge:** validar a árvore final, atualizar o painel de DEMs, devolver nº dos PRs + hash do merge + tag ao PLANNER.
8. **Relatórios em bloco copiável.** Todo relatório — erro **ou** finalização OK — é entregue como um **bloco de texto copiável** (o que rodou, defeito/resultado, ação tomada, callback com PRs/hashes/tag). Sem isso, a decisão humana fica sem material.
9. **Diário de publicação `deploy/jornada.md`.** Mantenha o histórico vivo das operações (PRs, homologação, reprovações, retries, tag), simétrico à `dev/jornada.md`; bata o ponto por tarefa.

> **Por que as regras 1, 4 e 6 existem (incidente fundador):** uma feature promovida direto a produção e, ao tentar corrigir, um `revert + re-merge` **descartou silenciosamente arquivos de guarda** da produção — detectado só depois por `git diff --stat`. E uma homologação **em estado limpo** já reprovou uma release e pegou um bug que a validação anterior não viu, porque a evidência de runtime era **falso positivo** de estado residual. Essas cicatrizes viraram regra.
