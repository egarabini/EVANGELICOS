# A jornada do EVAL — a fatia 2 das obras (a DEM-011)

## A 1ª rodada — o FAIL no critério 5 (o fluxo do aluno fake)

O EVAL julgou o **PR #9** (o head **`8ae1a3c`**; os runs `40038005779`/`40038006423`/`40038703819`).

**PASS:**

| # | O critério | A evidência |
|---|---|---|
| 1 | **O rbac** | **não existe o `v1/rbac.py`**; a matriz real é o **`gsi_ebd/utils/rbac.py#L34-L37`**: `/admin/obras` = (ADMIN,), `/revisor/obras` = (REVISOR,), `/obras` = (ADMIN, REVISOR); o `v1/auth.py#L92-L101` usa o `pode()` |
| 2 | **A matriz 15** | o `test_obras_matriz.py#L33-L60`: **15 parametrizados**, cada um com o permitido (200) e o negado (403) — os 15 PASSED |
| 3 | **A vacuidade** | o `test_matriz_obras_falha_sem_as_tres_chaves` (#L79-L87): remove as 3 chaves → Admin `/admin/obras` 403, Admin `/obras` 403, Revisor `/revisor/obras` 403, Revisor `/obras` 403 |
| 4 | **O ADR-020** | o `test_obras_adr020.py` (7 testes): o Revisor 403 nas 5 ações admin; o Admin 403 nas 4 do revisor; a liberação pelos dois (o Admin sozinho 409, o Revisor sozinho 403, os dois 303); a **N imutável** e a **N+1**; o **hash LF+NFC** (2 params); a `aberta → suspensa_para_novos`; o cancelar |
| 6 | **Os testes** | a v1 **130**; a v0 **272**; no head `8ae1a3c` a suíte completa dá **273** (o `tests/test_ci.py`) |
| 7 | **O CI** | os runs `40038005779` (o `workflow_dispatch`), o `40038006423` (o `pull_request` no `3f9246e`) e o `40038703819` (o `pull_request` no `8ae1a3c`) — todos `success` |
| 8 | **A branch** | o `git log 5c0bc3e..HEAD` = o `3f9246e` + o `8ae1a3c`; o `3f9246e^ = 5c0bc3e`; o diff do `5c0bc3e..3f9246e` **sem** o esqueleto do #5 (27 arquivos, só as obras/as telas/os testes) |

**FAIL — o critério 5 (os alunos fake, o fluxo):**

- **a isolação passa**: o `ALUNOS_FAKE` só no `v1/seed_homolog_estudo.py#L28-L39`; o
  `recusar_producao` (#L42-L51) recusa o "producao" e o banco ≠ `didasko_v1`; **0 matches** de
  `aluno.fake`/`homolog.didasko.local`/`seed_homolog_estudo` no `gsi_ebd/data/seed.py`;
- **mas o `test_estudo_fake.py` NÃO testa o fluxo do plano (§3)**: só faz o `entrar(Revisor)` (L49) e
  o `entrar(Admin)` (L52); **não há o `entrar(aluno)`**; o `StudyAssignment`/`UserResponse`/`Progress`
  são **inseridos direto** (L96, L113, L124) e o teste **só relê o banco**; **não há o GET/POST do
  aluno** nem a **rota de aluno** na v1;
- **o `recusar_producao(url=..., ambiente="")` é `fail-open`**: aceita qualquer ambiente que **não
  seja literalmente "producao"**;
- **o seed não é chamado pelo `subir.sh`** (o L150-L160 roda o `gsi_ebd.data.seed`; **0 refs** ao
  `seed_homolog_estudo` no `deploy/`);
- o `popular()` do seed **exercitado à mão em SQLite** criou 2 fake users/1 estudo/1 study+version/1
  assignment — **mas isso não está na suíte**.

**O que falta para PASS:**

- **(a)** um teste **real** do aluno fake: o `login` como `aluno.fake.a`, o **GET da obra/estudo
  liberado**, o **POST da resposta**, o **assert** do `UserResponse`/`Progress`; e o `aluno.fake.b`
  recebendo **403/vazio** na obra **não liberada**;
- **(b)** chamar/executar o **`popular()`/`run()`** do seed num **teste com o engine `didasko_v1`**
  (ou o wire no `subir.sh`/README) e **exigir o `DIDASKO_AMBIENTE=homologacao`** (recusar o
  **vazio/desconhecido**), testando o **fail-open**;
- **(c)** se "desenvolvimento (capítulos, questões)" for requisito duro: hoje o `conteudo_form.html`
  só tem os capítulos/adendos da obra, **não o `EstudoCapitulo.questions_json`**; o design-fatia-2
  diz que as **telas de aluno são de outra fatia** → **a ambiguidade de escopo é do ARQUITECT**.

**RESSALVAS** (não bloqueiam sozinhas): o `relatorio-fatia-2.md` ainda descreve o **PR #5/`3b5f56c`/
157+269** (não o #9/`3f9246e`/130+272); o **briefing está um commit atrasado** (o head `8ae1a3c`) e
cita o run do `workflow_dispatch` em vez do `pull_request` `40038006423`.
