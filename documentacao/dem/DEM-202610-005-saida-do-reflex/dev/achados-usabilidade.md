# Achados de usabilidade — a v1

> Achados encontrados **em uso**, registrados para tratamento posterior. Não são falhas do EVAL: são
> observações de experiência que o EVAL não cobra (o comportamento é o projetado) e que o
> ARQUITECT decide quando entram.

## A-01 — o `/` responde 401 em vez de redirecionar ao login

- **Onde:** `https://homolog.didasko.app.br/` (o marco 1, em 21/10/2026).
- **O que acontece:** o browser cai na página de **401** com o texto "Entre para continuar" — **sem
  tratamento**. O usuário que abre a raiz do sistema vê uma parede em vez do login.
- **O que deveria:** redirecionar (**303**) para o `/login`, preservando o destino (o `?next=...`
  quando a rota pedida era outra).
- **A análise:** o **401** é a resposta correta do **servidor** para uma requisição não autenticada
  (API); para uma **navegação de browser**, a resposta correta é o **redirecionamento**. São
  respostas de contextos diferentes, e o handler da raiz está usando a do contexto errado.
- **O impacto:** o primeiro contato com o sistema é uma página de erro. Quem já tem o link do
  `/login` não sofre; quem abre a raiz, sim.
- **A prioridade:** **baixa** — não bloqueia o login nem o EVAL; a correção é uma linha no handler
  da raiz (um `RedirectResponse` com o 303).
- **Quando:** o marco 1 está **no EVAL** — a correção entra no **marco 1b** (ou num ajuste do marco
  1, se o EVAL o devolver por outro motivo). **Não** é, por si, bloqueio do EVAL.
- **A regra para as próximas rotas:** as rotas de **navegação** da v1 redirecionam ao login quando
  não autenticadas; as de **API** devolvem o 401. O teste do marco 1b cobre as duas.

## O formato de um achado

- o **onde** e o **quando** (o ambiente, a data);
- o **que acontece** e o **que deveria** — sem opinião, o comportamento;
- a **análise** (por que a diferença importa);
- o **impacto** e a **prioridade**;
- o **quando** (o marco/o ajuste) e a **decisão** do ARQUITECT, quando houver.
