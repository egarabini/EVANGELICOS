# A observação — o CI não aparece no PR da branch (a causa e a correção)

> Registrado por ordem do ARQUITECT (23/10). **Proposta, não decisão.**

## O que aconteceu

O **PR #8** foi mesclado com o **`--admin`** porque o GitHub **não associava** o check `testes (pytest)`
— verde no head `f8ffe0a` — ao PR. A **proteção da develop exige** esse check:

```text
required_status_checks: ["testes (pytest)"]
```

## A causa (lida no código)

O `ci.yml` tem:

```yaml
on:
  pull_request:
    branches: [develop, main]
  push:
    branches: [develop, main]
  workflow_dispatch:
```

- o **`pull_request` só dispara quando a base do PR é `develop` ou `main`**;
- o **#8 tinha a base na `feature/DEM-202610-005-marco1`** (a branch do marco 1, já mesclada) — então
  o `pull_request` **não rodou** no PR;
- o check que o GitHub exibia vinha do **`workflow_dispatch`** (o disparo manual) — e **o manual não
  aparece no PR**;
- a **proteção exige o check** → o merge só passou com o `--admin`.

**A lição**: **o CI está certo para a base `develop`/`main`**, mas os PRs **empilhados** (a base numa
`feature/*`) ficam **sem o check** — e a proteção não distingue.

## A correção proposta (a decisão é do ARQUITECT)

**Opção A (a mais simples)**: o `pull_request` **sem** o `branches` — todo PR dispara o CI:
```yaml
on:
  pull_request:
  push:
    branches: [develop, main]
  workflow_dispatch:
```

**Opção B**: o `branches: [develop, main, "feature/**"]` — cobre as branches do projeto.

**Opção C**: manter o `ci.yml` e a proteção exigir o check pelo **nome do job**, com o workflow a
rodar no `pull_request` — é a opção A com o nome explícito.

**O custo**: a opção A roda o CI em **todo** PR (inclusive os de documentação) — o custo é minutos de
runner, e o **benefício** é o PR mostrar o check **antes** do merge, **sem** o `--admin`.

## O teste da correção

Um **PR de teste** (`feature/x` → `develop`) mostra o check `testes (pytest)` **verde no PR**; o
merge **passa sem o `--admin`**.

## O risco

| O risco | A mitigação |
|---|---|
| o CI rodar em todo PR (o custo) | a opção B (o `feature/**`) limita; o custo é aceitável |
| a proteção continuar exigindo um check que não roda | o teste do PR prova; a opção A garante |
| o `--admin` virar hábito | a correção **elimina** a necessidade dele para o PR normal |
