# O despacho — o menu mobile da landing (o fix visual)

- **Data:** 2026-10-21 · **Nível 2** (a ADR-018) — um fix dentro do marco 2L.
- **O gatilho:** o ARQUITECT viu o menu aberto na homologação (o print) e não gostou: o painel cobria
  o conteúdo, os botões ocupavam a largura toda e os títulos vazavam pelo fundo translúcido.
- **A referência:** o protótipo **já está corrigido** (o commit `1135930`, o
  `planner/landing-prototipo/`) — o DEVS **porta**, não redesenha.

## O que mudar

1. **`v1/templates/landing/index.html`** e **`v1/templates/landing/homenagens.html`**: a **ordem do
   menu** — o `<input class="menu__alternador">` e o `<label class="menu__botao">` **antes** do
   `<a class="marca">` (o hambúrguer à esquerda).
2. **`v1/static/landing/landing.css`**: o bloco `@media (max-width: 1000px)`:
   - o **hambúrguer à esquerda** (`order: -1`);
   - o **menu como painel lateral** (`min(320px, 86vw)`, da esquerda, **fundo branco opaco**, a
     sombra, o canto arredondado — **sem** o fundo translúcido que deixava o conteúdo vazar);
   - ele abre no **hover** (o `.menu__botao:hover ~ .menu` e o `.menu:hover`), com o **checkbox
     como fallback do toque**.

## O que **não** muda

O conteúdo, o `v1/landing.yaml`, as rotas, a regra do **sem banco**. O fix é **só de CSS e de
ordem de HTML**.

## O DoD

- o **CI verde**;
- o **DEPLOY** roda o `bash deploy/subir.sh --v1` na branch da landing;
- a **homologação** mostra o menu novo — o ARQUITECT valida;
- o **EVAL** confere (o menu em 360/1024, o hover, o painel lateral).

## A ordem

O DEVS porta → o CI → o DEPLOY roda o `subir.sh --v1` → o ARQUITECT valida → o EVAL → a produção
(com a autorização específica).
