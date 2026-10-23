# Changelog — DEM-005

## 2026-10-23 — aceite 2L: hero no celular, vão zero, yaml sem exemplo

- `@media ≤960`: `.hero__visual { display: none; }`. Desktop inalterado.
- Menu: `top: calc(100% - 14px)` (zera o vão de 0,7 px do `-13px`).
- `v1/landing.yaml` sem e-mail/telefone/item de exemplo, mesmo comentado.
- `.gitignore`: `.eval*/` e `.eval4-tmp/`. Removido `.eval4-tmp/` da raiz.
- Commit `67f0623`. Local: **71** da v1 + **269** da v0. CI:
  https://github.com/egarabini/gsi_ebd/actions/runs/39951215227 (success).
  DEPLOY: `subir.sh --v1` (não executado aqui). VISION: 360 sem logo do hero,
  painel encostado, rótulo AA, link de homenagens ausente.

## 2026-10-23 — vao do menu e AA do texto pequeno

- Painel `.menu` no `@media ≤1000`: `top: calc(100% - 13px)` (antes `100%`).
  Encosta no label; o vão de 13,7 px fechava o hover.
- `.rotulo`: `#9A3412` (texto pequeno AA). `#E87722` era 2,42–2,96; o exemplo
  `#B45309` falha no `--azul-claro` (4,11).
- Número dos níveis: `linear-gradient(140deg, --roxo-escuro, --roxo)` (mesmo
  tratamento do botão/cartão). O número permanece no CSS.
- Testes: painel encostado; `.rotulo` e `.trilha__passo span` ≥ 4,5:1.
- Commit `2ca4610`. Local: **70** da v1 + **269** da v0. CI:
  https://github.com/egarabini/gsi_ebd/actions/runs/39933115533 (success).
  DEPLOY: `subir.sh --v1` (não executado aqui; publica `906a6dd` + este fix).
  VISION valida o hover e o AA.

## 2026-10-23 — ARQUITECT: link condicional das homenagens

- Menu "Homenagens", seção `#homenagens` e link do rodapé no `index.html`
  só renderizam com `{% if homenagens %}` (item `ativo: true` no
  `v1/landing.yaml`). Mesma regra dos depoimentos.
- `_homenagem` exige `ativo`. `homenagens: []` no arquivo commitado.
- Testes: sem homenagens, o HTML do `/` não contém `href="/homenagens"` nem
  `#homenagens`; com uma ativa, contém; só inativa, não abre o link.
- Homologação mantém `Path(/homenagens)`. Produção da v1 (proposta de
  autorização): só `/` e `/static/landing`; `/homenagens`, `/login` e o resto
  seguem na v0.
- Commit `906a6dd`. Local: **67** da v1 + **269** da v0. CI:
  https://github.com/egarabini/gsi_ebd/actions/runs/39931396359 (success).
  DEPLOY: `subir.sh --v1` (não executado aqui). EVAL confere o HTML do `/`
  sem o link.

## 2026-10-22 — VISION: cartão de contato, teste de contraste, LCP, portão /homenagens

- `.contato__cartao` (home e `/homenagens`): `linear-gradient(125deg, #3B1470, #4B1E8C)`
  e parágrafo com `opacity: 1`. Pior ponto medido **11,27:1** (limiar 4,5:1).
- Teste WCAG: luminância relativa no pior ponto do gradiente; falha abaixo de
  4,5:1 no cartão e no `.botao--primario`; prova de que o ciano reprova.
- `/homenagens` permanece na app e na homologação. Fora do roteador de produção
  da v1 até o ARQUITECT autorizar (homenagens reais).
- LCP vigente: **1.924 ms** (768 px, VISION, navegador real).
- Commit `52495cd`. Local: **64** da v1 + **269** da v0. DEPLOY: `subir.sh --v1`
  (não executado aqui).

## 2026-10-22 — fix do parecer do EVAL (marco 2L): contraste e placeholder

- Commit `a703389` na branch `feature/DEM-202610-005-landing` (sobre o `02eff4a`).
- `.botao--primario`: o gradiente roxo→índigo→ciano caía a **3,11:1** sob o texto
  branco (a norma exige 4,5:1); agora `linear-gradient(120deg, --roxo-escuro,
  --roxo)`, as duas pontas escuras, **>=8,5:1** em qualquer ponto.
- Removido o placeholder "Os canais de contato aparecem quando estiverem
  cadastrados." (o `{% else %}` dos dois templates, o CSS `.contato__nota` e o
  assert do teste) — sem canais, a seção de contato fica só com o convite.
- Qualidade (não bloqueante): `mimetypes.add_type("image/webp", ".webp")` em
  `v1/landing.py` (o slim não conhecia a extensão; servia `application/octet-stream`);
  checkbox do menu focável por teclado só no breakpoint mobile (`sr-only`; o
  Espaço alterna o `:checked`, sem JS).
- Verificação local (sem pytest completo — faltam as dependências da v0/Reflex
  nesta estação; a suíte roda no CI): script direto contra `v1.landing` confirma
  as duas páginas 200, sem o placeholder, `content-type: image/webp` nos assets
  e o novo gradiente no CSS servido.
- CI: https://github.com/egarabini/gsi_ebd/actions/runs/39835747275 (success).
- Homologação: `subir.sh --v1`, CSS novo em `landing.e8784ecbc0f4a9c1.css`,
  `/`, `/homenagens`, `/login` 200; Traefik e app de produção não reiniciados.
- **Pendente** (fora do alcance desta sessão — não há navegador automatizado,
  ADR de perfil): as capturas 768/1024/1440 e do painel aberto no head, e a
  remedição do LCP. Avaliação visual segue com o ARQUITECT/EVAL.

## 2026-10-22 — hash no nome e cache das 3 correções

- Commit `02eff4a` na branch `feature/DEM-202610-005-landing` (worktree `.worktrees/DEM-005-landing`).
- Hash SHA-256 do conteúdo no **nome** (`logo-88.<hash>.webp`, `landing.<hash>.css`),
  gerado no build da imagem (`python -m v1.landing_assets`).
- HTML: `Cache-Control: no-cache` + ETag (304 na revalidação).
- CSS/WebP versionados: `public, max-age=31536000, immutable`. URL sem hash: 404.
- Teste de que trocar o arquivo troca a URL (e o `srcset`).
- Visual já portado: logo recortado 45px / 90w, rodapé 34px, menu à esquerda.
- `landing-prototipo/` permanece CONGELADO. Homologação: o DEPLOY com `subir.sh --v1`.
- Local: **60** testes da v1 + **269** da v0.

## 2026-10-21 — cache do porte completo

- `a753222`: assets versionados por hash de conteúdo; HTML/CSS com no-cache,
  WebP versionado com cache de um ano e immutable.
- Testes de render nas duas páginas: srcset 90w, topo 45 px, rodapé 34 px,
  recorte novo; testes de cache e revalidação por ETag.
- Local: 58 testes da v1 e nove de páginas passaram.
- CI: https://github.com/egarabini/gsi_ebd/actions/runs/39698536189.

## 2026-10-21 — logo novo e agrupamento mobile

- `0c8f0ef`: porte do complemento local do protótipo (logo novo, 45 px,
  botão de 40 px, marca e hambúrguer juntos à esquerda).
- URLs versionadas do CSS/logo para atualização do cache do navegador.
- 54 testes da v1 e nove de páginas passaram; captura local conferida.
- CI: https://github.com/egarabini/gsi_ebd/actions/runs/39698022094.

## 2026-10-21 — correção visual do menu mobile

- Commit: `74e3ee3`, na branch da landing, PR #8.
- CI **success**: https://github.com/egarabini/gsi_ebd/actions/runs/39694772157.
- Porte do protótipo `1135930`: controles antes da marca, hambúrguer à esquerda,
  painel lateral branco opaco com hover e fallback por checkbox.
- Validação local: **269 + 54 testes passaram**; Chrome em ambas as páginas,
  mobile em 360 px e verificação desktop em 1440 px.
- Capturas `menu-fix-*-360.png` em `dev/capturas-landing/`.
- Atualização da homologação cabe ao DEPLOY.

## 2026-10-21 — landing (marco 2L) entregue para revisão

- Branch: `feature/DEM-202610-005-landing` (worktree `.worktrees/DEM-005-landing`), a partir do marco 1.
- Commit do código: `f9aa301a4a4a44745b787746d7deea1cda860df3`.
- PR: https://github.com/egarabini/gsi_ebd/pull/8 → `feature/DEM-202610-005-marco1`.
- CI: https://github.com/egarabini/gsi_ebd/actions/runs/39689542371 — **success**
- Código: serviço `v1.landing:create_app` (Jinja2, sem banco) + labels Traefik no compose da homologação.
- Suíte da v1: 54 passaram. Regressão da v0: 269 passaram.
- LCP local (4G simulado): 1 064 ms. Carga 2x: ~92 KB.
- Relatório: `dev/relatorio-landing.md`. Capturas: `dev/capturas-landing/`.
- Homologação ao vivo: aguarda o DEPLOY (`bash deploy/subir.sh --v1`). Traefik não reiniciado.

## 2026-10-20 — esqueleto da v1 entregue para revisão

## 2026-10-20 — esqueleto da v1 entregue para revisão

- Commit do código: `4a344dd3ea5e46a491d14e5769a1ad04527ee17d`.
- Commit do isolamento do Compose: `4f9e9c9c07e25aa2f9cf6e393ca1d036a8e689d4`.
- PR: https://github.com/egarabini/gsi_ebd/pull/7 → `develop`.
- CI verde: https://github.com/egarabini/gsi_ebd/actions/runs/39451719272 e
  https://github.com/egarabini/gsi_ebd/actions/runs/39452803850.
- Suíte da v1: 37 passaram, a partir de `v1/`. Regressão da v0: 269 passaram.
- Homologação em `https://homolog.didasko.app.br/login` (HTTP 200), certificado
  Let's Encrypt YR2, banco `didasko_v1` no baseline `0001_baseline`. O Traefik da v0
  não foi reiniciado.
- EVAL cego ainda não rodou. Sem merge.
