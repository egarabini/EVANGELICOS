# Design — DEM-202610-002 / guarda de papel no `/admin`

## 1. Referência

Spec: [`spec.md`](spec.md) · Intent: [`intent.md`](intent.md) — signed 2026-10-18

## 2. Componentes

| Arquivo | Mudança |
|---|---|
| `gsi_ebd/utils/rbac.py` | **+** `ROTAS_PROTEGIDAS` (a matriz como dado) · **+** `pode_acessar(rota, papel)` · manter `require_role`/`can_manage` como estão |
| `gsi_ebd/states/auth.py` | **+** três handlers de `on_load` (`guarda_admin`, `guarda_coordenador`, `guarda_revisao`) e um privado `_guarda(rota)` |
| `gsi_ebd/gsi_ebd.py` | trocar o `on_load` de `/admin`, `/coordenador` e `/revisao` |
| `gsi_ebd/states/admin.py` | `load_coordenadores`: sair cedo se o papel não pode `/admin` |
| `gsi_ebd/states/coordenador.py` | `load_all`: idem para `/coordenador` |
| `gsi_ebd/states/revisao.py` | `load_fila`: idem para `/revisao` |
| `tests/test_rbac.py` | **novo** — a matriz, a invariante e os guards |

**Não muda:** nenhum corpo de página, nenhum modelo, nenhum schema, nenhuma dependência.

## 3. Fluxo

```
navegador → /admin
  → on_load AuthState.guarda_admin
       não logado        → /login
       logado sem papel  → redirect_for_role (a casa dele)
       ADMIN/REVISOR     → segue
  → on_load AdminState.load_coordenadores
       sem papel → return imediato (nada é consultado)
       com papel → carrega
```

## 4. Decisões técnicas

- **Handlers dedicados, sem argumento.** `on_load=AuthState.guarda_admin` é o padrão mais seguro do
  Reflex; passar argumento para `on_load` funcionaria, mas é superfície nova sem ganho. Três
  métodos de três linhas cada.
- **Redirecionar, não renderizar 403.** A guarda roda no `on_load`; o que fecha o furo de verdade é
  o **loader sair cedo** — sem ele, o painel renderiza com os dados carregados. A rota devolve o
  aluno ao próprio painel, que é melhor UX que uma tela de erro e mais simples que um componente de
  acesso negado no corpo (que exigiria mexer na página — o risco que derrubou produção em 16/10).
- **A matriz é dado, não `if`s espalhados.** `ROTAS_PROTEGIDAS` é a fonte; guardas e loaders leem a
  mesma função pura. O teste da matriz substitui a inspeção manual.
- **`is_admin` não serve para `/admin`.** O REVISOR também entra (decisão 9.2a); usar `is_admin`
  bloquearia o revisor e criaria o loop. A guarda usa `pode_acessar`.
- **Defesa em profundidade.** Guarda no `on_load` **e** no início de cada loader: um evento
  disparado do cliente não pode carregar dado administrativo.

## 5. Migrations / dados

- [x] Nenhuma.

## 6. Impacto

- **Páginas**: nenhuma alteração de corpo; só `on_load` em `gsi_ebd.py`.
- **Estados**: 3 linhas de guarda em 3 loaders.
- **Teste de compilação** (`test_paginas.py`) continua obrigatório.

## 7. Ordem

1. `rbac.py`: matriz + `pode_acessar` (puro, testável)
2. `tests/test_rbac.py`: matriz + invariante (o teste existe **antes** da fiação — TDD)
3. `auth.py`: os três handlers
4. `gsi_ebd.py`: `on_load` das três rotas
5. os três loaders: saída cedo
6. suíte completa + `test_paginas.py`

## 8. Riscos

| Risco | Mitigação |
|---|---|
| **Loop de redirecionamento** (casa do papel fora da matriz) | invariante testada: `redirect_for_role(papel)` ∈ `ROTAS_PROTEGIDAS` |
| Guarda no `on_load` e loader rodando antes | loader também guarda (defesa em profundidade) |
| Reflex: `on_load` com handler que devolve `None` | é o mesmo padrão de `check_auth`, que já funciona |
| REVISOR tratado como admin no restante do admin | **fora do escopo**: o revisor vê o que já via; a DEM não muda a UI dele |
| Quebrar `test_paginas.py` | nenhum corpo de página é tocado — risco baixo, teste roda igual |
