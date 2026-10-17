# Jornada EVAL — DEM-202610-003 / inventário de fontes

- **Agente:** EVAL (cego e independente; não escreveu o artefato)
- **Data:** 2026-10-17
- **DEM:** DEM-202610-003
- **Hash do artefato:** `2960a70fecd025cee362e8917a766be224d9c169`
- **Branch:** `feature/DEM-202610-003-inventario-de-fontes`
- **Artefato:** `documentacao/fontes/inventario.csv` · `documentacao/fontes/verificar_inventario.py` · `documentacao/fontes/README.md`
- **Réguas:** `planner/intent.md` (signed) · `planner/spec.md` (Anexo A) · `planner/plano-testes.md`
- **Ambiente:** Windows, repositório local; `C:\Python314\python.exe` para o verificador; `.venv` do `GSI_EBD` para o pytest (o Python global não tem as dependências do projeto).

## Veredito

```
hash: 2960a70fecd025cee362e8917a766be224d9c169
F: FAIL · H: PASS · C: PASS · N: PASS · G: N-A (ARQUITECT)
agregado: FAIL
```

**FAILs:** F-01 (CA01: colunas obrigatórias vazias em 7+2 linhas) e F-04 (regime `curto` em 4 linhas com licença `a confirmar`, contra a spec §6.1). O verificador do autor passa; ele não cobre nenhum dos dois pontos.

## Evidência por caso

| Caso | Status | Evidência |
|---|---|---|
| F-01 | **FAIL** | Estrutura OK: bytes iniciais `EF BB BF`, cabeçalho com 17 colunas na ordem, 80 linhas físicas (1 cabeçalho + 79 dados), **todas as 79 linhas com exatamente 17 campos**, nenhuma linha vazia. **CA01 falha:** `atribuicao_exigida` vazia em F-068, F-069, F-070, F-071, F-072, F-078, F-079 (7 linhas) e `localizacao` vazia em F-078, F-079 (2 linhas) — ambas marcadas `Obrigatório: sim` na spec §4. O verificador do autor não testa campos obrigatórios. |
| F-02 | PASS | Extração independente do `DATA_LICENSES.md` §2 (regex sobre as tabelas, sem usar a lista do verificador): **46 ids**. CSV: **46 linhas** `Sensus — <id>: ...` (F-012..F-057), sem duplicata, sem id faltando, sem id extra; conjunto igual e mesma ordem. |
| F-03 | PASS | **12 linhas** com `licenca = a confirmar` (F-001, F-002, F-027, F-063, F-068, F-069, F-070, F-071, F-072, F-074, F-078, F-079). Todas têm o quê (licença/titular), com quem (`junto a/ao ...`) e quando (`antes de ...`). Nenhum gatilho incompleto. |
| F-04 | **FAIL** | Todos os valores pertencem ao conjunto, mas **F-002, F-027, F-063 e F-074** têm `licenca = a confirmar` e `regime_exibicao = curto`. A spec §6.1 diz que `curto` exige licença que **permite** exibir trecho curto e que `integral_interno` cobre "licença a confirmar"; a precedência manda usar o mais restritivo. O próprio `observacoes` dessas linhas diz "antes de qualquer exibição ao usuário", o que contradiz `curto`. F-001 é a exceção do ACF (ADR-012 10.10, "citação hoje"), não contada. |
| F-05 | PASS | `decisao` ∈ {entra, nao_entra, depende}: 59 `entra`, 5 `depende`, 15 `nao_entra`. **Todas as 20 linhas com decisão ≠ `entra` têm `motivo` não vazio.** Observação: F-024 (RWP) é `depende` com licença não comercial declarada; tensão com §6.2/ADR 10.4, registrada em H-03. |
| F-06 | PASS | 12 decisões da ADR-012 conferidas; **0 contradição direta**. Uma tensão registrada (F-024, ver tabela abaixo). |
| F-07 | PASS | `adequacao_doutrinaria` preenchida em 79/79: `ok` 58, `atencao` 16, `fora` 5, `a_revisar` 0. `revisado_por`/`revisado_em` vazios em 79/79 = pendência de revisão do ARQUITECT, como a spec §4 e o README descrevem. |
| F-08 | PASS | Fontes internas e externas no mesmo arquivo: F-007, F-008, F-009, F-010 em `ESTUDOS_BIBLICOS`; 79 linhas no total, 55 `fonte_dados`, 11 `conteudo`, 3 `codigo`, 5 `ferramenta`, 2 `obra`, 1 `corpus`, 1 `referencia_cruzada`, 1 `adendo`. |
| F-09 | PASS | Os três arquivos existem nos caminhos declarados: `documentacao/fontes/inventario.csv`, `.../README.md`, `.../verificar_inventario.py`. Observação: o README (54 linhas) explica manutenção e critérios, mas **não traz o dicionário das 17 colunas** que o RF09 pede ("explicando colunas"); e a tabela "Pendências" diz que F-004/F-007/F-008 estão `a confirmar`, enquanto o CSV as marca `direito reservado`. Não é caso do plano; fica registrado. |
| F-10 | PASS | As **12 exclusões do RF10** existem com `decisao = nao_entra` e `motivo` não vazio: F-011 (código Sensus), F-060 (deuterocanônicos), F-068 (lff), F-069 (lff-en), F-070 (lffe), F-071 (sangue), F-072 (LaTeX), F-073 (código biblia-plataforma), F-076 (jesus-cristo), F-077 (mapas), F-078 (Jev), F-079 (Laya). O plano diz "13 exclusões", mas o RF10 da spec enumera 12; usei a lista fechada da spec (o próprio verificador do autor também usa 12). |
| H-01 | PASS | `.venv\Scripts\python.exe -m pytest tests -q` → **82 passed, 1 warning in 8.40s**. Com `C:\Python314\python.exe` o pytest coleta com erro de dependência (`sqlalchemy`, `sqlmodel`, `reflex` ausentes) — é falta de provisionamento do interpretador global, não regressão do código; o ambiente do projeto é o `.venv`. |
| H-02 | PASS | `git diff --stat 2f5996b..2960a70` só tem caminhos em `documentacao/`; nenhum workflow/deploy, nenhum arquivo de corpus, nenhuma escrita em produção. O baseline HTTP 200 + "João 3:16" não foi exercitado: o plano declara ambiente local e "não há produção envolvida"; a prova possível é o diff. |
| H-03 | PASS | **0 contradição direta** com as 12 decisões; 1 tensão (F-024) e 1 nota de redação (10.1). Tabela abaixo. |
| C-01 | PASS | `git show --name-status 2960a70`: 10 arquivos, todos em `documentacao/`. Nenhum caminho em `ESTUDOS_BIBLICOS/GSI_EBD/`. O ponteiro do submódulo no worktree (`ac712dd`, 10:37) difere do registrado no commit (`a6c5b80`), mas é anterior ao commit do artefato (18:07) e **não** está no diff do commit. Nenhum arquivo de banco. |
| N-01 | PASS | Nenhuma migração/modelo/tabela nova no diff; o CSV é catálogo, não persistência. |
| N-02 | PASS | Nenhum importador ou ingestão no diff; as fontes são apenas catalogadas. |
| N-03 | PASS | Nenhuma tela, rota ou motor de busca no diff. |
| N-04 | PASS | Nenhum léxico ou original ingerido; SBL GNT/WLC/MorphGNT aparecem só como linha de inventário (F-065..F-067). |
| N-05 | PASS | Os 12 gatilhos `a confirmar` foram preservados; nenhum virou licença concreta sem evidência. Observação: o README lista F-004/F-007/F-008 como `a confirmar`, mas o CSV as classifica como `direito reservado` (licença esperada na spec A.2/A.3); é inconsistência de documentação, não resolução silenciosa no CSV. |
| G-01 | **N-A** | Aceite do ARQUITECT; não é automatizável e não foi executado. |

## F-01 — detalhe do FAIL (CA01)

Estrutura (passa):

```
bytes iniciais: EF BB BF
BOM: True
cabecalho: 17 colunas, na ordem da spec §4
registros: 80 (1 cabecalho + 79 dados)
distribuicao de campos por linha de dados: {17: 79}
linhas com campos != 17: []
linhas de dados vazias: []
```

Conteúdo obrigatório (falha):

```
atribuicao_exigida vazia:
  F-068 (linha 69), F-069 (70), F-070 (71), F-071 (72),
  F-072 (73), F-078 (79), F-079 (80)
localizacao vazia:
  F-078 (linha 79), F-079 (80)
```

A spec §4 marca as duas colunas como `Obrigatório: sim`; `atribuicao_exigida` aceita "texto a exibir, ou `nao`" e `localizacao` aceita "caminho no repositório, ou `fora do git`". As linhas não usam `nao`/`fora do git`; ficam vazias. CA01: "todas as colunas obrigatórias preenchidas" → não atendido.

## F-04 — detalhe do FAIL (§6.1)

| Linha | `licenca` | `regime_exibicao` | `decisao` | `observacoes` (trecho) |
|---|---|---|---|---|
| F-002 | a confirmar | **curto** | depende | "confirmar titular e licença da tradução PT ... antes de qualquer exibição ao usuário" |
| F-027 | a confirmar | **curto** | depende | "confirmar titular e licença de redistribuição dos trechos ... antes de qualquer exibição ao usuário" |
| F-063 | a confirmar | **curto** | depende | "confirmar titular e licença junto ao Pleiades antes de qualquer exibição ao usuário" |
| F-074 | a confirmar | **curto** | depende | "confirmar titular e licença (autoria e licença) ... antes de qualquer exibição ao usuário" |

A spec §6.1: `curto` = "a licença permite exibir trecho curto com atribuição"; `integral_interno` = "obra de terceiro, licença restritiva, ou **licença a confirmar**"; "na dúvida entre dois regimes, o mais restritivo". As quatro linhas não sabem se a licença permite; o gatilho diz que não se deve exibir antes de confirmar. O regime correto seria `integral_interno` (ou `nao_exibir`), não `curto`. O verificador do autor só testa se o valor está no conjunto, por isso passa.

F-001 (ACF) também é `a confirmar` + `curto`, mas a ADR-012 10.10 aceita o risco e autoriza "citação hoje"; por isso não entra neste FAIL.

## F-06 / H-03 — as 12 decisões da ADR-012

| # | Decisão | Linha(s) correspondente(s) | Status |
|---|---|---|---|
| 10.1 | Público do 1º corte: coordenador/instrutor; aluno só depois via assistente | Nenhuma linha agenda o 1º corte. F-004/F-007/F-010 dizem "curto é o que o aluno vê" — leitura de superfície futura, não de 1º corte | sem contradição direta; nota de redação |
| 10.2 | Trecho curto com fonte; integral só interno e nunca no aluno | F-001/F-004/F-005/F-007..F-010 `curto` com atribuição; F-006 `integral_interno` é material próprio; nenhuma linha oferece integral de terceiro ao aluno | sem contradição |
| 10.3 | CC BY-SA aceito; derivado mantém a licença | F-012 (CC BY-SA 4.0) e F-067 (CC BY-SA 3.0), com obs de share-alike | sem contradição |
| 10.4 | Sem lucro; fonte não comercial aceita; com lucro, sai | F-024 (RWP, não comercial) está `depende`, com motivo de jurisdição/expiração e gatilho "se houver comercialização remover" | **tensão**: a ADR já aceita o regime; o inventário fica pendente. Não é "não entra" |
| 10.5 | ADR de política antes da DEM-A | Esta ADR existe | n/a (não é fonte) |
| 10.6 | Deuterocanônicos fora (66 livros) | F-060 `nao_entra`, `adequacao = fora`, motivo "fora do cânon adotado (10.6)" | sem contradição |
| 10.7 | lff/lff-en/lffe/sangue fora; skill jesus-cristo fora | F-068..F-071 e F-076 `nao_entra`, motivo 10.7 | sem contradição |
| 10.8 | Mapa em JS → ADR-013 | Nenhuma linha de fonte de mapa JS; não se aplica | n/a |
| 10.9 | SBL GNT, WLC e MorphGNT entram no 1º corte | F-065/F-066/F-067 `entra`, `curto`, motivo 10.9 | sem contradição |
| 10.10 | ACF: risco aceito, citação hoje, confirmação depois, nunca redistribuir integral | F-001 `a confirmar`, `entra`, `curto`, gatilho + ADR-002 | sem contradição (o gatilho "antes de qualquer exibição" é mais restritivo que "citação hoje"; anotado) |
| 10.11 | Resumo por IA entra na busca, com citação; nada gerado vira conteúdo aprovado | Nenhuma linha de fonte de resumo por IA; não é fonte do inventário | n/a |
| 10.12 | Jev/Laya fora; reavaliar na DEM-E | F-078/F-079 `nao_entra`, motivo 10.12 | sem contradição |

Contagem H-03: **0 contradição direta; 1 tensão (10.4/F-024); 3 decisões n/a (10.5, 10.8, 10.11).**

## Verificador do autor x EVAL

Comando: `C:\Python314\python.exe documentacao\fontes\verificar_inventario.py`

```
linhas: 79
AVISO fontes internas na mesma tabela: 4 linha(s)

PASS — estrutura, enums, motivo, gatilho e cobertura do Anexo A
EXIT=0
```

Concorda comigo no que cobre: BOM, `;`, 17 colunas, 79 linhas, 46 ids do Sensus, 12 exclusões, enums, `motivo` e gatilho. **Não concorda no veredito** porque não testa:

1. campos obrigatórios vazios (`atribuicao_exigida`, `localizacao`) — CA01;
2. a escolha do `regime_exibicao` pelos critérios do §6.1 — ele só verifica se o valor está no conjunto;
3. o conteúdo do README (RF09) e a cobertura do Anexo A fora do Sensus (a mensagem "cobertura do Anexo A" é mais ampla do que o código faz).

Ou seja: o PASS do verificador é um falso negativo nesses pontos; o problema é sério porque a entrega se declara pronta com base nele.

## Não aplicável (N-A)

- **G-01** — aceite do ARQUITECT; caso humano, não executado pelo EVAL.
- **ADR-012 10.5 / 10.8 / 10.11** — não são fontes do acervo; não há linha a conferir.
- **H-02 baseline HTTP 200 + "João 3:16"** — o plano declara ambiente local e "não há produção envolvida"; a prova de não-intervenção é o diff do commit, que não toca deploy/corpus.

## Observações fora do veredito (não corrigidas)

- **F-024** (RWP): `depende` com licença não comercial declarada. A ADR 10.4 aceita fontes não comerciais no regime sem lucro; o motivo preserva o gatilho de comercialização. Tensão, não contradição direta.
- **F-001** (ACF): `a confirmar` + `entra` + `curto` é a exceção explícita da ADR 10.10. O texto do gatilho ("antes de qualquer exibição ao usuário") é mais restritivo que "citação hoje"; a decisão `entra`/`curto` é a que corresponde à ADR.
- **README**: não há dicionário das 17 colunas (RF09 pede "explicando colunas"); a tabela de pendências diz que F-004/F-007/F-008 estão `a confirmar`, mas o CSV as marca `direito reservado`; F-061 tem `licenca_verificada = sim` e `observacoes` pedindo identificar a edição da Almeida.
- **`atribuicao_exigida`**: 8 linhas usam `não` (acentuado) em vez do literal `nao` da spec §4 (F-006, F-011, F-058, F-064, F-073, F-075, F-076, F-077). Não é enum fechado no verificador; anotado.
- **A.5 do Anexo A**: a tabela "Fontes e licenças de conteúdo" do README do atlas tem 5 linhas; o CSV cobre 4 delas (F-059..F-062) e acrescenta Pleiades (F-063) e Bíblia de Jerusalém (F-064), que estão na prosa. A 5ª linha da tabela ("Identificações dos povos e lugares", licença `—`) não tem linha própria; interpretei como não-fonte licenciada (não é obra de terceiro), então não conto como lacuna. Se o ARQUITECT contar como item do Anexo A, é lacuna de cobertura.
- **Plano F-10**: o plano fala em "13 exclusões"; a spec RF10 e o despacho falam em 12. Usei a lista fechada da spec (12).
- **Escopo do commit**: além do inventário, o commit inclui `documentacao/dem/DEM-202610-004-ci-cd-fase-a3/planner/intent.md` e `documentacao/visao/LEVANTAMENTO-FONTES-aux-architect.md`. Tudo em `documentacao/`, então C-01 passa; é scope creep, não violação do critério.
- **Worktree**: `ESTUDOS_BIBLICOS/GSI_EBD` aponta para `ac712dd` (10:37) no worktree e `a6c5b80` no commit (18:07); é estado anterior ao artefato, não alteração do commit. `estudos/` está não versionado no repositório guarda-chuva.
