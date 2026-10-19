# Plano de testes — DEM-202610-005 / a v1

> Nível 3. O plano é **incremental por marco**: cada marco entra com os seus testes antes de
> começar. O EVAL cego usa o `metodo/templates/briefing-eval.md` (com os contornos de ambiente).

## 1. Por marco

| Marco | Os testes | O que prova |
|---|---|---|
| **1 — esqueleto** | a **matriz papel × rota** (todas as rotas da v1 × os 4 papéis); o login/logout; o CSRF (o POST sem token recusado); o cookie (httponly/secure); o **banco `didasko_v1` com o baseline** | H-04/H-05; a auth própria; o banco próprio |
| **2 — admin/revisor/obras** | o fluxo pela tela (importar → revisar → liberar → alterar → contestar); o **H-14**; o `exec -e` no script | o fluxo da DEM-011 nas telas |
| **3 — coordenador** | vincular/desvincular + o adendo do ambiente; o **H-15** (o coordenador criado sem senha fixa) | a autonomia do coordenador sem a D-10 |
| **4 — instrutor** | ver a turma, corrigir; a matriz | as telas do instrutor |
| **5 — lição** | o **H-06** (a lição: HTTP 200 + "João 3:16" e as relacionadas) | o estudo completo |
| **6 — virada** | o **retorno** (a v0 em ≤ 5 min); o critério dos dados reais escrito; o HTTP no domínio principal | H-13 |

## 2. Os testes transversais (desde o marco 1)

- **H-14 (a D-11)**: usuário com a flag só alcança a troca e o logout; **qualquer rota/evento
  protegido recusa antes** da troca.
- **H-15 (a D-10)**: a criação do coordenador **sem senha fixa** (o token de uso único com
  expiração ou a senha aleatória nunca exibida).
- **A matriz + o inventário de rotas**: o teste que **renderiza todas as rotas por papel** e
  compara com a matriz (a DEM-002, na base nova).
- **A prova de mutação**: remover a dependência de papel de uma rota → o teste da matriz falha;
  remover o bloqueio da flag → o H-14 falha.

## 3. Baseline

| Item | Hoje | Esperado |
|---|---|---|
| a suíte da v1 | não existe | o baseline da v1, escrito no marco 1 |
| a matriz na base nova | migrar da DEM-002 | o teste que renderiza |
| as dívidas | D-10/D-11 abertas | fechadas pelos H-14/H-15 |

## 4. O que **não** é teste desta DEM

A v0 (o Reflex) — ela só recebe correção até a virada; os testes dela são os 128 atuais.

