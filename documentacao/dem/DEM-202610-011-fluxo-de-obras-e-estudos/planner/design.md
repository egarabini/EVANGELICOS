# Design — DEM-202610-011 / **fatia 1: o domínio** (v3 — fecha as lacunas do Codex e as 3 do ARQUITECT)

> Nível 3 (ADR-018). **Esta fatia não tem tela.** A v3 acrescenta as três correções de 19/10: o
> **instantâneo "visto"** (o texto que o Revisor leu), a **assinatura contra conteúdo não visto** e
> o **`alterar` com o conteúdo novo**. Inclui o requisito de deploy do inventário.

## 1. Os modelos

### `Obra` (existente) — acrescentar
- `status: str` — o estado publicado (`em_revisao|aguardando_admin|devolvida|liberada`);
- `versao_liberada_id: Optional[int]`;
- **`fonte_id: Optional[str]` (indexado)** — o `F-xxx` do inventário, persistente;
- `updated_at`.

### `ObraVersao` (nova)
```python
class ObraVersao(SQLModel, table=True):
    id, obra_id, numero
    status: str                          # em_revisao|aguardando_admin|devolvida|liberada|substituida
    conteudo_hash: str                   # o agregado DESTA versão
    parecer, ajustes_propostos (JSON), revisor_id, revisado_em, hash_visto
    ajustes_descritos, admin_id, liberada_em, hash_liberado
```
**Sem `itens_visto` em JSON**: ele é **derivado** do instantâneo "visto" (§3) — uma fonte só.

### As snapshots do conteúdo — **com o momento** (a correção 1)
```python
class ObraVersaoCapitulo(SQLModel, table=True):
    id, versao_id (FK), momento: str       # "visto" | "liberado"
    ordem, titulo, conteudo_md, item_hash
class ObraVersaoAdendo(SQLModel, table=True):
    id, versao_id (FK), momento: str       # "visto" | "liberado"
    codigo, titulo, texto, item_hash
```

- **`revisar` cria o instantâneo `visto`** (a cópia do conteúdo no momento em que o Revisor lê).
- **`liberar` cria o instantâneo `liberado`** (a cópia no momento da publicação).
- A diferença da RF11b compara **os dois instantâneos**: mostra **quais itens** mudaram **e o texto
  de cada lado** — não só "mudou".
- O adendo do coordenador (`ambiente_id` ≠ `NULL`) **não** entra em nenhum dos dois.

### `Adendo` (existente) — acrescentar
- `ambiente_id: Optional[int]` (indexado).

## 2. O `flow.py` — as sete operações (com as assinaturas corrigidas)

| Operação | De → para | Notas |
|---|---|---|
| `importar(fonte, obra, admin)` | — → `em_revisao` | grava o `fonte_id`; gate 1 (`nao_entra`) |
| **`revisar(versao, parecer, ajustes, revisor, hash_esperado)`** | `em_revisao` → `aguardando_admin` | **correção 2**: recusa se o conteúdo atual ≠ `hash_esperado` ("o conteúdo mudou desde que você abriu"); cria o instantâneo **visto**; grava o `hash_visto` |
| **`recusar(versao, parecer, revisor, hash_esperado)`** | `em_revisao` → `devolvida` | a mesma checagem do `hash_esperado` |
| `reenviar(versao, ajustes, admin)` | `devolvida` → `em_revisao` | o Admin ajusta e devolve à revisão |
| `liberar(versao, ajustes_descritos, admin)` | `aguardando_admin` → `liberada` | gate 2 (`depende`); **cria o instantâneo liberado**; `hash_liberado`; `Obra.status`/`versao_liberada_id` |
| **`alterar(obra, conteudo, admin)`** | — → nova versão `em_revisao` | **correção 3**: recebe o **conteúdo novo** (`capitulos` + `adendos` da base) e o aplica à obra; a liberada **fica** |
| `contestar(versao, revisor)` | **a versão contestada volta a `em_revisao`** (sem criar outra); `Obra.status` → `em_revisao`; o `versao_liberada_id` → `NULL` | a salvaguarda (RF11) |

**Invariantes no código**: `revisar`/`recusar`/`contestar` = REVISOR; `importar`/`reenviar`/
`liberar`/`alterar` = ADMIN; `liberar` exige `revisor_id` + `hash_visto`.

**`flow.py` não importa `reflex`** (a correção 3) — um teste de grep que prova.

## 3. O hash

```
item_capitulo = sha256(f"{ordem}|{titulo}|{conteudo_md}")
item_adendo   = sha256(f"{codigo}|{titulo}|{texto}")     # só os da base
conteudo_hash = sha256("v1|" + "|".join(sorted(itens)))  # o agregado, versionado
```

- O `hash_visto`/`hash_liberado` = o agregado dos itens de cada instantâneo.
- O `itens_visto` = derivado do instantâneo `visto` (não há campo separado).
- A diferença (RF11b) = o confronto dos itens dos dois instantâneos (o hash **e** o texto).

## 4. A fonte e o inventário

- `services/fontes.py`: `fonte_decisao(fonte_id) -> str` lê o `inventario.csv` uma vez (o cache no
  módulo; o caminho **configurável**), com teste. O `liberar` consulta **na hora**.
- **Requisito de deploy da v1**: o `inventario.csv` precisa estar **acessível no contêiner**. O
  Compose hoje só monta `conteudo/ESTUDOS_BIBLICOS`; o inventário fica em
  `EVANGELICOS/documentacao/fontes/inventario.csv` (o repositório de conteúdo). A v1 precisa montá-lo
  (ou copiá-lo para dentro da imagem no build) e apontar o `CAMINHO_INVENTARIO`. **Registrado como
  requisito da DEM-005 (o deploy da v1).**

## 5. Os testes

O [`plano-testes.md`](plano-testes.md) (v3) acrescenta: o instantâneo visto + a diferença com o
texto (F-08/C-06), a assinatura contra conteúdo não visto (N-08), o `alterar` com o conteúdo (F-09)
e o teste de que o `flow.py` não importa `reflex` (C-07).

## 6. Riscos

- **A snapshot duplica conteúdo (agora duas vezes: visto e liberado)** — o custo é espaço; o ganho é
  a RF11b mostrar o texto. Aceito.
- **O banco da v1 é próprio**: o schema nasce do zero + o baseline de Alembic; sem `ALTER` na v0.
- **A canonização** determinística (a ordem, o `sorted`, o encoding).
- O `Study` fica para a fatia seguinte.

## 7. O que o EVAL julga

O plano v3 — com a mutação: sem o gate do `nao_entra` → N-01; sem a checagem do `revisor_id` → N-03;
sem o instantâneo no `liberar` → N-07; **sem a checagem do `hash_esperado`** → N-08; **sem o
instantâneo visto** → F-08 falha.
## 8. A v4 — as 4 lacunas do relatório do DEVS (decisões do PLANNER, 19/10)

**L1 — a canonização sem escape (o furo mais grave).** O item era
`sha256(f"{ordem}|{titulo}|{conteudo_md}")`: um `|` no texto **ambíguo** o hash. **Decisão**: a
canonização é **JSON canônico** — `sha256(json.dumps({...}, ensure_ascii=False, sort_keys=True,
separators=(",", ":")))` — os campos são nomeados e o JSON escapa; não há separador a escapar. O
agregado: `sha256("v1\n" + "\n".join(f"{item_key}\t{item_hash}" for os itens ordenados))` (os hashes
são hex — sem `\t`/`\n` dentro). O prefixo `v1|` vira `v1\n` (o algoritmo versionado).
**Sem assinatura persistida ainda** — a troca não invalida nada.

**L2 — a trilha imutável (o RF08).** O modelo só tem o estado do ciclo; sucessivas recusas/reenvios
perdem o histórico. **Decisão**: a `ObraVersaoEvento` (append-only):
`id, versao_id, tipo (importada|vista|recusada|reenviada|liberada|alterada|contestada), autor_id,
quando, detalhe (JSON: o hash, o parecer)`. Cada operação **acrescenta** um evento. A app não
atualiza nem apaga; a imutabilidade contra SQL direto (o trigger/ACL) é do deploy da v1.

**L3 — o cache × a decisão atual.** A liberação consulta o inventário **relendo** o arquivo
(`fonte_decisao(fonte_id, recarregar=True)`); o cache serve à exibição, **não ao gate**. O
`liberar` faz a leitura fresca.

**L4 — a remoção de item.** Nesta fatia o `alterar` **não remove** itens (só adiciona/atualiza); a
remoção fica para a fatia com o mapa de origem e o adendo de ambiente, com a política das FKs
explicitada. Registrado como limite da fatia 1, não como esquecimento.

**L1a — a normalização antes do hash (o acréscimo do ARQUITECT, 19/10).** Antes de hashear, cada
campo passa por: quebras de linha **LF** (`\r\n` e `\r` → `\n`) e texto em **NFC**
(`unicodedata.normalize`). Os capítulos vêm de Markdown editado no **Windows** — sem isso, o mesmo
texto salvo com CRLF e com LF gera **hashes diferentes**, e a assinatura desmente o conteúdo por
causa do formato do arquivo. Os testes: **CRLF e LF dão o mesmo hash; NFC e NFD dão o mesmo hash.**

**L4a — a próxima fatia precisa poder remover (o acréscimo do ARQUITECT).** O Admin precisará
**desfazer uma importação equivocada**: "remover capítulo/adendo da base" é **requisito da fatia
seguinte** (junto com o mapa de origem e o adendo de ambiente), com a política das FKs.

**L5 — a transação é da camada de rotas (a DEM-005).** O domínio só faz `flush()`; a v1 abre e
fecha a transação: **um `commit` por operação do fluxo**, com `rollback` em `FluxoBloqueado`.
Registrado na DEM-005 (RF12).
## 9. A v5 — a clarificação do `contestar` (o EVAL da fatia 1)

O EVAL reprovou o **F-06**: o código cria uma v2 e deixa a versão contestada `liberada` com a `Obra.status`
`liberada`. O design v3 era **ambíguo** ("`liberada` → `em_revisao` (nova versão)") — o "nova versão"
era entre parênteses, sem dizer quem volta. **A decisão é a do RF11**, e o EVAL leu certo:

- o `contestar` **não cria versão**: a **versão contestada** volta a `em_revisao` (é ela que vai à
  revisão de novo, com o parecer do Revisor);
- o `Obra.status` → `em_revisao` e o `versao_liberada_id` → `NULL`: **a publicação é suspensa** (o
  conteúdo contestado não continua disponível);
- o evento `contestada` fica na **versão contestada** (não numa v2);
- o `alterar` (o Admin) é que cria a versão nova — e aí a 9.2 vale (a liberada fica disponível).

E o **N-01**: o `importar` precisa de `recarregar=True` — o cache serve à exibição, não ao gate
(a regra L3 vale para **os dois** gates, não só para a liberação).

O `liberar` de uma v2 também corrige o estado: a `Obra.status` → `liberada`, o `versao_liberada_id`
→ a nova, e a **anterior** → `substituida` (o EVAL notou que o status `substituida` nunca era usado).
## 10. A v6 — a rodada de revisão (a lacuna do DEVS pós-v5)

A mesma versão pode ir à revisão **mais de uma vez**: a recusa → o reenvio → nova revisão; a
contestação → nova revisão. Com só `momento` (`visto`/`liberado`), os instantâneos das rodadas
**se sobrepõem** — e não há como dizer qual "visto" é o da revisão atual.

**Decisão**: a versão tem uma **rodada**.

- `ObraVersao.rodada: int = 0` — a rodada de revisão corrente.
- As snapshots ganham `rodada: int` (além de `momento`): a chave única é `(versao_id, momento,
  rodada)`. Cada `revisar` faz `rodada += 1` e cria o **"visto" da rodada nova**; o `liberar` cria
  o **"liberado" da rodada corrente**.
- A **RF11b** compara o "visto" **da rodada corrente** com o "liberado" da mesma rodada — nunca
  contra uma rodada antiga.
- A recusa/reenvio/contestação **não apagam** os instantâneos antigos (o histórico fica; os eventos
  registram o que aconteceu). O parecer corrente é o da rodada corrente; os anteriores ficam na
  trilha (`ObraVersaoEvento`).

Isso fecha a lacuna **sem** tabela nova: é uma coluna na versão e uma nas duas snapshots.
