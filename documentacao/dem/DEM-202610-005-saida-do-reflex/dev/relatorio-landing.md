# DEM-005 — relatório do marco 2L (a landing)

- **Branch:** `feature/DEM-202610-005-landing`, de `feature/DEM-202610-005-marco1` (`3d28934`).
- **Worktree:** `.worktrees/DEM-005-landing` (o checkout da fatia 2 não foi alterado).
- **Assunção:** a v1 e o compose da homologação vivem no marco 1; `develop` ainda não os tem.
- **Commit:** `f9aa301a4a4a44745b787746d7deea1cda860df3`
- **PR:** https://github.com/egarabini/gsi_ebd/pull/8
- **CI:** https://github.com/egarabini/gsi_ebd/actions/runs/39689542371 — **success**

## O que a landing faz

Serviço **separado** (`v1.landing:create_app`): FastAPI + Jinja2, porte do protótipo
(`index.html`, `homenagens.html`, `landing.css`, os 3 WebP). **Sem banco, sem sessão,
sem login.** O `landing.yaml` entra vazio; o Jinja só mostra depoimentos com
`ativo: true`, canais de contato se existirem, e homenagens se a lista tiver item.

O Traefik da v0 observa as labels. Prioridade **100** no Host da homologação para `/`,
`/homenagens` e `/static/landing`. O `/login` continua na `app-v1`. **Não reinicia o
Traefik.**

## Testes

| Suíte | Onde | Resultado |
|---|---|---|
| v1 | `v1/` no worktree | **54 passaram** (40 do marco 1 + 14 da landing) |
| v0 | raiz do worktree | **269 passaram** |
| render vazio | `GET /` e `GET /homenagens` | 200, `lang=pt-BR`, `alt` no hero, sem "Em breve", sem `mailto:`/`wa.me` |
| render preenchido | yaml temporário | ativos e canais aparecem; inativo some; hero/sobre sobrepõem |
| compose | `test_rf_landing_compose_sem_banco_sem_rede_interna` | sem `DATABASE_URL`, sem rede `interna`, só `borda` |

## Peso e LCP (local, 2026-10-21)

Carga inicial medida em `http://127.0.0.1:8010/` (sem JS de terceiros; a página não tem `<script>`):

| Recurso | Bytes |
|---|---|
| HTML `/` | 9 864 |
| `landing.css` | 13 562 |
| `logo-88.webp` (topo) | 3 838 |
| `logo-440.webp` (hero 1x) | 29 718 |
| `logo-880.webp` (hero 2x) | 66 960 |
| **1x (HTML+CSS+88+440)** | **56 982 (~56 KB)** |
| **2x (HTML+CSS+88+880)** | **94 224 (~92 KB)** |

Orçamento: **500 KB**. Folga ampla.

**LCP** em viewport 360×800, DPR 2, 4G simulado (1,6 Mbps down, RTT 150 ms, CPU 4×):
**1 064 ms**, elemento `IMG.hero__logo` (`logo-880.webp`). Abaixo do limiar “bom” (2,5 s).
Registro: `dev/capturas-landing/lcp.json`.

## Capturas (360 / 768 / 1024 / 1440)

Em `dev/capturas-landing/`:

| Arquivo | O que mostra |
|---|---|
| `landing-360.png` | hambúrguer (corte 1000 px) |
| `landing-360-menu.png` | menu aberto; Entrar roxo no contorno; Quero participar branco no gradiente |
| `landing-768.png` | hambúrguer ainda visível |
| `landing-1024.png` | menu horizontal (acima de 1000) |
| `landing-1440.png` | desktop |
| `landing-1440-pagina.png` | página inteira: obra + estudo dirigido, 5 papéis, 4 níveis, contato sem canais |
| `homenagens-360.png` / `homenagens-1440.png` | mesma casa visual; lista vazia, sem cartões de exemplo |

## Homologação

O `deploy/subir.sh --v1` agora recria a `landing` com `--force-recreate --no-deps`,
recusa `DATABASE_URL` no contêiner e exige **200** em `/`, `/homenagens` e `/login`.

A publicação na VPS é do **DEPLOY** (ADR-016). Este marco **não** rodou `subir.sh` e
**não** reiniciou o Traefik. A raiz de `homolog.didasko.app.br` segue 401 até o
executor subir esta branch.

## O que este marco não fecha

- a publicação em produção (autorização específica do ARQUITECT, §6 do `landing.md`);
- o banco para a landing (dívida pós-v1);
- as obras (fatia 2) e o acesso (marco 1b);
- o merge do marco 1 (PR #7).
