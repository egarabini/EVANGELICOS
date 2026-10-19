# Intent: DEM-202610-012 / credencial-de-seed

status: signed
owner: PLANNER
signed_by: ARQUITECT
origin: achado de 2026-10-19 (a senha do seed é pública) + D-01 da ADR-018 + ADR-008
signed_at: 2026-10-19
supersedes: —
open_questions_open: 0
spec_citations: 100% — todo RF cita §2, §4 ou uma decisão do §8
nivel_agil: 3 — segurança (ADR-018)
executor: **Codex** (DEVS; ver a DEM-014)
nota_de_assinatura: o ARQUITECT fechou a única pergunta (9.1: **abortar**) e aprovou a correção do escopo do RF04 (2026-10-19).

## 1. Problema

`gsi_ebd/data/seed.py` tem `DEFAULT_PASSWORD = "senha123"` e `ADMIN_EMAIL = "admin@gsi.ebd"`, e
cria o admin com **`must_change_password=False`**. O repositório é **público** e o site está no ar:
**qualquer pessoa que leia o código entra como admin** — vê leads, aprova estudos, gerencia
usuários. Depois da DEM-002, o admin é o **único** papel que faz essas três coisas.

A ADR-008 já declarou a dívida; o **D-01** (ADR-018) fixou o gatilho. Esta DEM tira a senha do
código. A **rotação dos usuários que já existem** em produção é operação do ARQUITECT.

## 2. Outcome

**Um seed novo não cria nenhuma conta com senha conhecida.** A senha vem do ambiente, é
obrigatória, e **todos** os usuários do seed nascem com `must_change_password=True` — inclusive o
admin. E a senha **não aparece** nos arquivos do seed, nos testes, nos docs operacionais nem na
saída do deploy.

## 3. Afetados

Quem roda o seed (o ARQUITECT, com o `.env`), o admin e os usuários de demonstração de produção
(que **não** mudam sozinhos — a rotação é dele), o deploy (a saída do `subir.sh`) e os testes.

## 4. Escopo

**In** (o **escopo de remoção** da senha, definido com o ARQUITECT em 19/10)
- o seed lê a senha de **`SEED_PASSWORD`** (ambiente), sem default;
- **fail-fast** se `SEED_PASSWORD` estiver ausente **ou vazia** (aborta, não gera);
- `must_change_password=True` para **todos** os usuários do seed, **incluindo o admin**;
- remover `senha123` de: **`gsi_ebd/data/seed.py`**, **`tests/`**, **`README.md`**,
  **`deploy/DEPLOY.md`** e **`deploy/subir.sh`** (este último imprime a senha no fim do deploy);
- `.env.example` documenta `SEED_PASSWORD=` **sem valor real**;
- teste que prova: (a) sem a variável o seed falha; (b) com ela, todos nascem com a troca
  obrigatória; (c) os arquivos do escopo **não** contêm a senha.

**Exceções explícitas** (citam a senha por necessidade histórica e **não** entram na varredura):
- `documentacao/adr/ADR-008*` (o registro da dívida) e os registros de **DEM/EVAL**;
- `Diagnostico/*.md` (registro histórico do próprio projeto);
- `gsi_ebd/states/admin.py` (`create_gestor`) e `gsi_ebd/pages/admin.py` (o texto da tela) —
  são a **D-10**.

**Out (non-goals)**
- **trocar a senha dos usuários que já existem** em produção — operação do ARQUITECT (D-01);
- **`create_gestor` e o texto da tela** — são a **D-10** (coordenador criado com senha conhecida);
- alterar o fluxo de troca de senha (já existe e `must_change_password` já é respeitado).

## 5. Constraints

- **Nível 3** (segurança): processo completo, com EVAL cego.
- **Nenhum segredo no repositório** (ADR-008): a senha não aparece em código, docs, testes nem
  no `.env.example` com valor real.
- **O seed continua idempotente** ("já existe → pula").
- O `.env` de produção ganha `SEED_PASSWORD` — **tarefa do ARQUITECT**, fora do código.

## 6. Health metrics

- **H-01** · a suíte continua verde · baseline **113 testes** · porteiro **EVAL**
- **H-10** · seed **sem** `SEED_PASSWORD` (ou com ela vazia) falha · baseline **não existe** · porteiro **EVAL**
- **H-11** · **zero** ocorrências de `senha123` **nos arquivos do §4** (a varredura cobre a lista, não o repositório inteiro — as exceções estão declaradas) · baseline **existe no seed, no README, no DEPLOY.md, no subir.sh** · porteiro **EVAL**

## 7. Sinal de sucesso

Um seed novo num ambiente limpo **não** cria admin com senha conhecida; a saída do deploy não
imprime senha; e a varredura do escopo não encontra `senha123`. O ARQUITECT troca a senha do admin
de produção no fechamento do D-01.

## 8. Decisões (fechadas pelo ARQUITECT)

| # | Questão | Decisão |
|---|---|---|
| 8.1 | De onde vem a senha | **`SEED_PASSWORD`** do ambiente; sem default |
| 8.2 | O que fazer sem a variável | **abortar** (fail-fast) — decidido em 19/10 |
| 8.3 | O admin | **`must_change_password=True`** — o admin não é exceção |
| 8.4 | Quem rotaciona produção | **o ARQUITECT**, no fechamento do D-01 |
| 8.5 | `create_gestor` e o texto da tela | **D-10** — fora desta DEM |

## 9. Perguntas abertas

**Nenhuma.** A 9.1 foi fechada (abortar).

## 10. Fora de julgamento

O formato do hash (bcrypt já é o padrão), o nome do script, a mensagem exata do erro.
