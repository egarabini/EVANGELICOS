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
