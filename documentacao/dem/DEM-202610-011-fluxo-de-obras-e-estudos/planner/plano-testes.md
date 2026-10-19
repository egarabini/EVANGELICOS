# Plano de testes — DEM-202610-011 / fatia 1 (domínio)

> Nível 3 (ADR-018). O EVAL é cego e usa o template `documentacao/metodo/templates/briefing-eval.md`
> (com os contornos de ambiente já conhecidos: `python -m pytest`, `--basetemp` fora do app,
> mutação em cópia fiel).

## 1. Funcionais — o fluxo (F)

| ID | Caso | Esperado |
|---|---|---|
| **F-01** | `importar` de fonte `entra` | a obra + a versão v1 nascem em `em_revisao` |
| **F-02** | `revisar` em `em_revisao` | `aguardando_admin`; o parecer + os ajustes + o `hash_visto` gravados |
| **F-03** | `recusar` em `em_revisao` | `devolvida` (o estado `devolvida` existe e é alcançável) |
| **F-04** | `liberar` em `aguardando_admin` | `liberada`; o `hash_liberado`; o `Obra.status`; o `versao_liberada_id` |
| **F-05** | `alterar` numa `liberada` | a versão N+1 em `em_revisao`; a liberada **não** é despublicada; o `versao_liberada_id` continua o anterior |
| **F-06** | `contestar` numa liberada | a **versão contestada** volta a `em_revisao`; a `Obra.status` → `em_revisao`; o `versao_liberada_id` → NULL; **nenhuma versão nova** é criada; o evento `contestada` fica na versão contestada |
| **F-06b** | `liberar` de uma v2 | a `Obra.status` → `liberada`; o `versao_liberada_id` → a v2; a **v1 anterior** → `substituida` |
| **F-07** | `reenviar` numa `devolvida` | o Admin ajusta e a versão volta a `em_revisao` (o reenvio registrado) |
| **F-08** | o instantâneo **visto** | o `revisar` cria a cópia do conteúdo que o Revisor leu; a diferença com o liberado mostra o **texto** de cada item |
| **F-09** | `alterar` com o conteúdo novo | a obra recebe os capítulos/adendos novos e nasce a versão N+1; a liberada fica |
| **F-10** | a trilha imutável | cada operação acrescenta um `ObraVersaoEvento`; a recusa e o reenvio sucessivos ficam no histórico |
| **F-11** | a **rodada de revisão** | após a contestação (ou o reenvio), o `revisar` cria o "visto" da **rodada nova**; a RF11b compara o visto × o liberado da **mesma rodada**; os instantâneos antigos ficam no histórico |

## 2. Gates e permissões (N)

| ID | Caso | Esperado |
|---|---|---|
| **N-01** | `importar` de fonte `nao_entra` | **bloqueado** (a obra não nasce) |
| **N-02** | `liberar` de fonte `depende` | **bloqueado** (a versão não libera) |
| **N-03** | `liberar` sem o Revisor ter assinado | **bloqueado** (o invariante) |
| **N-04** | `revisar`/`recusar` por papel ≠ REVISOR | **bloqueado** |
| **N-05** | `importar`/`liberar`/`alterar` por papel ≠ ADMIN | **bloqueado** |
| **N-06** | `liberar` de uma `em_revisao` (transição inválida) | **bloqueado** |
| **N-07** | alterar a obra **depois** da liberação | a **snapshot da versão liberada não muda** (o conteúdo publicado é o congelado) |
| **N-08** | `revisar`/`recusar` com `hash_esperado` diferente do atual | **recusado** ("o conteúdo mudou desde que você abriu") |

## 3. Hashes e diferença (C)

| ID | Caso | Esperado |
|---|---|---|
| **C-01** | o `hash_visto` × o `hash_liberado` | iguais quando não há ajuste; diferentes quando há |
| **C-02** | a canonização | determinística: a mesma obra → o mesmo hash; um capítulo alterado → hash novo |
| **C-03** | o "tamanho do que mudou" | conta os capítulos/adendos cujo hash individual mudou |
| **C-04** | o C-03 **por item** | o `itens_visto` (o parecer) vs os `item_hash` da snapshot liberada: os itens com hash diferente são o tamanho |
| **C-05** | o `fonte_id` | persiste na `Obra`; o `liberar` consulta a decisão **atual** do inventário |
| **C-06** | a diferença da RF11b | mostra **quais itens** mudaram **e o texto** de cada lado (os dois instantâneos) |
| **C-07** | a independência do domínio | `services/flow.py` **não importa `reflex`** (o teste de grep) |
| **C-08** | a canonização com `\|`/aspas/newline no texto | o **JSON canônico** não é ambíguo (dois textos diferentes → hashes diferentes) |
| **C-09** | o `liberar` relê o inventário | a decisão é a **atual** (mudar o CSV e liberar → o gate usa a nova decisão) |
| **C-10** | a normalização antes do hash | **CRLF e LF dão o mesmo hash**; **NFC e NFD dão o mesmo hash** |

## 4. Saúde (H)

- **H-01** · a suíte verde (o baseline da fatia + os novos)
- **H-14** · o fluxo completo por papel (o teste de jornada)
- **H-15** · a alteração pós-`liberada` não despublica
- **H-16** · os dois gates de licença
- **A prova de mutação**: remover o gate do `nao_entra` → o N-01 falha; remover a checagem do
  `revisor_id` no `liberar` → o N-03 falha; remover a checagem do papel → o N-04 falha; **não criar
  a snapshot no `liberar`** → o N-07 falha.

## 5. Baseline e escopo

| Item | Hoje | Esperado |
|---|---|---|
| o fluxo | não existe (a `Obra` não tem status) | o fluxo completo, testado |
| a assinatura | a ADR-011 não implementada | o par `(revisor_id, revisado_em, hash_visto)` |
| os gates | não existem | os dois, testados + a mutação |
| a suíte | 128 | 128 + os novos |

**Fora desta fatia**: as telas (fatia 2), o `Study` (a fatia seguinte), o `planejar` (a fatia
posterior, a 9.5), o multi-ambiente real (D-06).






