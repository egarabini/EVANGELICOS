# Jornada do EVAL cego — DEM-005, marco 2L (a landing)

> O EVAL julgou o PR #8 (o head `02eff4a`) na homologação, sem confiar no relatório. O veredito:
> **FAIL** — um critério de contraste e uma decisão do despacho. O resto: PASS, com ressalvas.

## O veredito: **FAIL**

### Os dois bloqueios

**1. O contraste AA do `.botao--primario` — FAIL.**
O botão é `#fff` sobre `linear-gradient(120deg, #4B1E8C, #6D72C3 55%, #29ABE2)`. Medido **no pixel do
texto** (a captura `landing-1024.png`, o bbox do texto x870..980/y30..43; a fórmula do gradiente
validada contra o pixel):

| O ponto do gradiente | O contraste |
|---|---|
| o pior ponto **sob o texto** | **3,11:1** (no x980) |
| o stop **ciano** (`#29ABE2`) | **2,62:1** |
| o stop **índigo** (`#6D72C3`) | 4,33:1 |

O texto é 15,2 px/600 (o topo) e 16 px/600 (o hero) → **exige 4,5:1**. O defeito aparece no
**"Quero participar"** do topo **e** do hero (a mesma regra). O **"Entrar"** (o contorno, `#4B1E8C`
em `#F8F9FA`) = **10,69** ✓; os links do rodapé = 12,02/6,96 ✓; **a nota do contato** (o branco
85%, 14,7 px) = **3,52** — **também abaixo**.

**2. A decisão 3 do despacho (o contato) — FAIL.**
Os canais estão corretos (nenhum `mailto:`/`wa.me`), **mas** o template acrescenta o placeholder
*"Os canais de contato aparecem quando estiverem cadastrados."* (`index` l.229, `homenagens` l.61) —
**na cara do visitante**. O despacho §2.3 diz: **sem canais, a seção fica só com o convite** — sem
placeholder.

### O que **PASS** (com as ressalvas)

- **O menu**: PASS com ressalva — o CSS está certo (o `order: -1`, o painel lateral, o hover, o
  checkbox); as capturas 768/1024/1440 são de **antes do head** (a de 768 mostra o hambúrguer à
  direita — stale); **o teclado não abre** o menu (o checkbox é `display:none` e o label é
  `aria-hidden`) — a observação de acessibilidade do DoD.
- **As duas definições**: PASS (o HTML e a captura 1440).
- **Sem bastidor**: PASS (o grep — nenhum n+1/hash/snapshot; o "papel" só na classe).
- **Sem dados de teste**: PASS (o grep; o `landing.yaml` só com os exemplos **comentados**).
- **O peso**: PASS — 60,2 KB (1x) / 96,5 KB (2x), o limite 512 KB; zero `<script>`, zero CDN.
- **A raiz**: PASS — o `/` 200 (10.000 B), o `/homenagens` 200, o `/login` 200.
- **O LCP**: PASS com ressalva — 1.064 ms, o `IMG.hero__logo` (o logo-880), o 4G simulado; medido
  em `127.0.0.1:8010` e **antes** do `02eff4a` (as URLs sem hash); não reproduzido (sem browser).
- **O cache**: PASS — o CSS versionado com `public, max-age=31536000, immutable`; o HTML com
  `no-cache` + o `etag:"57c3afaaecc63f03"` e o **304** no `If-None-Match`; os nomes sem hash →
  **404**; o hash = o `sha256(conteúdo)[:16]` (o CSS servido = `fbc3428c9a2a7e6a` ✓). Nuances: o
  `curl -I /` → **405** (o HEAD não implementado); o WebP servido como `application/octet-stream`.
- **As decisões**: B1/B2/B4/B5 PASS (o `landing.yaml` sem banco; o `create_app` recusa o
  `DATABASE_URL`; o contêiner sem a variável; a seção dos depoimentos sem o `id` quando vazio; o
  `inspect` com só o `LANDING_LOGIN_URL` e a rede `deploy_didasko`).
- **A fonte única**: PASS (o `landing-prototipo/README.md` = CONGELADO; o diretório limpo).
- **Os testes**: PASS — a v1 **60**, a v0 **269**, o CI do `02eff4a` (o run `39771652866`) success.

### O que ele **não** testou

O painel aberto no head (360/768) e o **hover real** (sem browser no sandbox); o **LCP** no head; o
**teclado** do menu; o `curl -I /` (405). Não tocou na produção/no Traefik/na v0; não fez `up/down`.

## O que falta para passar

1. **O contraste do `.botao--primario` ≥ 4,5:1** sob o texto (escurecer o fim do gradiente, usar o
   sólido ou o texto escuro no fim claro) no topo e no hero — **e a nota do contato**;
2. **Remover a `contato__nota`** (e o teste que a exige) para a seção ficar **só com o convite**;
3. **Re-tirar as capturas** 768/1024/1440 no head e **re-medir o LCP**;
4. **(A qualidade)**: o `content-type: image/webp` e o **acesso por teclado** ao menu.

**A lição do EVAL**: o contraste foi medido **no pixel**, com a fórmula do gradiente validada — não
é "parece claro"; é **3,11:1 onde o texto está**. E o placeholder era o tipo de coisa que o autor
acha que ajuda e o visitante lê como sistema inacabado.
## A 2ª rodada — o FAIL no cartão do contato (o head `a703389`)

O EVAL julgou de novo, do zero, sem confiar em documento. Os **dois bloqueios do parecer anterior
estão CORRIGIDOS** e PASS:

- o `.botao--primario`: o `linear-gradient(120deg, #3B1470, #4B1E8C)` — o `#3B1470` = **13,82:1**, o
  `#4B1E8C` = **11,27:1**, e a varredura de **1001 pontos** do gradiente: o pior = **11,27** (≥ 4,5);
- a `contato__nota`: **0 ocorrências** de "cadastrados"/`contato__nota` no HTML servido, no CSS e nos
  templates; o teste que a exigia saiu.

O resto também PASS: o **cache** (o `no-cache` + o `ETag` + o **304**; o `immutable` com o hash; o
**404** sem hash; o `?v=` → 404, não usado); o **`image/webp`**; as **decisões** (o sem banco; os
depoimentos só com o `ativo`; os canais; o contêiner só na `borda`); a **fonte única** (o CONGELADO);
os **testes 60/269** (o EVAL rodou os 329 juntos); o **CI**; o **peso** (60,4/125,8 KiB); a **raiz**;
as **definições**.

### O FAIL: o parágrafo do `contato__cartao`

O cartão usa o `linear-gradient(125deg, #4B1E8C, #6D72C3 60%, #29ABE2)` — **o ciano de novo no
fim**. O parágrafo (16 px/400, branco, `opacity: .92`) sobre o fim claro:

| O ponto | O contraste |
|---|---|
| o 1440 (o fim da 1ª linha, o fundo `#6876C5`) | **4,21:1** (o branco puro) / **3,84** (o glifo com o 92%) |
| o head (o cartão mais baixo, sem a nota) | **~3,7:1** |
| o 360 (o fim da 2ª linha, o fundo `#4C8DD2`) | **~3,2:1** |

A norma exige **4,5:1**. A `opacity: .92` **piora**: o branco puro ainda dá **4,08** no 1440 e 3,44 no
360 — **o fundo tem de escurecer**.

### O fix

O gradiente do cartão com as **duas pontas roxas** (o `#3B1470` → o `#4B1E8C`, como o botão) e o
`opacity: 1`; **remedir** o pior pixel do parágrafo em **360 e 1440 ≥ 4,5**.

### A ressalva do menu (o hover)

O vão de **~13,7 px** entre o label (40 px, o fim em y=53,7) e o painel (o `top: 100%`, o y=67,4) —
no hover o cursor pode sair do label e o painel **fechar**. O clique/o checkbox funciona. O fix é o
painel **encostar** no label (o `top: calc(100% - X)` ou o `padding`).

### O que **não** deu

O pixel real no head (sem browser); o hover/o teclado/o painel aberto; o LCP no head (o registro é do
`127.0.0.1:8010`, antes do head); o `HEAD /` (405). **O EVAL não fabricou nada.**
## A 3ª rodada — o **PASS com ressalvas** (o `52495cd`)

O EVAL julgou o `52495cd` (o CI `39856130366`; o container up; o CSS servido byte-idêntico ao head).

**PASS:**
- **o contraste**: o `.contato__cartao` — o **11,2687** (o pior, no `#4B1E8C`) a 13,8158 (o
  `#3B1470`), em **4097 amostras**; o `.botao--primario` idem; o **360 e o 1440 sem media query de
  cor** → o pior ponto possível é o `#4B1E8C` → **≥ 11,27 nas duas larguras**;
- **o teste WCAG**: o `test_contraste_landing.py` (**3 testes**: o cartão, o botão e a **prova do
  ciano**) rodam e passam; a prova extra existe — com o CSS real do `02eff4a`, a mesma função dá
  **2,43** (cartão) e **2,619** (botão), abaixo de 4,5;
- **o `/homenagens`**: 200 na homologação; o `docker-compose.producao.yml` do head **não** tem o
  serviço landing nem o `Path(/homenagens)` — o roteador da v1 não a inclui. **Nuance**: a v0 tem a
  própria página `/homenagens`; a URL de produção é a da v0, não a da v1;
- **o cache** (a URL `b7d755afbdfcf7fc.css`; o `no-cache` + o `ETag` + o 304; o `immutable`; o 404
  sem hash; a URL muda `fbc3428c → e8784ecb → b7d755af`); as **decisões**; a **fonte única**; os
  **64/269**; o **CI**; o **peso** (61.901 B 1x / 99.143 B 2x); a **raiz**; as **definições**.

**As ressalvas:**
- **o vão do menu (o 13,7 px) NÃO foi corrigido** — o `.menu { top: 100% }` do `@media ≤1000` no head;
  o **DoD "painel encostado" não está cumprido**; o VISION validou o teclado/o clique, mas o **hover
  pode fechar**. **Se o aceite exigir o DoD literal, é FAIL**;
- as **capturas** 360/768/1024/1440 do repositório são de 21/10 (pré-head); não há a do **painel no
  head**;
- **fora do critério medido** — o `.rotulo` laranja (`#E87722`) **2,42–2,96:1** em texto pequeno; o
  **número dos níveis** (o branco sobre o roxo→ciano) **2,62 no ciano** / ~4,29 no canto do glifo. **O
  AA da página inteira não passaria**; os **2 alvos do foco** (o botão e o cartão) passam.

**O worktree sujo** durante a auditoria (7 arquivos) é o **WIP das homenagens/produção** — o
`{% if homenagens %}`, o filtro do `ativo`, o roteador de produção comentado e 3 testes — **não está
no `52495cd` nem na homologação**; ele julgou o HEAD pelo `git archive`.
