# Proposta ao ARQUITECT — o `--remove-orphans` no `subir.sh`/`deploy-entry`

> **Infraestrutura: só com a autorização do ARQUITECT.** Proposta, não decisão.

## O quê

Incluir o **`--remove-orphans`** no `$COMPOSE up -d --build` do `subir.sh` (o L121) — ou no
`deploy-entry` — para que o **rollback derrube os contêineres órfãos** (o serviço que **saiu do
arquivo do compose**).

## O porquê

O **rollback da `v0.1.1` exigiu o `docker rm` manual do `didasko_landing`**: o `git checkout --force`
tira o **serviço** do compose, mas o **contêiner continua no ar** com os **rótulos do Traefik** — e
**continua servindo o `/`**. O `--remove-orphans` faz o compose **derrubar o que não está mais no
arquivo** — o rollback fica **uma ação só**.

## A regra que ele corrige

**Voltar de um serviço que entrou no compose exige DUAS ações** (a lição de 23/10):
1. o **`checkout --force` da tag antiga** (o compose sem o serviço);
2. a **remoção do contêiner** (o `docker rm -f` do serviço **ou** o `--remove-orphans`).

**Sem a segunda, a primeira é uma ilusão**: o compose diz "não há landing" e o `/` continua sendo a
landing.

## O DoD

- o rollback de um serviço que saiu do compose **derruba o contêiner sozinho**;
- **o teste**: o `git checkout --force refs/tags/v0.1.0` + o `subir.sh` (com o `--remove-orphans`) →
  o `didasko_landing` **não existe mais**; o `/` → **200** da v0; o `/login` → o 307; o `/static/landing/x.css` → o 404;
- **o deploy normal** (a tag nova): o `--remove-orphans` **não** derruba nada que deva ficar (o compose
  da tag tem todos os serviços).

## O risco

| O risco | A mitigação |
|---|---|
| o `--remove-orphans` derrubar contêineres de **outros projetos** | o **`-p` (o projeto)** + o `--env-file` explícitos; a **validação** numa janela antes |
| o `--build` recriar os serviços da v0 | **já é o comportamento atual** (o `up -d --build`); o `--remove-orphans` não muda |
| a mudança de infraestrutura sem o aceite | **a proposta é do ARQUITECT**; o DEVS só executa com a autorização dele |
