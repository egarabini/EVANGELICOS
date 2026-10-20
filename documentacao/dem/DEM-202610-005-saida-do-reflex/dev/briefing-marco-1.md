# Briefing do DEVS — DEM-005, **marco 1** (o esqueleto da v1)

> **Para:** o Codex (o DEVS) — ou outro executor sob a mesma autorização do ARQUITECT.
> **O que este marco entrega**: a **primeira versão da v1** — a app, a autenticação (a interface), o
> banco `didasko_v1`, a imagem e o pipeline. O **marco 1b** (a identidade pelo provedor, a ADR-021)
> vem **depois** — por isso o marco 1 entrega a **interface** de identidade com uma implementação
> **mínima própria**, que o 1b substitui sem tocar nas telas.

## 1. O que ler, nesta ordem

1. `ESTUDOS_BIBLICOS/GSI_EBD/AGENTS.md` e `CONVENTIONS.md`.
2. `documentacao/dem/DEM-202610-005-saida-do-reflex/planner/spec.md` — os **RF01–RF15**, os CA01–CA08.
3. `.../planner/design.md` — a estrutura da v1 e o **marco 1** (a §2).
4. `.../planner/design-marco-1b.md` — **o que o 1b vai trocar**: a interface `usuario_atual`,
   `exigir(papel)`, `ambiente_atual`. O marco 1 **entrega essa interface** com a implementação
   mínima própria.
5. `.../planner/plano-testes.md` — a matriz, o CSRF, o H-14, o render.
6. As ADRs **002** (o corpus), **003** (a Escritura), **008** (os segredos), **014 v3** (a v1 na base
   nova), **018** (o nível) e **021** (o provedor — o 1b).

## 2. O escopo do marco 1

- a **`v1/`** com o `main.py` (o FastAPI), o `db.py` (a engine do SQLModel; o `DATABASE_URL`; o
  `create_all` dos modelos e o **baseline de Alembic**), o `auth.py` (**a interface + a
  implementação mínima própria**: a sessão de servidor, o CSRF, o `login`/`logout`, o
  `usuario_atual`, o `exigir(papel)`, o `ambiente_atual`), os routers (o login, o perfil, a raiz), os
  templates (o layout, o login, o perfil), o static e os **tests**;
- a **matriz papel × rota** (a DEM-002, `gsi_ebd/utils/rbac.py`) aplicada como **dependências**;
- o **H-14** (a D-11): a flag `must_change_password` **bloqueia** as rotas até a troca (a
  implementação própria; o 1b usa a do provedor);
- o **Postgres próprio da homologação** (o contêiner dedicado, a **rede interna**, o **volume próprio**) com o banco **`didasko_v1`** + o **baseline de Alembic** — **NÃO** criar papel nem banco no `didasko_postgres` antes da virada (a condição b);
- a **imagem** (o Dockerfile da v1) e o **pipeline** (a v1 no **Compose próprio** da homologação;
  o `subir.sh` com o **`exec -e SEED_PASSWORD`** — o A-2, **a partir da próxima tag** — e o
  **`--force-recreate`**; o **Traefik da v0 não é reiniciado nem reconfigurado** — os labels do
  roteador vão no Compose da v1);
- a **homologação** no `homolog.didasko.app.br` (o DNS já existe; o **certificado** — o RF14);
- o **RF13** (o issuer alcançável do contêiner — a solução **versionada** no Compose).

## 3. As regras

- a branch `feature/DEM-202610-005-marco1` a partir do `develop`; o PR; os commits pt-BR.
- **O domínio não se reescreve**: o `gsi_ebd/` é importado (os models/services); a v1 não duplica
  regra.
- **A suíte da v1 roda do diretório da v1** (`v1/`); a **regressão da v0 (269) continua verde**.
- **Nada de segredo no repositório**: o `.env.example`; o `.env` na VPS.
- **Sem tocar no v0**: a produção (`/home/eduardo/didasko`) e o Traefik não mudam no marco 1.
- **Sem a 1b**: o login do marco 1 é a implementação própria mínima, **atrás da interface**.
- **Os limites de memória e de CPU** dos contêineres da v1 na homologação (os valores vão no
  relatório; o E-04 e a latência medem o uso real) — a condição c.
- **NÃO AUTORIZADO neste marco**: qualquer mudança no **Ollama**, no **Traefik** ou nos
  contêineres da **v0**; o limite de CPUs do Ollama (o RF15) fica para o **marco 1b** — a condição f.
- **O desmonte** da homologação exige a **confirmação do ARQUITECT na hora** — a condição g.
- **Se a emissão do certificado falhar**: recriar **só** os contêineres do serviço da v1; se
  persistir, **PARE e devolva ao PLANNER** — a condição a.
- Se faltar uma decisão (a infra, um campo), **PARE e devolva ao PLANNER** — como nas fatias 1 e 2.

## 4. O Definition of Done

- o **login local** funcionando, com a **matriz** bloqueando por papel;
- o **CSRF**, o **H-14** e o **render** (todas as rotas) testados;
- o **`didasko_v1`** criado com o baseline e o `create_all`;
- a **imagem** e o **pipeline** rodando a v1; o **certificado** na homologação (o RF14);
- a **suíte da v1 verde** + a regressão (269); o **CI verde**; o relatório.

## 5. O que **não** é deste marco

- o **marco 1b** (a identidade pelo provedor — a ADR-021);
- os **marcos 2–6** (as telas do fluxo, o coordenador, o instrutor, a lição, a virada);
- o desmonte do experimento, o DNS, a infra do ARQUITECT.



