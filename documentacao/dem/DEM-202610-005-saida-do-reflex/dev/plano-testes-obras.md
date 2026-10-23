# Plano de testes — as obras (DEM-011, fatia 2)

> O plano do **EVAL cego** e do **CI**. A régua: o **rbac** (as 3 chaves) + a **matriz de papéis** +
> as **regras do ADR-020** + o **modo estudo com os alunos fake**.

## 1. A matriz de papéis × rotas (o teste NÃO vacuoso)

| A rota | ADMIN | COORDENADOR | INSTRUTOR | ALUNO | REVISOR |
|---|---|---|---|---|---|
| `/admin/obras` | **200** | 403 | 403 | 403 | 403 |
| `/revisor/obras` | 403 | 403 | 403 | 403 | **200** |
| `/obras` | **200** | 403 | 403 | 403 | **200** |

**A regra do teste**: **cada célula** tem **duas asserções** — o **permitido** (200) e o **negado**
(403/404). **O teste tem de FALHAR** se o `rbac.py` for vazio (a lição do marco 1: a matriz que só
verifica o permitido passa com tudo liberado).

**A prova da vacuidade**: um teste auxiliar que **remove** as 3 chaves (num monkeypatch) e **confirma
que a matriz falha** — o mesmo padrão do `test_rf02_matriz` do marco 1.

## 2. As regras de autoridade (o ADR-020)

- **só o Admin** muda o **estado de publicação** (o `publicar`/o `suspender`);
- **o Revisor** move o **estado editorial** (o `em_revisao`/o `aprovado`), **assina o parecer** e o
  **`solicitar_revisao`**;
- **a liberação exige a assinatura do Revisor + a liberação do Admin** (o teste: o Admin sozinho
  **não** libera; o Revisor sozinho **não** libera; os dois **sim**);
- **a versão liberada é imutável** (o teste: a tentativa de editar a versão liberada → erro; o ciclo
  cria a **N+1**);
- **o hash canônico** com a **normalização LF + NFC** (o teste: dois arquivos com o mesmo conteúdo e
  os line endings/Unicode diferentes → o **mesmo** hash).

## 3. O modo estudo com os alunos fake

- o fluxo: a **inclusão da obra** → o **desenvolvimento** (os capítulos, as questões) → a
  **aprovação** → o **estudo com os alunos fake**;
- **onde os dados fake vivem**: o banco **`didasko_v1` de HOMOLOGAÇÃO** — **nunca** a produção;
- o teste: o aluno fake **entra**, **vê a obra liberada**, **responde as questões**, e o **progresso**
  é registrado; o **outro** aluno fake **não** vê a obra **não liberada** (o teste da disponibilidade
  + o estado).

## 4. O que o EVAL cego vai medir

- a **matriz** (as 15 células, com as duas asserções);
- a **vacuidade** (a matriz falha sem o `rbac`);
- o **ADR-020** (a liberação exige os dois; a imutabilidade; o hash);
- o **modo estudo** (o aluno fake; o dado só na homologação);
- o **CI** e os **testes** (a contagem).

## 5. O risco

| O risco | A mitigação |
|---|---|
| a matriz vacuosa | as duas asserções por célula + a prova da vacuidade |
| o dado fake na produção | o seed de homologação; a produção nunca recebe |
| o Revisor com autoridade demais | o ADR-020; a liberação exige os dois |
| o escopo inflar | a fatia 2 = o fluxo mínimo (a inclusão → o teste); o resto na fatia 3 |
