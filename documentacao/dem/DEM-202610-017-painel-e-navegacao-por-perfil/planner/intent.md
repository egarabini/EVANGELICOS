# DEM-202610-012 — o painel e a navegação por perfil na v1 (pós-login)

> **O intent do ARQUITECT** — as fatias e as perguntas abertas. **Devolver ao ARQUITECT antes de
> despachar.**

## 1. O intent

O ARQUITECT logou na v1 e viu: **(a) a volta à landing** e **(b) um menu da v0** (Obras, Catálogo,
Trocar a senha, Sair). **Na v1 hoje o login leva o Admin ao `/admin/obras` (lista) e o Revisor ao
`/revisor/obras`; não há painel nem menu por perfil.** O destino pós-login é o `destino(usuario)` no
`v1/auth.py`.

**O pedido do produto**:

1. O login leva cada perfil ao seu **PAINEL** (dashboard), com o **menu de navegação próprio** do
   perfil;
2. **ADMIN**: um painel-resumo com
   - as **obras e os estudos** disponíveis e em estudo;
   - os **coordenadores**, com os **estudos que cada um escolheu**;
   - para cada coordenador: **seus instrutores, com seus alunos**;
   - a **lista de todos os alunos**, com os estudos feitos e a fazer e os **resultados**;
3. **O ADMIN pode adicionar obras e estudos**, ver as **avaliações e liberações do REVISOR** e os
   **testes dos alunos fake**;
4. **Os demais perfis** (REVISOR, COORDENADOR, INSTRUTOR, ALUNO): definir o painel e o menu de cada
   um, **em fases**.

## 2. O que a v1 **já tem** (a investigação no código)

**Os modelos** (`gsi_ebd/models/` — a v1 usa a mesma biblioteca):

| O modelo | O que ele já guarda |
|---|---|
| `User` (o `Role`) | as 5 personas: ADMIN, COORDENADOR, INSTRUTOR, ALUNO, REVISOR |
| **`Ambiente`** | o **tenant do coordenador** (o `coordenador` dono da turma/do conteúdo) |
| **`Equipe` / `EquipeInstrutor`** | a **equipe do coordenador e os instrutores dela** |
| **`Turma` / `TurmaMembro`** | a **turma e os alunos dela** |
| **`VinculoObra.coordenador_id`** | **qual coordenador vinculou qual obra** |
| `Estudo` / `EstudoCapitulo` | o **estudo** (a obra aplicada em capítulos) |
| `Obra` / `ObraVersao` / o `ObraCapitulo` | a **obra** e as **versões** (a liberação, a N+1) |
| **`StudyAssignment`** | **o aluno × o estudo** (a atribuição) |
| **`Progress` / `UserResponse`** | os **resultados** (as respostas e o progresso) |

**A conclusão da investigação**: **a hierarquia coordenador/instrutor/aluno JÁ EXISTE no modelo** —
**o que falta é a v1 usá-la nas telas** e no **destino do login**.

**As telas** (o `v1/routers/` + o `v1/templates/`): o `/admin/obras` (a lista/o detalhe/a nova), o
`/revisor/obras` (a lista/o detalhe), o `/obras` (a lista), o `/aluno` (a lista/a lição), o
`/perfil/alterar-senha`, o `/login`.

**O que NÃO existe na v1**: o **painel** (o dashboard), o **menu por perfil**, a **criação do ESTUDO**
(a obra aplicada em capítulos — o `/admin/estudos`), a **visão do coordenador** (os seus instrutores/os
seus alunos), a **visão do instrutor** (os seus alunos).

## 3. As fatias propostas

| A fatia | O que entrega | O porquê desta ordem |
|---|---|---|
| **1. O painel do Admin e do Revisor + o menu por perfil** | o **dashboard-resumo** (só **leitura** sobre o que a v1 tem) + o **menu por perfil** + as **rotas novas na matriz** (sem teste vacuoso) | é o **pedido direto** do ARQUITECT; **não cria entidade nova** (só consultas); o menu é a **porta** de tudo |
| **2. A criação do ESTUDO + as avaliações/liberações** | o **`/admin/estudos`** (a obra aplicada em capítulos) + a **visão das avaliações/liberações do REVISOR** + os **testes dos fake** | **exige** a fatia 1 (o menu e o painel); o modelo do `Estudo` **já existe** — falta a tela |
| **3. Os demais perfis** | o painel do **COORDENADOR** (os estudos escolhidos; os instrutores; os alunos), o do **INSTRUTOR** (os alunos; o progresso) e o do **ALUNO** (os estudos; o progresso) | **em fases** — o pedido 4; cada perfil é um painel |
| **4. A hierarquia nas telas** | a **navegação** coordenador → instrutor → aluno (o drill-down) | depende das 1–3; é a **camada de interação** |

**O que a fatia 1 NÃO inclui**: a criação de nada. **Ela lê** o que existe e **organiza** o menu.

## 4. As perguntas abertas (para o ARQUITECT)

1. **A prioridade**: esta DEM **antes ou depois do 1b (o Zitadel)**? **A recomendação do PLANNER**: **depois do 1b** — porque o 1b **muda o login** (o Zitadel), e o painel **depende do `destino`** — fazer o painel antes é **refazer** o destino. **A decisão é do ARQUITECT.**
2. **O menu por perfil × o `rbac.py`**: o menu é **derivado da matriz** (a fonte única) ou **hard-coded** no template? **A recomendação**: **derivado** (o `rbac.py`'s a matriz) — o menu **mostra só o que o papel pode**, e o **teste da matriz** cobre as rotas novas.
3. **A criação do ESTUDO na fatia 1 ou na 2?** — o pedido 3 (o Admin adiciona obras e estudos) **pode** estar na 1 (o botão) mas a **tela** na 2. **A recomendação**: a **tela na 2** (a 1 é a leitura).
4. **Os testes dos alunos fake** no painel: **ler** os `UserResponse`/`Progress` dos fake (a fatia 2) — ou uma **tela própria**? **A recomendação**: a **lista no painel** (a fatia 2).
5. **O nível do processo (o ADR-018)**: **o EVAL cego** em cada fatia (o modo ágil, o máximo de 2 rodadas) — **a recomendação**: **sim**, como nas obras.
6. **O defeito do retorno (a v0 → a landing)**: ver o §5.

## 5. O defeito separado — a volta do login da v0 para a landing

**O sintoma**: na produção, **depois de entrar pelo login da v0**, o usuário **volta à landing** —
porque o **`/` da produção passou a ser a landing da v1** (a `v0.1.1`) e **a v0 retorna ao `/`**.

**As opções**:

| A opção | O efeito |
|---|---|
| **(a) Ajustar o retorno da v0** | a v0 **redireciona** para a sua **casa por papel** (o `/aluno`, o `/admin`…) em vez do `/` — **mexe no roteamento da v0** (precisa da **autorização do ARQUITECT**) |
| **(b) Aceitar até a virada da v1** | a **v1** assume o `/login` (o 1b) e o retorno **passa a ser o `destino`** — **sem mexer na v0**; o defeito **dura até a virada** |

**A recomendação do PLANNER**: **a (b)** — **é o mesmo trabalho que a virada fará** (o `/login` na v1), e a **(a)** **mexe na v0** (o roteamento) **sem resolver a médio prazo**. **A (a) só vale se o defeito incomodar muito até a virada** — **a decisão é do ARQUITECT**.

## 6. O que **não** se faz

- **não ler o banco da v0** (a decisão do ARQUITECT);
- **não mexer no roteamento** sem a autorização do ARQUITECT (a correção do §5);
- **não decidir a prioridade** — o PLANNER **recomenda**;
- **não despachar** antes da revisão do ARQUITECT.
## 7. As respostas do ARQUITECT (24/10)

1. **NÚMERO**: **não** usar o `DEM-202610-012` (já existe a **credencial-de-seed**, o PR #3) —
   **renomeada para `DEM-202610-017`** (o `015` não está no repositório, mas o `016` está; o `017`
   era a sugestão).
2. **PRIORIDADE**: **a fatia 1 ANTES do 1b**. A interface `usuario_atual`/`exige` (o ADR-021)
   **isola o login**; o Zitadel **não obriga a refazer o `destino`/o menu**. O 1b segue **depois**,
   com as pendências dele (a infra do `oidc` e o AGPL).
3. **ESCOPO da fatia 1**: **confirmado** — o Admin e o Revisor, **só leitura**, o **menu derivado do
   `rbac.py`**, as **rotas novas na matriz sem teste vacuoso**, o **EVAL cego** (o máximo de 2
   rodadas). As **fatias 2 a 4** como propostas.
4. **O DEFEITO "volta à landing"**: **a hipótese do AUXILIAR NÃO está confirmada** — o código da v0
   **redireciona para o `self.redirect_path`** (a casa do papel: o `gsi_ebd/states/auth.py` L62 e
   L148). **Não decidir a (a)/(b) ainda** — o ARQUITECT vai informar **o endereço exato e os
   passos**; depois uma **investigação curta** (sem mexer no roteamento nem na v0) diz a **causa**.

### A REGRA que fica

**Hipótese do AUXILIAR não é fato.** O defeito **"volta à landing"** fica registrado como **"a
confirmar"** — **com o endereço e os passos do ARQUITECT** antes de qualquer conclusão. **A hipótese
do AUXILIAR (a v0 retorna ao `/`) foi REFUTADA pelo código** (`self.redirect_path`).
