# Despacho ao DEVS — a fatia 2 da DEM-017 (a criação do Estudo + as avaliações)

> **O quê / o porquê / o DoD / o risco.** A **branch nova a partir da `develop`** (o **`b5573bd`**).
> A fatia 1 (os painéis) está no merge; **esta é a criação e o fluxo editorial**.

## 1. O quê

1. **A CRIAÇÃO DO ESTUDO pelo Admin** (o `/admin/estudos`): a **obra aplicada em capítulos** — o
   `Estudo` + o `EstudoCapitulo` (o modelo **já existe**); a **lista** dos estudos e o **formulário**
   (a obra de origem, os capítulos, as questões).
2. **As AVALIAÇÕES/LIBERAÇÕES do Revisor** (o `/revisor/avaliacoes`): a **fila**; o **parecer**
   (o `revisar`/o `recusar`); a **liberação** — o **ADR-020**: a **assinatura do Revisor + a
   liberação do Admin**; a **N imutável** (o ciclo cria a N+1); o **hash LF+NFC**.
3. **Os TESTES DOS ALUNOS FAKE na lista do painel** (o `/admin`): o **"Aluno Fake A"/o "Aluno
   Fake B"** com os **resultados** (o `Progress`/o `UserResponse`) — a lista que a fatia 1 deixou
   pronta.

## 2. As rotas novas (a matriz, sem teste vacuoso)

| A rota | O papel |
|---|---|
| **`/admin/estudos`** | **ADMIN** (a lista) |
| **`/admin/estudos/nova`** | **ADMIN** (o formulário) |
| **`/revisor/avaliacoes`** | **REVISOR** (a fila/o parecer) |
| (as do fluxo) | as da matriz |

**O teste**: a **matriz** (o permitido 200 **E** o negado 403), a **vacuidade** (o monkeypatch →
403), o **menu** (o ADMIN vê o **Estudos**; o REVISOR vê as **Avaliações**), e o **só leitura × a
escrita** (aqui **há** escrita — o teste distingue o `GET` do `POST`).

## 3. O plano de testes

| # | O teste | A prova |
|---|---|---|
| 1 | **A criação do Estudo** | o `POST /admin/estudos/nova` → 303; o `Estudo` + o `EstudoCapitulo` criados |
| 2 | **A lista dos estudos** | o `GET /admin/estudos` → 200 com os estudos |
| 3 | **A fila do Revisor** | o `GET /revisor/avaliacoes` → 200 com o que está em revisão |
| 4 | **O parecer** | o `POST` do parecer → 303 (o Revisor); o **Admin sozinho** → 403/409 |
| 5 | **A liberação pelos dois** | a assinatura do Revisor + a liberação do Admin → 303; a **N imutável** |
| 6 | **O hash LF+NFC** | o mesmo conteúdo com o LF/NFC → o mesmo hash |
| 7 | **Os fake na lista** | o `/admin` → 200 com o "Aluno Fake A/B" e os **resultados** |
| 8 | **A matriz** | as rotas novas com o permitido **e** o negado; a vacuidade; o menu |
| 9 | **A não-vacuidade** | o teste **falha** se as chaves forem removidas |

## 4. O DoD

- a **criação do Estudo** (o form + a lista); as **avaliações/liberações** (o ADR-020); os **fake na
  lista**;
- as **rotas na matriz** sem teste vacuoso; o **EVAL cego** (o máximo de 2 — o ADR-018); o **CI
  verde**; a **documentação** da DEM-017 atualizada.

## 5. O risco

| O risco | A mitigação |
|---|---|
| a criação **furar o ADR-020** (a liberação sem os dois) | o teste 5 (o Admin sozinho → 403/409) |
| a **N** ser editada (a imutabilidade) | o teste 5 (a N+1) |
| a matriz **vacuosa** | o teste 9 |
| o escopo inflar (o estudo completo/UI) | o **fluxo mínimo** (a criação → a liberação → a lista); a UI fina na fatia 3 |

## 6. O prompt para o DEVS

```text
A fatia 2 da DEM-202610-017 — a criacao do Estudo + as avaliacoes/liberacoes + os testes dos fake.

A BRANCH NOVA a partir da develop (o b5573bd). NUNCA o #11.

O QUE:
1. A CRIACAO DO ESTUDO pelo Admin (o /admin/estudos + o /admin/estudos/nova): a obra aplicada em
   capitulos (o Estudo + o EstudoCapitulo); a lista e o formulario.
2. As AVALIACOES/LIBERACOES do Revisor (o /revisor/avaliacoes): a fila; o parecer (o revisar/o
   recusar); a liberacao - o ADR-020: a assinatura do Revisor + a liberacao do Admin; a N imutavel
   (o ciclo cria a N+1); o hash LF+NFC.
3. Os TESTES DOS ALUNOS FAKE na lista do painel (o /admin): o "Aluno Fake A/B" com os resultados (o
   Progress/o UserResponse).

AS ROTAS NOVAS (a matriz do rbac.py, sem teste vacuoso): o /admin/estudos = ADMIN; o /admin/estudos
/nova = ADMIN; o /revisor/avaliacoes = REVISOR.
O TESTE: a matriz (o permitido 200 E o negado 403); a vacuidade (o monkeypatch -> 403); o menu (o
ADMIN ve o Estudos; o REVISOR ve as Avaliacoes); a criacao (o POST -> 303; o Estudo criado); a
liberacao (os dois; o Admin sozinho -> 403/409); a N imutavel; o hash LF+NFC; os fake na lista.

O DoD: a criacao; as avaliacoes/liberacoes; os fake na lista; a matriz nao vacuosa; o EVAL cego (o
maximo de 2); o CI verde; a documentacao da DEM-017.

NAO: a UI fina dos demais papeis (a fatia 3); o banco da v0; o roteamento de producao; o subir.sh.
```
