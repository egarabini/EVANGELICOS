# Despacho ao DEPLOY — a dívida do clone de produção

> **O quê / o porquê / o DoD / o risco.** O ato é do ARQUITECT; o DEPLOY executa pelo procedimento
> (ADR-016). **Prazo: antes de qualquer outro deploy em produção.**

## O quê

Resolver o **clone de produção divergente** na VPS: hoje ele está no **HEAD destacado da tag
`v0.1.0`** com os **3 caminhos da v1** e o **`deploy/docker-compose.producao.yml`** (os rótulos da
etapa b) como **alterações não commitadas** na árvore de trabalho.

**O caminho (a decisão do ARQUITECT):** depois do merge do PR #8, criar uma **tag nova** (a sugestão é
a `v0.1.1`, a decisão é do ARQUITECT) que contenha **a v0 mais os arquivos da landing/produção**, e
fazer o clone **checkout da tag nova** — **sem nenhum commit na VPS**.

## O porquê

- **Não commitar dentro do clone da VPS**: criaria um **histórico divergente** do repositório, e o
  próximo `git checkout` de tag **continuaria quebrando** (os arquivos da v1 ficariam presos numa
  árvore que a tag não tem);
- **A tag nova** é a **fonte de produção**: o clone passa a estar num commit **rastreável** (a tag no
  repositório), e o próximo deploy tem um ponto de partida **limpo**;
- **Sem o commit na VPS**, o `git status` limpo é a **prova** de que a produção está exatamente na tag.

## O DoD (o checklist)

**ANTES (o registro):**
1. o `git status` e o `git diff` do clone **registrados** (os 3 caminhos + o compose);
2. o `git rev-parse HEAD` e o `git describe --tags` do clone;
3. a **tag `v0.1.0` intacta** (o `git rev-parse v0.1.0` igual ao de antes);
4. os **`StartedAt` dos 6 contêineres** (os 5 da v0 + o `didasko_landing`) registrados.

**O ATO:**
5. **descartar as alterações por caminho explícito** — o `git checkout -- <os caminhos>` ou o
   `git restore <os caminhos>` **nomeados**, um a um; **NUNCA** o `git add -A`, **NUNCA** o
   `git reset --hard` genérico;
6. o **`git checkout` da tag nova** (`v0.1.1` ou a que o ARQUITECT decidir);
7. **o `git status` LIMPO** e **sem nenhum commit novo** na VPS (o `git log` na tag).

**DEPOIS (o teste — os mesmos códigos da linha de base):**
8. o `/` → **200** com o HTML referenciando **`/static/landing/landing.<hash>.css`**, e esse CSS
   **200** com o `cache-control: immutable`;
9. o `/login`, o `/homenagens`, o `/aluno`, o `/admin` → **307** (como antes);
10. o `/static/landing/x.css` → **404**;
11. os **`StartedAt` dos 6 contêineres INALTERADOS** (nenhum recriado);
12. **o Traefik NÃO reiniciou**.

**A VOLTA ATRÁS (escrita antes do ato):**
```bash
cd /home/didasko-deploy/didasko
git checkout 8805705 -- deploy/docker-compose.producao.yml
sudo -n docker compose --env-file .env -f deploy/docker-compose.producao.yml up -d --force-recreate --no-deps landing
```
**O efeito**: o `/` volta para a v0 **sem** reiniciar o Traefik.

## O risco

| O risco | A mitigação |
|---|---|
| o `git restore` genérico apagar os arquivos da v1 **antes** do checkout da tag | o checkout da tag **traz** a árvore; se a tag não tiver os arquivos, o **PARAR** e devolver (o passo 6 antes do 5? **não**: o 5 limpa, o 6 traz) — **a ordem correta é descartar e então o checkout**, e a tag **precisa** ter os 42 arquivos da v1 |
| o `--force-recreate` recriar um contêiner da v0 | o `--no-deps landing` — **só** o serviço da landing |
| a tag nova não ter a árvore da v1 | o **teste** do `/` com o `landing.<hash>.css` **antes** de qualquer outro ato; se falhar, a **volta atrás** |
| o Traefik reiniciar | **proibido** no despacho; o `docker compose` **não** o reinicia |
