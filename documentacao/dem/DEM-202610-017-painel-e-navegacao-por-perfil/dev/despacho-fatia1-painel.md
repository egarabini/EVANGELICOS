# Despacho ao DEVS — a fatia 1 da DEM-017 (o painel do Admin e do Revisor)

> **O quê / o porquê / o DoD / o risco.** A fatia 1 é **só leitura**: o **painel-resumo** do Admin e
> do Revisor + o **menu por perfil** (derivado do `rbac.py`) + as **rotas novas na matriz** (sem teste
> vacuoso). **Nada de criação** (a fatia 2).

## 1. O quê — o painel do ADMIN (só leitura)

O `/admin` (o painel) com:

1. **as obras e os estudos**: as **disponíveis** e as **em estudo** (o `Obra`/o `ObraVersao`/o
   `Estudo`);
2. **os coordenadores**: com os **estudos que cada um escolheu** (o `Ambiente`/o `AmbienteEstudo`/o
   `VinculoObra.coordenador_id`);
3. **para cada coordenador**: os **instrutores** (o `Equipe`/o `EquipeInstrutor`) com os **alunos** (o
   `Turma`/o `TurmaMembro`);
4. **a lista de todos os alunos**: os **estudos feitos e a fazer** e os **resultados** (o
   `StudyAssignment`/o `Progress`/o `UserResponse`).

## 2. O quê — o painel do REVISOR (só leitura)

O `/revisor` (o painel) com:

- a **fila de revisão** (o que está em revisão);
- as **avaliações/liberações feitas** (o histórico do `ObraVersaoEvento`/o `revisado_em`).

**A nota**: os **testes dos alunos fake** ficam na **fatia 2** (a lista no painel) — **não** na 1.

## 3. O menu por perfil — **derivado do `rbac.py`**

- o **`base.html`** renderiza o **menu do papel atual** a partir da **matriz do `rbac.py`** (a fonte
  única) — **não** hard-coded no template;
- o **ADMIN** vê: o **Painel** (`/admin`), as **Obras** (`/admin/obras`), os **Estudos** (a fatia 2),
  os **Alunos** (o painel), o **Sair**;
- o **REVISOR** vê: o **Painel** (`/revisor`), a **Revisão** (`/revisor/obras`), o **Sair**;
- **o menu não mostra rota que o papel não pode** — e **a matriz é o teste**.

## 4. As rotas novas (na matriz, sem teste vacuoso)

| A rota | O papel | O que é |
|---|---|---|
| **`/admin`** | o **ADMIN** | o painel-resumo |
| **`/revisor`** | o **REVISOR** | o painel do revisor |
| (as rotas do menu) | as da matriz | as já existentes (`/admin/obras`, `/revisor/obras`, `/obras`) |

**O teste**: a **matriz** (o papel × a rota) com o **permitido (200)** **e** o **negado (403)**; a
**vacuidade** (o monkeypatch remove as chaves → o 403); o **menu** (o ADMIN vê as rotas do ADMIN; o
REVISOR **não** vê as do ADMIN; o anônimo não vê o menu).

## 5. O plano de testes

| # | O teste | A prova |
|---|---|---|
| 1 | **O painel do ADMIN** | o `/admin` → 200 com os dados (as obras/os coordenadores/os instrutores/os alunos) |
| 2 | **O painel do REVISOR** | o `/revisor` → 200 com a fila/o histórico |
| 3 | **A matriz** | as **4 rotas novas** com o permitido **e** o negado (a célula de cada papel) |
| 4 | **A vacuidade** | o monkeypatch remove as chaves → o 403 nas 4 |
| 5 | **O menu** | o HTML do ADMIN **tem** os links do ADMIN; o do REVISOR **não** tem os do ADMIN; o anônimo **não** tem o menu |
| 6 | **Só leitura** | **nenhuma rota nova escreve** (o POST no `/admin` → 405/403) |

## 6. O DoD

- o **painel do Admin** e o **do Revisor** (só leitura);
- o **menu por perfil derivado do `rbac.py`**;
- as **rotas na matriz** com o **teste não vacuoso** (o permitido **e** o negado; a vacuidade);
- o **EVAL cego** (o máximo de **2** rodadas — o ADR-018);
- o **CI verde**; a **documentação** da DEM-017 atualizada.

## 7. O risco

| O risco | A mitigação |
|---|---|
| o menu hard-coded **divergir** da matriz | o **menu derivado**; o **teste** do menu × a matriz |
| o painel virar **escrita** (o escopo) | o teste 6 (nenhuma rota nova escreve) |
| a **consulta** pesada (o N+1) | o **resumo** com as consultas agregadas; o EVAL mede |
| o escopo inflar (a criação do Estudo) | **a fatia 2** — o despacho diz |
## O PROMPT PARA O DEVS (a entrega obrigatória)

> **A regra (anotada em 24/10)**: a cada despacho, a entrega é **O PROMPT PARA O DEVS** — o texto que
> o ARQUITECT **cola** no DEVS. O despacho explica; **o prompt é o que se envia**. Sem o prompt, o
> despacho **não está entregue**.

```text
A fatia 1 da DEM-202610-017 — o painel do Admin e do Revisor (só leitura).

O QUE:
1. O /admin (o painel do ADMIN, só leitura): as obras/os estudos (as disponíveis e em estudo); os
   coordenadores com os estudos escolhidos; os instrutores (o EquipeInstrutor) com os alunos (o
   TurmaMembro); a lista de todos os alunos com os estudos feitos/a fazer e os resultados (o
   StudyAssignment/o Progress).
2. O /revisor (o painel do REVISOR, só leitura): a fila de revisão; o histórico das
   avaliações/liberações.
3. O MENU por perfil DERIVADO do gsi_ebd/utils/rbac.py (a fonte única): o base.html renderiza só as
   rotas que o papel pode; o ADMIN vê o Painel/as Obras/Os Estudos/Os Alunos/Sair; o REVISOR vê o
   Painel/A Revisão/Sair; o anônimo não vê o menu.
4. As ROTAS novas na matriz: o /admin = ADMIN; o /revisor = REVISOR.

O TESTE (o plano de testes, o dev/despacho-fatia1-painel.md):
- o painel do Admin (200 + os dados); o do Revisor (200 + a fila/o histórico);
- a matriz (o permitido 200 E o negado 403 nas rotas novas);
- a vacuidade (o monkeypatch remove as chaves -> 403);
- o menu (o HTML do ADMIN tem os links do ADMIN; o do REVISOR NÃO tem os do ADMIN; o anônimo não tem
  o menu);
- o só leitura (nenhuma rota nova escreve: o POST -> 405/403).

O DoD: os painéis; o menu derivado; a matriz não vacuosa; o EVAL cego (o máximo de 2); o CI verde; a
documentação da DEM-017 atualizada.

NÃO: a criação de obras/estudos (a fatia 2); o banco da v0; o roteamento de produção.
```
