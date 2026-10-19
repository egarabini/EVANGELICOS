# Design — DEM-202610-011 / **fatia 1: o domínio**

> Nível 3 (ADR-018). **Esta fatia não tem tela** — é o domínio, o fluxo e os hashes. As telas são a
> fatia 2, na v1 (DEM-005). O descrito aqui é o que o Codex implementa.

## 1. Os modelos (o que existe + o que nasce)

**`Obra`** (existente — `gsi_ebd/models/obra.py`): acrescentar
- `status: str` — o estado **publicado** (`em_revisao|aguardando_admin|devolvida|liberada`), para o
  catálogo;
- `versao_liberada_id: Optional[int]` — a versão que os coordenadores veem hoje;
- `updated_at: Optional[datetime]`.

**`ObraVersao`** (nova) — o coração do fluxo:

```python
class ObraVersao(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    obra_id: int = Field(foreign_key="obra.id", index=True)
    numero: int = Field(default=1)              # 1, 2, 3...
    status: str = Field(default="em_revisao")   # em_revisao|aguardando_admin|devolvida|liberada|substituida
    conteudo_hash: str = Field(default="")      # o hash do conteúdo DESTA versão (a canonização, §3)
    # o parecer do Revisor
    parecer: str = Field(default="")
    ajustes_propostos: str = Field(default="[]")  # JSON: lista de ajustes
    revisor_id: Optional[int] = Field(default=None, foreign_key="user.id")
    revisado_em: Optional[datetime] = Field(default=None)
    hash_visto: str = Field(default="")           # o que o Revisor viu (a assinatura dele)
    # a liberação do Admin
    ajustes_descritos: str = Field(default="")    # o que o Admin fez
    admin_id: Optional[int] = Field(default=None, foreign_key="user.id")
    liberada_em: Optional[datetime] = Field(default=None)
    hash_liberado: str = Field(default="")        # o que o Admin liberou
    created_at: Optional[datetime] = Field(default=None)
```

**A assinatura = o par `(revisor_id, revisado_em, hash_visto)`** — a ADR-011, com a emenda da
ADR-019: a assinatura vale para a **versão vista**, e a **diferença** é o par
`(hash_visto, hash_liberado)`.

**`Adendo`** (existente): acrescentar
- `ambiente_id: Optional[int] = Field(default=None, foreign_key="ambiente.id", index=True)` —
  `None` = adendo **da base** (admin/revisor); com valor = adendo **do ambiente** (coordenador).

**`Study`** (existente): o enum novo + `versao_id`/`hash` — a **fatia do estudo** fica para depois
da obra (o fluxo é o mesmo; o `Study` já tem `StudyVersion`); nesta fatia, só a obra.

## 2. O `flow.py` (as transições — tudo server-side)

```python
# gsi_ebd/services/flow.py (novo)
def importar(sessao, fonte: FonteInventario, obra: Obra, admin: User) -> ObraVersao
    # gate 1: fonte.decisao == "nao_entra" -> raise FluxoBloqueado("a fonte não entra")
    # cria a Obra (se nova) + a ObraVersao v1 em_revisao
def revisar(sessao, versao, parecer: str, ajustes: list[str], revisor: User) -> ObraVersao
    # só em em_revisao; grava o parecer + os ajustes + o hash_visto; -> aguardando_admin
def recusar(sessao, versao, parecer: str, revisor: User) -> ObraVersao
    # só em em_revisao; -> devolvida
def liberar(sessao, versao, ajustes_descritos: str, admin: User) -> ObraVersao
    # só em aguardando_admin; gate 2: fonte.decisao == "depende" -> raise FluxoBloqueado
    # grava o hash_liberado; -> liberada; Obra.status/versao_liberada_id
def alterar(sessao, obra, admin: User) -> ObraVersao
    # cria a versão N+1 em em_revisao; a liberada fica (a versão em uso não muda)
def contestar(sessao, versao, revisor: User) -> ObraVersao
    # a salvaguarda (RF11): reabre a revisão de uma liberada -> a nova versão volta a em_revisao
```

**Invariante no código** (não na tela): `liberar` exige `revisor_id` + `hash_visto` preenchidos;
`revisar`/`recusar` exigem o papel `REVISOR`; `liberar`/`alterar`/`importar` exigem `ADMIN`.

## 3. O hash (a canonização)

```
conteudo = "v1|" + para cada capítulo em ordem: f"{ordem}|{titulo}|{sha256(conteudo_md)}" +
           "|" + para cada adendo da BASE em ordem de codigo: f"{codigo}|{sha256(texto)}"
hash = sha256(conteudo.encode())  # hex
```

- O prefixo `v1|` **versiona o algoritmo** — uma mudança futura não invalida as assinaturas antigas.
- O `hash_visto` é calculado **no momento do parecer**; o `hash_liberado` **no momento da
  liberação**; a diferença é auditável (a ADR-019).
- O "tamanho do que mudou" (a RF11) = a contagem de capítulos/adendos cujo hash individual mudou.

## 4. A fonte e o inventário

O `decisao` de cada fonte vem do `documentacao/fontes/inventario.csv` (a DEM-003, o verificador).
O `flow.py` **não** lê o CSV em runtime: uma tabela/const gerada do inventário (o design decide a
carga: um módulo `fontes.py` gerado, ou uma leitura cacheada no boot). **Nesta fatia**: uma função
`fonte_decisao(fonte_id) -> str` que lê o CSV uma vez (o caminho configurável), com teste.

## 5. As telas (fatia 2 — na v1)

Admin (importar/ajustar/liberar), Revisor (parecer/recusar), Coordenador (vincular/adendar) — na
v1, com a matriz papel × rota. **Nada disso nesta fatia.**

## 6. Riscos

- **A migração** (o `Obra.status`/`Adendo.ambiente_id` novos): o SQLModel/SQLite nos testes e o PG
  em produção; o `ALTER`/`create_all` — o design da migração fica com o deploy da v1 (sem
  `alembic` ainda: o projeto não usa).
- **A canonização** precisa ser **determinística** (a ordem, o separador, o encoding) — um
  capítulo reordenado muda o hash (é o desejado).
- **O `Study` no mesmo fluxo** fica para a fatia seguinte (o estudo tem as `StudyVersion`).

## 7. O que o EVAL julga (o plano)

Ver o [`plano-testes.md`](plano-testes.md) — os estados, os gates, os hashes, as permissões, os
invariantes e a **prova de mutação** (remover o gate do `nao_entra`/a checagem do `revisor_id` e
ver o teste falhar).
