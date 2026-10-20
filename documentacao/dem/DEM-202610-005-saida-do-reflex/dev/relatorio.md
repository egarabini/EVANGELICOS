# DEM-005 — relatório do marco 1 (o esqueleto da v1)

- **Branch:** `feature/DEM-202610-005-marco1`, de `develop` (`7670aec`).
- **PR:** https://github.com/egarabini/gsi_ebd/pull/7 → `develop`, aberto, sem merge.
- **Commits:** `4a344dd3ea5e46a491d14e5769a1ad04527ee17d` e
  `4f9e9c9c07e25aa2f9cf6e393ca1d036a8e689d4`.
- **CI:** https://github.com/egarabini/gsi_ebd/actions/runs/39452803850 — sucesso.

## O que a v1 faz

A app em `v1/` é FastAPI + Jinja2 + HTMX. O domínio `gsi_ebd` é importado. A v1 não
duplica regra. As telas deste marco são o login, o logout, a troca de senha e a raiz.

A interface que o marco 1b substitui está em `v1/auth.py`:

- `usuario_atual`
- `exigir` — a dependência grava `chave_permissao` e decide com `rbac.pode`
- `ambiente_atual`

A implementação própria guarda a sessão no servidor (o cookie `didasko_v1` só leva o
sid; httponly, secure, samesite lax, uma hora). O CSRF compara o formulário ou o header
`X-CSRF-Token` com o token da sessão. O H-14 deixa passar só `/perfil/alterar-senha` e
`/logout` enquanto `must_change_password` está ligado.

O argumento de `exigir` é a chave da matriz (`rota:/...`). O design escreve
`exigir(papel)`. Uma rota admite vários papéis, então a chave é o que a matriz sabe
decidir. As telas já chamam `exigir` assim. O 1b precisa da mesma assinatura.

A troca de senha não chama `on_password_changed`. Esse serviço suspende quem não é
admin, e o H-14 pede que as rotas abram depois da troca. A implementação zera a flag,
mantém `ativo` e renova a sessão. O login segue `on_login_success` / `on_login_failure`.

## Banco, imagem e pipeline

- Banco `didasko_v1`, `create_all` e baseline Alembic `0001_baseline` numa árvore
  própria (`v1/alembic`). As seis revisões da v0 não rodam. Outro nome de banco é recusado.
- Imagem `deploy/app-v1.Dockerfile` (Python 3.12, sem Node). O `requirements.txt` da v1
  puxa o da v0 e acrescenta Jinja2 3.1.6 e itsdangerous 2.2.0.
- `deploy/subir.sh --v1` usa o Compose da homologação, sobe o Postgres próprio, recria
  só `app-v1` com `--force-recreate --no-deps` e passa `SEED_PASSWORD` por
  `exec -e`. O valor não entra no `environment:` do Compose. O `up` da v0 continua
  `$COMPOSE up -d --build`, sem `--force-recreate`.
- `extra_hosts` está no Compose. O IP fica em `TRAEFIK_EDGE_IP` no `.env` da VPS.
- Limites: cada container da v1 com 512 MiB e 0,50 CPU. Na imagem local, o login
  respondeu dentro de 512 MiB (cerca de 76 MiB em repouso). Na VPS o seed terminou
  dentro desse limite.

## Testes

| Suíte | Onde | Resultado |
|---|---|---|
| v1 | diretório `v1/` | 37 passaram |
| v0 | raiz do worktree | 269 passaram |
| imagem | `GET /login` local, limite de 512 MiB | 200 |
| CI | os dois pushes do PR | verde |

O plano de testes ainda cita 128 testes da v0. A contagem viva é 269. O texto do
PLANNER ficou como está.

## Homologação

Clone em `/home/didasko-deploy/homolog-v1`. A produção (`~/didasko` e
`/home/eduardo/didasko`) não foi o diretório do comando. O entrypoint de deploy por tag
não foi usado, porque ele mexe no checkout e no banco da v0.

| Verificação | Resultado |
|---|---|
| `https://homolog.didasko.app.br/login` | 200 |
| Emissor do certificado | Let's Encrypt, CN YR2, nome `homolog.didasko.app.br` |
| Revisão Alembic | `0001_baseline` |
| Usuários do seed | 5 |
| Projeto Compose | `homolog-v1` |
| Traefik `StartedAt` | 2026-10-18T17:27:43Z, igual antes e depois |
| `https://didasko.app.br/` | 200 |
| `https://homolog.didasko.app.br/experimento` | 401 |

O certificado YR2 já estava emitido (desde 2026-10-20 09:40 GMT). O roteador da v1
passou a usar esse certificado. Não houve obtain novo e o Traefik não foi reiniciado.

O primeiro `up` adotou o projeto `deploy` da produção, porque o arquivo está em
`deploy/` e ainda não tinha `name:`. Não houve `--remove-orphans` nem restart do
Traefik. Os dois containers da v1, a rede `deploy_interna` e o volume
`deploy_didasko_v1_data` foram removidos por nome. A segunda subida, já com
`name: homolog-v1` e `-p homolog-v1`, é a que ficou no ar. O `down` do projeto da
produção não rodou.

## O que este marco não fecha

O EVAL cego, o merge, o marco 1b, as telas dos marcos 2–6, o pin do Traefik, o limite
de CPU do Ollama e o desmonte da homologação. O desmonte continua dependendo da
confirmação do ARQUITECT na hora.
## A conferência do ARQUITECT (20/10) — os 4 pontos

1. **A prova completa do quase-acidente**: o `State.StartedAt` de **todos** os contêineres da v0
   (a consulta do PLANNER em 20/10, 18:20): `didasko_app` 2026-10-19T12:10:13Z; `didasko_traefik`,
   `didasko_postgres`, `didasko_chromadb` e `didasko_ollama` 2026-10-18T17:27:43Z — **todos
   anteriores** à subida do marco 1. Nenhum contêiner da v0 foi recriado pelo `up` acidental do
   projeto `deploy`.
2. **As credenciais da homologação (o defeito confirmado)**: o `subir_v1()` usa o
   `--env-file .env` (o da produção), **não** o `deploy/.env.v1-homolog` que o PR criou — o Postgres
   da v1 herdou o `POSTGRES_USER`/`POSTGRES_PASSWORD` da v0. **Correção**: o `--env-file
   .env.v1-homolog` no `subir_v1`, e o `.env.v1-homolog` com o `POSTGRES_USER=didasko_v1` e a
   senha **aleatória** (a condição d).
3. **O IP fixo do Traefik**: o `TRAEFIK_EDGE_IP` muda se o Traefik for recriado → o design do
   marco 1b passa a prever o **`host-gateway`** (a alternativa estável), não testada ainda.
4. **A homologação pública**: o `/login` 200, os 5 usuários do seed — até o EVAL, proteger com a
   **basic auth** ou a lista de IPs (a decisão do ARQUITECT).

**A troca de senha**: a bifurcação provisória (a v1 não chama o `on_password_changed`) fica
registrada — o marco 1b a resolve do lado do provedor.

## Reset do volume da v1 (20/10) — condição 4

O commit `7524ac74d56380bea896d3b577cc2c87792a3d4a` troca o `--env-file` do `subir_v1`
para `.env.v1-homolog` e exige `POSTGRES_USER=didasko_v1`. O CI do PR #7 ficou verde:
https://github.com/egarabini/gsi_ebd/actions/runs/39502094527.

O volume removido, conferido antes do `down`, foi exatamente `homolog-v1_didasko_v1_data`.
O `ps` do projeto `homolog-v1` tinha só `didasko_v1_app` e `didasko_v1_postgres`. O `down`
não usou `--remove-orphans`. Os volumes do projeto `deploy` (`deploy_chroma_data`,
`deploy_letsencrypt`, `deploy_ollama_models`, `deploy_pgdata`) continuaram. A subida
`bash deploy/subir.sh --v1`, no checkout `7524ac7`, recriou o volume vazio
(`CreatedAt` 2026-10-20T18:42:38-03:00) e semeou 5 usuários. O Postgres da v1 ficou com
`POSTGRES_USER=didasko_v1` e `POSTGRES_DB=didasko_v1`. Revisão Alembic `0001_baseline`.
`https://homolog.didasko.app.br/login` respondeu 200, a produção 200 e `/experimento` 401.

| Container | StartedAt antes | StartedAt depois |
|---|---|---|
| `didasko_v1_app` | 2026-10-20T15:55:50.90330865Z | 2026-10-20T21:42:46.489069386Z |
| `didasko_v1_postgres` | 2026-10-20T15:55:43.493758956Z | 2026-10-20T21:42:39.20981457Z |
| `didasko_app` | 2026-10-19T12:10:13.854096936Z | 2026-10-19T12:10:13.854096936Z |
| `didasko_postgres` | 2026-10-18T17:27:43.532867086Z | 2026-10-18T17:27:43.532867086Z |
| `didasko_chromadb` | 2026-10-18T17:27:43.520845985Z | 2026-10-18T17:27:43.520845985Z |
| `didasko_ollama` | 2026-10-18T17:27:43.521563773Z | 2026-10-18T17:27:43.521563773Z |
| `didasko_traefik` | 2026-10-18T17:27:43.522467189Z | 2026-10-18T17:27:43.522467189Z |

Os cinco da v0 ficaram com o mesmo `StartedAt`. O Traefik não foi reiniciado.
