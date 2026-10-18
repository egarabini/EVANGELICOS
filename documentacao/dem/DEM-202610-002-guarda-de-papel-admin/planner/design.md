# Design — DEM-202610-002 / guarda de papel no `/admin` (v3 — List 2.1)

> v3 incorpora os três itens do List 2.1 (18/10): **auto setters** (bloqueante), **leitura ×
> aprovação do catálogo** e **decorador síncrono**.

## 1. Referência

Spec: [`spec.md`](spec.md) · Intent: [`intent.md`](intent.md) — signed 2026-10-18

## 2. O que o código diz (medido, com o `cwd` do app)

> **Lição medida nesta rodada:** o Reflex descobre o `rxconfig.py` a partir do **diretório atual**.
> Rodando o teste do diretório errado, `state_auto_setters` não é lido e os setters não existem —
> e `test_paginas` falha 9/9. **Os testes rodam do diretório do app** (`ESTUDOS_BIBLICOS/GSI_EBD`),
> como o CI faz. Medido: do diretório do app, **82 passed**.

| Achado | Medido |
|---|---|
| `rxconfig.py` tem `state_auto_setters=True` (depreciado na 0.9.0, removido na 1.0) | sim |
| Do diretório do app, `AuthState` expõe **25 eventos / 17 setters** | sim |
| Setters de identidade existentes | `set_current_user_{role,id,name,status,ambiente}`, `set_is_authenticated`, `set_must_change_password` |
| Rotas `/admin`, `/coordenador`, `/revisao` só chamam `check_auth` | sim |
| `AdminState.update_lead_status` sem verificação | sim |
| `activate/suspend/cancel_user` só com `can_manage` (REVISOR nível 1 gerencia COORDENADOR nível 2) | sim |
| `CoordenadorState.assign_study` (**escrita**) e `load_*` sem verificação | sim |
| `RevisaoState.abrir/fechar_resposta`, `usar/descartar_sugestao` sem verificação | sim |
| `require_role` em `utils/rbac.py` | **zero usos** |

## 3. Item 1 — BLOQUEANTE: o cliente escreve o próprio papel

A guarda inteira lê `self.current_user_role`. Com o auto setter, o cliente dispara
`set_current_user_role(1)` por evento direto e **vira ADMIN para o servidor**. Matriz e `@exige`
passariam a proteger um estado que o atacante controla.

**Correção: opção (a) — desligar `state_auto_setters` e escrever os setters explícitos.**

Por quê (a), e não (b) "sobrescrever os 5 de identidade":
- (b) deixa a **classe** aberta: qualquer var nova sensível ganha setter automático de novo, e o
  teste do AUXILIAR ("nenhum `set_current_user_*` pode existir") **não** é satisfeito — eles
  continuariam existindo;
- (a) é o que o próprio Reflex manda fazer na 1.0 (a flag **some**); fazer agora é planejado, não
  retrabalho;
- **a rede de segurança já existe**: setter ausente → `AttributeError` na **chamada da página** →
  `tests/test_paginas.py` reprova. Foi exatamente o que aconteceu no diagnóstico desta rodada
  (9 falhas) — o teste pega cada setter faltando.

**Setters explícitos a escrever** (enumerados do código, não de memória):

| Estado | Setters usados pelas páginas/components |
|---|---|
| `AuthState` | `login_email`, `login_password` |
| `AdminState` | `tab_atual`, `new_gestor_nome`, `new_gestor_email`, `reject_motivo` |
| `AlunoState` | `user_answer`, `selected_study_option` |
| `RevisaoState` | `parecer_texto`, `considerou_correto` |
| `PerfilState` | `senha_atual`, `nova_senha`, `confirma_senha` |
| `LandingState` (em `landing_content/`) | `form_nome` e demais `form_*` (mapear na implementação) |
| `CoordenadorState` | mapear na implementação |

A implementação **enumera** (`grep '\.set_[a-z_]+'` em todo `gsi_ebd/`), escreve, e roda a suíte do
diretório do app. **Selos:** nenhum `set_*` gerado; nenhuma página quebrada.

## 4. Item 2 — leitura × aprovação do catálogo

A DEM-002 **não cria poder novo**. O revisor lê o catálogo (é a casa dele) e **não aprova**: hoje
`aprovar_estudo`/`aprovar_todos`/`rejeitar_estudo` exigem `is_admin`, e o modelo tem **um** só
`aprovado_por` ("FK → User (Admin)").

```python
PERMISSOES = {
    "rota:/admin":         (Role.ADMIN, Role.REVISOR),
    "rota:/coordenador":   (Role.ADMIN, Role.COORDENADOR),
    "rota:/revisao":       (Role.ADMIN, Role.INSTRUTOR),
    "acao:catalogo_ler":   (Role.ADMIN, Role.REVISOR),   # load_estudos_pendentes, load_obras…
    "acao:catalogo_aprovar": (Role.ADMIN,),              # aprovar_estudo, aprovar_todos, rejeitar_estudo
    "acao:usuarios":       (Role.ADMIN,),
    "acao:leads":          (Role.ADMIN,),
    "acao:coordenacao":    (Role.ADMIN, Role.COORDENADOR),
    "acao:revisao":        (Role.ADMIN, Role.INSTRUTOR),
}
```

Assim a futura DEM de **aprovação em dupla** só acrescenta a assinatura do revisor, sem refazer a
guarda.

## 5. Item 3 — decorador síncrono, preservando o tipo

- **Não** reaproveitar o `require_role` (é `async` e faz `await` — converteria handler síncrono em
  assíncrono sem necessidade).
- Nenhum handler dos três estados usa `yield` nem `async` (verificado) → wrapper **síncrono**.
- O eixo do plano B é **preservar o tipo da função** (síncrona/gerador/assíncrona) e a
  **assinatura** (`functools.wraps` → `__wrapped__`). Se o Reflex recusar a assinatura, a variante
  é pelo **tipo**, não pelo número de argumentos.
- O decorador grava `__exige__` no wrapper (marcador para a varredura da classe).

## 6. Componentes

| Arquivo | Mudança |
|---|---|
| `rxconfig.py` | **`state_auto_setters=False`** |
| `gsi_ebd/states/*.py` | **+** setters explícitos dos campos de formulário (tabela do §3) |
| `gsi_ebd/utils/rbac.py` | matriz rotas+ações · `pode()` · `exige()` (marcador) · `guarda_rota()` |
| `gsi_ebd/states/auth.py` | **+** handlers de `on_load` (`_guarda`) |
| `gsi_ebd/gsi_ebd.py` | `on_load` de `/admin`, `/coordenador`, `/revisao` |
| `gsi_ebd/states/{admin,coordenador,revisao}.py` | `@exige` em **todos** os eventos públicos |
| `tests/test_rbac.py` | **novo** — matriz, invariante, varredura, **e "nenhum `set_current_*`/`set_is_authenticated`/`set_must_change_password` existe"** |
| `tests/test_paginas.py` | intocado; roda do diretório do app |

## 7. Defesa em profundidade (4 camadas)

| Camada | Barra |
|---|---|
| 0. Estado | **sem auto setter** — o cliente não escreve papel/identidade |
| 1. Rota | `on_load` com `guarda_rota` |
| 2. Loader | `@exige("acao:...")` — nada é consultado |
| 3. Mutador | `@exige("acao:...")` — nada é escrito |

## 8. Ordem

1. `rxconfig.py` (desligar) + setters explícitos + suíte do diretório do app **verde** (senão nada
   mais importa)
2. `tests/test_rbac.py` (TDD: matriz, varredura, ausência dos setters de identidade)
3. `rbac.py` + `auth.py` + `gsi_ebd.py` + `@exige` nos três estados
4. suíte completa + `test_paginas.py`

## 9. Riscos

| Risco | Mitigação |
|---|---|
| Setter esquecido quebra página | `test_paginas` reprova e diz qual (`AttributeError`) |
| `state_auto_setters` desligado quebra algo não mapeado | a suíte inteira + compile test das 9 páginas |
| Loop de redirecionamento | invariante testada |
| Evento novo sem guarda | varredura (`__exige__`) |
| Assinatura do wrapper não aceita pelo Reflex | teste de compilação + chamada direta; plano B por **tipo** |
| **Fora do escopo** | `can_manage` não confere ambiente → **DEM-202610-010**; aprovação em dupla → **DEM-202610-011** |
