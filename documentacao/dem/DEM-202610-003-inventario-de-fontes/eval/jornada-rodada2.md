# EVAL — DEM-202610-003 / inventário de fontes — rodada 2

- **Agente:** EVAL (cego e independente)
- **Data:** 2026-10-17
- **DEM:** DEM-202610-003 / inventario-de-fontes
- **Hash avaliado:** `17fc6653d25f55e433ddce50fb3eec33d11ac4dc` (`17fc665`)
- **Artefato:** `documentacao/fontes/inventario.csv` (79 linhas, 17 colunas)
- **Instrumento do autor:** `documentacao/fontes/verificar_inventario.py`
- **Ambiente:** leitura do repositório; `C:\Python314\python.exe`; `.venv` de `ESTUDOS_BIBLICOS/GSI_EBD`; sem produção.
- **Cegueira:** não li o `README.md` da DEM, `dev/` nem `eval/jornada.md` da rodada 1. O CSV foi lido do git (worktree = `HEAD`, SHA-256 idêntico), não de memória.

## 1. Resultado por caso

| Caso | Execução | Evidência | Resultado |
|---|---|---|---|
| F-01 | BOM, delimitador, 17 colunas, linhas | 27.249 bytes; BOM `EF BB BF`; 80 linhas (cabeçalho + 79); cabeçalho exato na ordem da spec; 0 linha com nº de campos ≠ 17; ids `F-001`…`F-079` únicos e completos | **PASS** |
| F-02 | Reconstrução dos ids do Sensus | `DATA_LICENSES.md` §2 → 46 ids; CSV → 46 linhas `Sensus — …`; 46/46; 0 faltando, 0 sobrando; o conjunto hardcoded do verificador também tem 46/46 | **PASS** |
| F-03 | Gatilho completo | 12 linhas com `licenca = a confirmar`; todas com `observacoes` não vazio contendo o quê, com quem e quando | **PASS** |
| F-04 | Regime e §6.1 | `regime_exibicao` ∈ {curto, integral_interno, nao_exibir} em 79/79; todas as 12 linhas `a confirmar` em `integral_interno`/`nao_exibir`, exceto F-001 (`curto`, exceção ADR-012 10.10) | **PASS** |
| F-05 | Decisão e motivo | `decisao` ∈ {entra, nao_entra, depende}: 59 entra, 5 depende, 15 nao_entra; 20/20 linhas não-`entra` com `motivo` não vazio | **PASS** |
| F-06 | 12 decisões da ADR-012 | 12/12 conferidas; 0 contradição (tabela do §5) | **PASS** |
| F-07 | Adequação doutrinária | 79/79 preenchidas (`ok` 58, `atencao` 16, `fora` 5); `revisado_por`/`revisado_em` vazios em 79/79 = revisão do ARQUITECT pendente, registrada no README | **PASS** |
| F-08 | Internas e externas no mesmo CSV | Internas: F-004/F-005 (`DOUTRINAS_CRISTAS`), F-006 (adendo), F-007…F-010 (`ESTUDOS_BIBLICOS`); externas: corpus, Sensus, atlas etc. — mesmo arquivo | **PASS** |
| F-09 | Caminhos declarados | `documentacao/fontes/inventario.csv` e `documentacao/fontes/README.md` existem | **PASS** |
| F-10 | Exclusões como linha | 12/12 exclusões do RF10 presentes, todas `nao_entra` e com motivo (F-011, F-060, F-068, F-069, F-070, F-071, F-072, F-073, F-076, F-077, F-078, F-079) | **PASS** |
| H-01 | Suíte do código | `pytest tests -q` no `.venv` de `ESTUDOS_BIBLICOS/GSI_EBD`: **82 passed**, 1 warning (cache do pytest não gravável), 5,58 s | **PASS** |
| H-02 | Nada regrediu | `git diff --stat 17fc665^ 17fc665`: 6 arquivos, **todos** em `documentacao/`; nenhum diff em `ESTUDOS_BIBLICOS/`, corpus ou banco | **PASS** |
| H-03 | 0 contradições com a ADR-012 | 12/12 decisões conferidas; 0 contradição | **PASS** |
| C-01 | Código/banco intocados | O commit só toca `documentacao/fontes/*`, `documentacao/dem/.../planner/plano-testes.md` e `documentacao/dem/.../eval/*`; `gsi_ebd/`, banco e corpus com diff vazio. O único `.py` tocado é o instrumento do inventário, sob `documentacao/fontes/`, não código da aplicação | **PASS** |
| N-01 | Nada persistido no banco | Nenhuma migração, schema, tabela ou código de persistência no diff | **PASS** |
| N-02 | Nenhuma ingestão | Nenhum importador, pipeline ou dado novo; só documentação | **PASS** |
| N-03 | Nenhuma busca/tela | Nenhum código de UI, busca ou rota no diff | **PASS** |
| N-04 | Nenhum léxico/original ingerido | Linhas F-017…F-020 e F-065…F-067 são catálogo, não ingestão; nenhum arquivo de dado novo | **PASS** |
| N-05 | Nenhum `a confirmar` resolvido por suposição | Nenhum valor de `licenca` mudou no commit; as 12 linhas `a confirmar` continuam com gatilho | **PASS** |
| G-01 | Aceite do ARQUITECT | Não executável pelo EVAL | **N-A** |

**F-02 — os 46 ids reconstruídos de `DATA_LICENSES.md` §2 (todos no CSV):**
`theographic`, `tagnt`, `grc-tr`, `tahot`, `hbo-wlc`, `stepbible-tbesg`, `stepbible-tbesh`, `stepbible-tflsj`, `stepbible-tipnr`, `openbible-geo`, `openbible-xref`, `blivre`, `sword-rwp`, `kjv`, `gill`, `patristic`, `sword-barnes`, `sword-calvincommentaries`, `sword-clarke`, `sword-jfb`, `sword-kd`, `sword-mhc`, `sword-scofield`, `sword-wesley`, `sword-abbott`, `sword-burkitt`, `sword-catena`, `sword-lightfoot`, `sword-luther`, `sword-pnt`, `sword-tfg`, `egw-great-controversy`, `egw-patriarchs`, `egw-prophets`, `egw-acts`, `egw-object-lessons`, `egw-steps`, `egw-thoughts`, `smith-daniel`, `sword-easton`, `sword-hitchcock`, `sword-isbe`, `sword-smith`, `sword-nave`, `sword-torrey`, `sword-tsk`.

## 2. F-01/CA01 — os campos obrigatórios (FAIL da rodada 1)

**Resultado: corrigido.**

Conferência linha a linha das 12 colunas marcadas `Obrigatório: sim` na spec §4 (`id`, `fonte`, `tipo`, `titular`, `licenca`, `licenca_verificada`, `regime_exibicao`, `atribuicao_exigida`, `versao_data`, `adequacao_doutrinaria`, `decisao`, `localizacao`): **0 vazios em 79 linhas**. Também 0 `None` de campo faltante e 0 linha com nº de campos diferente de 17.

As 7 linhas que a rodada 1 viu com `atribuicao_exigida` vazio e as 2 com `localizacao` vazio estão preenchidas:

| Linha | `atribuicao_exigida` | `localizacao` |
|---|---|---|
| F-068 | não se aplica (material não exibido) | estudos/estudos-biblicos/cadernos/livros/lff |
| F-069 | não se aplica (material não exibido) | estudos/estudos-biblicos/cadernos/livros/lff-en |
| F-070 | não se aplica (material não exibido) | estudos/estudos-biblicos/cadernos/livros/lffe |
| F-071 | não se aplica (material não exibido) | estudos/estudos-biblicos/cadernos/temas/sangue |
| F-072 | não se aplica (ferramenta, não exibida) | estudos/estudos-biblicos/modelos |
| F-078 | não se aplica (não é fonte de conteúdo) | não identificado no acervo (citado como candidato) |
| F-079 | não se aplica (não é fonte de conteúdo) | não identificado no acervo (citado como candidato) |

**Ressalva de forma (não FAIL):** para F-068…F-072 e F-078/F-079 a resposta é uma frase (`não se aplica…`), não o token literal `nao` que a spec §4 exemplifica para `atribuicao_exigida`; e a `localizacao` de F-078/F-079 não é caminho nem `fora do git`. O campo está preenchido, é verdadeiro para material que não é exibido/está fora do acervo, e o critério F-01/CA01 é preenchimento/estrutura — não token exato. Fica como normalização cosmética para a DEM-B, não como FAIL.

## 3. F-04/§6.1 — o regime (FAIL da rodada 1)

**Resultado: corrigido, com a exceção F-001 julgada legítima.**

As 12 linhas com `licenca = a confirmar` (valor exato) e seus regimes:

| Linha | Regime | Situação |
|---|---|---|
| F-001 (ACF) | `curto` | exceção ADR-012 10.10 |
| F-002 (Henry PT) | `integral_interno` | conforme |
| F-027 (patristic) | `integral_interno` | conforme |
| F-063 (Pleiades) | `integral_interno` | conforme |
| F-068, F-069, F-070, F-071 (lff/lff-en/lffe/sangue) | `nao_exibir` | conforme (mais restritivo) |
| F-072 (LaTeX) | `integral_interno` | conforme |
| F-074 (resumos bplataforma) | `integral_interno` | conforme |
| F-078, F-079 (Jev/Laya) | `integral_interno` | conforme |

Nenhuma outra linha `a confirmar` está em `curto`. Todas as 12 têm `licenca_verificada = nao`.

**F-001 — legítima, não desculpa.** A ADR-012 10.10 diz textualmente: *"Risco aceito: citação hoje, confirmação da licença depois"*. A tabela de riscos da mesma ADR diz que, **se** a licença se mostrar restritiva, o corpus passa a interno — ou seja, hoje ele não está tratado como interno; a "citação hoje" é exatamente o regime `curto` (trecho curto com atribuição). O Anexo A da spec amarra o ACF a "(ADR-012 10.10)", e a linha F-001 carrega o gatilho com a SBTB. A exceção é a aplicação de uma decisão `Accepted`, não uma invenção do autor. **Ressalva:** o texto do gatilho diz "antes de qualquer exibição ao usuário", mais restritivo que "citação hoje"; lido ao pé da letra, ele adia a exibição até a confirmação. Isso é conservador e não converte a classificação em violação.

## 4. As 3 observações da rodada 1

| Observação | Status | Evidência |
|---|---|---|
| **F-024 (RWP):** o `motivo` separa a cláusula não comercial (aceitável no 10.4) da jurisdição de copyright? | **Corrigida** | `motivo` = "a cláusula não comercial é aceitável no regime sem lucro (10.4), o que falta é confirmar a jurisdição e a expiração do copyright". Separa as duas coisas. Regime passou de `curto` para `integral_interno`; `decisao = depende`; `observacoes` mantém "confirmar a jurisdição aplicável junto ao detentor (CrossWire) antes de qualquer exibição" e "se houver comercialização, remover". |
| **`fontes/README.md`:** existe o dicionário das 17 colunas e a tabela de pendências não contradiz mais o CSV (F-004/F-007/F-008)? | **Corrigida** | Seção "Como ler as 17 colunas" documenta os 17 nomes (16 linhas; a última agrupa `revisado_por`/`revisado_em`). A pendência agora diz: a **obra** está em `direito reservado` (F-004, F-007, F-008), o que falta identificar é a **tradução**; Henry PT é `a confirmar` (F-002). O CSV confirma: F-004/F-007/F-008 com `licenca = direito reservado` e `titular` com "editora da tradução (a identificar)"; F-002 com `a confirmar`. Sem contradição. |
| **`plano-testes.md`:** as exclusões agora são 12 (não 13), coerente com a spec? | **NÃO integralmente — resíduo** | A tabela de rastreio (linha do F-10) foi corrigida para **12**. Mas o caso F-10, nos "passos", ainda diz **"buscar as 13 exclusões do RF10"**. A spec RF10 tem 12 (lff, lff-en, lffe, sangue, mapas, deuterocanônicos, jesus-cristo, código Sensus, código biblia-plataforma, LaTeX, Jev, Laya) e a tabela do plano diz 12. O resíduo é documental; o CSV tem as 12. F-10 foi executado contra as 12 da spec: **PASS**. |

## 5. F-06 / H-03 — as 12 decisões da ADR-012

| # | Decisão | Evidência no CSV | Contradição? |
|---|---|---|---|
| 10.1 | 1º corte: coordenador/instrutor; aluno depois (DEM-E) | O CSV classifica **licença** (`regime_exibicao`), não o público do corte; nenhuma linha afirma exibição ao aluno no 1º corte | não |
| 10.2 | Trecho curto com fonte; integral só interno | F-004/F-005/F-007…F-010 em `curto` com atribuição; F-024/F-027/F-063 etc. em `integral_interno`; nenhuma linha põe integral em superfície de aluno | não |
| 10.3 | CC BY-SA aceito; derivado mantém a licença | F-012 (Theographic) e F-067 (MorphGNT) com observação de share-alike | não |
| 10.4 | Não comercial aceito no regime sem lucro | F-024 com `depende`, observação 10.4 e "se houver comercialização, remover" | não |
| 10.5 | ADR de política antes da DEM-A | ADR-012 existe e é citada nas linhas | não |
| 10.6 | Deuterocanônicos fora | F-060 `nao_entra`, `adequacao = fora`, motivo "cânon (10.6)" | não |
| 10.7 | lff, lff-en, lffe, sangue fora | F-068…F-071 `nao_entra` com motivo 10.7 | não |
| 10.8 | Mapa interativo em JS: abrir ADR-013 | F-058 é o **código do atlas** (MIT, não copiado), não o componente de mapa; F-077 é o projeto de mapas de terceiro (direito reservado) | não |
| 10.9 | SBL GNT, WLC, MorphGNT no 1º corte | F-065, F-066, F-067 `entra` com ADR-012 10.9 | não |
| 10.10 | ACF: risco aceito, citação hoje | F-001 `entra`, `a confirmar`, `curto`, gatilho SBTB | não (exceção deliberada) |
| 10.11 | Resumo por IA com citação; nada gerado vira conteúdo aprovado | Não há linha de resumo por IA (não é fonte licenciada); nenhuma linha contradiz | não |
| 10.12 | Jev/Laya fora; reavaliar na DEM-E | F-078/F-079 `nao_entra`, motivo 10.12 | não |

**0 contradições em 12/12.** PASS (julgamento, não automatizável).

## 6. Cobertura do Anexo A (CA02)

| Seção | Itens | Linhas no CSV |
|---|---|---|
| A.1 Corpus e dados bíblicos | ACF; Henry PT; OpenBible xref | F-001, F-002, F-003 |
| A.2 Obra e adendos | Grudem PT; Grudem EN; adendos | F-004, F-005, F-006 |
| A.3 Fontes internas | Cosmovisão; Dicionário de Paulo; Clark; Edwards | F-007, F-008, F-009, F-010 |
| A.4 Sensus | código + 46 fontes de dados | F-011 + F-012…F-057 (46) |
| A.5 Atlas | código; conteúdo; deuterocanônicos | F-058; F-059…F-064; F-060 (Figueiredo) |
| A.6 estudos-biblicos | SBL GNT; WLC; MorphGNT; lff/lff-en/lffe/sangue; LaTeX | F-065…F-067; F-068…F-071; F-072 |
| A.7 Outros projetos | código bplataforma; resumos; top-skills; jesus-cristo; mapas | F-073…F-077 |
| A.8 Modelos | Jev; Laya | F-078, F-079 |

**79 linhas = 79 itens do Anexo A mapeados**, sem sobra. A tabela de conteúdo do atlas tem ainda a linha "Identificações dos povos e lugares" (licença `—`), que não é fonte de terceiro licenciada e por isso não tem linha própria; as fontes licenciadas da tabela (Bíblia Livre, Figueiredo, Almeida, Natural Earth) e as citadas na prosa (Pleiades, Bíblia de Jerusalém) estão cobertas. **PASS**, com essa ressalva de interpretação.

## 7. Verificador do autor

```
C:\Python314\python.exe documentacao\fontes\verificar_inventario.py
linhas: 79
AVISO fontes internas na mesma tabela: 4 linha(s)
PASS — estrutura, enums, motivo, gatilho e cobertura do Anexo A
exit=0
```

**Concorda com o veredito.** Rodei o verificador do zero; ele deu PASS, e a minha conferência independente também. Mas o PASS dele não é auto-suficiente:

- o verificador foi **alterado neste mesmo commit** para ganhar as duas checagens que faltavam na rodada 1 (campos obrigatórios e regra `a confirmar` × regime);
- ele **codifica a exceção F-001** (`rid != "F-001"`), em vez de derivá-la da ADR — a exceção é legítima, mas o instrumento não a prova;
- ele usa igualdade exata para `licenca = "a confirmar"` e, por isso, **não vê** `MIT (a confirmar)` em F-075/F-076 (ambas `nao_exibir`/`nao_entra`, sem operação de exibição);
- o gatilho é checado por substring ("licen"/"titular", "junto", "antes de"), não por conteúdo;
- a "cobertura do Anexo A" do verificador é, na prática, só Sensus (46) + 12 exclusões; a cobertura A.1/A.2/A.3/A.5/A.6/A.7/A.8 foi conferida por mim, não por ele;
- ele não lê o `plano-testes.md` e, portanto, **não detecta** o resíduo "13" do caso F-10.

Nada disso vira FAIL: os casos do plano passam na conferência independente. São limites do instrumento, registrados.

**Ressalvas registradas (sem FAIL):** F-075/F-076 usam `MIT (a confirmar)` com `licenca_verificada = nao` e sem gatilho; não são a marca exata `a confirmar` do critério F-03, mas são licença não verificada — normalizar na DEM-B. F-068…F-072/F-078/F-079 usam texto explicativo em `atribuicao_exigida`; F-078/F-079 usam localização textual, não caminho. O arquivo usa LF (a spec exige BOM, não CRLF); BOM e `;` presentes, 17 colunas e acentuação legíveis.

## 8. N-A

- **G-01** — aceite do ARQUITECT (percurso do inventário e resposta "pode exibir ao aluno?"): não executável pelo EVAL.
- **H-02 baseline de produção** (HTTP 200 + "João 3:16"): N-A; o plano ancora "não há produção envolvida" e o despacho manda conferir o diff do commit.
- **Verificação jurídica das licenças `a confirmar`**: fora do escopo (intent §4 Out); o inventário registra pendência + gatilho, não parecer.
- **Persistência, ingestão, busca, assistente**: non-goals (DEM-B…E) — verificados como ausência (N-01…N-05), não como entrega.

## 9. Veredito

```
hash: 17fc6653d25f55e433ddce50fb3eec33d11ac4dc
F: PASS · H: PASS · C: PASS · N: PASS · G: N-A (ARQUITECT)
agregado: PASS
```

**FAILs de caso:** nenhum.
**Resíduo documental (fora do agregado):** `plano-testes.md`, caso F-10, ainda diz "13 exclusões" enquanto a tabela do mesmo plano e a spec dizem 12; o CSV tem as 12 corretas. Não reabre F/H/C/N, mas o autor não pode afirmar que a observação 3 foi integralmente corrigida.
