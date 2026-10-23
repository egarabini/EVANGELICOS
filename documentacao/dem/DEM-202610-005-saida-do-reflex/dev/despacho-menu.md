# O despacho — o porte do protótipo INTEIRO para a v1 (+ o cache)

- **Data:** 2026-10-22 · **Nível 2** (a ADR-018) — o fix do marco 2L, aprovado pelo ARQUITECT com
  **três correções**.
- **O gatilho:** o protótipo avançou 4 arquivos (o logo/45px/90w/o recorte) e a v1 (`74e3ee3`) tem só
  o menu; e o sintoma "o deploy não mudou a página" revelou o **cache heurístico**.

## As três correções do ARQUITECT

### 1. O cache longo SÓ vale com a URL versionada

- **O HTML**: `Cache-Control: no-cache` + o **ETag** — o navegador revalida a cada visita.
- **O CSS, os WebP e os demais assets**: `max-age` longo + `immutable` **SOMENTE** com o **hash do
  conteúdo no nome** (`logo-88.<hash>.webp`) ou em **`?v=<hash>`** nas referências. O hash é
  **gerado no build a partir do conteúdo**, nunca um número de versão manual.
- **Trocar o conteúdo de um asset troca a URL dele** — vale também para o **`srcset`**.
- **O motivo**: o `logo-88.webp` mudou de conteúdo mantendo o nome; o `immutable` com o nome fixo
  repetiria o sintoma — quem já visitou continuaria vendo o logo antigo.

### 2. O porte carrega as decisões anteriores, não só o visual

Além do logo (o 45px, o `srcset` 90w), do menu e do cache, o porte inclui — e o **EVAL confere**:

1. o **conteúdo condicional vem de arquivo versionado** (`v1/landing.yaml`), **SEM banco** e **SEM
   `DATABASE_URL`** (a opção A, já decidida);
2. a seção de **depoimentos só renderiza com pelo menos um item `ativo: true`**; sem item ativo,
   **ela não existe no HTML**;
3. **cada canal de contato só aparece se estiver no arquivo**; sem canais, a seção fica **só com o
   convite**;
4. o arquivo entra **sem nenhum dado de teste** (nenhum `mailto:`/`wa.me` de exemplo);
5. o **contêiner da landing sobe sem variável de banco e sem rede para o banco**.

### 3. Uma só fonte da landing: a V1

- **Depois do porte, a `v1` é a única fonte.** O `landing-prototipo/` vira **histórico** (o README
  dele marcado como **CONGELADO**) — ou é removido da DEM.
- **Todo ajuste visual nasce direto na v1** e é validado na homologação.
- **A regra anterior** ("o protótipo é a fonte da verdade visual") **sai do briefing** — ela só
  administrava a duplicação, e a duplicação acabou.

## O que portar (o visual)

| O arquivo do protótipo | O que portar para a v1 |
|---|---|
| o `landing.css` | o `.marca__logo { width: 45px; height: 45px }` (a v1 está em 44px) |
| o `index.html` | o `srcset` **90w** e o `sizes` **45px** no logo do topo (o rodapé os 34px) |
| o `homenagens.html` | o mesmo `srcset`/`sizes` |
| o `assets/logo-88.webp` | o **recorte novo** (o livro preenchendo os 45px) — com o **hash no nome** |

## O DoD (os acréscimos do ARQUITECT)

- o **CI verde**; o **DEPLOY** roda o `bash deploy/subir.sh --v1`;
- o **teste automatizado dos cabeçalhos**: o HTML com o `no-cache` + o `ETag`; os assets versionados
  com o `max-age` longo + o `immutable`;
- o **teste de que o nome/a URL do asset muda quando o conteúdo muda**;
- a **validação do ARQUITECT em janela anônima** na homologação (**sem** o `Ctrl+F5`): o **logo do
  recorte**, o **menu**, a **versão de celular**, os **textos de obra e estudo dirigido**;
- o **EVAL confere**: as 5 decisões do item 2 + o cache (o item 1) + a fonte única (o item 3).

## A ordem (mantida)

**O DEVS porta** → o **CI** → o **DEPLOY** (o `subir.sh --v1`) → a **validação do ARQUITECT** (a
janela anônima) → o **EVAL cego do marco 2L** → a **produção** (com a autorização específica do
roteamento).
## O adendo do EVAL (o parecer do marco 2L) — o fix dos 2 bloqueios

O EVAL deu **FAIL** em duas coisas. O resto passou (com ressalvas).

### 1. O contraste do `.botao--primario` (o bloqueio de acessibilidade)

Medido **no pixel do texto**: o pior ponto sob o texto = **3,11:1**; o stop ciano = 2,62; o índigo =
4,33. O texto (15,2 px/600 no topo, 16 px/600 no hero) **exige 4,5:1**.

**O fix**: o `.botao--primario` deixa o gradiente que termina no **ciano claro** e passa a um
**fundo escuro** — o sólido `#4B1E8C` ou o `linear-gradient(120deg, #3B1470, #4B1E8C)` (o
contraste do branco sobre o `#4B1E8C` é ~8,5:1). **A nota do contato** (`rgba(255,255,255,.85)`,
14,7 px, o 3,52) sobe para o **branco a 100%** (ou o texto escuro) — e o mesmo vale para qualquer
texto sobre o gradiente do `contato__cartao`.

### 2. A `contato__nota` (a decisão 3 do despacho)

O placeholder *"Os canais de contato aparecem quando estiverem cadastrados."* **sai do template** —
a seção fica **só com o convite** (o título + a frase + o botão do CTA do contato). Remover também o
teste que a exige (`test_landing.py` l.227) e o CSS `.contato__nota`.

### 3. As provas a refazer (as ressalvas do EVAL)

- **as capturas 768/1024/1440** de novo, **no head** (as atuais são de 21/10, antes do `02eff4a`);
- **o painel aberto** (o hover) no 360/768 — a captura que o EVAL não tinha;
- **o LCP** de novo, no head, da homologação (o medido foi em `127.0.0.1:8010`).

### 4. A qualidade (não bloqueia, mas o EVAL registrou)

- o `content-type: image/webp` nos WebP (hoje `application/octet-stream`);
- o **acesso por teclado** ao menu (o checkbox é `display:none` + o label `aria-hidden`) — o
  `:focus-within`/o `sr-only` ou o botão real (o JS mínimo) resolvem.

## O DoD do fix

O contraste **≥ 4,5:1** medido no pixel (o topo, o hero, a nota); **sem a `contato__nota`**; as
capturas e o LCP **no head**; o CI; o DEPLOY roda o `subir.sh --v1`; a validação do ARQUITECT em
janela anônima.
## O adendo do 3º parecer (a 2ª rodada do EVAL) — o cartão do contato

Os dois bloqueios anteriores estão **corrigidos** (o `.botao--primario` 11,27:1; a `contato__nota`
0). O que reprova agora:

### 1. O parágrafo do `.contato__cartao` (o contraste)

O cartão usa o `linear-gradient(125deg, #4B1E8C, #6D72C3 60%, #29ABE2)` — o **ciano** de novo no fim.
O parágrafo (16 px/400, branco, `opacity: .92`): o **4,21:1** (o branco puro) / **3,84** (o glifo com o
92%) no 1440; **~3,7** no head; **~3,2** no 360. A norma exige **4,5**.

**O fix**: o gradiente do cartão com as **duas pontas roxas** (o `#3B1470` → o `#4B1E8C`) e o
`opacity: 1`; **remedir** o pior pixel em **360 e 1440 ≥ 4,5**.

### 2. O vão do menu no hover (a ressalva)

O vão de **~13,7 px** entre o label e o painel (`top: 100%`) — o painel pode **fechar** quando o
cursor sai do label. **O fix**: o painel **encostar** no label (`top: calc(100% - X)` ou o `padding`).

### O DoD

O contraste do parágrafo **medido ≥ 4,5** (o 360 e o 1440); o painel **encostado** no label; o CI; o
DEPLOY (o `subir.sh --v1`); a validação do ARQUITECT em janela anônima.
## O adendo do VISION (a verificação do ARQUITECT, 22/10)

O VISION confirmou o **mesmo ponto** do EVAL, agora no navegador real: o `.contato__cartao` (a home e
o `/homenagens`) tem o gradiente até o `rgb(41,171,226)` com o texto pequeno branco — o **4,33:1** no
meio e o **2,62:1** no canto. **O fix é o mesmo do botão** (as duas pontas escuras), **mais**:

**O teste de contraste** (a exigência do VISION): um teste automatizado que **calcule a razão de
contraste** (a fórmula da luminância relativa) do texto do `.contato__cartao` contra o **gradiente** —
o pior ponto — e **falhe** se ficar abaixo de 4,5:1. O mesmo teste vale para o `.botao--primario`.

**O `/homenagens` sem conteúdo**: a página tem só o título, a frase e o cartão. **A decisão de ela
entrar na primeira publicação é do ARQUITECT** — o DEVS **não** a remove nem a esconde sem essa
decisão; o portão fica registrado.

**O LCP**: o registro atualizado — **1.924 ms** na 768 px, medido no navegador real pelo VISION.
## O adendo da verificação do ARQUITECT (22-23/10) — o link condicional das homenagens

O cartão do contato está **resolvido** (o `11,27:1`) — o item 1 fecha. A **decisão nova**:

- **O `/homenagens` fica FORA da produção** até haver homenagens reais.
- **A consequência**: o link **"Homenagens"** (o menu **e** a seção `#homenagens` da home) **só
  renderiza se houver homenagem ativa** no `v1/landing.yaml` — a **mesma regra dos depoimentos**:
  - o `{% if homenagens %}` no item do menu e na seção;
  - o `homenagens: []` no arquivo vazio → **nada** aparece;
  - quando o ARQUITECT preencher o arquivo, o link **volta sozinho**.
- **O teste**: sem homenagens, o HTML do `/` **não contém** `href="/homenagens"` nem `#homenagens`; com
  uma homenagem ativa, **contém**. O **EVAL confere**.
- **A produção**: o **roteador cobre só o `/`** (e os assets estáticos); o `/homenagens`, o `/login` e
  o resto **seguem na v0** — é o que a proposta de autorização vai registrar.
## O adendo do VISION (23/10) — o logo do hero no celular

**O pedido**: no celular, o logo dentro do `.hero__logo` (o `.hero__visual`) **não deve aparecer** —
a marca do topo (o `.marca`, os 45 px) já mostra o Didasko; na tela pequena o logo grande é
**redundante** e ocupa a primeira dobra.

**O fix** (no `v1/static/landing/landing.css`, no `@media (max-width: 960px)`):

```css
.hero__visual { display: none; }
```

**O teste**: no 360, o `#hero` **não** tem o `.hero__visual`; no 1024/1440, **tem**.
**O que não muda**: o desktop; o `hero` fica com o título direto no celular.
**A validação**: o VISION (a janela anônima, no 360).
