# Jornada do EVAL — DEM-202610-011, fatia 1 (verificação)

> **EVAL cego.** Não sei quem implementou e não procurei saber. Julguei pelo plano aprovado
> (`planner/`), pela **ADR-020**, pelo diff e pelo código.
> **O que foi julgado:** branch `feature/DEM-202610-011-fatia1-dominio`, commit
> `bab117e67ce8c5ed5ae684f0b9cd7483ab9fc5d0` (o PR #4, 5 commits), app em
> `ESTUDOS_BIBLICOS/GSI_EBD`.
> **Data:** 2026-10-19.
> **Veredito: PASS** — 39/39 casos do plano v4 PASS, 269 testes verdes, 9/9 mutações
> detectadas, a distinção editorial × publicação provada e os dois bloqueios da rodada
> anterior (F-06 e N-01) fechados. Os avisos da §7 são não bloqueantes.

---

## 1. Ambiente, escopo e contornos

| Item | Situação |
|---|---|
| cwd | `C:\Projetos\EM_ESTUDO\EVANGELICOS` |
| app | `ESTUDOS_BIBLICOS\GSI_EBD` |
| branch / HEAD | `feature/DEM-202610-011-fatia1-dominio` / `bab117e67ce8c5ed5ae684f0b9cd7483ab9fc5d0` |
| árvore do app | limpa antes e depois (`git status --porcelain` vazio); **não** fiz checkout, commit nem toquei na branch |
| Python | `.venv\Scripts\python.exe` — **3.14.6**; pytest 9.1.0; sqlmodel 0.0.38 |
| `python` do PATH | 3.14.6 **sem** `sqlmodel`; por isso usei o interpretador da `.venv` com `-m pytest` (o briefing pedia `python -m pytest`, não `pytest.exe`) |
| CI | `.github/workflows/ci.yml` roda `python -m pytest tests -q` em **Python 3.12**; o PR #4 está reportado verde. Localmente só há 3.14.6; a suíte foi reproduzida nele (§2) |
| docs do DEVS | **não li** `dev/jornada.md` nem `dev/relatorio.md` (a cegueira). Li o `eval/jornada.md` anterior apenas como artefato do próprio EVAL (formato/histórico), não os docs do DEVS |

**Contorno 1 — o `tmp_path` 0o700 no Windows/sandbox.** A primeira execução, sem contorno,
falhou nos testes que usam `tmp_path` e abortou no `pytest_sessionfinish`:

```text
PermissionError: [WinError 5] Acesso negado:
  'C:\Projetos\EM_ESTUDO\EVANGELICOS\.eval-tmp-basetemp'
```

A causa é de ambiente: `Path.mkdir(mode=0o700)` (usado pelo pytest) cria, neste
Windows/sandbox, um diretório que o próprio processo não consegue enumerar. Só o
`--basetemp` fora do app **não** bastou. Para julgar o **código**, carreguei um
`sitecustomize.py` de harness (`.eval-shim/sitecustomize.py`, via `PYTHONPATH`) que troca
`mode=0o700` por `0o777` no `os.mkdir` em Windows. O shim **não** altera o app nem os
testes; sem ele a suíte não é executável neste ambiente. Com ele, `--basetemp` em `%TEMP%`
e a suíte rodam normalmente.

**Contorno 2 — a cópia fiel para a mutação.** Fiz a cópia com
`git archive --format=zip HEAD` do commit `bab117e`, extraí em `.eval-mut/repo` e
inicializei um git local (`git init` + um commit `snapshot bab117e`). A cópia tem 135
arquivos; o `sha256` do `flow.py` da cópia é
`533640FE7622BBD95D110C780D72501A6947E07812C18D0C48E946BF74E3B216`, **igual** ao do app.
A cópia de base roda `141 passed` (`test_flow.py` + `test_fontes.py`); cada mutação foi
restaurada com `git checkout -- gsi_ebd/services/flow.py`, com `git status --porcelain`
vazio e o sha256 de volta ao original (§6).

**Contorno 3 — o cache do pytest.** O `.pytest_cache` do app é read-only no sandbox; a
suíte final rodou com `-p no:cacheprovider` para não gerar ruído. Sem essa opção, o pytest
emite um `PytestCacheWarning` (ambiente), não uma falha.

**Escopo lido:** `planner/intent.md`, `planner/spec.md` (aprovada), `planner/design.md`
(v7), `planner/plano-testes.md` (v4), a **ADR-020** e a **ADR-019**, o diff
`origin/develop...bab117e` e o código (`flow.py`, `models/obra.py`, testes).

---

## 2. A suíte (H-01)

Comando final (do diretório do app):

```powershell
cd C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD
$env:PYTHONPATH = "C:\Projetos\EM_ESTUDO\EVANGELICOS\.eval-shim"
$bt = Join-Path $env:TEMP ("gsi-verif-" + [guid]::NewGuid().ToString("N"))
.\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --basetemp=$bt
```

Saída:

```text
269 passed, 18 warnings in 24.63s
```

Os **269** são o baseline de 128 + **132** em `tests/test_flow.py` + **9** em
`tests/test_fontes.py`. Os 18 warnings são `datetime.utcnow()` depreciado no código
existente (seed/`user_status_service`) — nenhum é falha. **H-01 = PASS.**

O diff é o esperado para a fatia: 7 arquivos, 1.628 inserções e 1 remoção
(`models/__init__.py`, `models/obra.py`, `services/erros_fluxo.py`, `services/flow.py`,
`services/fontes.py`, `tests/test_flow.py`, `tests/test_fontes.py`), sem alteração fora do
domínio. O commit está 5 commits à frente de `origin/develop`:
`f202eb6`, `8f6608a`, `8c2e1bc`, `27c991b`, `bab117e`.

---

## 3. Os casos do plano (PASS/FAIL)

Todos os grupos abaixo foram executados **em processos pytest próprios**, com
`-q -p no:cacheprovider --tb=line --basetemp=$bt`, a partir do app. O laço que rodou cada
linha separadamente está em §3.5.

### 3.1 F — o fluxo (17 casos)

| ID | Esperado (plano v4) | Resultado | Evidência |
|---|---|---|---|
| **F-01** | `importar` de `entra`: obra + v1 em `em_revisao` | **PASS** | `test_rf01_f01_f02_f04_h14_jornada`: `obra.status == versao.status == "em_revisao"`, `numero == 1`, `fonte_id == "F-001"` |
| **F-02** | `revisar` em `em_revisao` → `aguardando_admin`; parecer + ajustes + `hash_visto` | **PASS** | mesmo teste: `revisor_id`, `revisado_em`, `parecer`, `json.loads(ajustes_propostos)` e `hash_visto == hash_obra` |
| **F-03** | `recusar` em `em_revisao` → `devolvida` | **PASS** | `test_rf01_f03_f07_recusa_e_reenvio`: `obra.status == versao.status == "devolvida"` |
| **F-04** | `liberar` em `aguardando_admin` → `liberada`; `hash_liberado`; `Obra.status`; `versao_liberada_id` | **PASS** | jornada: `obra.status == versao.status == "liberada"`, `versao_liberada_id == versao.id`, `hash_visto == hash_liberado`, `liberada_em`/`admin_id` |
| **F-05** | `alterar` numa `liberada`: N+1 em `em_revisao`; a liberada não despublicada; `versao_liberada_id` anterior | **PASS** | `test_rf05_f05_f09_n07_snapshot_liberada_imutavel`: `nova.numero == 2`, `nova.status == "em_revisao"`, `versao.status == "liberada"`, `obra.versao_liberada_id == versao.id` |
| **F-06** | **a versão nova**: `alterar` cria a N+1 em `em_revisao`; a N fica `liberada` e a snapshot imutável; a disponibilidade → `suspensa_para_novos`; `solicitar_revisao` não muda estado nem disponibilidade; só o Admin abre ciclo | **PASS** | `test_rf11_f06_solicitacao_nao_abre_ciclo_e_so_admin_altera` (4 parametrizações): `len(ObraVersao) == 1` após o pedido; `obra.status == "liberada"`/`disponibilidade == "aberta"` após o pedido; `nova.id != versao.id`, `nova.numero == 2`, `nova.status == "em_revisao"`; `disponibilidade == "suspensa_para_novos"`; `versao_liberada_id == versao.id`; `versao.model_dump() == anterior`; as snapshots existentes após o `alterar` são iguais (a sonda confirma as snapshots da N intactas após `revisar`/`recusar` da N+1); após `revisar`/`recusar` da N+1, publicação e disponibilidade continuam as mesmas; `not hasattr(flow, "contestar")` |
| **F-06b** | `liberar` a N+1: N → `substituida` (continua legível por quem está fixado); disponibilidade → `aberta`; `versao_liberada_id` → N+1 | **PASS** | `test_rf05_f06b_liberar_v2_substitui_v1_e_atualiza_catalogo`: `primeira.status == "substituida"`, `primeira.hash_liberado == original`, `obra.status == segunda.status == "liberada"`, `obra.versao_liberada_id == segunda.id`; a disponibilidade `aberta` é afirmada em F-12 e a leitura da N por quem está fixado em F-14 |
| **F-07** | `reenviar` numa `devolvida` → `em_revisao`, reenvio registrado | **PASS** | `test_rf01_f03_f07_recusa_e_reenvio`: `obra.status == versao.status == "em_revisao"`, `versao.ajustes_descritos == "Texto corrigido"`; evento `reenviada` no F-10 |
| **F-08** | `revisar` cria o instantâneo `visto`; a diferença mostra o **texto** dos dois lados | **PASS** | `test_rf11_f08_c01_c04_c06_diferenca_mostra_texto`: o `visto` tem `conteudo_md == "Original"`; `diferenca(atual=True)` mostra `visto.texto == "Original"` e `liberado.texto == "Ajustado"`; após `liberar`, a diferença é a mesma |
| **F-09** | `alterar` com conteúdo novo: capítulos/adendos novos; N+1; a liberada fica | **PASS** | `test_rf05_f05_f09...` e `test_rf05_delta_alterar_preserva_itens_omitidos_e_hash_completo`: `nova.conteudo_hash == hash_obra`; itens omitidos preservados (ids 2 e 3); a N continua `liberada` |
| **F-10** | cada operação acrescenta um `ObraVersaoEvento`; recusas/reenvios sucessivos no histórico | **PASS** | `test_rf08_f10_eventos_append_only_em_todas_as_operacoes` (7 tipos, cada passo +1, prefixo imutável), `..._operacao_bloqueada_nao_acrescenta_evento` e `..._transacao_do_chamador` — 3 passed. **Ressalva:** o `vincular` não emite `ObraVersaoEvento` (ele grava o `VinculoObra`, com autor/versão/data); ver §7.1 |
| **F-11** | a rodada: após recusa/reenvio, o `revisar` cria o `visto` da rodada nova; a diferença é da **mesma rodada**; snapshots antigos ficam no histórico | **PASS** | `test_rf11_f11_rodada_apos_recusa_reenvio_preserva_historico` (rodada 1→2, diferença da rodada 2, snapshots da 1 intactos), `..._revisao_bloqueada_e_rollback_nao_consumem_rodada` (hash errado não consome rodada; rollback volta a 1) e `..._diferenca_nao_inclui_itens_de_rodadas_antigas` — 3 passed |
| **F-12** | disponibilidade: `alterar`/`aceitar` → `suspensa_para_novos`; `liberar`/`cancelar_ciclo` → `aberta`; `solicitar_revisao` **não** muda | **PASS** | `test_rf12_f12_disponibilidade_so_muda_pelo_admin` (4 combinações `alterar`/`aceitar` × `liberar`/`cancelar`): `solicitar` → `aberta`; abertura → `suspensa`; `revisar` → continua `suspensa`; fechamento → `aberta` |
| **F-13** | a solicitação: `solicitar_revisao` só registra; `aceitar`/`dispensar` (Admin); a dispensa exige motivo | **PASS** | `test_rf13_f13_solicitacao_dispensa_com_motivo_visivel_e_novo_pedido` (motivo `""`/`"  "`/`None` bloqueiam; dispensa com motivo, sem mudar a versão; novo pedido); `..._nao_aceita_pedido_duplicado_ou_ciclo_paralelo`; `..._decisoes_e_pedidos_compartilham_transacao`; `..._f15_decisoes_de_ciclo_exigem_admin` (3 operações × 4 papéis = 12) e `..._f16_pedidos_e_posicoes_exigem_revisor` (2 × 4 = 8) — 23 passed |
| **F-14** | o `versao_id` fixado: o `VinculoObra` fixa a versão; na suspensão, **novas** vinculações bloqueadas e as **existentes** continuam | **PASS** | `test_rf14_f14_vinculo_fixa_versao_e_suspensao_bloqueia_so_novos`: `vinculo.versao_id == original.id`; durante a suspensão, `vincular` levanta "indisponivel" e o vínculo antigo segue `ativo`; após liberar, o novo vínculo fixa a N+1; a snapshot `liberado` da N continua `"Original"`; coordenador de outro ambiente é bloqueado |
| **F-15** | o `cancelar_ciclo`: o Admin descarta a N+1; disponibilidade → `aberta`; a N continua liberada | **PASS** | `test_rf15_f15_cancelar_preserva_evidencias_reabre_e_impede_liberar_descartada`: `nova.status == "cancelada"`, `obra.disponibilidade == "aberta"`, `versao_liberada_id == original.id`, `original.status == "liberada"`, snapshots preservados, evento `ciclo_cancelado`, `liberar(nova)` e segundo `cancelar` bloqueados, e um novo `alterar` cria a próxima versão |
| **F-16** | a posição do Revisor: `posicionar` registra o evento (não bloqueia) | **PASS** | `test_rf16_f16_posicao_nao_bloqueia_decisao_do_admin` (2 posições): `evento.tipo == "posicao"`, autor Revisor, `detalhe["posicao"]` correto, estado (`versao_liberada_id`, `disponibilidade`, status da N+1) inalterado; depois o Admin aprova/libera |

### 3.2 N — gates e permissões (8 casos)

| ID | Esperado | Resultado | Evidência |
|---|---|---|---|
| **N-01** | `importar` de `nao_entra`: **bloqueado** (a obra não nasce) | **PASS** | `test_rf07_n01_nao_entra_nao_cria_obra` (cache frio) **e** `test_rf07_n01_importar_rele_inventario_com_cache_quente` (cache quente: o CSV vira `nao_entra` depois de `fonte_decisao("F-001") == "entra"`; o `importar` relê e bloqueia; sem Obra/Versão/Evento) — 2 passed |
| **N-02** | `liberar` de fonte `depende`: bloqueado | **PASS** | `test_rf07_n02_depende_importa_mas_nao_libera`: o `importar` passa, o `liberar` levanta "fonte"; a versão fica `aguardando_admin` e `versao_liberada_id is None` |
| **N-03** | `liberar` sem assinatura: bloqueado | **PASS** | `test_rf03_n03_assinatura_incompleta_bloqueia`: 3 parametrizações (`revisor_id=None`, `revisado_em=None`, `hash_visto=""`); todas levantam "Assinatura" e a versão fica `aguardando_admin` |
| **N-04** | `revisar`/`recusar` por papel ≠ REVISOR: bloqueado | **PASS** | `test_rf02_n04_papel_incorreto_na_revisao`: 2 operações × 4 papéis = 8; "Papel"; a versão fica `em_revisao` |
| **N-05** | `importar`/`liberar`/`alterar` por papel ≠ ADMIN: bloqueado | **PASS** | `test_rf02_n05_papel_incorreto_na_administracao`: 3 operações × 4 papéis = 12; "Papel" |
| **N-06** | `liberar` de `em_revisao` (transição inválida): bloqueado | **PASS** | `test_rf01_n06_transicao_invalida`: "Transicao" |
| **N-07** | `alterar` depois da liberação: a snapshot da versão liberada não muda | **PASS** | `test_rf05_f05_f09_n07...`: a snapshot `liberado` continua `"Original"`/`"Base"` e `hash_liberado` é o mesmo após `commit`/`expire_all`; a sonda confirma `snapshots_v1_iguais == true` em todo o ciclo |
| **N-08** | `revisar`/`recusar` com `hash_esperado` diferente: recusado | **PASS** | `test_rf03_n08_hash_esperado_impede_assinar_conteudo_nao_visto`: 2 operações; "mudou"; a versão fica `em_revisao` e `hash_visto` vazio |

### 3.3 C — hashes e diferença (10 casos)

| ID | Esperado | Resultado | Evidência |
|---|---|---|---|
| **C-01** | `hash_visto` × `hash_liberado`: iguais sem ajuste; diferentes com ajuste | **PASS** | jornada (`hash_visto == hash_liberado` sem ajuste) + F-08 (`hash_visto != hash_liberado` após ajuste) |
| **C-02** | canonização determinística; capítulo alterado → hash novo | **PASS** | `test_rf03_c02_vetor_canonico_v4` (vetor exato com JSON canônico e `v1\n`), 3 parametrizações de capítulo, 3 de adendo e `test_rf03_c02_hash_obra_exclui_adendo_ambiente_e_outra_obra` — 8 passed |
| **C-03** | "tamanho do que mudou" conta capítulos/adendos com hash individual diferente | **PASS** | `test_rf11_c03_diferenca_conta_alterados_incluidos_e_removidos` (3 alterados/incluídos/removidos; 0 para iguais; 0 para vazios) |
| **C-04** | o C-03 por item: `itens_visto` × `item_hash` da snapshot liberada | **PASS** | F-08 compara os dois instantâneos por item (`diferenca` devolve item/hash/texto); o teste `test_rf03_snapshot_persiste_texto_normalizado_e_hash_recomputavel` confirma `item_hash == hash_capitulo(cap)`/`hash_adendo(nota)` |
| **C-05** | o `fonte_id` persiste na `Obra`; o `liberar` consulta a decisão **atual** | **PASS** | `test_rf07_c05_consulta_fonte_persistida_na_liberacao`: `commit`/`expire_all`, troca do CSV/caminho, o `liberar` bloqueia com `depende` e libera com `entra`; `obra.fonte_id == "F-001"` |
| **C-06** | a diferença da RF11b mostra **quais itens** mudaram **e o texto** dos dois lados | **PASS** | F-08: `previa[0]["visto"]["texto"] == "Original"`, `previa[0]["liberado"]["texto"] == "Ajustado"`; a diferença é a mesma antes/depois de liberar e após uma edição posterior |
| **C-07** | `services/flow.py` **não importa `reflex`** | **PASS** | `test_rf03_c07_flow_nao_importa_reflex` (AST); a inspeção dos imports confirma: `collections.abc`, `hashlib`, `datetime`, `json`, `unicodedata`, `sqlmodel`, `gsi_ebd.models`, `gsi_ebd.services.fontes`, `gsi_ebd.services.erros_fluxo` |
| **C-08** | canonização com `\|`/aspas/newline: o JSON canônico não é ambíguo | **PASS** | `test_rf03_c08_json_distingue_campos_com_separadores`: 2 passed; textos diferentes → hashes diferentes |
| **C-09** | o `liberar` relê o inventário; a decisão é a **atual** | **PASS** | `test_rf07_c09_liberar_rele_csv_no_mesmo_caminho` (2 decisões), `test_rf07_c09_fonte_regularizada_libera_sem_limpar_cache`, e os 2 `test_fontes.py::test_rf07_c09_recarregar_*` — 5 passed |
| **C-10** | a normalização antes do hash: CRLF/LF e NFC/NFD dão o mesmo hash | **PASS** | 11 passed: 4 de capítulo (título/conteúdo × LF/CRLF, NFC/NFD), 6 de adendo (código/título/texto × LF/CRLF, NFC/NFD) e `test_rf03_c10_hash_obra_normaliza_chave_do_adendo` |

### 3.4 H — saúde (4)

| ID | Esperado | Resultado | Evidência |
|---|---|---|---|
| **H-01** | a suíte verde | **PASS** | `269 passed, 18 warnings in 24.63s` (§2) |
| **H-14** | o fluxo completo por papel (admin → revisor → admin) | **PASS** | `test_rf01_f01_f02_f04_h14_jornada` (F-01/F-02/F-04) |
| **H-15** | a alteração pós-`liberada` não despublica | **PASS** | `test_rf05_f05_f09_n07...` (F-05/N-07) |
| **H-16** | os dois gates de licença | **PASS** | N-01 (cache frio **e** quente) + N-02; M6 prova que o `recarregar=True` do `importar` é load-bearing |

### 3.5 Execução separada por caso (evidência)

Cada linha abaixo foi um processo pytest próprio (exit 0). O comando por linha foi:

```powershell
& .\.venv\Scripts\python.exe -m pytest -q -p no:cacheprovider --tb=line `
    --basetemp=$bt $nos
```

```text
Grupo                    Exit  Saída
F-01/02/04/H-14            0    1 passed in 0.62s
F-03/07                    0    1 passed in 0.94s
F-05/09/N-07/H-15          0    1 passed in 0.70s
F-06                       0    4 passed in 1.29s
F-06b                      0    1 passed in 0.77s
F-08/C-01/C-04/C-06        0    1 passed in 0.76s
F-09-delta                 0    1 passed in 1.16s
F-10                       0    3 passed in 0.77s
F-11                       0    3 passed in 1.07s
F-12                       0    4 passed in 0.89s
F-13                       0   23 passed in 1.87s
F-14                       0    1 passed in 1.02s
F-15                       0    1 passed in 0.80s
F-16                       0    2 passed in 0.88s
N-01                       0    2 passed in 0.90s
N-02                       0    1 passed in 0.62s
N-03                       0    3 passed in 1.22s
N-04                       0    8 passed in 0.86s
N-05                       0   12 passed in 1.67s
N-06                       0    1 passed in 0.60s
N-08                       0    2 passed in 0.99s
C-02                       0    8 passed in 0.82s
C-03                       0    1 passed in 0.55s
C-05                       0    1 passed in 1.22s
C-07                       0    1 passed in 0.62s
C-08                       0    2 passed in 1.05s
C-09                       0    5 passed in 0.85s
C-10                       0   11 passed in 1.03s
```

**Números dos casos:** **39** casos (17 F, 8 N, 10 C, 4 H) — **39 PASS, 0 FAIL.**

---

## 4. A distinção editorial × publicação (a prova)

### 4.1 A regra (ADR-020)

| Estado | Quem move | No código |
|---|---|---|
| **Editorial** (da **versão**, dentro do ciclo): `em_revisao` → `aguardando_admin` (parecer) ou → `devolvida` (recusa) | **Revisor** | `revisar` (`flow.py:175-193`) e `recusar` (`196-210`) mudam `versao.status` e espelham em `Obra.status` via `_publicar_estado` (`129-133`) |
| **De publicação** (a `Obra`): a `versao_liberada_id` | **só o Admin** | `liberar` (`227-257`) é o único caminho que atribui `obra.versao_liberada_id` (`252`); `alterar`/`aceitar`/`cancelar`/`solicitar`/`dispensar`/`revisar`/`recusar` não |
| **De disponibilidade** (a `Obra`): `aberta` / `suspensa_para_novos` | **só o Admin** | `_suspender` (`318-323`) no `alterar` (`287`) e no `aceitar` (`356`); `aberta` no `liberar` (`251`) e no `cancelar` (`389`); `revisar`/`recusar`/`solicitar`/`dispensar` não tocam |

### 4.2 A sonda independente

Script `.eval-harness/probe_semantica.py` (fora do app; SQLite em memória, inventário
temporário). Saída real, recortada:

```text
importar             : obra.status=em_revisao    disp=aberta  versao_liberada_id=None
revisar_v1           : obra.status=aguardando_admin disp=aberta versao_liberada_id=None
liberar_v1           : obra.status=liberada      disp=aberta  versao_liberada_id=1
solicitar_revisao    : obra.status=liberada      disp=aberta  versao_liberada_id=1  snapshots_v1_iguais=true
alterar_N1           : v2.id=2 numero=2 status=em_revisao
                       v1.status=liberada        disp=suspensa_para_novos
                       versao_liberada_id=1      snapshots_v1_iguais=true
revisar_v2           : v2.status=aguardando_admin v1.status=liberada
                       disp=suspensa_para_novos  versao_liberada_id=1
recusar_v2           : v2.status=devolvida        v1.status=liberada
                       disp=suspensa_para_novos  versao_liberada_id=1
liberar_v2           : v2.status=liberada         v1.status=substituida
                       disp=aberta               versao_liberada_id=2
                       snapshots_v1_iguais=true  (a N continua legível)
vincular_suspensao   : vinculo.versao_id=2 ativo=true
                       novo vinculo bloqueado: "Obra indisponivel para novas vinculacoes"
cancelar_ciclo       : v3.status=cancelada        v2.status=liberada
                       disp=aberta               versao_liberada_id=2
posicionar           : evento tipo=posicao        obra.status=liberada disp=aberta versao_liberada_id=2
```

O que a sonda prova, sem depender dos testes:

1. o `revisar`/`recusar` **nunca** mudam `versao_liberada_id` nem `disponibilidade` (o
   `revisar` v1 acontece com a disponibilidade `aberta` e ela continua `aberta`);
2. o `solicitar_revisao` **só** grava o evento: a obra, a versão e as snapshots ficam
   idênticas;
3. o `alterar` (Admin) cria um **registro novo** (id 2, número 2) e a N continua
   `liberada`; a disponibilidade vira `suspensa_para_novos`; as snapshots da N ficam
   **iguais**;
4. o `revisar`/`recusar` da N+1 movem o estado **editorial** da N+1 e deixam a N
   publicada e a disponibilidade suspensa;
5. o `liberar` da N+1 marca a N como `substituida`, atualiza `versao_liberada_id` e
   reabre para novos; a N continua legível (snapshots intactas);
6. o `cancelar_ciclo` descarta a N+1 (status `cancelada`), mantém a N publicada e reabre;
7. o `vincular` fixa a versão e a suspensão bloqueia só **novos** vínculos;
8. o `posicionar` não muda nenhum estado.

### 4.3 Onde o código garante

- `_estado` (`flow.py:77-82`) valida a transição **no serviço** (`em_revisao`,
  `aguardando_admin`, `devolvida`, `liberada`); o `revisar`/`recusar` só aceitam
  `em_revisao` (o `recusar` também `aguardando_admin`); o `liberar` só `aguardando_admin`.
- `_conferir_visto` (`167-172`) recalcula o hash do conteúdo atual e recusa se ≠
  `hash_esperado` ("O conteudo mudou desde que voce abriu") — o N-08.
- `_congelar` (`97-109`) grava a snapshot com o momento (`visto`/`liberado`), a rodada e o
  `item_hash`; o `revisar` chama `_congelar(..., "visto", ...)` (`183`); o `liberar`,
  `_congelar(..., "liberado", ...)` (`239`).
- `liberar` (`227-257`) é o único que atribui `obra.versao_liberada_id` (`252`) e
  `obra.disponibilidade = "aberta"` (`251`); exige `revisor_id` + `revisado_em` +
  `hash_visto` (`230-233`); relê o inventário (`234`).
- `alterar` (`260-315`) cria a N+1 (`_nova_versao`, `136-148`), suspende (`287`), atualiza
  a base preservando as identidades dos itens existentes (`288-309` — omitir não remove) e
  grava o evento `alterada` com `versao_anterior_id` (`314`).
- `_suspender` (`318-323`) é o único lugar que grava `suspensa_para_novos`; é chamado só
  pelo `alterar` (`287`) e pelo `aceitar` (`356`).
- `solicitar_revisao` (`339-346`) só grava o evento `revisao_solicitada`; `dispensar`
  (`362-371`) só grava `solicitacao_dispensada` (com motivo); nenhum dos dois toca a obra.
- `cancelar_ciclo` (`374-393`) marca a versão pendente como `cancelada`, mantém
  `versao_liberada_id` e grava `ciclo_cancelado`; não libera a versão cancelada.
- `vincular` (`405-420`) exige `disponibilidade == "aberta"` e a versão publicada
  `liberada`; grava `VinculoObra` com `versao_id` fixo.

---

## 5. Invariantes no código

| Invariante (briefing) | Onde | Resultado |
|---|---|---|
| as transições são validadas **no serviço** (não no template) | `_estado` (`flow.py:77-82`), `_nova_versao` (`136-148`) e os gates de `importar`/`alterar`/`cancelar`; não há template nesta fatia | **PASS** (N-06) |
| `revisar`/`recusar` recusam com `hash_esperado` diferente | `_conferir_visto` (`167-172`), usado por ambos | **PASS** (N-08) |
| `liberar` cria o instantâneo **liberado** | `_congelar(..., "liberado", ...)` (`239`) | **PASS** (N-07; M7) |
| `revisar` cria o instantâneo **visto** | `_congelar(..., "visto", ...)` (`183`) | **PASS** (F-08; M9) |
| `alterar` **não remove** | `alterar` (`288-309`): `pop` dos existentes e omissão preservada; teste delta | **PASS** |
| cada operação acrescenta um `ObraVersaoEvento` | `_evento` (`119-126`) em `importar` (`163`), `revisar` (`192`), `recusar` (`209`), `reenviar` (`223`), `liberar` (`254`), `alterar` (`314`), `solicitar` (`346`), `aceitar` (`357`), `dispensar` (`370`), `cancelar` (`392`), `posicionar` (`402`) — **11 de 12**; o `vincular` (`405-420`) grava `VinculoObra`, não `ObraVersaoEvento` | **PASS com ressalva** (§7.1) |
| `liberar` usa `recarregar=True` | `flow.py:234` | **PASS** (C-09; M6 no `importar`) |
| a normalização (LF + NFC) antes do hash | `_normalizar` (`23-24`), `_hash_json` (`28`), `_congelar` (`100-108`), `_hash_itens` (`113-116`) | **PASS** (C-10; M4) |
| `flow.py` **não importa `reflex`** | imports do módulo; teste AST | **PASS** (C-07) |
| `liberar` exige `revisor_id` + `revisado_em` + `hash_visto` | `flow.py:230-233` | **PASS** (N-03; M8) |
| papéis REVISOR/ADMIN exatos | `exigir_papel` (`18-20`) via `_autor` (`64-67`) | **PASS** (N-04/N-05; M1) |
| o Revisor não muda a publicação nem a disponibilidade | `revisar`/`recusar` não tocam `obra.versao_liberada_id`/`obra.disponibilidade`; sonda §4.2 | **PASS** (F-06; M3) |
| a N liberada é imutável e todo ciclo cria a N+1 | `alterar`/`aceitar` via `_nova_versao`; snapshots por versão; `liberar` marca a anterior `substituida` (`246-249`); sonda §4.2 | **PASS** (F-05/F-06/F-06b/N-07) |
| a disponibilidade é `aberta`/`suspensa_para_novos` e só o Admin a move | `_suspender` (`318-323`), `liberar` (`251`), `cancelar` (`389`); `solicitar`/`dispensar` não | **PASS** (F-12) |
| `contestar` foi substituído por `solicitar_revisao` + aceitar/dispensar | não existe `contestar` em `gsi_ebd/` (grep); `solicitar`/`aceitar`/`dispensar` em `flow.py:339-371` | **PASS** (F-06/F-13) |

---

## 6. Prova de mutação

**Método.** Cópia fiel do commit `bab117e` (§1), com git local. Cada mutação foi aplicada
em `gsi_ebd/services/flow.py` da cópia, o teste-alvo rodado, e a cópia restaurada com
`git checkout -- gsi_ebd/services/flow.py`; `git status --porcelain` e o sha256 do
`flow.py` foram conferidos após **cada** rodada. A cópia de base roda `141 passed`
(`test_flow.py` + `test_fontes.py`).

Comando por mutação (exemplo do M1; os demais trocam a chave e o nó):

```powershell
cd C:\Projetos\EM_ESTUDO\EVANGELICOS\.eval-mut\repo
$py = "C:\Projetos\EM_ESTUDO\EVANGELICOS\ESTUDOS_BIBLICOS\GSI_EBD\.venv\Scripts\python.exe"
& $py C:\Projetos\EM_ESTUDO\EVANGELICOS\.eval-harness\mutate.py M1
& $py -m pytest -q -p no:cacheprovider --tb=line --basetemp=$bt `
    tests/test_flow.py::test_rf11_f06_solicitacao_nao_abre_ciclo_e_so_admin_altera
git checkout -- gsi_ebd/services/flow.py
git status --porcelain
```

| # | Mutação no `flow.py` | Alvo | Resultado | Restauração |
|---|---|---|---|---|
| **M1** | removido `_autor(admin, Role.ADMIN)` do `alterar` | F-06 | **FAIL** — `Failed: DID NOT RAISE FluxoBloqueado` (test_flow.py:216); `4 failed` | `git status` vazio; sha OK |
| **M2** | removida a linha `obra.disponibilidade = "suspensa_para_novos"` do `_suspender` | F-12 | **FAIL** — `AssertionError: assert 'aberta' == 'suspensa_para_novos'` (test_flow.py:796); `4 failed` | vazio; sha OK |
| **M3** | o `revisar` passou a gravar `obra.versao_liberada_id = versao.id` (vazamento editorial → publicação) | F-06 | **FAIL** — `AssertionError: assert 2 == 1` (test_flow.py:229); `4 failed` | vazio; sha OK |
| **M4** | `_normalizar` passou a `return texto` (sem LF/NFC) | C-10 | **FAIL** — hashes CRLF/LF e NFC/NFD divergem (test_flow.py:401/412); `11 failed` | vazio; sha OK |
| **M5** | removido o `_evento(..., "vista", ...)` do `revisar` | F-10 | **FAIL** — `assert 5 == (5 + 1)` (test_flow.py:468); `2 failed, 1 passed` | vazio; sha OK |
| **M6** | `importar` voltou a `fonte_decisao(fonte)` (cache) | N-01 | **FAIL** — `Failed: DID NOT RAISE FluxoBloqueado` no caso de cache quente (test_flow.py:560); `1 failed, 1 passed` | vazio; sha OK |
| **M7** | removido `_congelar(..., "liberado", ...)` do `liberar` | N-07 (extra) | **FAIL** — `assert 0 == 1` (test_flow.py:183); `1 failed` | vazio; sha OK |
| **M8** | removida a checagem `if versao.revisor_id is None` do `liberar` | N-03 (extra) | **FAIL** — `DID NOT RAISE` em `[revisor_id-None]` (test_flow.py:294); `1 failed, 2 passed` | vazio; sha OK |
| **M9** | removido `_congelar(..., "visto", ...)` do `revisar` | F-08 (extra) | **FAIL** — `sqlalchemy.exc.NoResultFound` no `visto`; `1 failed` | vazio; sha OK |

As **seis** mutações obrigatórias (M1 F-06, M2 F-12, M3 F-06, M4 C-10, M5 F-10, M6 N-01)
foram detectadas; as três extras (M7 N-07, M8 N-03, M9 F-08) também. Trechos reais:

```text
M1  Failed: DID NOT RAISE FluxoBloqueado   (4 failed)
M2  assert 'aberta' == 'suspensa_para_novos' (4 failed)
M3  assert 2 == 1                          (4 failed)
M4  assert '5b57904ce75d...' == '589a5dd817f3...' (11 failed)
M5  assert 5 == (5 + 1)                    (2 failed, 1 passed)
M6  Failed: DID NOT RAISE FluxoBloqueado   (1 failed, 1 passed)
M7  assert 0 == 1                          (1 failed)
M8  Failed: DID NOT RAISE FluxoBloqueado   (1 failed, 2 passed)
M9  NoResultFound                          (1 failed)
```

**Leitura:** sem o Admin no `alterar` o F-06 falha (M1); sem a suspensão o F-12 falha
(M2); quando o `revisar` mexe na publicação o F-06 falha (M3); sem a normalização o C-10
falha (M4); sem o evento o F-10 falha (M5); sem o `recarregar=True` no `importar` o N-01
falha no cache quente (M6). A regressão está coberta.

---

## 7. Avisos não bloqueantes

1. **`vincular` não emite `ObraVersaoEvento`.** O invariante literal "cada operação
   acrescenta um `ObraVersaoEvento`" vale para 11 das 12 operações; o `vincular`
   (`flow.py:405-420`) grava o `VinculoObra` (com `coordenador_id`, `versao_id` e
   `created_at`), que é a trilha própria da vinculação, mas não um evento na versão. O
   F-10 não testa `vincular`; o design v7 não define um tipo de evento para ele. Se a
   intenção for literal, falta o evento; se não, o invariante deve ser reescrito. **Não
   bloqueia** os casos julgados.
2. **`desvincular` e o adendo do ambiente.** A spec aprovada (RF06/§10) diz que esta fatia
   cobre "vincular/desvincular e o adendo do ambiente"; o design v7 (o plano julgado) tem
   só `vincular` e o campo `Adendo.ambiente_id`, sem `desvincular` e sem `adendar`
   (`flow.py` não tem essas operações), e o plano v4 não tem caso para elas. É uma
   **divergência de escopo entre a spec e o design v7**, não um FAIL dos casos julgados;
   o PLANNER deve reconciliar (incluir na fatia 2 ou registrar o adiamento).
3. **O ciclo de vida da solicitação pendente.** Um `solicitar_revisao` pode ser criado
   enquanto já há um ciclo aberto na N ainda publicada; ele sobrevive a um `alterar` ou a
   um `cancelar_ciclo`, e um `aceitar` posterior pode abrir uma N+2 "extra" a partir de um
   pedido antigo. O plano não testa esse caminho; vale definir se o pedido deve ser
   bloqueado/consumido quando o ciclo abre ou fecha.
4. **O `conteudo_hash` do `importar` é o do instante da criação.** No fluxo de teste, os
   capítulos/adendos são acrescentados depois do `importar`; o `importar` calcula
   `conteudo_hash` em `flow.py:143` antes de o chamador anexar a base, então até o primeiro
   `revisar` ele é o hash da base vazia (a sonda mostra `hash_visto` vazio antes do
   `revisar`). Se uma tela/auditoria ler o hash imediatamente após a importação, verá um
   valor defasado; documente a ordem ou recompute após anexar a base.
5. **O `recusar` atualiza `hash_visto` mas não cria um novo `visto`.** Se o conteúdo mudou
   entre a revisão e a recusa, o `hash_visto` é o atual, mas a snapshot `visto` da rodada
   continua a da revisão anterior; a diferença da rodada corrente usa a snapshot antiga.
   O F-03/F-11 não cobrem esse intervalo. Não bloqueia.
6. **A prévia `diferenca(atual=True)` usa o texto cru da base.** As snapshots são
   normalizadas (bom), mas o lado "liberado" da prévia vem de `_trabalho`, sem
   normalização; uma mudança só de CRLF/NFD tem o mesmo hash e pode aparecer como
   diferença de texto na prévia. O C-10 prova os hashes, não a prévia.
7. **Sem migração Alembic nesta fatia e FK circular.** Não há `alembic/versions` no diff;
   `Obra.versao_liberada_id` referencia `obraversao.id` e `ObraVersao.obra_id` referencia
   `obra.id` — o baseline da v1 (DEM-005) precisa criar as tabelas e resolver a circular
   (o SQLite dos testes aceita; o Postgres do deploy pode exigir `use_alter`). O design §7
   prevê o banco próprio da v1; é deploy, não falha de domínio.
8. **O `importar` não valida base duplicada.** `hash_obra` deduplica silenciosamente no
   dicionário se houver duas linhas com a mesma `ordem`/código normalizado; a validação
   (`_trabalho`) só ocorre em `revisar`/`recusar`/`liberar`/`alterar`. Uma importação com
   base duplicada cria a v1 e só falha depois. Não está no plano; é robustez.
9. **O cache de exibição do inventário não é atualizado pelo `recarregar=True`.** O gate
   relê (`importar`/`liberar`), mas o `lru_cache` de exibição pode continuar mostrando a
   decisão velha depois de uma liberação. O design diz que o cache serve à exibição; a tela
   da fatia 2 precisa saber disso.
10. **Robustez de teste:** o F-06 compara `select(...).all()` sem `order_by` (linhas 208-209
    e 225-226); a ordem física não é garantida por SQL. No SQLite passa; em outro banco
    pode ficar frágil. Trocar por `order_by` explícito é barato.
11. **Ambiente/CI:** o CI roda em Python 3.12; a verificação local foi em 3.14.6 (a `.venv`
    do app), com 18 warnings de `datetime.utcnow()` (código pré-existente). O PR #4 está
    reportado verde no CI; não houve 3.12 local para reproduzir. O `.pytest_cache` do app é
    read-only no sandbox (por isso `-p no:cacheprovider`).

---

## 8. Veredito e números

**Veredito: PASS.**

- **Suíte:** `269 passed` (H-01), 18 warnings; 132 em `test_flow.py` + 9 em
  `test_fontes.py` + 128 do baseline.
- **Casos:** **39** (17 F, 8 N, 10 C, 4 H) — **39 PASS, 0 FAIL**. O F-06 é a versão nova
  (N+1; a N intacta; só o Admin abre; a solicitação não muda nada) e o F-06b/F-12..F-16
  estão cobertos. O N-01 cobre **cache frio e quente**.
- **Mutação:** 9 mutações (6 obrigatórias + 3 extras), **9/9 detectadas**; a cópia foi
  restaurada e conferida (status vazio + sha256) a cada rodada.
- **Invariantes:** transições no serviço, `hash_esperado`, os dois instantâneos, o
  `alterar` sem remover, um evento por operação (com a ressalva do `vincular`), o
  `recarregar=True` nos dois gates, LF+NFC, `flow.py` sem `reflex`, a assinatura do
  Revisor, os papéis e a distinção editorial × publicação — **todos no código**.
- **Os dois bloqueios da rodada anterior estão fechados:** o `importar` relê o inventário
  (`flow.py:153`; N-01 quente + M6) e o F-06 segue a **ADR-020** (o `alterar` cria a N+1;
  a N fica `liberada`/imutável; a publicação e a disponibilidade são só do Admin; o
  `solicitar_revisao` não muda nada; o `contestar` não existe).

**Justificativa.** O domínio entrega o que o plano v4 e a ADR-020 pedem, com testes que
não codificam desvios: a suíte verde é acompanhada dos 39 casos executados
individualmente, da sonda independente que separa os três estados (editorial, publicação,
disponibilidade) e das nove mutações que derrubam os testes certos. Os avisos da §7 são de
escopo/traceabilidade (notadamente `desvincular`/`adendar` e o evento do `vincular`),
robustez e ambiente; nenhum é um defeito de contrato nos casos julgados. Por isso o
veredito é **PASS**, com os avisos registrados para o PLANNER.

---

## 9. Resíduos e o que não foi tocado

- **App:** árvore limpa, `HEAD` `bab117e67ce8c5ed5ae684f0b9cd7483ab9fc5d0`, branch
  `feature/DEM-202610-011-fatia1-dominio`; **nenhum** commit, `checkout` ou escrita no
  app. O `.pytest_cache` do app é read-only no sandbox; a suíte rodou com
  `-p no:cacheprovider`.
- **Harness (fora do app):** `.eval-harness/` (sonda, mutador, logs), `.eval-mut/` (cópia
  fiel + git local) e `.eval-shim/` (o `sitecustomize.py` do `tmp_path`) foram
  **removidos** depois do julgamento; os logs foram usados para as citações acima.
- **Resíduos de ambiente:** `.eval-basetemp/` (da rodada anterior), `.eval-tmp-b2/`,
  `.eval-tmp-basetemp/` e `eval-tmp-py700/` ficaram **inacessíveis** (criados com
  `mode=0o700` antes do shim; nem `icacls`/`Remove-Item` os leem). Estão **fora do app**,
  não são versionados e são resíduo de ambiente, não do código. `.eval-basetemp-v/`,
  `eval-tmp-normal/`, `eval-tmp-shimtest/`, `.acl-test-1/`, `.hidden-normal/` e os dois
  `.log` foram removidos.
- **Raiz do workspace:** o `git status` da raiz mostra `M ESTUDOS_BIBLICOS/GSI_EBD`
  (ponteiro do repo aninhado) e `M .../dev/changelog.md`, `dev/jornada.md`,
  `dev/relatorio.md` + `?? dev/evidencias-mutacao-v7/` **pré-existentes**; não os toquei e
  **não li** `dev/jornada.md` nem `dev/relatorio.md`.
- **Docs do DEVS:** não lidos (a cegueira). A única leitura de `eval/` foi a jornada
  anterior, substituída por esta.
