# Despacho ao DEVS — o fix do EVAL da fatia 2 (o fluxo do aluno fake)

> **O EVAL deu FAIL em 1 de 7** (o critério 5: o fluxo do aluno fake). **O resto passou** — o rbac, a
> matriz 15, a vacuidade, o ADR-020, os testes, o CI e a branch. **O fix é focado.**

## O quê

1. **O teste REAL do aluno fake** (o item (a) do parecer): no `v1/tests/test_estudo_fake.py`, o teste
   **do fluxo do plano §3**:
   - o **login como `aluno.fake.a`**;
   - o **GET da obra/estudo liberado** → **200**;
   - o **POST da resposta** (a questão) → **201/303**;
   - o **assert do `UserResponse`/`Progress`** no banco (o progresso registrado);
   - e o **`aluno.fake.b`** na obra **não liberada** → **403/vazio**.
2. **O seed exercitado num teste** (o item (b)): o `popular()`/`run()` do `seed_homolog_estudo.py`
   com o **engine `didasko_v1`** (o SQLite serve) — e o **`DIDASKO_AMBIENTE=homologacao`** exigido:
   - o `recusar_producao` **fecha o `fail-open`**: o **vazio/desconhecido** → **erro** (não a URL);
   - o teste do **fail-open** (o `ambiente=""` → o erro).
3. **O relatório** (a ressalva): o `relatorio-fatia-2.md` **atualizado** — o **#9/`3f9246e`/130+272**,
   não o #5/`3b5f56c`/157+269.
4. **O briefing** (a ressalva): o head **`8ae1a3c`** e o run do **`pull_request` `40038006423`** (não
   o do `workflow_dispatch`).

## O porquê

**A isolação dos fake está certa** — o que falta é **provar o fluxo**: o plano §3 diz que o aluno
fake **entra, vê e responde**; o teste atual **insere as linhas direto e relê o banco** — ele prova o
**esquema**, não o **caminho**. **O EVAL pega o teste vacuoso** — o mesmo erro da matriz do marco 1.

**E o `fail-open` do `recusar_producao` é um risco real**: um ambiente **vazio** (o default do shell)
seria aceito — e o seed rodaria **fora** da homologação.

## O DoD

- o `test_estudo_fake.py` **com o `entrar(aluno.fake.a)`** e o fluxo completo (o GET, o POST, o
  assert); o `aluno.fake.b` → 403/vazio;
- o **`popular()`** exercitado **num teste** (o SQLite com o esquema `didasko_v1`); o
  **`DIDASKO_AMBIENTE`** exigido e o **vazio/desconhecido** recusado (o fail-open fechado);
- o `relatorio-fatia-2.md` e o briefing **atualizados**;
- o **CI verde**; o **2º EVAL** (a 2ª rodada — o máximo do ADR-018).

## O risco

| O risco | A mitigação |
|---|---|
| o teste "passar" sem o fluxo | o teste **falha** se a rota do aluno não existir (o 404/403); o login é real |
| o seed rodar fora da homologação | o `DIDASKO_AMBIENTE` **obrigatório**; o `ambiente=""` **recusa** |
| a 2ª rodada do EVAL esgotar | o ADR-018: **máximo 2** — o fix tem de ser **completo** |
| o escopo inflar (as telas de aluno) | **(c)** é **ambiguidade de escopo** — o ARQUITECT decide; o fix é o **teste** do fluxo que **já existe** |
