# Changelog — DEM-005

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
