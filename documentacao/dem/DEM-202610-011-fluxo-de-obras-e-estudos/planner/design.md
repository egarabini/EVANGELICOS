# Design — DEM-202610-011 / **fatia 1: o domínio** (v7 — a autoridade e a disponibilidade)

> Nível 3. **v7 (19/10):** as regras de autoridade do ARQUITECT mudam a semântica. O **Admin**
> define o registro e **toda alteração é dele**; a liberação depende **dos dois** (a assinatura do
> Revisor **e** a liberação do Admin); o Revisor é **auxiliar de qualidade** (parecer, assinatura,
> **solicitação de revisão**) e **não muda estado nem disponibilidade**.
> **A v5 está substituída**: a versão liberada é **imutável**, e todo ciclo de revisão cria a N+1.
> **ADR-020** (as regras) · **ADR-019 emendada** (o `contestar` → `solicitar_revisao`) ·
> a **9.2 da DEM-005 superada em parte** (a suspensão para novos).

## 1. Os modelos

### `Obra` — o registro (do Admin) + a disponibilidade
- `status: str` — o estado da **versão corrente** (`em_revisao|aguardando_admin|devolvida|liberada`);
- **`disponibilidade: str`** — **o conceito próprio**: `aberta` | `suspensa_para_novos`;
- `versao_liberada_id: Optional[int]` — a última versão liberada (a N);
- `fonte_id: Optional[str]` (indexado) — o `F-xxx` do inventário;
- `updated_at`.

### `ObraVersao` — a versão (imutável quando liberada)
```python
class ObraVersao(SQLModel, table=True):
    id, obra_id, numero
    status: str                    # em_revisao|aguardando_admin|devolvida|liberada|substituida
    rodada: int = 0                # a rodada DENTRO desta versão (recusa/reenvio/nova revisão)
    conteudo_hash: str
    parecer, ajustes_propostos (JSON), revisor_id, revisado_em, hash_visto
    ajustes_descritos, admin_id, liberada_em, hash_liberado
```

### As snapshots (com o momento **e** a rodada)
```python
class ObraVersaoCapitulo: versao_id, momento ("visto"|"liberado"), rodada, ordem, titulo, conteudo_md, item_hash
class ObraVersaoAdendo:   versao_id, momento, rodada, codigo, titulo, texto, item_hash
```
A chave única é `(versao_id, momento, rodada)`. A **N liberada é imutável**: a snapshot `liberado` da
N não muda. A N+1 é um **novo registro** (as suas próprias snapshots).
**A snapshot guarda o texto normalizado** (LF + NFC) — o hash recomputa a partir dela.

### `VinculoObra` — a vinculação **fixada na versão** (nova)
```python
class VinculoObra(SQLModel, table=True):
    id, ambiente_id (FK), obra_id (FK), versao_id (FK), coordenador_id, ativo: bool, created_at
```
A vinculação fixa a **versão** — a suspensão para novos **não** atinge os vínculos existentes.

### `Adendo` — acrescentar `ambiente_id` (o do coordenador; `NULL` = da base).

### A posição do Revisor (o item opcional 8 — **custo baixo, adotado**)
`ObraVersaoEvento` com o tipo `posicao` e o `detalhe {"posicao": "concordo"|"objeto", "texto": "..."}`.
O Revisor registra a posição sobre uma decisão do Admin; **não bloqueia**, mas fica na trilha e
visível ao Admin. Custo: um tipo de evento e uma operação (`posicionar`).

## 2. O `flow.py` — as operações (a autoridade é a regra)

| Operação | Autor | Efeito |
|---|---|---|
| `importar(fonte, obra, admin)` | **Admin** | cria a Obra + a v1 em `em_revisao`; gate `nao_entra` (com `recarregar=True`) |
| `revisar(versao, parecer, ajustes, revisor, hash_esperado)` | Revisor | `aguardando_admin`; a assinatura + o instantâneo **visto** da rodada; recusa se o conteúdo ≠ o aberto |
| `recusar(versao, parecer, revisor, hash_esperado)` | Revisor | `devolvida` |
| `reenviar(versao, ajustes, admin)` | **Admin** | `devolvida` → `em_revisao` (a mesma versão; a rodada avança na próxima revisão) |
| `liberar(versao, ajustes_descritos, admin)` | **Admin** | **o único caminho para `liberada`** — exige a assinatura do Revisor para a versão vista; gate `depende` (com `recarregar=True`); cria o instantâneo **liberado**; se for a N+1, a N → `substituida`; a disponibilidade → `aberta` |
| `alterar(obra, conteudo, admin)` | **Admin** | cria a **N+1** em `em_revisao`; a disponibilidade → `suspensa_para_novos` |
| `solicitar_revisao(versao, revisor, motivo)` | Revisor | **um pedido registrado**; não muda estado nem disponibilidade |
| `aceitar_solicitacao(obra, admin)` | **Admin** | cria a N+1 em `em_revisao`; suspende para novos |
| `dispensar_solicitacao(obra, admin, motivo)` | **Admin** | a dispensa (o motivo **obrigatório**), visível ao Revisor; a disponibilidade **não** muda |
| `cancelar_ciclo(obra, admin)` | **Admin** | descarta a N+1 em revisão; a disponibilidade → `aberta` |
| `posicionar(versao, revisor, posicao, texto)` | Revisor | o evento `posicao` (não bloqueia) |

**Invariantes**: só o **Admin** abre, suspende, cancela e libera; o Revisor **nunca** muda estado nem
disponibilidade; `liberar` exige `revisor_id` + `hash_visto`; a versão `liberada` **não** volta a
`em_revisao` (a v5 está substituída).

## 3. A disponibilidade (a regra 4)

- `aberta`: a versão liberada é a vigente; **novas** vinculações/atribuições usam a versão corrente.
- `suspensa_para_novos`: o Admin abriu um ciclo (o `alterar` ou o `aceitar`) — **bloqueia novas**
  vinculações/atribuições; **quem já está fixado continua** na versão em que está e recebe o aviso
  (a fatia 2).
- Volta a `aberta` ao `liberar` a N+1 **ou** ao `cancelar_ciclo`.

## 4. O hash (a v4 continua)

A normalização (LF + NFC) + o JSON canônico + o agregado `v1\n`; o item hash e o agregado; a
diferença da RF11b = o **visto** × o **liberado da mesma rodada** (dentro de uma versão; entre
versões, a comparação é a N × N+1 — a fatia 2).

## 5. As fontes

`services/fontes.py`: `fonte_decisao(fonte_id, recarregar=True)` — **os dois gates** relêem
(importação e liberação); o cache serve à exibição. O `inventario.csv` acessível no contêiner (o RF11
da DEM-005).

## 6. A rodada (a v6) — só dentro da versão

A rodada serve à **recusa, ao reenvio e a uma nova revisão da mesma versão**. A contestação **não**
é rodada: ela é a `solicitar_revisao` do Revisor (um pedido) + a decisão do Admin (a N+1 ou a
dispensa).

## 7. Riscos

- **A mudança da semântica** chegou depois do EVAL — o F-06 e os testes que o cercam são **reescritos**
  (o plano v4), não "corrigidos".
- **O banco da v1 é próprio** (`didasko_v1`) com o baseline de Alembic; sem `ALTER` na v0.
- **A imutabilidade da N**: na aplicação; o trigger/ACL contra SQL direto é do deploy da v1.
- O `Study` fica para a fatia seguinte.

## 8. O que o EVAL julga

O plano **v4**: o F-06 reescrito (a versão nova; a liberada intacta; só o Admin abre ciclo; a
solicitação não muda a disponibilidade) + os casos novos da disponibilidade, do cancelamento e do
`versao_id` fixado + a regressão.
