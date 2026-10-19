# Design — DEM-202610-011 / **fatia 1: o domínio** (v2 — fecha as 4 lacunas)

> Nível 3 (ADR-018). **Esta fatia não tem tela.** A v2 responde às quatro lacunas que o DEVS apontou
> antes de codar — todas eram decisões de arquitetura que faltavam no design.

## 1. Os modelos

### `Obra` (existente) — acrescentar
- `status: str` — o estado **publicado** (`em_revisao|aguardando_admin|devolvida|liberada`);
- `versao_liberada_id: Optional[int]` — a versão que os coordenadores veem;
- **`fonte_id: Optional[str]` (indexado)** — a linha do inventário (o `F-xxx`); **persistente**, é o
  que a liberação consulta (lacuna 3);
- `updated_at`.

### `ObraVersao` (nova) — o estado do ciclo
```python
class ObraVersao(SQLModel, table=True):
    id, obra_id, numero
    status: str                                   # em_revisao|aguardando_admin|devolvida|liberada|substituida
    conteudo_hash: str                            # o agregado da versão
    parecer, ajustes_propostos (JSON), revisor_id, revisado_em, hash_visto
    ajustes_descritos, admin_id, liberada_em, hash_liberado
    itens_visto: str = "{}"                       # JSON: {item_key: item_hash} no parecer (lacuna 2)
```

### As **snapshots** do conteúdo (novas) — a lacuna 1
O conteúdo liberado **não pode** viver no `ObraCapitulo`/`Adendo` da obra (que o Admin altera). A
versão **congela uma cópia** no momento em que é **liberada**:

```python
class ObraVersaoCapitulo(SQLModel, table=True):   # a cópia congelada dos capítulos
    id, versao_id (FK), ordem, titulo, conteudo_md, item_hash
class ObraVersaoAdendo(SQLModel, table=True):     # a cópia congelada dos adendos da BASE
    id, versao_id (FK), codigo, titulo, texto, item_hash
```

- A **versão liberada** é a fonte da verdade do que está publicado; o `ObraCapitulo`/`Adendo` viram a
  **cópia de trabalho** (o que o Admin edita).
- O **adendo do coordenador** (`Adendo.ambiente_id` ≠ `NULL`) **não** entra na snapshot: é
  sobreposição por ambiente, não conteúdo da obra.
- A snapshot é **imutável** depois da liberação — uma correção é uma **nova versão** (o RF05).

### `Adendo` (existente) — acrescentar
- `ambiente_id: Optional[int]` (indexado) — `None` = da base; com valor = do coordenador.

## 2. O `flow.py` — as **sete** operações (a lacuna 4 é a `reenviar`)

| Operação | De → para | Notas |
|---|---|---|
| `importar(fonte, obra, admin)` | — → `em_revisao` | grava o `Obra.fonte_id`; **gate 1** (`nao_entra`) |
| `revisar(versao, parecer, ajustes, revisor)` | `em_revisao` → `aguardando_admin` | grava `hash_visto` + **`itens_visto`** |
| `recusar(versao, parecer, revisor)` | `em_revisao` → `devolvida` | — |
| **`reenviar(versao, ajustes, admin)`** | **`devolvida` → `em_revisao`** | **lacuna 4**: o Admin ajusta e devolve à revisão; registra o que ajustou |
| `liberar(versao, ajustes_descritos, admin)` | `aguardando_admin` → `liberada` | **gate 2** (`depende`); grava `hash_liberado`; **cria a snapshot**; `Obra.status`/`versao_liberada_id` |
| `alterar(obra, admin)` | — → nova versão `em_revisao` | a liberada **fica**; o `versao_liberada_id` não muda |
| `contestar(versao, revisor)` | `liberada` → `em_revisao` (nova versão) | a salvaguarda (RF11) |

**Invariantes no código**: `revisar`/`recusar`/`contestar` exigem REVISOR; `importar`/`reenviar`/
`liberar`/`alterar` exigem ADMIN; `liberar` exige `revisor_id` + `hash_visto` preenchidos.

## 3. O hash — o agregado **e** o item (a lacuna 2)

```
item_capitulo = sha256(f"{ordem}|{titulo}|{conteudo_md}")
item_adendo   = sha256(f"{codigo}|{titulo}|{texto}")     # só os da BASE
conteudo_hash = sha256("v1|" + "|".join(sorted(itens)))  # o agregado, versionado
```

- No **parecer**, grava-se o `itens_visto` (o mapa `item_key → item_hash`).
- Na **liberação**, a snapshot grava o `item_hash` de cada item.
- **O C-03 (o tamanho do que mudou)** = comparar o `itens_visto` com os `item_hash` da snapshot
  liberada: os itens com hash diferente (ou só num lado) são o "tamanho".
- O `hash_visto` = o agregado dos `itens_visto`; o `hash_liberado` = o agregado da snapshot.

## 4. A fonte e o inventário (a lacuna 3)

- `Obra.fonte_id` **persistente** — o vínculo que faltava; o `importar` o grava.
- `services/fontes.py`: `fonte_decisao(fonte_id) -> str` lê o `inventario.csv` **uma vez** (cache no
  módulo, o caminho configurável), com teste. O `liberar` consulta **na hora** (a fonte pode ter
  mudado de `entra` para `depende` desde a importação).

## 5. Os testes

O [`plano-testes.md`](plano-testes.md) (v2) cobre as lacunas: o reenvio (F-07), a **snapshot
imutável** (N-07), o **C-03 por item** (C-04), o **`fonte_id` persistente** (C-05).

## 6. Riscos

- **O banco da v1 é próprio** (`didasko_v1`): o schema nasce do zero + o baseline de Alembic; **não
  há `ALTER` no banco da v0**. (O Alembic **existe** no repositório, mas **fora do deploy** e
  possivelmente defasado — o baseline da v1 corrige para a frente; o schema da v1 será registrado
  pelo DEVS, sem executar migração.)
- **A snapshot duplica conteúdo** (o custo é o espaço) — é o preço de a versão liberada ser a
  verdade. Aceito.
- **A canonização** é determinística: a ordem dos capítulos, o `sorted` do agregado, o encoding.
- O `Study` no mesmo fluxo fica para a fatia seguinte; nesta, só a obra.

## 7. O que o EVAL julga

O plano v2 — com a **prova de mutação**: remover o gate do `nao_entra` → N-01 falha; remover a
checagem do `revisor_id` → N-03 falha; **não criar a snapshot no `liberar`** → N-07 falha.
