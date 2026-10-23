# Despacho ao DEPLOY — a tag `v0.1.1` (o DEPLOY PLANEJADO)

> **O quê / o porquê / o DoD / o risco.** O ARQUITECT decidiu: a `v0.1.1` é um **DEPLOY PLANEJADO**.
> O push de uma tag `v*` dispara o `deploy.yml` (**o backup do banco, o `checkout --force` da tag, o
> `subir.sh`, a verificação HTTP**). **O ato é do ARQUITECT**; o DEPLOY executa pelo procedimento
> (ADR-016). **Prazo: antes de qualquer outro deploy em produção.**

## O que MUDOU com a decisão do ARQUITECT

- **A divergência se resolve no deploy**: o `deploy-entry` (o L91) faz o
  `git -c advice.detachedHead=false checkout --force refs/tags/$TAG` — **o `checkout --force`**.
  **Não há** o "descartar as alterações por caminho" antes do ato;
- **A promessa "os `StartedAt` inalterados" SAIU**: o `subir.sh` (o L121) roda o
  `$COMPOSE up -d --build` — o **compose inteiro**, não só o app. **A garantia passa a ser**: "a **v0**
  e a **landing no ar**, conferidas pelos **códigos da linha de base**";
- **O backup do banco é do pipeline** (o `deploy-entry` L66–L84: o `pg_dump` + o `gzip` + o
  `checksum`; o backup **vazio ABORTA** o deploy);
- **O `deploy.yml` exige o `environment: producao`** — a **aprovação do ARQUITECT** antes de qualquer
  comando; a pipeline **não contorna**;
- **A alternativa** (a tag **fora** do `v*` + o ato manual) **só se o ARQUITECT pedir**: com o
  `git diff <tag> -- <os 42 arquivos + o compose>` **VAZIO** antes de qualquer descarte.

## O que o PLANNER leu (a condição do ARQUITECT)

| O ponto | O que o código diz |
|---|---|
| **O `subir.sh` (L121)** | o `$COMPOSE up -d --build` sobe **todos os serviços** do compose de produção — **o `landing` incluído** (o compose da tag o tem). **O serviço é mantido.** |
| **O `deploy-entry` (L17)** | a ordem: o **backup do banco** → o **checkout da tag** → o **`subir.sh`** → a **verificação HTTP** |
| **O `deploy-entry` (L91)** | o `git -c advice.detachedHead=false checkout --force refs/tags/$TAG` — **resolve a divergência** |
| **O `deploy-entry` (L109)** | a verificação HTTP; se falhar: **o rollback** (o `git checkout <tag anterior> + bash deploy/subir.sh`) |

**A condição está satisfeita** — o deploy **sem `--v1`** sobe o compose inteiro e **mantém o
`didasko_landing`**. **Não é preciso mudar o script de entrada.**

## O DoD

**ANTES (a janela e o aviso):**
1. uma **janela curta** definida e **avisada** (o deploy roda o `--build` e o `up -d` — o site pode
   oscilar por alguns minutos);
2. a **volta atrás escrita**:
   ```bash
   cd /home/didasko-deploy/didasko
   git -c advice.detachedHead=false checkout --force refs/tags/v0.1.0
   bash deploy/subir.sh --pular-import
   ```
   (o deploy da **`v0.1.0`** — a landing sai, o `/` volta para a v0);

**O ATO (o ARQUITECT):**
3. o **merge do PR #8** na `develop`;
4. a **criação da tag `v0.1.1`** no commit da `develop` que contém o #8;
5. o **push da tag** → o `deploy.yml` dispara → **a aprovação do `environment: producao`** (o
   ARQUITECT).

**DEPOIS (a conferência — os códigos da linha de base):**
6. o `/` → **200** com o HTML referenciando **`/static/landing/landing.<hash>.css`**, e esse CSS
   **200** com o `cache-control: immutable`;
7. o `/login`, o `/homenagens`, o `/aluno`, o `/admin` → **307** (como na base);
8. um asset **`/assets/...`** da v0 → **200** (o resto na v0);
9. **a v0 e a landing no ar** (o `docker ps` com os dois);
10. **o Traefik não reiniciou** (o `StartedAt` dele inalterado — **o único** que o despacho promete,
    porque o `up -d --build` pode recriar os serviços do compose).

## O risco

| O risco | A mitigação |
|---|---|
| o `up -d --build` recriar os serviços da v0 (o `StartedAt` muda) | **é o comportamento do pipeline** — a garantia é **funcional** (a v0 e a landing no ar, os códigos da base), não o `StartedAt`; o teste do `/login` (o 307) prova a v0 |
| o `/` sair da v0 e a landing falhar | a **volta atrás** (o deploy da `v0.1.0`) **escrita antes** |
| o backup falhar | o `deploy-entry` **ABORTA** (o backup vazio/gzip inválido) — o site fica como estava |
| a tag não conter o `landing` no compose | o **merge do #8 antes**; o `git diff <tag> -- deploy/docker-compose.producao.yml` antes do push |
| a tag disparar sem o aceite | o `environment: producao` **exige a aprovação do ARQUITECT** — a pipeline não contorna |
