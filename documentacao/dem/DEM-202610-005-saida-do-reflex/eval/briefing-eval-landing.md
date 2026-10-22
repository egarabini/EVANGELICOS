# Briefing do EVAL cego — DEM-005, **marco 2L** (a landing)

> Julgue **sem confiar no relatório** e **sem ler a jornada do DEVS**. A régua é o despacho, o
> briefing e o plano. A saída é o **PASS/FAIL por critério, com a evidência** (o comando e a saída).

## 1. O alvo

- o **PR #8**, o head **`02eff4a`**;
- a **homologação** `homolog.didasko.app.br` (o `/`, o `/homenagens`, o `/login`);
- o **`v1/landing.yaml`** (vazio, por enquanto);
- o **deploy**: o `subir.sh --v1` (o fast-forward `a753222..02eff4a`), os assets versionados
  `landing.fbc3428c9a2a7e6a.css` + `logo-*.{hash}.webp`, o contêiner `didasko_v1_landing` só na
  rede `borda`.

## 2. O que ler (a régua)

1. `documentacao/dem/DEM-202610-005-saida-do-reflex/dev/despacho-menu.md` — **as 3 correções** (o
   cache versionado, as decisões no porte, a v1 como fonte única) e o DoD;
2. `.../dev/briefing-landing.md` — os §6/§7/§8;
3. `.../planner/landing.md` — os §10–§14;
4. `.../eval/briefing-eval-marco-1.md` — o formato (não é o alvo deste EVAL);
5. as ADRs **002/003/008/014 v3/018/021**.

## 3. O que julgar (os critérios)

| # | O critério | A prova |
|---|---|---|
| 1 | o **contraste AA** dos botões (o topo, o hero, o rodapé) | a medição da cor do texto × o fundo |
| 2 | o **menu** em **360, 768, 1024, 1440** (o hambúrguer à esquerda; o painel lateral no hover) | as capturas + o CSS |
| 3 | as **duas definições** de obra e estudo dirigido | o texto no HTML e na tela |
| 4 | **sem linguagem de bastidor** (a N+1, o hash, o snapshot, o número do papel) | o grep no HTML |
| 5 | **os links sem dados de teste** (nenhum `mailto:`/`wa.me` de exemplo) | o grep |
| 6 | o **peso** (< 500 KB na carga inicial; sem JS de terceiros) | a soma + o grep |
| 7 | a **raiz da homologação** serve a landing (o `/` 200, o `/homenagens` 200) | o `curl` |
| 8 | o **LCP** em móvel simulado (o registro do DEVS) | o valor |
| **A** | **o cache**: o HTML `no-cache` + `ETag` (o 304); os assets `max-age` longo + `immutable` **só** com o hash na URL; **a URL muda com o conteúdo**; **sem hash, o 404** | os headers + o `curl` |
| **B** | **as decisões**: o `landing.yaml` sem banco/`DATABASE_URL`; os depoimentos só com o `ativo` (**sem ativo, a seção não existe no HTML**); os canais só se existirem; **sem dados de teste**; o contêiner **sem a variável e sem a rede** para o banco | o compose + o HTML + o postgres |
| **C** | **a fonte única**: a `v1` é a landing; o `landing-prototipo/` está **CONGELADO** (o README) | o README + o commit |
| **D** | os **testes**: a v1 **60**; a v0 **269**; o CI do `02eff4a` (o run `39771652866`) | o pytest + o run |

## 4. A régua do veredito

- **PASS/FAIL por critério**, com a **evidência** (o comando e a saída);
- no FAIL, **o que falta** e **o que faria passar**;
- o que **não deu** para testar, dito com todas as letras;
- **não confie** no relatório nem na jornada — **o comando é a prova**.

## 5. O que **não** fazer

- tocar na **produção**/no **Traefik**/na **v0**;
- o `down`/o desmonte da homologação;
- alterar o código do PR;
- editar o `landing-prototipo/` (CONGELADO);
- inventar valores.
