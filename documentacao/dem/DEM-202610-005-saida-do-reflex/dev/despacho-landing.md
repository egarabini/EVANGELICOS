# O despacho — a landing (o marco 2L) para o DEVS

- **Data:** 2026-10-21 · **Nível 2** (a ADR-018): **uma** rodada de EVAL.
- **O alvo:** a landing na **v1** (o Jinja2), na **homologação** (`homolog.didasko.app.br/`), **sem
  login** e **sem banco**.
- **A referência visual:** `planner/landing-prototipo/` (o `index.html`, o `homenagens.html` e o
  `landing.css`) — **porte-o, não o reescreva**.
- **O contrato do conteúdo:** `v1/landing.yaml` (vazio por enquanto) — os `depoimentos[]`, o
  `contato` e o `hero`/`sobre` (opcionais).

## As regras (o briefing §6/§7 e o landing.md §10–13)

1. **O contraste** dos botões (WCAG AA) — o do topo, o do hero e o do rodapé.
2. **O menu** vira hambúrguer **abaixo de 1000 px**; testar em **360, 768, 1024 e 1440** e registrar
   as capturas.
3. **A seção de obras** com as duas definições: **A obra** (a fonte) e **O estudo dirigido** (a obra
   aplicada: capítulos + questões + instrutor).
4. **Sem linguagem de bastidor** (o texto do site é do visitante); **sem dados de teste**.
5. **Os depoimentos** só renderizam com pelo menos um `ativo: true` no `v1/landing.yaml`; **sem
   "Em breve"**. **O contato** só aparece se o `email`/o `whatsapp` existirem no arquivo; sem canais,
   a seção fica só com o convite.
6. **A página `/homenagens`** no mesmo padrão da landing (o conteúdo do `landing.yaml` — a lista de
   homenagens; hoje não há).
7. **A landing NÃO recebe `DATABASE_URL`** e **não tem rede para o banco**; o contêiner sobe sem a
   variável — o EVAL confere.
8. **O orçamento**: menos de **500 KB** na carga inicial; **sem JS de terceiros**; o **LCP**
   registrado em conexão móvel simulada.
9. **A raiz da homologação** serve a landing (hoje 401).

## O Definition of Done

- a landing **na raiz** da homologação (**200**), com o `/homenagens`;
- os **testes** do render (as seções, o `{% if %}` com o `landing.yaml` vazio **e** preenchido);
- a **suíte da v1 verde** + a **regressão da v0 (269)**; o **CI verde**; o **relatório** com as
  capturas (360/768/1024/1440), o **LCP** e o **peso** da página.

## O que **não** é deste despacho

- a **publicação em produção** — exige a **autorização específica do ARQUITECT** (o roteador do `/`
  e do `/homenagens`, os limites, a volta atrás, o teste de que o `/login` e o app da v0 seguem
  respondendo). **Não reiniciar o Traefik**;
- o **banco** para a landing (a dívida do pós-v1);
- as **obras** (a fatia 2) e o **acesso** (o 1b) — depois da landing.

## A ordem

O despacho → a homologação (o executor avisa o ARQUITECT quando a raiz servir a landing) → a
validação dele → o EVAL cego (a §12 do `landing.md`) → a autorização da produção.
