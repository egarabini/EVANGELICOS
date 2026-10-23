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

**LCP vigente (VISION, 22/10, navegador real na homologação, 768 px): 1 924 ms.**
Abaixo do limiar “bom” (2,5 s). Registro: `dev/capturas-landing/lcp.json`.

Medição anterior (21/10, local, 360×800, 4G simulado): 1 064 ms, `IMG.hero__logo`.

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
## A verificação do ARQUITECT (VISION) na homologação — 22/10

**PASSOU:**
- os cabeçalhos: o `no-cache` + o `ETag` no HTML; o `immutable` com o hash nos assets; o `image/webp`;
- sem dado de teste;
- o botão do topo: **11,27–13,82:1**;
- o menu em **1440/1024/768/375**, sem rolagem horizontal;
- o teclado: o `Tab` chega ao controle, o `Espaço` abre o menu;
- o `/login` 200;
- o **LCP 1.924 ms** (a 768 px);
- **~52 KB** na home.

**CORRIGIR (bloqueia o aceite) — fix em `52495cd`:**
- o `.contato__cartao` passou a `linear-gradient(125deg, #3B1470, #4B1E8C)` com
  parágrafo em `opacity: 1`; pior ponto **11,27:1**;
- teste WCAG no pior ponto do gradiente (cartão e `.botao--primario`), limiar 4,5:1.

**DECISÃO PENDENTE DO ARQUITECT:**
- a página `/homenagens` está **sem conteúdo** (só o título, a frase e o cartão); aguardar a decisão
  se ela entra na primeira publicação.

**O LCP:** o registro atualizado — **1.924 ms** na 768 px (o anterior, 1.064 ms, era anterior ao
`02eff4a`).
