# Despacho ao DEVS — o seed **fail-closed** (a dívida 15)

> **O quê / o porquê / o DoD / o risco.** O pedido do AUXILIAR após a passada técnica (24/10): **o
> seed deve FALHAR com mensagem clara quando não houver obra liberada.**

## O quê

O `v1/seed_homolog_estudo.py` deve **falhar** (o `RuntimeError`) quando **não houver nenhuma `Obra`
com o `versao_liberada_id`** no `didasko_v1`. Hoje ele é **fail-open**: sem a obra liberada, ele
**cria só os alunos e sai em silêncio** (o `studyassignment` com **0 linhas**).

## O porquê

**O silêncio é o defeito**: o seed "passou" (exit 0) e **não criou o estudo nem o assignment** — quem
depende dele (a validação visual) **vê as telas vazias** e **não sabe por quê**. **Um seed que não
semeia tem de gritar**, não sussurrar.

## O fix

No **`popular()`** (ou no início do `run()`):

```python
if not session.exec(select(Obra).where(Obra.versao_liberada_id.is_not(None))).first():
    raise RuntimeError(
        "o seed de alunos fake exige ao menos uma Obra com versao_liberada_id no didasko_v1; "
        "libere a obra no fluxo do Admin/Revisor antes de rodar o seed"
    )
```

**A ordem no seed**: o `recusar_producao` (o ambiente/o banco) **primeiro**, depois a **obra
liberada**, depois os alunos.

## O DoD

- o seed **sem** a obra liberada → **`RuntimeError`** com a mensagem clara (não o exit 0);
- o seed **com** a obra liberada → os **2 alunos fake** + o **estudo** + o **assignment**;
- o **teste** (`test_seed_homolog.py`): o caso **sem a obra** → o `pytest.raises(RuntimeError)`; o
  caso **com a obra** → o fluxo completo;
- o **`recusar_producao`/o `DIDASKO_AMBIENTE`** intactos; **o seed nunca roda em produção**;
- o **CI verde**.

## O risco

| O risco | A mitigação |
|---|---|
| o seed quebrar na homologação por falta da obra | **é o objetivo** — a mensagem diz **o que fazer** (liberar a obra) |
| o teste antigo do `popular()` passar a falhar | o teste **com a obra** é o caminho normal; o **sem a obra** é o novo caso |
| o seed rodar em produção | o `recusar_producao` continua **primeiro** |
