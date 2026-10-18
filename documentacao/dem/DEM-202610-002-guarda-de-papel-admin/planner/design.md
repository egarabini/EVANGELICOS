# Design — DEM-202610-002 / guarda de papel no `/admin` (v2 — List 2.0)

> v2 aplica os **dois ajustes** pedidos na resposta ao List 1.0 (ARQUITECT via AUXILIAR-ARCHITECT,
> 2026-10-18): defesa em profundidade em **todo** evento público (não só um loader) e **teste de
> chamada direta** de evento por papel.

## 1. Referência

Spec: [`spec.md`](spec.md) · Intent: [`intent.md`](intent.md) — signed 2026-10-18

## 2. O que o código diz (inspecionado, não suposto)

O levantamento dos eventos públicos dos três estados administrativos mostra que o furo **não para
no `/admin`**:

| Estado | Evento sem verificação nenhuma | Por que importa |
|---|---|---|
| `AdminState` | `load_coordenadores`, `load_leads`, `load_estudos_pendentes`, `load_obras`, `load_estudos_aplicados` | leitura de dados administrativos por evento direto |
| `AdminState` | **`update_lead_status`** | **escrita** em dados de quem pediu contato |
| `AdminState` | `activate_user`, `suspend_user`, `cancel_user` | só `can_manage` — e na hierarquia do `rbac.py` o **REVISOR (nível 1) gerencia coordenador, instrutor e aluno**, o que contraria o próprio `Role` ("função editorial, fora da cadeia de comando") |
| `CoordenadorState` | `load_all`, `load_estudos`, `load_turmas`, `toggle_aluno`, `select_all_alunos`, `assign_study` | **`assign_study` é escrita** (atribui estudo a aluno) |
| `RevisaoState` | `abrir_resposta`, `fechar_resposta`, `usar_sugestao`, `descartar_sugestao` | **`salvar_parecer`-adjacente**: abrir/descartar resposta mexe no fluxo de correção |
| — | `require_role` em `utils/rbac.py` | **zero usos** no projeto |

**Os `@rx.var` não são eventos** (`tem_pendentes`, `fila_label`, `media_progresso_label`,
`study_options`, `has_alunos`, `has_estudos`) — não entram na guarda.

## 3. Componentes

| Arquivo | Mudança |
|---|---|
| `gsi_ebd/utils/rbac.py` | **+** `PERMISSOES` (matriz única: rotas **e** ações) · **+** `pode(chave, papel)` · **+** `exige(chave)` (decorator de **evento**) · **+** `guarda_rota(rota)` (decorator de **on_load**) · mantém `require_role`/`can_manage` (agora marcados como legado) |
| `gsi_ebd/states/auth.py` | **+** `_guarda(rota)` e os 3 handlers de `on_load` |
| `gsi_ebd/gsi_ebd.py` | `on_load` de `/admin`, `/coordenador`, `/revisao` |
| `gsi_ebd/states/admin.py` | `@exige(...)` em **todos** os 13 eventos públicos |
| `gsi_ebd/states/coordenador.py` | `@exige("coordenacao")` nos 8 eventos (vira a guarda central; `load_alunos` mantém o filtro de ambiente) |
| `gsi_ebd/states/revisao.py` | `@exige("revisao")` nos 6 eventos |
| `tests/test_rbac.py` | **novo** — matriz + invariante + **varredura da classe** |
| `tests/test_paginas.py` | intocado, tem que passar |

**Não muda:** corpos de página, modelos, schema, dependências.

## 4. A matriz (dado único)

```python
PERMISSOES = {
    # rotas (usadas pelo on_load)
    "rota:/admin":        (Role.ADMIN, Role.REVISOR),
    "rota:/coordenador":  (Role.ADMIN, Role.COORDENADOR),
    "rota:/revisao":      (Role.ADMIN, Role.INSTRUTOR),
    # ações (usadas pelos eventos)
    "acao:catalogo":      (Role.ADMIN, Role.REVISOR),   # aprovar/rejeitar estudo, obras, fila
    "acao:usuarios":      (Role.ADMIN,),                # criar/ativar/suspender/cancelar
    "acao:leads":         (Role.ADMIN,),                # update_lead_status
    "acao:coordenacao":   (Role.ADMIN, Role.COORDENADOR),
    "acao:revisao":       (Role.ADMIN, Role.INSTRUTOR),
}
```

Atribuição dos eventos de `AdminState`: `load_estudos_pendentes`/`load_obras`/`load_estudos_aplicados`
→ `catalogo`; `load_coordenadores`/`load_leads` → `usuarios`/`leads`; `create_gestor`,
`activate_user`, `suspend_user`, `cancel_user`, `update_lead_status` → `usuarios`/`leads`;
`aprovar_estudo`, `aprovar_todos`, `rejeitar_estudo` → `catalogo`.

## 5. O decorator

```python
def exige(chave: str):
    def decorador(fn):
        @functools.wraps(fn)
        def wrapper(self, *args, **kwargs):
            if not pode(chave, getattr(self, "current_user_role", -1)):
                return            # nao executa; sem erro visivel ao cliente
            return fn(self, *args, **kwargs)
        wrapper.__exige__ = chave     # marcador que o teste procura
        return wrapper
    return decorador
```

- **Marcador** (`__exige__`): é o que permite o teste **varrer a classe** e falhar se alguém criar
  um evento novo sem guarda — o requisito explícito do ajuste 2.
- **`functools.wraps`** preserva nome e assinatura; é o mesmo padrão do `require_role` existente.
- **Risco sinalizado**: o `require_role` do repositório nunca foi usado, então o padrão
  `wrapper(self, *args, **kwargs)` **não está provado** neste projeto. Mitigação: o teste de
  compilação das páginas + a chamada direta cobrem; se o Reflex recusar a assinatura, a saída é
  gerar um wrapper por assinatura (2 ou 3 variantes) — decisão do DEVS, registrada na jornada.

## 6. Defesa em profundidade (ajuste 1)

| Camada | O que barra |
|---|---|
| 1. Rota | `on_load` com `guarda_rota` → não logado vai a `/login`; sem papel vai à casa |
| 2. Loader | `@exige(...)` no loader → **nada é consultado** sem papel |
| 3. Mutador | `@exige(...)` no mutador → **nada é escrito** sem papel |
| 4. Página | renderiza com o estado vazio (nada a esconder) |

A camada 2/3 é a que faltava: o cliente pode disparar o evento **sem** passar pela rota, e até hoje
`assign_study` e `update_lead_status` escreviam para qualquer sessão.

## 7. Migrations / dados

- [x] Nenhuma.

## 8. Ordem

1. `rbac.py`: matriz + `pode` + decorators
2. `tests/test_rbac.py`: matriz, invariante, **varredura** (TDD — o teste falha antes da fiação)
3. `auth.py`: handlers de `on_load`
4. `gsi_ebd.py`: `on_load` das 3 rotas
5. `states/admin.py`: `@exige` nos 13 eventos
6. `states/coordenador.py` e `states/revisao.py`: `@exige` nos eventos
7. suíte completa + `test_paginas.py`

## 9. Riscos

| Risco | Mitigação |
|---|---|
| Loop de redirecionamento | invariante testada (`redirect_for_role(papel)` permitido) |
| Evento novo sem guarda | varredura da classe (`__exige__` em todo método público) |
| Decorator com `*args` não provado no Reflex | teste de compilação + chamada direta; plano B: wrapper por assinatura |
| Guarda em `load_alunos` que já filtra por ambiente | manter o filtro; o `@exige` só soma |
| REVISOR perde acesso a algo que usava | matriz `catalogo` mantém o revisor no catálogo; só usuários/leads viram ADMIN |
| **Fora do escopo (achado)** | `can_manage` não confere **ambiente (tenant)**: um coordenador pode agir sobre usuário de outro ambiente por evento direto → **DEM própria** |
