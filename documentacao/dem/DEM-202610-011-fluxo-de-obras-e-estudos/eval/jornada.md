# Jornada do EVAL — DEM-202610-011, fatia 1 (o domínio)

> **EVAL cego.** Não sei quem implementou e não procurei saber. Julguei pelo plano aprovado
> (`planner/`), pelo diff e pelo código.
> **O que foi julgado:** branch `feature/DEM-202610-011-fatia1-dominio`, commit `8f6608a`
> (`fix: fecha lacunas do dominio conforme design v4`), PR #4 — o app em
> `ESTUDOS_BIBLICOS/GSI_EBD`.
> **Data:** 2026-10-19.
> **Veredito: FAIL** — a suíte está verde (211), as seis mutações obrigatórias são detectadas e
> quase todo o plano se sustenta, mas **F-06** e **N-01/H-16** não se sustentam: o `contestar`
> não devolve a versão/obra a `em_revisao` (o teste do repositório codifica o contrário) e o
> gate de importação usa a decisão **em cache**, admitindo uma fonte que o inventário atual
> marca `nao_entra`. Os detalhes estão nas §3, §6 e §7.

---

## 1. Ambiente e contornos

| Item | Situação |
|---|---|
| cwd | `C:\Projetos\EM_ESTUDO\EVANGELICOS` |
| app | `ESTUDOS_BIBLICOS\GSI_EBD` |
| branch / HEAD | `feature/DEM-202610-011-fatia1-dominio` / `8f6608a4bdeab6a381e8db95246a5c8badd5e60f` |
| árvore do app antes e depois | limpa (`git status --porcelain` vazio); **não** fiz checkout nem toquei na branch |
| Python | `.venv\Scripts\python.exe` — **Python 3.14.6**; pytest 9.1.0; sqlmodel 0.0.38 |
| `python` do PATH | Python 3.14.6 **sem** `sqlmodel`; por isso usei o interpretador da `.venv` com `-m pytest` (o briefing já pedia `python -m pytest`, não `pytest.exe`) |
| `--basetemp` | fora do app (em `%TEMP%`), como o briefing pedia |

**Contorno 1 — o `tmp_path` 0o700 do Windows/Python 3.14.** Só o `--basetemp` fora do app **não
bastou**: o pytest cria o diretório com `Path.mkdir(mode=0o700)` e, neste Windows/sandbox, o
diretório criado fica **não enumerável** pelo próprio processo (`PermissionError: [WinError 5]`).
Isso derrubou os testes que usam `tmp_path` (as fixtures de `test_flow.py`/`test_fontes.py`
dependem dele; a execução mostrou 11 `E` e, no fim da sessão, o `cleanup_dead_symlinks` do pytest
também estourou). Para julgar o **código**, carreguei um plugin **de harness**
(`.eval-harness/no_tmp_cleanup.py`, via `PYTHONPATH` + `-p no_tmp_cleanup`) que (a) troca
`mode=0o700` por `0o777` no `Path.mkdir` e (b) desliga o scan de symlinks mortos. O plugin **não**
altera o app nem os testes; sem ele, a suíte não é executável neste ambiente.

**Contorno 2 — a cópia fiel para a mutação.** `git worktree add` foi negado
(`Permission denied` em `.git/worktrees/...`) e `git clone` local falhou no sandbox
(`sh: couldn't create signal pipe, Win32 error 5`). Fiz a cópia fiel com
`git -C ESTUDOS_BIBLICOS/GSI_EBD archive --format=zip --output=... 8f6608a`, extraí em
`.eval-mut/repo` e inicializei um git local (`git init` + um commit `snapshot 8f6608a`). O
`flow.py` da cópia tem o mesmo sha256 do app (`031DD0...B7AA`), a cópia de base roda os mesmos
83 testes verdes, e cada mutação foi restaurada com `git checkout -- gsi_ebd/services/flow.py`
com `git status --porcelain` vazio depois.

**Contorno 3 — o `.eval-basetemp` no workspace.** A primeira tentativa de `--basetemp` dentro do
workspace criou um diretório com uma ACL que nem o `icacls` consegue ler; o basetemp passou a
ficar em `%TEMP%`. O diretório `.eval-basetemp` ficou **inacessível** na raiz do workspace (não
está no app nem é versionado; não foi possível removê-lo sem escalar permissão — ver §8).

---

## 2. A suíte (H-01)

Comando (do diretório do app):

```powershell
cd C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD
$bt = Join-Path $env:TEMP ("gsi-eval-" + [guid]::NewGuid().ToString("N"))
$env:PYTHONPATH = "C:\Projetos\EM_ESTUDO\EVANGELICOS\.eval-harness"
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider -p no_tmp_cleanup --basetemp=$bt
```

Saída:

```text
211 passed, 18 warnings in 23.62s
```

São **211** testes (o baseline de 128 + **83** novos: 74 em `tests/test_flow.py` e 9 em
`tests/test_fontes.py`). **H-01 = PASS.** Os 18 warnings são `datetime.utcnow()` e cache do
pytest; nenhum é falha.

Registro do primeiro contato sem o plugin: a coleta e a execução andam, mas os testes de
`tmp_path` dão `E` no setup (11 ocorrências) e a sessão aborta no `pytest_sessionfinish` com
`PermissionError` — **ambiente**, não código. Confirmado que, com a ACL contornada, os mesmos
testes passam.

---

## 3. Os casos do plano

Mapa caso → nó(s) de teste (todos executados a partir do app, com `-q -p no:cacheprovider
-p no_tmp_cleanup --basetemp=$bt`):

| Caso | Nó(s) de teste | Evidência |
|---|---|---|
| F-01/F-02/F-04/H-14 | `test_rf01_f01_f02_f04_h14_jornada` | `1 passed` |
| F-03/F-07 | `test_rf01_f03_f07_recusa_e_reenvio` | `1 passed` |
| F-05/F-09/N-07/H-15 | `test_rf05_f05_f09_n07_snapshot_liberada_imutavel` | `1 passed` |
| F-06 | `test_rf11_f06_contestar_preserva_assinaturas` | `1 passed` — **mas o teste afirma o contrário do plano** |
| F-08/C-01/C-04/C-06 | `test_rf11_f08_c01_c04_c06_diferenca_mostra_texto` | `1 passed` |
| F-09 (delta) | `test_rf05_delta_alterar_preserva_itens_omitidos_e_hash_completo` | `1 passed` |
| F-10 | os três `test_rf08_f10_*` | `3 passed` |
| N-01 | `test_rf07_n01_nao_entra_nao_cria_obra` | `1 passed` (só com cache frio; ver §3.2) |
| N-02 | `test_rf07_n02_depende_importa_mas_nao_libera` | `1 passed` |
| N-03 | `test_rf03_n03_assinatura_incompleta_bloqueia` | `3 passed` |
| N-04 | `test_rf02_n04_papel_incorreto_na_revisao` | `8 passed` |
| N-05 | `test_rf02_n05_papel_incorreto_na_administracao` | `12 passed` |
| N-06 | `test_rf01_n06_transicao_invalida` | `1 passed` |
| N-08 | `test_rf03_n08_hash_esperado_impede_assinar_conteudo_nao_visto` | `2 passed` |
| C-02 | `test_rf03_c02_vetor_canonico_v4`, os `_capitulo_alterado_muda_hash`, os `_adendo_alterado_muda_hash` e `test_rf03_c02_hash_obra_exclui_adendo_ambiente_e_outra_obra` | `8 passed` |
| C-03 | `test_rf11_c03_diferenca_conta_alterados_incluidos_e_removidos` | `1 passed` |
| C-05 | `test_rf07_c05_consulta_fonte_persistida_na_liberacao` | `1 passed` |
| C-07 | `test_rf03_c07_flow_nao_importa_reflex` | `1 passed` |
| C-08 | `test_rf03_c08_json_distingue_campos_com_separadores` | `2 passed` |
| C-09 | `test_rf07_c09_liberar_rele_csv_no_mesmo_caminho`, `test_rf07_c09_fonte_regularizada_libera_sem_limpar_cache` e os dois `test_fontes.py::test_rf07_c09_recarregar_*` | `5 passed` |
| C-10 | os três `test_rf03_c10_*` | `11 passed` |
| H-16 | `test_rf07_n01_nao_entra_nao_cria_obra` + `test_rf07_n02_depende_importa_mas_nao_libera` | `2 passed` (mas o N-01 cai no caso quente; ver §3.2) |

Saída do laço que executou **cada caso separadamente** (é a evidência de que cada linha da
tabela foi um processo pytest próprio):

```text
F-01 | exit=0 | 1 passed in 0.76s      N-04 | exit=0 | 8 passed in 1.21s
F-02 | exit=0 | 1 passed in 0.66s      N-05 | exit=0 | 12 passed in 1.99s
F-03 | exit=0 | 1 passed in 0.91s      N-06 | exit=0 | 1 passed in 0.57s
F-04 | exit=0 | 1 passed in 0.64s      N-07 | exit=0 | 1 passed in 1.25s
F-05 | exit=0 | 1 passed in 0.84s      N-08 | exit=0 | 2 passed in 1.49s
F-06 | exit=0 | 1 passed in 1.36s      C-01 | exit=0 | 1 passed in 0.76s
F-07 | exit=0 | 1 passed in 0.64s      C-02 | exit=0 | 8 passed in 0.99s
F-08 | exit=0 | 1 passed in 0.95s      C-03 | exit=0 | 1 passed in 0.90s
F-09 | exit=0 | 2 passed in 0.61s      C-04 | exit=0 | 1 passed in 0.72s
F-10 | exit=0 | 3 passed in 1.26s      C-05 | exit=0 | 1 passed in 0.97s
N-01 | exit=0 | 1 passed in 0.58s      C-06 | exit=0 | 1 passed in 0.64s
N-02 | exit=0 | 1 passed in 0.89s      C-07 | exit=0 | 1 passed in 0.80s
N-03 | exit=0 | 3 passed in 0.70s      C-08 | exit=0 | 2 passed in 0.53s
                                       C-09 | exit=0 | 5 passed in 1.10s
                                       C-10 | exit=0 | 11 passed in 0.62s
H-14 | exit=0 | 1 passed in 0.82s      H-15 | exit=0 | 1 passed in 0.61s
H-16 | exit=0 | 2 passed in 1.09s
```

### 3.1 F — o fluxo

| ID | Esperado (plano) | Resultado do caso | Evidência |
|---|---|---|---|
| **F-01** | `importar` de `entra`: obra + versão v1 em `em_revisao` | **PASS** | `test_rf01_f01_f02_f04_h14_jornada`: `obra.status == versao.status == "em_revisao"`, `numero == 1`, `fonte_id == "F-001"` |
| **F-02** | `revisar` em `em_revisao` → `aguardando_admin`; parecer + ajustes + `hash_visto` | **PASS** | mesmo teste: `revisor_id`, `revisado_em`, `parecer`, `json.loads(ajustes_propostos)` e `hash_visto == hash_obra` |
| **F-03** | `recusar` → `devolvida` | **PASS** | `test_rf01_f03_f07_recusa_e_reenvio`: `obra.status == versao.status == "devolvida"` |
| **F-04** | `liberar` → `liberada`; `hash_liberado`; `Obra.status`; `versao_liberada_id` | **PASS** | jornada: `obra.status == versao.status == "liberada"`, `versao_liberada_id == versao.id`, `hash_visto == hash_liberado` (sem ajuste) |
| **F-05** | `alterar` numa `liberada`: v N+1 em `em_revisao`; a liberada intacta; `versao_liberada_id` anterior | **PASS** | `test_rf05_f05_f09_n07...`: `nova.numero == 2`, `nova.status == "em_revisao"`, `versao.status == obra.status == "liberada"`, `versao_liberada_id == versao.id` |
| **F-06** | `contestar` numa liberada: **a versão volta a `em_revisao`** (a obra volta a `em_revisao`) | **FAIL** | O teste passa, mas **afirma o oposto**: `nova.id != versao.id`, `nova.numero == 2`, `versao.status == "liberada"`, `obra.versao_liberada_id` inalterado. Ver §3.1.1 |
| **F-07** | `reenviar` numa `devolvida` → `em_revisao`; reenvio registrado | **PASS** | `ajustes_descritos == "Texto corrigido"`, `obra.status == versao.status == "em_revisao"`; evento `reenviada` no F-10 |
| **F-08** | `revisar` cria o instantâneo `visto`; a diferença mostra o **texto** dos dois lados | **PASS** | `test_rf11_f08...`: o registro `visto` tem `conteudo_md == "Original"`; `diferenca(atual=True)` mostra `visto.texto == "Original"` e `liberado.texto == "Ajustado"`; após liberar, `diferenca` é a mesma |
| **F-09** | `alterar` com conteúdo novo: a obra recebe capítulos/adendos; v N+1; a liberada fica | **PASS** | `test_rf05_f05_f09...` e `test_rf05_delta...`; a sonda P3 confirma no banco `capitulo == "Alterado"` e `adendo == "Nova base"`, com os snapshots da v1 ainda `"Original"` |
| **F-10** | cada operação acrescenta um `ObraVersaoEvento`; recusas/reenvios sucessivos no histórico | **PASS** | `test_rf08_f10_eventos_append_only_em_todas_as_operacoes` (7 tipos, cada passo +1, prefixo imutável), `..._operacao_bloqueada_nao_acrescenta_evento` e `..._transacao_do_chamador` |

#### 3.1.1 F-06 — o defeito

O plano é literal: `plano-testes.md` F-06, "`contestar` numa liberada | **a versão volta a
`em_revisao`** (a salvaguarda da ADR-019)"; o `design.md` (v4) repete na tabela do §2:
`contestar(versao, revisor)` | `liberada` → `em_revisao`; a `spec.md` RF11 diz "a **obra** volta
a `em_revisao`".

O código (`gsi_ebd/services/flow.py:304-312`) faz outra coisa:

```python
def contestar(sessao, versao, revisor: User) -> ObraVersao:
    _autor(revisor, Role.REVISOR)
    obra, versao = _estado(sessao, versao, "liberada")
    if obra.versao_liberada_id != versao.id:
        raise FluxoBloqueado("Conteste a versao publicada atual")
    # A assinatura e os instantaneos publicados permanecem como evidencia.
    nova = _nova_versao(sessao, obra, revisor)
    _evento(sessao, nova, "contestada", revisor, versao_anterior_id=versao.id)
    return nova
```

Ele **cria uma versão nova** em `em_revisao` e deixa a contestada `liberada`. E
`_publicar_estado` (`flow.py:129-134`) só atualiza `obra.status` enquanto
`obra.versao_liberada_id is None`; como a versão liberada continua apontada, `Obra.status`
**nunca** volta a `em_revisao`.

Sonda independente (script `.eval-harness/probe.py`, saída real):

```text
== p1_contestar
P1 antes      : ('liberada', 'liberada', 1)
P1 depois     : obra.status='liberada' contestada.status='liberada' versao_liberada_id=1
P1 nova versao: numero=2 status='em_revisao'
P1 eventos    : [(1, 'importada'), (1, 'vista'), (1, 'liberada'), (2, 'contestada')]
```

O teste que passa (`tests/test_flow.py:197-206`) **codifica o desvio**:

```python
nova = flow.contestar(sessao, versao, revisor)
assert nova.id != versao.id and nova.numero == 2 and nova.status == "em_revisao"
assert versao.status == "liberada" and versao.hash_liberado == antes
assert obra.versao_liberada_id == versao.id
```

**Causa:** `contestar` usa `_nova_versao` em vez de fazer a transição da versão contestada, e
`_publicar_estado` não repõe `Obra.status` quando já há `versao_liberada_id`.
**Efeito:** o conteúdo contestado **continua publicado/disponível**; a revisão reabre como uma
versão nova, sem os instantâneos `visto`/`liberado` da contestada; o evento `contestada` fica na
v2, não na versão contestada (a trilha da v1 não mostra a contestação).
**Nota de projeto:** se a intenção fosse manter a liberada disponível durante a revisão (9.2), o
plano precisaria dizer isso para o `contestar` — não diz; e uma transição da mesma versão
colidiria com o `UniqueConstraint(versao_id, momento, ordem)` no segundo `revisar` (o design
precisaria definir como re-snapshotar). De todo modo, o caso F-06 como aprovado **não** se
sustenta.

### 3.2 N — gates e permissões

| ID | Esperado | Resultado | Evidência |
|---|---|---|---|
| **N-01** | `importar` de fonte `nao_entra`: **bloqueado**, a obra não nasce | **FAIL** | O teste passa **só com o cache frio**; com o cache quente, a fonte que o CSV atual marca `nao_entra` é importada (sondas P2/P2b). Ver §3.2.1 |
| **N-02** | `liberar` de fonte `depende`: bloqueado | **PASS** | `pytest.raises(FluxoBloqueado, match="fonte")`; a versão fica `aguardando_admin` e `versao_liberada_id is None` |
| **N-03** | `liberar` sem assinatura: bloqueado | **PASS** | 3 parametrizações (`revisor_id=None`, `revisado_em=None`, `hash_visto=""`); todas bloqueiam com "Assinatura" |
| **N-04** | `revisar`/`recusar` por papel ≠ REVISOR: bloqueado | **PASS** | 8 combinações (2 operações × 4 papéis); estado fica `em_revisao` |
| **N-05** | `importar`/`liberar`/`alterar` por papel ≠ ADMIN: bloqueado | **PASS** | 12 combinações (3 operações × 4 papéis) |
| **N-06** | `liberar` de `em_revisao`: bloqueado | **PASS** | `pytest.raises(..., match="Transicao")` |
| **N-07** | `alterar` depois da liberação não muda a snapshot liberada | **PASS** | `test_rf05_f05_f09_n07...`: a snapshot `liberado` continua `"Original"`/`"Base"` e `hash_liberado` é o mesmo após `commit`/`expire_all` |
| **N-08** | `revisar`/`recusar` com `hash_esperado` diferente: recusado | **PASS** | 2 operações; a mensagem casa "mudou"; a versão fica `em_revisao` e `hash_visto` continua vazio |

#### 3.2.1 N-01 — o defeito do cache no gate de importação

O plano é literal: `plano-testes.md` N-01 / `intent.md` H-16 / ADR-019 §3: a fonte `nao_entra`
**bloqueia a importação**. O `liberar` consulta o inventário **relendo** (`flow.py:234`,
`fonte_decisao(..., recarregar=True)`), mas o `importar` consulta **o cache**
(`flow.py:154`):

```python
if fonte_decisao(fonte) == "nao_entra":      # importar: cache (default)
    raise FluxoBloqueado("A fonte nao entra")
...
if fonte_decisao(obra.fonte_id, recarregar=True) != "entra":   # liberar: leitura fresca
    raise FluxoBloqueado("A fonte nao permite liberacao")
```

O `design.md` L3 é explícito: "o cache serve à exibição, **não ao gate**". Sondas
independentes, com o CSV **atual** dizendo `nao_entra`:

```text
== p2_import_gate_cache
P2 cache frio : entra
P2 decisao atual (recarregar=True): nao_entra
P2 importar   : PASSOU com a decisao atual nao_entra -> obra.id=1 versao=1 status='em_revisao'

== p2b_import_gate_cache_por_importacao
P2b segunda importacao: PASSOU (decisao atual nao_entra) -> obra_b.id=2 versao=1
```

A primeira sonda aquece o cache por uma chamada de exibição (`fonte_decisao("F-001")` com
`entra`), reescreve o CSV para `nao_entra` e importa; a segunda aquece o cache **pela própria
importação** (uma primeira importação de `F-001` com `entra`), reescreve o CSV para `nao_entra`
e importa de novo em outra obra. Nos dois casos a obra nasce — o caso N-01, na acepção do
design, falha.

**Por que o teste passa:** a fixture `fluxo` chama `fontes._carregar.cache_clear()` antes de
cada teste (`tests/test_flow.py:96`), então `test_rf07_n01_nao_entra_nao_cria_obra` cobre
apenas o caminho de cache frio. A mutação M1 (§5) mostra que a linha do gate é load-bearing,
mas não que ela consulta a decisão **atual**.
**Causa:** falta `recarregar=True` no `importar`.
**Efeito:** depois de qualquer aquecimento de cache (a própria importação, uma tela da fatia 2
que exiba o inventário, uma tentativa anterior), uma fonte que virou `nao_entra` é importada;
**H-16** (o portão de importação) não está garantido.
**Correção provável (não feita):** `fonte_decisao(fonte, recarregar=True)` no `importar`, como
no `liberar`.

### 3.3 C — hashes e diferença

| ID | Esperado | Resultado | Evidência |
|---|---|---|---|
| **C-01** | `hash_visto` × `hash_liberado`: iguais sem ajuste; diferentes com ajuste | **PASS** | jornada: `hash_visto == hash_liberado`; F-08: `hash_visto != hash_liberado` |
| **C-02** | canonização determinística; capítulo alterado → hash novo | **PASS** | `test_rf03_c02_vetor_canonico_v4` (vetor v4 com JSON canônico e `v1\n`), os 6 parametrizados de capítulo/adendo e `hash_obra` excluindo adendo de ambiente e outra obra |
| **C-03** | "tamanho do que mudou" conta capítulos/adendos com hash individual diferente | **PASS** | `test_rf11_c03...`: 3 alterados/incluídos/removidos; 0 para iguais; 0 para vazios. **Aviso:** a função não é usada pelo fluxo (só pelos testes) — §6 |
| **C-04** | `itens_visto` derivados × `item_hash` da snapshot liberada: os diferentes são o tamanho | **PASS** | F-08 compara os dois instantâneos por item (`diferenca` devolve item/hash/texto); a versão v4 removeu `itens_visto` do parecer e deriva do instantâneo `visto` (design §1/§3) |
| **C-05** | `fonte_id` persiste; `liberar` consulta a decisão atual | **PASS** | `test_rf07_c05...`: `commit`/`expire_all`, troca do CSV/caminho, `liberar` bloqueia e depois libera; `fonte_id == "F-001"` |
| **C-06** | a diferença da RF11b mostra quais itens e o texto dos dois lados | **PASS** | F-08: `previa[0]["visto"]["texto"] == "Original"`, `previa[0]["liberado"]["texto"] == "Ajustado"`; a diferença é a mesma antes/depois de liberar e após uma edição posterior |
| **C-07** | `services/flow.py` não importa `reflex` | **PASS** | `test_rf03_c07...` (AST) e sonda P6: imports = `collections.abc`, `datetime`, `gsi_ebd.models`, `gsi_ebd.services.fontes`, `hashlib`, `json`, `sqlmodel`, `unicodedata`; nenhum `reflex` |
| **C-08** | canonização com `\|`/aspas/newline: JSON canônico não é ambíguo | **PASS** | `test_rf03_c08...` com `"\|"` e `"\|\\"\n"`; textos diferentes → hashes diferentes |
| **C-09** | `liberar` relê o inventário | **PASS** | 5 testes: CSV no mesmo caminho (`depende`/`nao_entra` bloqueiam; o cache continua `entra`), fonte regularizada libera sem limpar cache, e `fonte_decisao(recarregar=True)` ignora o cache (inclusive CSV inválido) |
| **C-10** | normalização antes do hash: CRLF/LF e NFC/NFD dão o mesmo hash | **PASS** | 11 testes (capítulo: título/conteúdo; adendo: código/título/texto; `hash_obra` com a chave do adendo); sonda P5: `True`/`True` |

### 3.4 H — saúde

| ID | Esperado | Resultado | Evidência |
|---|---|---|---|
| **H-01** | a suíte verde | **PASS** | `211 passed` (§2) |
| **H-14** | o fluxo completo por papel (admin → revisor → admin) | **PASS** | `test_rf01_f01_f02_f04_h14_jornada` (F-01/F-02/F-04) |
| **H-15** | a alteração pós-`liberada` não despublica | **PASS** | `test_rf05_f05_f09_n07...` (F-05/N-07) |
| **H-16** | os dois gates de licença | **FAIL** | o gate de `depende` (N-02/C-09) funciona; o de `nao_entra` na importação usa cache e pode ser burlado (§3.2.1) |

---

## 4. Invariantes no código

| Invariante (briefing) | Onde | Resultado |
|---|---|---|
| as transições são validadas **no serviço** | `_estado` (`flow.py:80-85`) exige o status atual e é chamado por `revisar`, `recusar`, `reenviar`, `liberar` e `contestar`; `_nova_versao` (`137-149`) bloqueia ciclo pendente; `importar`/`alterar` têm os próprios gates | **PASS** (N-06); **exceto** a transição do `contestar` (F-06) |
| `revisar`/`recusar` recusam com `hash_esperado` diferente | `_conferir_visto` (`168-173`), usado por ambos | **PASS** (N-08; mutação M2) |
| `liberar` cria o instantâneo **liberado** | `_congelar(..., "liberado", ...)` (`239`); sonda P4: 1 capítulo + 1 adendo | **PASS** (N-07; mutação M7) |
| `revisar` cria o instantâneo **visto** | `_congelar(..., "visto", ...)` (`183`); sonda P4: 1 + 1 | **PASS** (F-08; mutação M3) |
| `alterar` **não remove** | `alterar` (`254-301`) faz `pop` dos existentes e ignora os omitidos; teste `test_rf05_delta...` preserva os ids 2 e 3 | **PASS** |
| cada operação acrescenta um `ObraVersaoEvento` | `importar` (`164`), `revisar` (`192`), `recusar` (`209`), `reenviar` (`223`), `liberar` (`249`), `alterar` (`300`), `contestar` (`311`); `_evento` (`121-126`) | **PASS** (F-10; mutação M5) |
| `liberar` usa `recarregar=True` | `flow.py:234` | **PASS** (C-09) |
| normalização LF + NFC antes do hash | `_normalizar` (`26-27`), em `_hash_json` (`30-34`) e nas chaves de adendo (`95`, `117`, `331`) | **PASS** (C-10; mutação M4) |
| `flow.py` não importa `reflex` | imports do módulo; teste AST e sonda P6 | **PASS** (C-07) |
| `liberar` exige `revisor_id` + `revisado_em` + `hash_visto` | `flow.py:230-233` | **PASS** (N-03; mutação M6) |
| papéis REVISOR/ADMIN exatos | `exigir_papel` (`21-23`) via `_autor` (`67-70`) | **PASS** (N-04/N-05; mutação M8) |
| `Obra.status` volta a `em_revisao` no `contestar` | `_publicar_estado` (`129-134`) **não** atualiza quando `versao_liberada_id` existe; `contestar` (`304-312`) cria versão nova | **FAIL** (F-06) |
| o gate de importação é a decisão **atual** | `importar` (`154`) usa o cache; `liberar` (`234`) relê | **FAIL** (N-01/H-16) |

---

## 5. Prova de mutação

**Método.** Cópia fiel do commit `8f6608a` (ver §1), com git local. Cada mutação: aplicada no
`gsi_ebd/services/flow.py` da cópia; teste-alvo executado; restaurada com
`git checkout -- gsi_ebd/services/flow.py`; `git status --porcelain` **vazio** e o sha256 do
`flow.py` de volta a `031D02607BB7863CAEF51AF974404F9261F65A292DD15478FCA96E0C285B7AA`.
A cópia de base roda `83 passed` (`test_flow.py` + `test_fontes.py`).

Comando por mutação (exemplo do M1; os demais trocam só a chave e o nó; o interpretador é o da
`.venv` do app, porque a cópia não tem `.venv`):

```powershell
cd C:\Projetos\EM_ESTUDO\EVANGELICOS\.eval-mut\repo
$py = "C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD\.venv\Scripts\python.exe"
$bt = Join-Path $env:TEMP ("gsi-mut-" + [guid]::NewGuid().ToString("N"))
$env:PYTHONPATH = "C:\Projetos\EM_ESTUDO\EVANGELICOS\.eval-harness"
& $py C:\Projetos\EM_ESTUDO\EVANGELICOS\.eval-harness\mutate.py M1
& $py -m pytest -q -p no:cacheprovider -p no_tmp_cleanup `
    tests/test_flow.py::test_rf07_n01_nao_entra_nao_cria_obra --basetemp=$bt
git checkout -- gsi_ebd/services/flow.py
git status --porcelain
```

| # | Mutação (no `flow.py`) | Alvo | Resultado | Restauração |
|---|---|---|---|---|
| **M1** | removido o gate `if fonte_decisao(fonte) == "nao_entra":` (importar) | N-01 | **FAIL** — `DID NOT RAISE FluxoBloqueado`; `1 failed in 1.36s` | `git status` vazio |
| **M2** | removida a checagem `if atual != hash_esperado:` | N-08 | **FAIL** — as 2 parametrizações `DID NOT RAISE`; `2 failed` | vazio |
| **M3** | removido `_congelar(..., "visto", ...)` | F-08 | **FAIL** — `NoResultFound` no `visto`; `1 failed` | vazio |
| **M4** | `_normalizar` passou a `return texto` | C-10 | **FAIL** — `11 failed` (hashes CRLF/LF e NFC/NFD divergem) | vazio |
| **M5** | `_evento` passou a `return None` | F-10 | **FAIL** — `assert 0 == (0 + 1)`; `1 failed` | vazio |
| **M6** | removido `if versao.revisor_id is None:` (liberar) | N-03 | **FAIL** — `[revisor_id-None]` `DID NOT RAISE`; `1 failed, 2 passed` | vazio |
| **M7** | removido `_congelar(..., "liberado", ...)` | N-07 | **FAIL** — `assert 0 == 1` (snapshot liberada); `1 failed` | vazio |
| **M8** | removido `exigir_papel` do `_autor` | N-04/N-05 | **FAIL** — `20 failed` (todas as combinações de papel) | vazio |
| **M9** | removido o gate `if fonte_decisao(..., recarregar=True) != "entra":` (liberar) | N-02/C-09 | **FAIL** — `3 failed` (`depende` e os dois `C-09` do mesmo caminho) | vazio |

As **seis** mutações obrigatórias do briefing/plano (M1 N-01, M2 N-08, M3 F-08, M4 C-10,
M5 F-10 e M6 N-03) foram detectadas; as três extras (M7 N-07, M8 N-04/N-05, M9 N-02/C-09)
também. Trechos reais das saídas:

```text
M1: mutacao aplicada (94 -> 0 chars)
F                                                                        [100%]
E       Failed: DID NOT RAISE FluxoBloqueado
1 failed in 1.36s

M4: mutacao aplicada (88 -> 16 chars)
FFFFFFFFFFF                                                              [100%]
11 failed, 63 deselected in 1.09s

M5: mutacao aplicada (278 -> 69 chars)
E       assert 0 == (0 + 1)
1 failed in 1.35s

M6: mutacao aplicada (96 -> 0 chars)
F..                                                                      [100%]
1 failed, 2 passed in 1.01s

M8: mutacao aplicada (61 -> 28 chars)
FFFFFFFFFFFFFFFFFFFF                                                     [100%]
20 failed in 2.67s
```

---

## 6. Avisos não bloqueantes

1. **O evento `contestada` fica na versão nova, não na contestada** — `contestar` (`flow.py:311`)
   grava em `nova`, com `versao_anterior_id` só no `detalhe`; a trilha da v1 termina em
   `liberada` e não registra a contestação. (Consequência do F-06.)
2. **`substituida` está morto** — o design (v3, §1) lista o status
   `em_revisao|aguardando_admin|devolvida|liberada|substituida`, mas nenhuma operação o usa
   (`grep` em `gsi_ebd/` não acha `substituida`). Depois de liberar uma v2, a v1 continua
   `liberada`; a "atual" só é identificável por `Obra.versao_liberada_id`. Se a intenção é a
   9.2 (as liberadas ficam disponíveis), o status está sobrando; se é marcar a substituída,
   falta a transição.
3. **A RF11a ("tamanho do que mudou") não está ligada ao fluxo** — `tamanho_diferenca`
   (`flow.py:51`) só é chamada pelos testes; `diferenca` (`315`) devolve os itens alterados,
   mas nenhuma operação do fluxo expõe a contagem/tamanho no momento da liberação. A tela da
   fatia 2 precisará chamar as duas; hoje não há caminho de produção.
4. **Fonte ausente levanta `FonteInvalida`, não `FluxoBloqueado`** — `fontes.py:47` levanta
   `FonteInvalida` em `fonte_decisao`; `importar`/`liberar` a deixam propagar. Se a rota só
   tratar `FluxoBloqueado`, isso vira 500 em vez de bloqueio de domínio. Não está no plano
   como caso; o inventário inválido é fail-closed, o que é bom.
5. **`alterar` com `conteudo` malformado** — `conteudo["capitulos"]`, `item["ordem"]` e
   `item["codigo"]` (`flow.py:260-268`) levantam `KeyError`, não `FluxoBloqueado`. Sem teste.
6. **`importar` não valida a base duplicada** — `hash_obra` (`55-60`) deduplica silenciosamente
   no dicionário de `_hash_itens` se houver duas linhas com a mesma `ordem`/código normalizado;
   `_trabalho` (`88-97`) só valida em `revisar`/`liberar`/`alterar`. Uma importação com base
   duplicada cria a v1 e só falha depois, no `revisar`.
7. **A versão nova do `contestar` nasce sem instantâneos** — `diferenca(nova)` antes do novo
   `revisar` devolve todos os itens como "adicionados" (o `visto` está vazio); a visão de
   diferença depois de uma contestação só faz sentido depois de uma nova revisão.
8. **O cache de exibição não é atualizado pelo `recarregar=True`** — `fontes.py:43` relê para o
   gate mas não repopula o `lru_cache`; a exibição pode continuar mostrando a decisão velha
   depois de uma liberação. O design diz que o cache é para exibição; é aceitável, mas a tela
   precisa saber disso.
9. **A snapshot guarda o texto cru, o hash normaliza** — `_congelar` (`100-111`) grava
   `conteudo_md`/`texto` como vieram; `item_hash` usa a normalização. CRLF × LF têm o mesmo
   hash mas textos diferentes; `diferenca` compara hash **e** texto, então uma diferença só de
   formato pode aparecer como alteração de texto. O C-10 exige hash igual; o aviso é para a
   tela de diferença.
10. **Cobertura assimétrica** — os testes não cobrem o cache quente no `importar` (N-01) nem o
    comportamento do F-06 como o plano o descreve; o teste do F-06 **afirma** a versão nova e a
    v1 `liberada`, isto é, transforma o desvio em expectativa. A suíte verde não é prova desses
    dois casos.
11. **Sem migração Alembic nesta fatia** — o design diz que o schema nasce do zero com o
    baseline da v1 (DEM-005); não é falha, mas o deploy da v1 precisa criar as tabelas
    `obraversao`, `obraversaocapitulo`, `obraversaoadendo` e `obraversaoevento` e a FK
    `obra.versao_liberada_id`.

---

## 7. Veredito e números

**Veredito: FAIL.**

- **Suíte:** `211 passed` (H-01), 18 warnings; **83** testes novos (74 + 9).
- **Casos:** 32 (F-01..F-10, N-01..N-08, C-01..C-10, H-01/H-14/H-15/H-16).
  **29 PASS**, **3 FAIL** — **F-06**, **N-01** e, por consequência do N-01, **H-16**.
- **Mutação:** 9 mutações (as 6 obrigatórias + 3 extras), **todas detectadas** (o teste-alvo
  falha), com a cópia restaurada e limpa a cada rodada.
- **Invariantes:** todos os pedidos no briefing estão no código (transições no serviço, os dois
  hashes, os dois instantâneos, o `alterar` sem remover, um evento por operação,
  `recarregar=True` no `liberar`, LF+NFC, `flow.py` sem `reflex`) — **exceto** a transição do
  `contestar` (F-06) e a **frescor** do gate de importação (N-01/H-16).

**Justificativa.** A fatia entrega o essencial e com boa qualidade de testes: o fluxo, os dois
gates no caminho normal, os hashes canônicos e normalizados, os instantâneos, a trilha
append-only, as permissões e a independência do domínio. Mas o EVAL é amarrado ao plano:
F-06 pede que a versão (e a obra) volte a `em_revisao`, e o código mantém a contestada
`liberada` e cria uma v2 — o teste do repositório foi escrito para o comportamento do código,
não para o do plano. E o N-01 exige que a fonte `nao_entra` **não** seja importada; o código
consulta o cache no `importar`, então uma decisão atual `nao_entra` é ignorada quando o cache
está quente. São dois defeitos de contrato, não de estilo; por isso o veredito é **FAIL**, com
a recomendação de o PLANNER decidir o desenho do `contestar` (transição × versão nova, e o que
fazer com a liberada) e de o DEVS trocar `fonte_decisao(fonte)` por
`fonte_decisao(fonte, recarregar=True)` no `importar`.

---

## 8. Resíduos e o que não foi tocado

- **App:** árvore limpa, `HEAD` `8f6608a`, branch `feature/DEM-202610-011-fatia1-dominio`;
  nenhum commit, nenhum `checkout`, nenhuma escrita no app. O `.pytest_cache` do app é
  read-only no sandbox; a suíte rodou com `-p no:cacheprovider`.
- **Harness (fora do app):** `.eval-harness/` (plugin do `tmp_path`, `probe.py`,
  `mutate.py`) e `.eval-mut/` (cópia fiel + git local) foram **removidos** depois do julgamento.
  Sobrou `.eval-basetemp/` na raiz do workspace: diretório criado pela primeira tentativa de
  basetemp, com ACL que nega leitura e remoção (`icacls` e `Directory.Delete` falharam); está
  vazio/inacessível, fora do app e do controle de versão — resíduo de ambiente, não do código.
- **Docs do DEVS:** não li `dev/jornada.md` nem `dev/relatorio.md` (a cegueira). O `git status`
  da raiz mostra `dev/changelog.md`, `dev/jornada.md`, `dev/relatorio.md` e
  `dev/evidencias-mutacao-delta-v4/` alterados/novos **antes** do meu trabalho; não os toquei.
  O `M ESTUDOS_BIBLICOS/GSI_EBD` na raiz é o ponteiro do repo aninhado, também pré-existente.
- **Pytest cache na raiz:** `pytest-cache-files-be8p7ga6/` e o cache da DEM-003 já existiam e
  estão com ACL restrita; não são resíduo meu.
