# A jornada do EVAL — a DEM-017, fatia 1 (o painel do Admin e do Revisor)

## A 1ª rodada — o **PASS** com 1 ressalva (o `9efe747`)

**O veredito: PASS** nos 7 critérios do despacho:

| # | O critério | O resultado |
|---|---|---|
| 1 | **O painel do ADMIN** | o `GET /admin` → 200 com as obras (as disponíveis/as em estudo), os estudos, os **coordenadores com os estudos escolhidos**, os **instrutores com os alunos**, a **lista com os feitos/a fazer/os resultados** (o probe exercitou o `completed=True`) |
| 2 | **O painel do REVISOR** | o `GET /revisor` → 200 com a **fila** e o **histórico** (`vista`/`recusada`/`liberada`) |
| 3 | **Só leitura** | o `POST /admin` → **405** (mesmo sem o CSRF — o router só tem o `@router.get`); o `POST /revisor` → 405 |
| 4 | **O menu derivado** | o HTML do ADMIN: o `/admin`, o `/admin/obras`, o `/admin#estudos`, o `/admin#alunos` + o Sair; o REVISOR: o `/revisor`, o `/revisor/obras` + o Sair; o anônimo: o `/login` **sem o nav**; o `itens_do_menu(papel)` × a matriz: o ADMIN [Painel, Obras, Estudos, Alunos], o REVISOR [Painel, Revisão], os demais [] |
| 5 | **A matriz** | o `PERMISSOES["rota:/admin"] == (ADMIN,)`; o `["rota:/revisor"] == (REVISOR,)`; **as 10 células** (2 rotas × 5 papéis) com o permitido 200 **e** o negado 403; a vacuidade (o monkeypatch) → as 4 → 403 |
| 6 | **A invariante da casa** | o `test_rf02` com o `GET /admin` e o `GET /revisor`; o `PERMISSOES["rota:/revisor"]==(REVISOR,)`; o `render_por_papel` para o `/revisor` nos 5 papéis |
| 7 | **Os testes/o CI** | a **v1 166**; a **v0 274**; o CI `40097452147` `success` |

## As ressalvas (fora dos 7)

### 1. **O v0/REVISOR — a decisão do ARQUITECT** (a única que ele levaria ao ARQUITECT antes do merge)

- **o `rbac` é compartilhado** entre a v0 e a v1: o `HOME_DO_PAPEL[REVISOR]="/revisor"` e o
  `rota:/admin` só o ADMIN;
- **a v0 (Reflex) NÃO tem a rota `/revisor`** — as rotas da v0 são: o `/`, o `/login`, o
  `/confirmar/[token]`, o `/admin`, o `/aluno`, o `/aluno/licao`, o `/coordenador`, o
  `/perfil/alterar-senha`, o **`/revisao`**, o `/aluno/pareceres`, o `/homenagens`;
- **o efeito**: o `guarda_admin` usa o `guarda_rota("/admin")` → o **REVISOR** é redirecionado para a
  **`home_do_papel(REVISOR)` = `/revisor`** → **404** na v0;
- **o teste da v0 foi atualizado para aceitar o redirect** — então **a suíte não pega o 404**;
- **a consequência**: **se a v0 ainda atende o REVISOR em produção** (o login da v0), **é bloqueio de
  merge** — **a decisão é do ARQUITECT**.

### 2. O `VinculoObra` calculado e não renderizado

O `v1/paineis.py:108` monta o `"obras"` do coordenador; o `v1/templates/admin/painel.html` **não tem**
o `bloco.obras`. **O despacho §1.2 cita o `VinculoObra.coordenador_id`**; os **"estudos escolhidos"**
(o `AmbienteEstudo`) **aparecem** — o critério 1 **passa como escrito**, mas **o vínculo de obras do
coordenador não chega à tela**.

### 3. A cobertura do PR

O `test_painel_admin_200_com_os_dados` **não exercita** as **"obras disponíveis"** (a fixture sem a obra
liberada), os **"feitos"** (o `completed=False`) nem a **"recusada"** no histórico; **o probe do EVAL
exercitou os três e todos renderizam**. **A recomendação**: acrescentar.

### 4. A UX fora da fatia 1

O **"Sair" estático** (o `base.html` L23 — fora do `itens_do_menu`) e o **menu vazio** para o ALUNO/o
COORDENADOR/o INSTRUTOR (**perderam o "Trocar a senha"** que existia). **Fora da fatia 1**; **a revisar
na fatia 3**.
## A correção das 4 ressalvas (o `a18fcb1`) — a conferência rápida

1. **As casas POR VERSÃO**: as chaves **compartilhadas** (o `rota:/admin` = ADMIN; o `rota:/revisor` =
   REVISOR); o **`HOME_DO_PAPEL` da v0 → o REVISOR → o `/admin`** (revertido ao que era); a **v1 ganhou
   o `HOME_DO_PAPEL_V1` → o REVISOR → o `/revisor`**; o teste **`revisor entra: 9.2a` REVERTIDO** (a
   v0 congelada); a **invariante da casa em cada mapa** (o `test_invariante_casa_do_papel` e o
   `test_rf02_invariante_casa_v1`).
2. **A cobertura**: o `test_painel_admin` cobre a **obra disponível** (o `versao_liberada_id` + a
   `aberta`), o **`completed=True`** e o **`recusada`** no histórico.
3. **O `VinculoObra` RENDERIZADO** ("Obras vinculadas") — a recomendação do PLANNER.
4. **O "Alterar senha" e o "Sair" no menu de TODOS os papéis** (o ADMIN, o REVISOR, o COORDENADOR, o
   INSTRUTOR e o ALUNO); o **teste por papel**; o restante do menu dos demais papéis **na fatia 3**.

**O CI `40100843953`**: o `testes (pytest)` **SUCCESS** — **277 da v0 + 172 da v1**.
**Sem o EVAL** (a conferência rápida, não uma rodada 2). **Sem o `subir.sh`.** A **ordem do merge é do
ARQUITECT**.
