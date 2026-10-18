# Spec — DEM-202610-002 / guarda de papel no `/admin`

> Dono: PLANNER. Cada RF cita um outcome (intent §2), um non-goal (§4 Out) ou uma constraint (§5).

## 1. Referência

Intent: [`intent.md`](intent.md) — **signed** 2026-10-18 · ADR-005 (papéis) · ADR-007 (guard-rails/TLC) · ADR-009 (PR)

## 2. A matriz papel × rota (baseline H-04)

Levantada **no código** (`gsi_ebd.py` e `AuthService.redirect_for_role`), não por suposição:

| Rota | Papéis que podem | Hoje |
|---|---|---|
| `/` · `/login` · `/confirmar/[token]` · `/homenagens` | **público** | público ✓ |
| `/admin` | **ADMIN, REVISOR** | qualquer logado ← **furo** |
| `/coordenador` | **ADMIN, COORDENADOR** | qualquer logado ← **furo** |
| `/revisao` | **ADMIN, INSTRUTOR** | qualquer logado ← **furo** |
| `/aluno` · `/aluno/licao` · `/aluno/pareceres` · `/perfil/alterar-senha` | **todo logado** | ✓ |

**Invariante de consistência** (evita loop): a **casa de cada papel** — `redirect_for_role` —
precisa estar **permitida** para aquele papel. `ADMIN→/admin`, `REVISOR→/admin`,
`COORDENADOR→/coordenador`, `INSTRUTOR→/revisao`, `ALUNO→/aluno` — todas coerentes com a
matriz acima.

## 3. Requisitos funcionais

- [ ] **RF01:** a matriz vira **dado único** no código (`ROTAS_PROTEGIDAS`), e uma função pura diz
  se um papel pode uma rota. — *(intent §2, 9.1)*
- [ ] **RF02:** `/admin`, `/coordenador` e `/revisao` **não servem conteúdo** a papel não
  autorizado: o carregamento de dados é bloqueado antes de qualquer consulta. — *(§2, H-06)*
- [ ] **RF03:** quem **não está logado** vai para `/login` (comportamento atual, preservado). — *(§5)*
- [ ] **RF04:** quem está logado **sem papel** é devolvido ao seu painel (`redirect_for_role`),
  **sem loop**. — *(§5, invariante)*
- [ ] **RF05:** a matriz é **testada** (`tests/test_rbac.py`), papel × rota, incluindo a
  invariante da casa. — *(H-04)*
- [ ] **RF06:** as páginas continuam compilando (`tests/test_paginas.py`). — *(ADR-007)*
- [ ] **RF07:** **todo evento público** dos três estados administrativos (`AdminState`,
  `CoordenadorState`, `RevisaoState`) é barrado pela matriz quando o papel não tem permissão, e um
  teste **varre a classe** reprovando evento novo sem guarda. — *(ajustes 1 e 2 do List 2.0)*
- [ ] **RF08:** os **mutadores** de usuário, lead e coordenação são exclusivos do papel da matriz
  (`acao:usuarios` e `acao:leads` = ADMIN; `acao:coordenacao` = ADMIN+COORDENADOR;
  `acao:revisao` = ADMIN+INSTRUTOR) — inclusive contra o `can_manage`, que deixava o **REVISOR**
  gerenciar papéis abaixo dele na hierarquia. — *(achado do AUXILIAR-ARCHITECT)*

## 3a. Matriz de ações (eventos) — ver `design.md` §4

| Ação | Papéis |
|---|---|
| `acao:catalogo` | ADMIN, REVISOR |
| `acao:usuarios` | **ADMIN** |
| `acao:leads` | **ADMIN** |
| `acao:coordenacao` | ADMIN, COORDENADOR |
| `acao:revisao` | ADMIN, INSTRUTOR |

`pode(chave, papel)` fecha para **chave desconhecida** (N-01).

## 4. Requisitos não funcionais

- **Sem dependência nova**; sem mudança de schema; sem refatoração fora do escopo.
- Guarda **central**: as regras vivem em `utils/rbac.py`, nunca copiadas por página.
- A resposta de acesso negado é **redirecionar**, não tela em branco nem 500.
- Nenhum dado administrativo pode chegar ao estado de um usuário sem papel.

## 5. Contratos

```python
# utils/rbac.py
ROTAS_PROTEGIDAS: dict[str, tuple[Role, ...]]
def pode_acessar(rota: str, papel: int) -> bool

# states/auth.py (novos handlers de on_load)
def guarda_admin(self)        # /admin          -> ADMIN, REVISOR
def guarda_coordenador(self)  # /coordenador    -> ADMIN, COORDENADOR
def guarda_revisao(self)      # /revisao        -> ADMIN, INSTRUTOR
```

## 6. Edge cases

- **REVISOR em `/admin`**: permitido (é a casa dele no código) — ver decisão 9.2a.
- **Anônimo em `/admin`**: `/login`, como hoje.
- **Papel sem casa** (valor inesperado): `/login`, sem loop.
- **Redirecionar para a própria rota**: impossível pela invariante testada.
- **Loader chamado sem guarda** (evento direto do cliente): cada loader **também** confere a
  matriz (defesa em profundidade) — RF02.

## 7. Critérios de aceitação

- [ ] **CA01:** aluno logado abre `/admin` e **não vê** dados (não permanece; volta a `/aluno`).
- [ ] **CA02:** coordenador abre `/coordenador` ✓ e `/admin` ✗.
- [ ] **CA03:** revisor abre `/admin` ✓; instrutor abre `/revisao` ✓.
- [ ] **CA04:** `tests/test_rbac.py` cobre a matriz inteira e falha se alguém remover uma permissão.
- [ ] **CA05:** suíte verde (82 + novos) e `test_paginas.py` passando.
- [ ] **CA06:** nenhuma mudança de schema, nenhuma dependência nova.
