# Intent: DEM-202610-012 / credencial-de-seed

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: achado de 2026-10-19 (a senha do seed é pública) + D-01 da ADR-018 + ADR-008
signed_at:
supersedes: —
open_questions_open: 1
spec_citations: — (preenchido ao fechar a spec)
nivel_agil: 3 — segurança (ADR-018)
executor: **Codex** (piloto DEM-014)

## 1. Problema

`gsi_ebd/data/seed.py` tem `DEFAULT_PASSWORD = "senha123"` e `ADMIN_EMAIL = "admin@gsi.ebd"`, e
cria o admin com **`must_change_password=False`** ("Admin não precisa trocar"). O repositório é
**público** e o site está no ar: **qualquer pessoa que leia o código entra como admin** — vê
leads, aprova estudos, gerencia usuários. Depois da DEM-002, o admin é o **único** papel que faz
essas três coisas.

A ADR-008 já declarou a dívida; o **D-01** (ADR-018) fixou o gatilho: **antes de dados reais ou de
divulgação**. Esta DEM tira a senha do código; a **rotação dos usuários que já existem** em
produção é operação do ARQUITECT (mudar a senha do admin, e decidir sobre os demos).

## 2. Outcome

**Um seed novo não cria nenhuma conta com senha conhecida.** A senha vem do ambiente, é obrigatória,
e **todos** os usuários criados pelo seed nascem com `must_change_password=True` — inclusive o
admin. E **nenhum arquivo do repositório contém `senha123`**.

## 3. Afetados

Quem roda o seed (o ARQUITECT, com o `.env`), o admin e os usuários de demonstração de produção
(que **não** mudam sozinhos — a rotação é dele), e os testes.

## 4. Escopo

**In**
- o seed lê a senha de **`SEED_PASSWORD`** (ambiente), sem default;
- **fail-fast** se `SEED_PASSWORD` não existir (não gera, não avisa e continua: aborta);
- `must_change_password=True` para **todos** os usuários do seed, **incluindo o admin**;
- remover `senha123` do código, das docs e dos testes (o teste usa uma senha de fixture);
- teste que prova: (a) sem a variável o seed falha; (b) com ela, todos nascem com a troca
  obrigatória; (c) **nenhum** `senha123` no repositório (varredura).

**Out (non-goals)**
- **trocar a senha dos usuários que já existem** em produção — é operação do ARQUITECT (D-01);
- alterar o fluxo de troca de senha (já existe e `must_change_password` já é respeitado);
- mexer em `create_gestor` (o convite de gestor tem o mesmo padrão — **registrar**, não mudar
  aqui: seria escopo novo).

## 5. Constraints

- **Nível 3** (segurança): processo completo, com EVAL cego.
- **Nenhum segredo no repositório** (ADR-008): a senha não aparece em código, docs, testes nem
  no `.env.example` com valor real.
- **O seed continua idempotente** ("já existe → pula").
- O `.env` de produção ganha `SEED_PASSWORD` — **tarefa do ARQUITECT**, fora do código.
- O `.env.example` ganha a chave **sem valor** (ou com placeholder óbvio).

## 6. Health metrics

- **H-01** · a suíte continua verde · baseline **113 testes** · porteiro **EVAL**
- **H-10** · seed **sem** `SEED_PASSWORD` falha (exit ≠ 0, mensagem clara) · baseline **não existe** · porteiro **EVAL**
- **H-11** · **zero** ocorrências de `senha123` no repositório · baseline **existe em `seed.py` e nas docs** · porteiro **EVAL**

## 7. Sinal de sucesso

Um seed novo num ambiente limpo **não** cria admin com senha conhecida; e a varredura do repo não
encontra `senha123`. O ARQUITECT troca a senha do admin de produção no fechamento do D-01.

## 8. Decisões já registradas (não são perguntas)

| # | Questão | Decisão |
|---|---|---|
| 8.1 | De onde vem a senha | **`SEED_PASSWORD`** do ambiente; sem default |
| 8.2 | O que fazer sem a variável | **abortar** (fail-fast), com mensagem que diga o que fazer |
| 8.3 | O admin | **`must_change_password=True`** — o admin não é exceção |
| 8.4 | Quem rotaciona produção | **o ARQUITECT**, no fechamento do D-01 |

## 9. Pergunta aberta — só o ARQUITECT fecha

- [ ] **9.1** O seed deve **gerar** uma senha aleatória forte e **imprimir uma vez** no terminal
  quando `SEED_PASSWORD` faltar, em vez de abortar? *Recomendação: abortar. O seed é uma operação
  explícita; quem roda sabe a senha que definiu — e uma senha impressa num log de CI vaza.*

## 10. Fora de julgamento

O formato do hash (bcrypt já é o padrão do projeto), o nome do script, a mensagem exata do erro.
