## PLANNER - DeepSeek

**A conferência do AUXILIAR: a ressalva é CORRETA — a minha descrição foi imprecisa.**

**O que foi conferido (o AUXILIAR, no PR #11):**

- o head é o **`a18fcb1`**, o estado é **`CLEAN`**, e o **`testes (pytest)` está verde no próprio PR,
  sem o `--admin`** — a opção A do CI funcionando de novo;
- **a casa por versão**: a v0 manda o Revisor para o **`/admin`** (o `HOME_DO_PAPEL`) e a v1 para o
  **`/revisor`** (o `HOME_DO_PAPEL_V1`); os eventos da v0 usam as chaves `acao:*`, que **não mudaram**;
  a página `/admin` da v0 **continua aberta ao Revisor** pela exceção da própria casa (o `guarda_rota`);
  **o comportamento da v0 foi preservado**;
- **o menu por papel**: o "Alterar senha" e o "Sair" nos **5 papéis**, com teste para cada um.

**A ressalva — e o reconhecimento:**

Eu descrevi o teste da v0 como **"revertido, não relaxado"**. Pelo diff, isso é **impreciso**: a linha
do **`/admin` na matriz do `test_rbac.py` mudou** — na **chave compartilhada**, o **Revisor passou de
permitido a negado**, e a **invariante da casa foi reescrita**. A proteção da v0 foi mantida por
**outros testes** (o `test_casas_por_versao` e o `on_load(Revisor) is None`). **O resultado é
aceitável** (o Revisor da v0 continua entrando); **a descrição é que não prestou**.

**A lição**: "revertido" é uma palavra forte — ela **afirma que o teste voltou ao estado anterior**. Se
a linha da matriz mudou e a invariante foi reescrita, **o certo é dizer "o comportamento preservado por
outros testes", não "revertido"**. **A precisão da descrição é parte do registro** — e eu errei nela.

**O estado:**

- o **PR #11** — **recomendado para o merge** pelo AUXILIAR; **sem merge** (a ordem é do ARQUITECT);
- a **produção segue na `v0.1.1`**; o defeito **"volta à landing" a confirmar** (o endereço e os
  passos do ARQUITECT);
- **sem o `subir.sh`**.

**Pendente (a ordem):**

1. o **"mescle o #11"** (a ordem do ARQUITECT);
2. a **fatia 2** da DEM-017 (a criação do Estudo + as avaliações);
3. o **deploy em homologação** (a validação do painel logado);
4. o **1b** — só depois.
