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
## A verificação do ARQUITECT (22-23/10) — o `52495cd`

- **O cartão do contato**: o gradiente `#3B1470 → #4B1E8C`, o pior contraste **11,27:1** (antes
  2,62:1). **O item 1 resolvido.**
- **O `/homenagens`**: **DECISÃO DO ARQUITECT** — fica **FORA da produção** até haver homenagens reais.
- **A consequência**: o link **"Homenagens"** (o menu **e** a seção `#homenagens` da home) **não pode
  aparecer** quando não há homenagens. **A mesma regra dos depoimentos**: só renderiza se existir item
  **ativo** no arquivo versionado (`landing.yaml`), para o link **voltar sozinho** quando houver
  conteúdo. **O EVAL confere**: sem homenagens, o HTML do `/` **não contém link para `/homenagens`**.
- **A produção**: o roteador cobre **só o `/`** (e os assets estáticos da landing); o `/homenagens`, o
  `/login` e o resto **seguem na v0**.
## O aceite do ARQUITECT (o VISION) — 23/10

**O ARQUITECT deu o ACEITE do marco 2L (a landing)** — após a validação em janela anônima e o parecer
do 4º EVAL (o PASS no `2ca4610`).

- **O aceite cobre**: a landing (o conteúdo, o visual, o **AA**, o **cache versionado**, o **link
  condicional**, o **sem banco**), a homologação no `2ca4610`.
- **As ressalvas aceitas** (registradas, não bloqueantes): o **0,7 px** residual do menu; o **LCP/as
  capturas** não re-medidos no head; os **exemplos comentados** no YAML; os **6 casos** de contraste
  (não 3).
- **O que falta para a produção** (o ato separado): o **fix do hero** (o `display: none` no 360) e a
  **AUTORIZAÇÃO da produção** (a proposta das 5 peças — o roteador, os limites, a volta atrás, o teste,
  a substituição).
## A validação do ARQUITECT no celular (23/10) — o marco 2L **ACEITO VISUALMENTE**

O ARQUITECT validou o **`67f0623`** no celular: **o marco 2L está ACEITO VISUALMENTE**. O head final é
o `67f0623` (o CI `39951215227`; o CSS `landing.dfa7e29213827a3a.css`; o `.hero__visual
{ display: none }` no mobile; o `.menu { top: calc(100% - 14px) }`).

**O próximo**: a **proposta de autorização da produção** (a revisão dos 7 pontos, no
`planner/proposta-autorizacao-producao.md`). **O ato é do ARQUITECT.** **Nenhum ato em produção até
o aceite; o Traefik NÃO reinicia.**

## O ajuste ao registro do ciclo do "não mudou"

Os **três conferires** (a correção do ARQUITECT):

1. **O hash do CSS** (o **cache** e o **build**) — a URL versionada prova que o navegador vai buscar o
   novo;
2. **O commit do clone / o `headSha` do CI** (o **deploy**) — o clone está no commit que o DEVS
   mandou?
3. **O arquivo no build** (o Dockerfile copiou o arquivo certo?).

**O hash do CSS NÃO prova o commit do clone.** Ele prova que o **conteúdo servido** é versionado — e
o hash pode ser o de **um commit antigo** (o `9175a181…` do `2ca4610` × o `dfa7e292…` do `67f0623`).
**Conferir os DOIS**: o `git -C /home/didasko-deploy/homolog-v1 rev-parse --short HEAD` (o clone) e o
`git log --oneline -1` (a mensagem do commit).
