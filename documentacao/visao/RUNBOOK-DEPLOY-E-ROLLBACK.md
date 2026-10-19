# Runbook — deploy e rollback (Didasko)

> Autoridade: perfil **DEPLOY** ([ADR-016](../adr/ADR-016-delegacao-de-publicacao-ao-deploy.md)).
> Caminho preferencial: **GitHub Actions**. Este é o procedimento; **o que não está aqui
> exige autorização específica** do ARQUITECT (ADR-016, "lista fechada").

## 1. Antes de publicar (conferir)

- [ ] **Release aceito** pelo ARQUITECT — a tag `vX.Y.Z` existe (o DEPLOY publica a tag, não a cria);
- [ ] **CI verde** no PR que originou o release;
- [ ] Environment `producao` com `DEPLOY_SSH_KEY` e `DEPLOY_KNOWN_HOSTS`; policies: **`main` e `v*`**;
- [ ] a chave do CI aceita pela VPS, na entrada com `restrict,command="/usr/local/bin/didasko-deploy-entry"`;
- [ ] na VPS: `/usr/local/bin/didasko-deploy-entry` (root, 755), `~/didasko` com `.env`, `~/backups` gravável.

## 2. Publicação (rotina — **sem aprovação por passo**)

1. o release cria a tag; o **push da tag** dispara `Deploy (producao)` (ou `workflow_dispatch` com a tag);
2. o workflow prepara a chave → SSH com **comando forçado** → o script:
   valida a tag → **`pg_dump`** → **`gzip -t`** → **`sha256sum -c`** → checkout da tag →
   `subir.sh --pular-import` → **HTTP 200**;
3. o artifact **`backup-manifest-<run>`** guarda o log com o caminho, o tamanho e o sha256 do
   backup (retenção de 90 dias);
4. **falha em qualquer passo bloqueia a publicação** — o site continua na versão anterior.

## 3. Rollback

**Critério** (qualquer um): HTTP ≠ 200 depois do deploy; versão errada no ar; app em loop de
restart; erro que aparece só em execução.

**Procedimento**: publicar a **tag anterior** — é a mesma rotina (`deploy <tag-anterior>`),
inclusive o backup verificado. O rollback **não** apaga backup nem altera `.env`/infra.

**Limite**: rollback é de **aplicação**. **Restaurar o banco exige autorização específica.**

## 4. Ato direto na VPS (só quando o CI não puder)

Lista fechada, com registro na jornada (comando, saída, motivo):

- `ping` (valida chave e comando forçado, sem tocar em nada);
- `git fetch --tags` + `git checkout <tag>` no clone do operador;
- `subir.sh`;
- `docker compose ps` / `logs` (diagnóstico).

## 5. Exige autorização específica e escrita (lista fechada)

Exclusão de dados · **restauração de banco** · migração · seed/importação com escrita ·
`.env`/compose/Traefik/DNS/firewall · **rotação/revogação de chave** · leitura de segredo.

**Proibido em qualquer caso:** contornar permissão administrativa usando Docker
(`docker run` com mount para ler arquivo, `docker exec` para dados).

## 6. Cadeia de chaves (estado em 2026-10-19)

| Chave | Onde | Restrição / estado |
|---|---|---|
| **CI** (`DEPLOY_SSH_KEY`) | secret do Environment | `restrict,command=...` na VPS |
| **operacional** (`~/.ssh/didasko_deploy`) | máquina do ARQUITECT | **sem `restrict` (dívida)** — restringir após o fluxo verde |
| **antiga** (`dsh-agent-didasko-deploy`) | — | revogar após o back-merge do release |

## 7. Follow-ups registrados

- transferir o **DUMP** como artifact (hoje o artifact é o manifesto);
- restringir/rotacionar a chave operacional;
- revogar a chave antiga e remover as privadas temporárias do disco.
