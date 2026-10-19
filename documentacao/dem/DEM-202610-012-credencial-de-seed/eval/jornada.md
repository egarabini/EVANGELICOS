# Jornada do EVAL — DEM-202610-012 / credencial de seed

> **Julgamento cego.** Não li `dev/jornada.md`, não procurei a identidade de quem
> implementou e não alterei o código. O julgamento segue o `planner/plano-testes.md`
> e a `planner/spec.md`.

## 0. Identificação

| Item | Valor |
|---|---|
| DEM | DEM-202610-012 — credencial de seed |
| Branch | `feature/DEM-202610-012-credencial-de-seed` |
| Commit avaliado | `427e8bb` (`fix(seed): exige senha do ambiente e troca no primeiro acesso`) |
| Estado da árvore | avaliada em `427e8bb`; ao fim do julgamento o `HEAD` foi movido **externamente** para `develop`/`dbbfc09` (merge do PR #3), com árvore **idêntica** (`git diff 427e8bb..HEAD` vazio). O EVAL não fez esse checkout. |
| Data do julgamento | 2026-10-19 |
| Papel | EVAL (subagente cego) |
| Baseline declarado | 113 testes |
| App | `ESTUDOS_BIBLICOS/GSI_EBD` |
| Docs lidos | `eval/briefing-eval.md`, `planner/intent.md`, `planner/spec.md`, `planner/plano-testes.md`, o diff `origin/develop...HEAD` e o código |

**Condição de cegueira respeitada:** o arquivo `dev/jornada.md` não foi aberto.
Não há, neste documento, qualquer referência à autoria da implementação.

## 1. O que foi executado

- Suíte completa a partir do diretório do app (`ESTUDOS_BIBLICOS/GSI_EBD`).
- Casos F-01 a F-07, N-01 a N-04 e C-01 a C-03, com verificação manual quando o
  teste automatizado não cobria a letra do caso.
- CA01 a CA05, um por um.
- Prova de mutação: senha reintroduzida no `seed.py`, login reintroduzido no
  `subir.sh` e fail-fast removido; depois, restauração com `git checkout --` e
  confirmação da árvore limpa.

## 2. Ambiente e desvios de procedimento

O ambiente de execução é Windows, com `venv` em Python 3.14.6 e um sandbox de
arquivos que nega escrita (e às vezes leitura) em parte da árvore. Isso obrigou a
três adaptações, todas **fora do código do app** e registradas aqui para que o
resultado não seja lido como se o comando literal tivesse rodado sem atrito.

### 2.1 `pytest.exe` do venv (uv trampoline)

Comando literal do plano:

```
.\.venv\Scripts\pytest.exe tests -q
```

Saída:

```
error: uv trampoline failed to canonicalize script path
[exit code: 1]
```

Não é falha do código: o `pytest.exe` do venv é um trampoline do `uv` que não
resolve neste ambiente. O próprio plano admite a alternativa `python -m pytest`,
que foi usada.

### 2.2 `tmp_path` e diretórios `0o700` no sandbox

Comando:

```
.\.venv\Scripts\python.exe -m pytest tests -q
```

Saída resumida:

```
117 passed, 2 warnings, 11 errors in 7.64s
...
PermissionError: [WinError 5] Acesso negado:
  'C:\Users\eduardo.neto\AppData\Local\Temp\dsh-...\pytest-of-eduardo.neto'
```

Os 11 erros são todos de `tmp_path` (os 11 testes novos que usam a fixture
`banco(tmp_path)`). A causa é ambiental: neste token do sandbox, um diretório
criado com modo `0o700` pelo Python 3.14 fica inacessível ao próprio processo que
o criou. Não é defeito do teste nem do código.

**Workaround usado** (fora do repositório): um `sitecustomize.py` em
`documentacao/.eval-env/` que ignora o `mode` na criação de diretórios, e
`--basetemp` apontando para uma área gravável. O shim não altera o app, não
altera os testes e foi removido no fim. Trecho do shim:

```python
import os
_orig_mkdir = os.mkdir
def _mkdir(path, mode=0o777, *args, **kwargs):
    return _orig_mkdir(path, 0o777, *args, **kwargs)
os.mkdir = _mkdir
```

Com o shim:

```
.\.venv\Scripts\python.exe -m pytest tests -q -p no:cacheprovider \
  --basetemp=C:\...\documentacao\.pytest-tmp-dem012-run2
```

```
128 passed, 18 warnings in 23.52s
```

### 2.3 Escrita na árvore do app negada pelo ACL

A árvore `ESTUDOS_BIBLICOS/GSI_EBD` tem uma ACE `Todos:(I)(CI)(DENY)(DC)`
(`DeleteSubdirectoriesAndFiles`) herdada e o token do sandbox não consegue
criar/alterar arquivos ali:

```
mkdir FAIL: Access to the path '...\GSI_EBD\.pytest_tmp_manual' is denied.
append FAIL: Access to the path '...\GSI_EBD\README.md' is denied.
```

Por isso, a prova de mutação foi feita em uma **cópia fiel** da árvore de trabalho
(criada a partir do worktree limpo em `427e8bb`), com um repositório git local
inicializado nela, para permitir o `git checkout -- <arquivo>` exigido pelo
briefing. A cópia rodou a suíte baseline com **128 passed** antes de qualquer
mutação. A árvore real **nunca foi modificada**:

```
$ git -C ESTUDOS_BIBLICOS/GSI_EBD status --short --branch
## feature/DEM-202610-012-credencial-de-seed...origin/feature/DEM-202610-012-credencial-de-seed
$ git -C ESTUDOS_BIBLICOS/GSI_EBD diff HEAD --stat
(vazio)
$ git -C ESTUDOS_BIBLICOS/GSI_EBD rev-parse HEAD
427e8bbffee73b3f1146b3daa25a91736136dbe7
```

Conferência de conteúdo dos dois arquivos que foram mutados na cópia:

```
gsi_ebd/data/seed.py  real=5118c556e14e431cf9d27864970d7619eb13d220  HEAD=5118c556e14e431cf9d27864970d7619eb13d220  equal=True
deploy/subir.sh       real=344c375d2ad0d1c789be8454267f0e99d35b10d6  HEAD=344c375d2ad0d1c789be8454267f0e99d35b10d6  equal=True
```

Depois de restaurar, a cópia também voltou a ter os dois arquivos com o hash do
`HEAD`, e `git status --short` ficou vazio.

### 2.4 Resíduos do ambiente (não do app)

Três diretórios criados pelo workaround ficaram com DACL inacessível e não
puderam ser removidos nem com `Remove-Item`, `icacls /reset` ou `shutil.rmtree`:

- `documentacao/.pytest-tmp-dem012/`
- `documentacao/eval_py_700b/`
- `documentacao/.eval_py_mkdir/`

Eles estão **fora** de `ESTUDOS_BIBLICOS/GSI_EBD`, não são versionados e não
afetam a árvore do app nem os resultados. `documentacao/.eval-work/` e
`documentacao/.eval-env/` foram removidos.

## 3. Suíte completa (H-01 / CA01)

| Comando | Resultado |
|---|---|
| `.\.venv\Scripts\pytest.exe tests -q` | falha do trampoline `uv` (ambiente) |
| `.\.venv\Scripts\python.exe -m pytest tests -q` | 117 passed, 11 errors (todos `tmp_path`/ACL) |
| `python -m pytest tests -q -p no:cacheprovider --basetemp=...` + shim | **128 passed**, 18 warnings, 23.52s |
| Cópia fiel, suíte baseline | **128 passed**, 28.36s |
| Cópia fiel, depois de restaurar as 3 mutações | **128 passed**, 24.34s |

Contagem: `tests/test_seed.py` coleta **15 testes novos**; 113 + 15 = **128**.
O baseline de 113 foi confirmado pela subtração e pela coleta (`15 tests
collected` no arquivo novo).

## 4. Casos do plano

### 4.1 Funcionais (F)

| ID | Resultado | Evidência |
|---|---|---|
| **F-01** | **PASS** | `run_seed()` sem `SEED_PASSWORD` (variável ausente): `Defina SEED_PASSWORD no ambiente para rodar o seed.`, `EXIT=1`, `DB_EXISTS=False` (nenhum usuário, nem tabela). Teste `test_rf02_seed_aborta_antes_de_acessar_banco[False-None]` passa. |
| **F-02** | **PASS** | Variável **presente e vazia** (`os.environ['SEED_PASSWORD']=''`): mesma mensagem, `EXIT=1`, `DB_EXISTS=False`. Teste `[False-]` passa. |
| **F-03** | **PASS** | Banco limpo + `SEED_PASSWORD='x'`: seed termina com `EXIT=0`; inspeção do SQLite mostra **5 usuários**; os 5 hashes são bcrypt `$2b$12$` e `bcrypt.checkpw('x', hash)` retorna `True` em todos. |
| **F-04** | **PASS** | Os 5 usuários (admin id 1, coordenador, instrutor, aluno1, aluno2) estão com `must_change_password=true`, **inclusive o admin**. O teste `test_rf01_rf03...` também verifica os 5. |
| **F-05** | **PASS** | Preparei o banco com flags `must_change_password=false` e `nome_base="MUTADO-PELO-USUARIO"`, rodei o seed de novo com outra senha (`y`): a saída mostra `Admin já existe — pulando`, `Coordenador já existe — pulando`, `Instrutor ja existe - pulando`, `Aluno ... já existe — pulando`, `Estudos já existem — pulando`, `Turmas ja existem - pulando`; `identical: True` para `(id, password_hash, must_change_password, nome_base)`; nada sobrescrito, nada duplicado. |
| **F-06** | **PASS** | `.env.example` linha 37: `SEED_PASSWORD=` (única ocorrência da chave; sem valor real). Teste `test_rf06_exemplo_sem_senha_real` passa. |
| **F-07** | **PASS** | `deploy/subir.sh` não tem `Login`, `admin@gsi.ebd` nem `senha123` (0 ocorrências); o rodapé termina em `Site`, `Homenagens`, `TROQUE AS SENHAS ...`, `Se algo falhar`, sem credencial. Teste `test_rf07_deploy_nao_imprime_credenciais` passa. |

### 4.2 Negativos (N)

| ID | Resultado | Evidência |
|---|---|---|
| **N-01** | **PASS** | Varredura dos 5 caminhos do RF04 (14 arquivos: 4 paths + 10 `tests/*.py`): **0 ocorrências** de `senha123`. Teste `test_rf04_varredura_do_escopo` passa. |
| **N-02** | **PASS** | Seed em banco limpo com senha sintética distinta (`EvalSeedPass-7Q2`): `EXIT=0`, 40 linhas de saída, `OUTPUT_CONTAINS_PASSWORD=False`; os hashes conferem (`password_match: true` em 5/5). Teste `test_rf01_rf03...` também usa `capsys` e uma senha `token_urlsafe` e passa. |
| **N-03** | **PASS** | Banco já populado (5 usuários) + `SEED_PASSWORD` ausente: `EXIT=1`, mensagem de fail-fast, `USERS_BEFORE=5`, `USERS_AFTER=5`, `DB_UNCHANGED=True`. O RF02 vence antes de olhar o banco; teste `[True-None]` passa. |
| **N-04** | **PASS** | Teste `test_rf04_varredura_repositorio_lista_excecoes` passa e imprime as exceções encontradas: `Diagnostico/plano-hierarquia-e-equipes.md`, `Diagnostico/roteiro-de-testes.md`, `gsi_ebd/pages/admin.py`, `gsi_ebd/states/admin.py` — todas declaradas na §5 (as duas de `admin.py` são a D-10). `git grep -n senha123` independente retorna exatamente as mesmas 4. |

### 4.3 Contratos (C)

| ID | Resultado | Evidência |
|---|---|---|
| **C-01** | **PASS** | `git diff origin/develop...HEAD -- requirements.txt requirements-dev.txt` → vazio. |
| **C-02** | **PASS** | `git diff origin/develop...HEAD -- gsi_ebd/models/` → vazio (nenhum schema novo). |
| **C-03** | **PASS** | `pytest tests/test_paginas.py -q` → **9 passed** em 1.64s. |

### 4.4 Saúde (H)

| ID | Resultado | Evidência |
|---|---|---|
| **H-01** | **PASS** | 128 passed (113 + 15), do diretório do app, com o workaround de ambiente documentado na §2. |
| **H-10** | **PASS** | F-01 e F-02: ausente e vazia abortam com exit ≠ 0, sem criar usuário. |
| **H-11** | **PASS** | 0 ocorrências nos 5 caminhos do RF04 (N-01); repositório do app só com as 4 exceções declaradas (N-04). |

## 5. Critérios de aceitação

| ID | Resultado | Justificativa |
|---|---|---|
| **CA01** | **PASS** | 128 testes verdes = 113 do baseline + 15 novos; suíte rodada do diretório do app. |
| **CA02** | **PASS** | F-01, F-02 e N-03: sem a variável (ou vazia), exit 1, zero usuários; em banco populado, o banco não muda. |
| **CA03** | **PASS** | F-04: 5/5 usuários com `must_change_password=True`, admin incluso; o teste de login percorre os 5 valores de `Role` (ADMIN, COORDENADOR, INSTRUTOR, ALUNO, REVISOR) e confirma o redirect para `/perfil/alterar-senha`. |
| **CA04** | **PASS (com nota de escopo)** | 5 caminhos do RF04: zero. Varredura do repositório do app: apenas as 4 exceções declaradas, e o teste as lista. **Nota:** os registros de DEM/EVAL e a `ADR-008` vivem no repositório guarda-chuva, não no repositório `GSI_EBD`; as permissões `documentacao/dem/` e `/eval/` do teste são inalcançáveis a partir dele. O CA04 está satisfeito para o repositório do app, mas não prova o guarda-chuva (ver aviso A-4). |
| **CA05** | **PASS (com nota)** | Nenhuma dependência nova (`requirements*` intactos) e nenhum schema novo (`gsi_ebd/models/` intacto). O CI do PR #3 está verde conforme o contexto da DEM; não foi reverificado localmente porque `gh` não está instalado neste ambiente. |

## 6. Prova de mutação

Todas as mutações foram feitas na **cópia fiel** (a árvore real não aceita
escrita — §2.3), com restauração por `git checkout -- <arquivo>` e verificação de
`git status` limpo. A cópia baseline rodou 128 testes verdes.

### M-1 — senha reintroduzida no `seed.py`

Mutação: acrescentada a linha `DEFAULT_PASSWORD = "senha123"` ao fim de
`gsi_ebd/data/seed.py`.

```
$ pytest tests/test_seed.py::test_rf04_varredura_do_escopo \
         tests/test_seed.py::test_rf04_varredura_repositorio_lista_excecoes -q
E       AssertionError: assert not ['gsi_ebd\\data\\seed.py']
tests/test_seed.py:119: AssertionError
E       AssertionError: ['gsi_ebd/data/seed.py']
tests/test_seed.py:159: AssertionError
Excecoes historicas encontradas: ['Diagnostico/...', '...', 'gsi_ebd/data/seed.py', ...]
FAILED tests/test_seed.py::test_rf04_varredura_do_escopo
FAILED tests/test_seed.py::test_rf04_varredura_repositorio_lista_excecoes
2 failed in 2.48s
```

Restauração:

```
$ git checkout -- gsi_ebd/data/seed.py
$ git status --short        # vazio
$ pytest ... (os mesmos dois testes)
2 passed in 3.23s
```

### M-2 — login/senha reintroduzidos no `subir.sh`

Mutação: acrescentada ao fim de `deploy/subir.sh` a linha
`echo "Login  : https://didasko.app.br/login  (admin@gsi.ebd / senha123)"`.

```
$ pytest tests/test_seed.py::test_rf07_deploy_nao_imprime_credenciais \
         tests/test_seed.py::test_rf04_varredura_do_escopo -q
E       assert 'echo "Login' not in '#!/usr/bin/...senha123)"'
E       AssertionError: assert not ['deploy\\subir.sh']
FAILED tests/test_seed.py::test_rf07_deploy_nao_imprime_credenciais
FAILED tests/test_seed.py::test_rf04_varredura_do_escopo
2 failed in 3.33s
```

Restauração:

```
$ git checkout -- deploy/subir.sh
$ git status --short        # vazio
$ pytest ... (os mesmos dois testes)
2 passed in 1.94s
```

### M-3 — fail-fast removido

Mutação: o bloco de `seed_password()` foi trocado para devolver
`"mutation-default"` quando a variável falta (sem `raise SystemExit`). O valor
não contém `senha123`, para isolar o F-01 do N-01.

```
$ pytest tests/test_seed.py::test_rf02_seed_aborta_antes_de_acessar_banco -q
E       Failed: Seed acessou o banco sem SEED_PASSWORD
FAILED ...[False-None]
FAILED ...[False-]
FAILED ...[True-None]
FAILED ...[True-]
4 failed in 6.82s
```

Restauração:

```
$ git checkout -- gsi_ebd/data/seed.py
$ git status --short        # vazio
$ pytest ... (os 4 parâmetros)
4 passed in 4.84s
$ pytest tests -q ...       # suíte completa
128 passed in 24.34s
```

Conferência final: os dois arquivos mutados voltaram ao hash do `HEAD`
(`seed.py 5118c55...`, `subir.sh 344c375...`) e a cópia ficou com
`git status --short` vazio. A árvore real está limpa e sem modificações do EVAL.

> **Nota de estado:** no fim do julgamento o worktree foi movido por outro
> processo para `develop` e `dbbfc09` (merge do PR #3). A branch
> `feature/DEM-202610-012-credencial-de-seed` continua em `427e8bb`;
> `git diff 427e8bb..HEAD` é vazio (mesma árvore) e o `HEAD^{tree}` é igual ao
> `427e8bb^{tree}`. Os resultados acima valem para o conteúdo avaliado; o
> checkout não foi feito pelo EVAL.

**Conclusão da prova:** os testes não são vacuosos. Se o guarda cai, o teste cai;
se o guarda volta, o teste volta. O N-01/F-07 pegam a senha reintroduzida no seed
e no `subir.sh`; o F-01/F-02/N-03 pegam o fail-fast removido.

## 7. Achados, avisos e riscos (separados dos FAILs)

Não houve FAIL de caso do plano. Os itens abaixo são avisos **não bloqueantes**
para o veredito de código, mas alguns são relevantes para o fechamento
operacional do D-01.

### A-1 (operacional, relevante) — `SEED_PASSWORD` só no `.env` não é lida pelo guarda

Teste realizado na cópia: `.env` com `SEED_PASSWORD=<valor sintético>` e a
variável **ausente** do ambiente do processo. Resultado:

```
Defina SEED_PASSWORD no ambiente para rodar o seed.
EXIT=1
DB_EXISTS=False
```

Causa: `run_seed()` chama `seed_password()` na linha 695 **antes** de
`from rxconfig import config` (linha 698); é o `rxconfig.py` que faz
`load_dotenv()`. O `intent.md` §5 diz que "o `.env` de produção ganha
`SEED_PASSWORD`"; a `spec.md` §4, porém, mostra o contrato com
`os.environ.get("SEED_PASSWORD")`, que é o que o código implementa. O código
segue a spec, mas a instrução operacional do intent não funciona sozinha.

Sugestão (fora do escopo desta DEM, para o PLANNER decidir): carregar o dotenv
antes do guarda (`load_dotenv()` no topo do `seed.py` ou mover o guarda para
depois do `from rxconfig import config`) e/ou documentar que a variável precisa
ser **exportada/passada** ao processo, não apenas escrita no `.env`.

### A-2 (operacional, relevante) — o Compose não repassa `SEED_PASSWORD` ao app

`deploy/docker-compose.producao.yml` (bloco `environment` do serviço `app`,
linhas 72–97) não tem `SEED_PASSWORD`. O `deploy/DEPLOY.md` (linhas 117–120)
reconhece a pendência: "o Compose atual não repassa `SEED_PASSWORD` ao serviço
`app`. Defini-la apenas no `.env` da VPS não a disponibiliza no contêiner. O seed
em banco novo permanece bloqueado até o PLANNER autorizar esse repasse."

Isso é honesto, mas significa que o comando documentado
(`docker compose ... exec app python -m gsi_ebd.data.seed`) **aborta** num
deploy limpo até que o Compose receba `SEED_PASSWORD` (ou o comando use
`exec -e SEED_PASSWORD=...`). O objetivo de segurança é atingido (fail-safe),
mas o passo operacional do ARQUITECT no fechamento do D-01 fica bloqueado. Não é
violação de RF desta DEM (o Compose não está no escopo "In"), e sim uma
pendência de integração a resolver antes de considerar o seed executável em
produção.

### A-3 (qualidade de teste, não bloqueante) — o F-07 é mais fraco que o N-01

`test_rf07_deploy_nao_imprime_credenciais` afirma apenas que não existe
`'echo "Login'` e que `admin@gsi.ebd` não aparece no `subir.sh`. Um
`echo "senha123"` isolado passaria nesse teste e só seria pego pelo N-01. Como o
N-01 existe e cobre a senha, não há furo na suíte; mas o F-07, sozinho, não
prova a ausência da senha. Sugestão: acrescentar ao F-07 a asserção da string
proibida (ou deixar explícito que o N-01 é o guarda da senha).

### A-4 (escopo da varredura, não bloqueante) — o N-04 só enxerga o repo do app

O teste roda `git ls-files` em `ROOT = ESTUDOS_BIBLICOS/GSI_EBD`. As exceções
`documentacao/dem/`, `/eval/` e `documentacao/adr/ADR-008*` estão no repositório
guarda-chuva, **fora** do repositório do app; as condições que as permitem no
teste são inalcançáveis ali. O N-04 prova o repositório do app, não o
guarda-chuva. Para o RF04 (lista de 5 caminhos do app) isso é suficiente; para
uma leitura literal do CA04 ("o repositório"), fica a nota. Nenhuma ocorrência
inesperada foi encontrada no repo do app.

### A-5 (cobertura de teste, não bloqueante) — `tests/` é varrido só em `*.py`

O RF04 diz `tests/`; o teste varre `(ROOT / "tests").rglob("*.py")`. Hoje
`tests/` tem **10 arquivos, todos `.py`**, e a varredura manual de todas as
extensões deu 0 ocorrências. O risco é futuro: uma fixture `.json`/`.txt` com a
senha não seria pega pelo teste. Sugestão: varrer todos os arquivos de `tests/`.

### A-6 (robustez, não bloqueante) — senha só de espaços é aceita

`seed_password()` usa `if not password`; `SEED_PASSWORD=" "` é truthy e vira
senha. A spec só define vazio como ausente, então não é violação; é um caso de
borda que um `password.strip()` resolveria. Não testado em produção; apontado
por leitura do código.

### A-7 (pré-existente, não bloqueante) — `print` com emoji no console cp1252

Rodando o seed com `stdout` redirecionado no Windows, o `print("\n🌱 ...")`
levanta `UnicodeEncodeError: 'charmap' codec ...`. Isso é **pré-existente**
(a linha não foi tocada por este diff) e não ocorre no teste (`capsys`) nem no
container Linux (UTF-8). Não afeta o julgamento; registrado porque apareceu no
CLI local.

### A-8 (procedimento) — resíduos do sandbox

Os três diretórios listados na §2.4 não puderam ser removidos por DACL. Eles
estão fora do app e não são versionados; o EVAL não conseguiu limpá-los. Se o
ambiente for reutilizado, convém removê-los com um token com `WRITE_DAC` ou
recriar a pasta `documentacao` a partir do git.

## 8. Veredito

**PASS** (com condições operacionais registradas em A-1 e A-2).

Justificativa:

1. **Todos os casos do plano passam** — F-01 a F-07, N-01 a N-04, C-01 a C-03,
   H-01/H-10/H-11. Não há FAIL de caso.
2. **Os CA01–CA05 estão atendidos** no escopo do código: 113 + 15 = 128 verdes,
   fail-fast sem usuário, todos com troca obrigatória, zero `senha123` nos 5
   caminhos e nenhuma dependência/schema novo.
3. **A prova de mutação mostra que os testes mordem**: reintroduzir a senha no
   `seed.py` derruba N-01/N-04; reintroduzi-la no `subir.sh` derruba F-07/N-01;
   remover o fail-fast derruba os 4 parâmetros de F-01/F-02/N-03. Restaurado com
   `git checkout --`, a suíte volta a 128 verdes e a árvore fica limpa.
4. **O objetivo de segurança da DEM foi atingido**: um seed novo não cria conta
   com senha conhecida; a senha vem do ambiente, é obrigatória e todos nascem
   com `must_change_password=True`, inclusive o admin; a senha não aparece nos
   arquivos do RF04, no log do seed nem no rodapé do `subir.sh`.

**Ressalvas que não mudam o veredito de código, mas precisam de decisão antes do
fechamento do D-01:**

- **A-1/A-2:** o passo operacional "definir `SEED_PASSWORD` no `.env`" não é
  suficiente; o Compose não repassa a variável e o guarda roda antes do
  `load_dotenv()`. O seed em produção limpa permanece bloqueado (fail-safe) até
  o PLANNER autorizar o repasse no Compose ou o comando passar a variável
  explicitamente (`exec -e`). Isso é uma pendência de integração, não um defeito
  do escopo de código desta DEM.
- **A-3 a A-6** são melhorias de teste/robustez, sem impacto no resultado atual.
