# Despacho ao DEVS — o fix da fatia 1 (as 4 ressalvas do EVAL)

> **A ressalva 1 BLOQUEIA o merge** — o fix vem **antes** do merge do #11. As 4 ressalvas vão **no
> mesmo commit**. **Não é uma nova rodada do EVAL** — é uma conferência rápida (o ARQUITECT a faz).

## 1. A ressalva 1 (BLOQUEIA o merge) — as casas **por versão**

**O problema**: o `rbac.py` é **compartilhado**; o `HOME_DO_PAPEL[REVISOR]` passou a `/revisor`, e a
**v0 não tem o `/revisor`** (tem o `/revisao`) → o REVISOR cai em **404 na v0**.

**O fix (a decisão do ARQUITECT):**

- **as chaves de permissão seguem compartilhadas** no `rbac.py` (o `rota:/admin`, o `rota:/revisor`, a
  matriz);
- **o mapa das casas passa a ser POR VERSÃO**:
  - o **`HOME_DO_PAPEL` da v0** **volta EXATAMENTE ao que era**: o **REVISOR → `/admin`**;
  - a **v1 ganha o próprio mapa**: o **REVISOR → `/revisor`**;
- **REVERTER a alteração do teste da v0** — ele **não pode ser relaxado** para acomodar a v1; a **v0
  fica congelada** (nenhuma mudança de comportamento da v0);
- **a invariante da casa (o `test_rf02`) vale para CADA mapa separadamente** — o mapa da v0 (o
  `test_rf02` da v0) e o mapa da v1 (o `test_rf02` da v1), **não um mapa único**.

**O DoD**: o REVISOR na **v0** → o `/admin` (como antes, sem o 404); o REVISOR na **v1** → o
`/revisor`; o **teste da v0 revertido** (a suíte da v0 **intacta**, sem o relaxamento); as **chaves
compartilhadas** (a matriz); a invariante **por mapa**.

## 2. As ressalvas 2 e 3 — no mesmo commit

**(2) A cobertura do `test_painel_admin_200_com_os_dados`**: cobrir
- as **obras disponíveis** (uma `Obra` com o `versao_liberada_id` e a disponibilidade `aberta`, na
  fixture);
- o **`completed=True`** (o "feitos" em vez do "a fazer");
- o **`recusada`** no histórico.

**(3) O `VinculoObra` calculado e não renderizado** (o `paineis.py:108` → o template sem o
`bloco.obras`): **decidir** —
- **renderizar** (o bloco das obras do coordenador no `admin/painel.html`), ou
- **remover** (tirar o cálculo do `paineis.py`, para não manter o código morto).

**A recomendação do PLANNER**: **renderizar** — o despacho §1.2 cita o vínculo de obras do
coordenador, e o dado **já é calculado**; **remover** deixaria o painel **sem** essa informação.

## 3. A ressalva 4 — **NÃO adiar**

**O "Alterar senha" e o "Sair" no menu de TODOS os papéis AGORA.**

- **O porquê**: a **troca de senha é obrigatória no 1º login** — **sem o link, o usuário fica preso**
  (o `must_change_password` sem a saída);
- **o menu** de cada papel: os **links** do papel (o ADMIN/os do ADMIN; o REVISOR/os do REVISOR; os
  demais **ainda sem os links de navegação**, a fatia 3) **+ o "Alterar senha" + o "Sair"**;
- **o teste**: o **menu de cada papel tem o "Alterar senha" e o "Sair"** (o `itens_do_menu` + o
  template);
- **o restante do menu dos demais papéis fica na fatia 3**.

## 4. O registro

- **a correção no relatório** da fatia 1 (o `dev/relatorio-fatia-1.md`? — o que existir);
- **não é uma nova rodada do EVAL** — **a conferência rápida** do ARQUITECT:
  1. a **suíte da v0 intacta** (sem o teste relaxado);
  2. o **menu por papel** (o "Alterar senha"/o "Sair" em todos);
  3. a **casa por versão** (o `/admin` na v0, o `/revisor` na v1).

## O prompt para o DEVS

```text
O fix da fatia 1 da DEM-202610-017 (as 4 ressalvas do EVAL; o #11).

1. A RESSALVA 1 (BLOQUEIA o merge) - as casas POR VERSAO:
   - as chaves de permissao seguem compartilhadas no rbac.py;
   - o HOME_DO_PAPEL da v0 VOLTA EXATAMENTE ao que era (o REVISOR -> o /admin);
   - a v1 ganha o PROPRIO mapa (o REVISOR -> o /revisor);
   - REVERTER a alteracao do teste da v0 (nao relaxar para acomodar a v1; a v0 fica congelada);
   - a invariante da casa (o test_rf02) vale para CADA mapa separadamente.

2. As RESSALVAS 2 e 3 (no mesmo commit):
   - o test_painel_admin cobrir as obras disponiveis, o completed=True e o recusada;
   - o VinculoObra calculado e nao renderizado: RENDERIZAR (a recomendacao) ou REMOVER.

3. A RESSALVA 4 (nao adiar):
   - o "Alterar senha" e o "Sair" no menu de TODOS os papeis AGORA (a troca de senha e obrigatoria
     no 1o login);
   - o teste: o menu de cada papel tem o "Alterar senha" e o "Sair";
   - o restante do menu dos demais papeis fica na fatia 3.

4. O REGISTRO: a correcao no relatorio; a conferencia rapida do ARQUITECT (a suite da v0 intacta, o
   menu por papel, a casa por versao).

O CI verde. Sem o merge (a ordem e do ARQUITECT).
```
