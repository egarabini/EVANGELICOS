# Jornada — EVAL rodada 3 · DEM-202610-003 / inventário de fontes

- **Agente:** EVAL
- **Data:** 2026-10-17
- **DEM:** DEM-202610-003
- **Hash avaliado:** `c0161ce9ad2c45af838ca31b86fbcf249d8a1008`
- **Artefato:** `documentacao/fontes/inventario.csv` (86 linhas) + `verificar_inventario.py`
- **Ambiente:** local, leitura do repositório; nenhuma produção envolvida.
- **Não lido (por regra):** `README.md` da DEM, `dev/`, jornadas das rodadas 1 e 2.
- **Não alterado:** o CSV, o verificador e qualquer critério. A única escrita foi este arquivo, em `eval/`.

## 0. Método

Refiz a conferência do zero, contra o disco, sem usar o PASS do autor como evidência:

1. Estrutura lida com `csv`/`bytes` (BOM, `;`, 17 colunas, 86 linhas, contagem de campos).
2. Os 46 ids do Sensus foram reconstruídos de `estudos/sensus/DATA_LICENSES.md` §2 (tabelas `| \`id\` |`), não copiados do verificador.
3. As 18 correções de identidade foram conferidas abrindo os READMEs/arquivos citados e listando os diretórios.
4. As 7 linhas novas foram conferidas por artefato no disco (contagens de arquivos e conteúdo).
5. O verificador foi lido e testado por simulação da própria lógica (sem alterar o arquivo): nome parecido com o erro original reintroduzido e cobertura inversa com cada linha nova removida.
6. `pytest tests -q` rodado no `.venv` de `ESTUDOS_BIBLICOS/GSI_EBD`.

## 1. Foco 1 — as 18 correções de identidade

Numeração igual à auditoria do AUXILIAR-ARCHITECT (`documentacao/visao/CORRECOES-inventario-aux-architect.md` §1). "OK" = o valor está no CSV **e** confere com o disco.

| # | Linha/campo | Estado | Evidência no disco |
|---|---|---|---|
| 1 | F-009 `fonte` | **OK** | `ESTUDOS_BIBLICOS/DEUS_E_O_MAL_GORDON_CLARK/README.md:1-3`: "Deus e o Mal: O Problema Resolvido — Gordon H. Clark". |
| 2 | F-009 `titular` | **OK** | Mesmo README: Gordon H. Clark (1902–1985). Adam Clarke não aparece no diretório. |
| 3 | F-009 `adequacao_doutrinaria` | **OK (desvio justificado)** | A auditoria propunha `a_revisar` e mandava o PLANNER reavaliar. O autor reavaliou para `atencao` com a controvérsia Clark–Van Til; é classificação defensável (ponto controverso), não o "metodista/arminiano" que era o erro. |
| 4 | F-009 `observacoes` | **OK** | Diretório tem 8 arquivos (7 capítulos + README); a observação registra a reprodução de terceiro e a distinção explícita com F-030. |
| 5 | F-010 `fonte` | **OK** | `JONATHAN_EDWARDS_.../README.md:1-3`: uma obra, "O Fim para o Qual Deus Criou o Mundo". |
| 6 | F-010 `titular` | **OK** | README: Jonathan Edwards (1703–1758); a tradução foi separada em F-080. |
| 7 | F-010 `licenca` | **OK** | Obra de 1703–1758 em domínio público; a tradução de 2015 virou F-080 com `direito reservado`. A separação atende RF02 (licenças diferentes). |
| 8 | F-005 `titular` | **OK no pedido; ressalva R-01** | `TEOLOGIA_SISTEMATICA/README.md:175-176`: "Editora original: Zondervan (1994)". O CSV tem Zondervan 1994. Ressalva: a linha é a fonte **EN** e acrescenta "tradução: Editora Vida Nova"; a tradução PT é F-004. |
| 9 | F-005 `localizacao` | **OK** | `ESTUDOS_BIBLICOS/Grudem_Doutrina_Biblica` existe e contém `Capitulo_NN/*_EN.md`. A auditoria citava também a derivada; o caminho canônico existe. |
| 10 | F-004 `titular` | **OK; ressalva R-02** | O README não nomeia tradutor humano (só `_PT.md`/`_PT_v1.md`), o que sustenta "sem titular humano". A origem "IA (Grok)" não tem rastro no disco; é testemunho do ARQUITECT, não contradito. |
| 11 | F-004 `observacoes` | **OK** | Registra a tradução por IA, a obra de Grudem e o gatilho com Zondervan/Vida Nova. |
| 12 | F-004 `localizacao` | **OK** | `ESTUDOS_BIBLICOS/Grudem_Doutrina_Biblica` existe; a árvore é declarada canônica no README do próprio diretório. |
| 13 | F-008 `titular` | **OK; ressalva R-03** | `DICIONARIO_PAULO_CARTAS/` tem 17 arquivos e o título "Dicionário de Paulo e suas cartas" (breadcrumbs/CETEP). Os organizadores e a Loyola não estão no disco; vêm da resposta do ARQUITECT (auditoria, 7.1). |
| 14 | F-008 `observacoes` | **OK** | Contagem conferida: 5 arquivos com `<!DOCTYPE html>` (Adoção, Angústias, Eleição, Graça, Ressurreição), 1 Markdown (Cruz), 11 convertidos = 17. |
| 15 | F-008 `localizacao` | **OK** | `ESTUDOS_BIBLICOS/DICIONARIO_PAULO_CARTAS` existe. |
| 16 | F-007 `localizacao` | **OK** | `ESTUDOS_BIBLICOS/COSMOVISAO_JAMES_SIRE` existe (README + 3 capítulos; o cap. 01 citado no README não está no diretório, mas isso não afeta a linha). |
| 17 | F-007 `titular` | **OK** | README: "James W. Sire ... O Universo ao Lado, Editora Hagnos". |
| 18 | F-009/F-010 `localizacao` | **OK** | `DEUS_E_O_MAL_GORDON_CLARK` e `JONATHAN_EDWARDS_O_FIM_PARA_O_QUAL_DEUS_CRIOU_O_MUNDO` existem. |

**Resultado do Foco 1: 18/18 aplicados e conferidos no disco.** As ressalvas R-01/R-02/R-03 são residuais, não desfazem os pontos pedidos.

## 2. Foco 2 — as 7 linhas novas

| Artefato | Linha | Estado | Conferência |
|---|---|---|---|
| Grafo de dados do atlas | F-082 | **Presente, mas NÃO conforme (B-01)** | `estudos/atlas-biblico` tem 14 `dados*.js` (13 `dados-*.js` + `dados.js`). A linha diz 14. O problema é de coerência: ver B-01. |
| Materiais da revista FAJOPA | F-083 | **OK** | `ESTUDOS_BIBLICOS/docs/` tem os 2 PDFs (escatologia, dons) + o MD dos dons + o MD Paulo/história; `licenca = a confirmar`, `a_revisar`, `depende`, gatilho completo (o quê/com quem/quando). |
| 34 planos de estudo dirigido | F-084 | **OK** | 34 `plano-de-estudo.md` em `DOUTRINAS_CRISTAS/estudo_dirigido/capitulo_01..34` (35 pastas, uma é `resumo_bibliografico`). `curto`, `entra`, observação de que o integral da obra não é renderizado. |
| Árvore TEOLOGIA_SISTEMATICA | F-085 | **OK** | 133 arquivos contados; `integral_interno`, `entra`, derivada de Grudem. |
| Serviços de mapa | F-086 | **OK com ressalva R-04** | `estudos/sensus/DATA_LICENSES.md` §2.8 lista OpenStreetMap (ODbL), OpenMapTiles (CC BY 4.0), OpenFreeMap (MIT) e maplibre (MIT). A linha cobre OSM/OpenMapTiles e cita OpenFreeMap; omite o MIT de OpenFreeMap/maplibre. `depende` por ADR-013 é coerente com a decisão pendente. |
| Tradução do Edwards | F-080 | **OK com ressalva R-05** | O PDF existe; metadados: `/Author: Rodrigo Reis de Faria`, criação 20/10/2015; página 1: "Tradução: Rodrigo Reis de Faria (20/10/2015)". `licenca_verificada = sim` não tem página de copyright no PDF; "direito reservado" é o default seguro. |
| Divisão das skills do top-skills por licença | F-075 + F-081 | **OK** | `estudos/top-skills/CREDITOS.md`: 4 MIT (book-to-skill, humanizer, last30days, notebooklm) = F-075; 3 sem licença (criar-skill-ouro, gerador-de-prompt, elliott-jaques) = F-081; jesus-cristo = F-076. |

**Resultado do Foco 2: 7/7 artefatos com linha; 6 linhas conformes e F-082 com defeito de coerência (B-01).**

### B-01 — defeito bloqueante em F-082

F-082 (`Grafo de dados do atlas`):

- `licenca` = "MIT (código) e dados conforme a tabela de fontes do atlas";
- `licenca_verificada` = `nao`;
- `decisao` = `depende`; `motivo` = "licença dos dados não confirmada registro a registro…";
- `regime_exibicao` = `curto`;
- `observacoes` = "14 arquivos dados-*.js. Risco aceito pelo ARQUITECT em 17/10. A ingestão do grafo é escopo da DEM-C";
- `atribuicao_exigida` = "conforme a tabela de fontes do atlas".

Problemas:

1. **§6.1 / RF04:** a licença dos dados é, por admissão da própria linha, não confirmada. O §6.1 manda `integral_interno` (ou `nao_exibir`) para licença `a confirmar`, e a precedência é o regime mais restritivo. `curto` é o único valor proibido nesse caso. O verificador só aplica essa regra quando `licenca.strip().lower() == "a confirmar"` (linha 122); o valor híbrido de F-082 escapa.
2. **RF03 / §6.3 / CA07:** a linha não traz licença identificada nem a marca `a confirmar`; `observacoes` não contém o gatilho de três partes (o quê · com quem · quando). "Risco aceito pelo ARQUITECT" não substitui o gatilho — a exceção documentada da ADR-012 é a F-001 (10.10), não esta linha.
3. **§4:** `atribuicao_exigida` deve ser "texto a exibir, ou `nao`"; "conforme a tabela de fontes do atlas" é uma remissão, não uma atribuição exibível. O verificador não valida o domínio dessa coluna.

O PASS do autor é compatível com F-082 por três escapes simultâneos (licença híbrida, gatilho só para `a confirmar` exato, atribuição não validada). É o exemplo mais claro de que o PASS das checagens novas não é probatório.

## 3. Foco 3 — o verificador endurecido

### (a) As 3 checagens funcionam?

- **Existência do caminho (linhas 185-198):** executa e encontrou 21 caminhos citados; todos os 21 existem (conferi com `Path.exists`). Funciona como *teste de existência*, mas:
  - só olha `localizacao`, não `observacoes`/`motivo`;
  - só enxerga strings que casam com o regex `(ESTUDOS_BIBLICOS|estudos|documentacao)/...`; locais genéricos como "ChromaDB (corpus)", "PostgreSQL (tabela adendo)" e "fora do git" são ignorados (legitimamente);
  - `localizacao` com "a confirmar" gera **aviso**, não falha (linhas 197-198), ao contrário do que a auditoria pediu ("falha para valor genérico quando o material está no git");
  - existência não é identidade: um caminho real e errado passa. Ex.: se F-005 apontasse para `TEOLOGIA_SISTEMATICA` em vez de `Grudem_Doutrina_Biblica`, o check passaria.
- **Nome parecido (linhas 200-226):** executa e emite 3 avisos. Mas o teste que fiz reintroduzindo o erro original (F-009 com "Adam Clarke", F-030 com "Adam Clarke") **não gera aviso algum** para Clark/Clarke: os tokens "Adam" e "Clarke" ficam com o mesmo conjunto de ids `{F-009, F-030}` e o código faz `if tokens[a] == tokens[b]: continue`. A checagem pega **sobrenomes diferentes** (Clark × Clarke), não o caso que aconteceu (mesmo nome em duas linhas). Os 3 avisos atuais são de nomes legítimos distintos.
- **Cobertura inversa (linhas 228-238):** executa sem avisos hoje. Mas só olha diretórios de **primeiro nível** e usa `d.name in c` (substring). Simulei remover cada linha nova:
  - remover F-083 → avisa `ESTUDOS_BIBLICOS/docs` (pega);
  - remover F-084 → avisa `DOUTRINAS_CRISTAS` (pega);
  - remover F-085 → avisa `TEOLOGIA_SISTEMATICA` (pega);
  - remover F-080, F-082, F-086, F-075 ou F-081 → **nenhum aviso** (os diretórios já estão cobertos por outras linhas).
  Portanto a cobertura inversa **não** teria pegado o grafo do atlas, a tradução do Edwards, os serviços de mapa nem a divisão das skills. A afirmação da auditoria de que ela pegaria "docs/ e o grafo do atlas" é falsa para o grafo: `estudos/atlas-biblico` já tinha F-058..F-064.

### (b) O PASS delas é confiável ou decorativo?

**Decorativo para identidade e para as linhas novas.** As três checagens:

- não comparam identidade com o disco (só existência, semelhança de sobrenome e cobertura de diretório);
- não pegam o erro que motivou a rodada (mesmo nome em duas linhas);
- não pegam a linha nova dentro de diretório já coberto;
- no caso de F-082, passam por três escapes (licença híbrida, gatilho só para `a confirmar` exato, atribuição não validada);
- para `localizacao` genérica, emitem aviso em vez de falha.

O PASS geral do autor é **confiável para a forma** que eu reproduzi de forma independente: BOM, `;`, 17 colunas, 86/86 linhas, enums, 46 ids do Sensus, 12 exclusões com motivo, 14 `a confirmar` com os três elementos. Não é confiável como prova das 18 correções nem das 7 linhas.

### (c) Os 3 avisos de nome parecido: erros reais ou falsos positivos?

- `Clark` (F-009) × `Clarke` (F-030): **falso positivo como erro atual**. Gordon H. Clark e Adam Clarke são pessoas distintas e as duas linhas agora estão corretas. O aviso é o fantasma do erro antigo; útil como tripwire, mas não indica defeito.
- `House` (F-013..F-020, "STEP Bible / Tyndale House") × `Rouse` (F-012, Robert Rouse / viz.bible): **falso positivo**. Instituição × pessoa.
- `Reid` (F-008, Daniel G. Reid, organizador) × `Reis` (F-080, Rodrigo Reis de Faria, tradutor): **falso positivo**. Pessoas distintas, funções distintas.

Nenhum dos três é erro de identidade no CSV atual.

## 4. Plano de testes — execução

| Caso | Resultado | Evidência |
|---|---|---|
| F-01 estrutura | **PASS** | `BOM=True`; `;`; 17 colunas na ordem; 86 linhas; 0 linha com contagem de campos ≠ 17; 86 ids únicos F-001..F-086. |
| F-02 granularidade Sensus | **PASS** | 46 linhas `Sensus — <id>:`; ids reconstruídos de `DATA_LICENSES.md` §2 = 46; `faltando=[]`, `sobrando=[]`. O conjunto hardcoded do verificador coincide com o arquivo hoje. |
| F-03 gatilho | **PASS (estrito)** | 14 linhas com `licenca=a confirmar`; todas com o quê/com quem/quando. Ressalva: F-082 é `a confirmar` na substância e não está marcada como tal (B-01). |
| F-04 regime | **FAIL (conteúdo) / PASS (enum)** | Todos os valores pertencem a `{curto, integral_interno, nao_exibir}`; F-082 usa `curto` com licença não confirmada, contra §6.1 (B-01). |
| F-05 decisão/motivo | **PASS** | 0 linhas com `decisao ≠ entra` sem `motivo`; 0 `entra` com motivo. |
| F-06 ADR-012 | **PASS** | 12 decisões conferidas: 10.1 sem campo de audiência; 10.2 regimes internos; 10.3 F-012/F-067; 10.4 F-024; 10.5 n/a; 10.6 F-060; 10.7 F-068..F-071; 10.8/ADR-013 F-086; 10.9 F-065..F-067; 10.10 F-001; 10.11 sem linha de resumo; 10.12 F-078/F-079. 0 contradição. |
| F-07 adequação | **PASS** | 86/86 preenchidas no enum; `revisado_por`/`revisado_em` vazios em 86/86 = revisão pendente registrada. |
| F-08 internas/externas | **PASS** | 11 linhas com `ESTUDOS_BIBLICOS` na `localizacao`, no mesmo CSV das externas. |
| F-09 caminhos | **PASS** | 21 caminhos citados; 21 existem no disco. |
| F-10 exclusões | **PASS** | F-011, F-060, F-068, F-069, F-070, F-071, F-072, F-073, F-076, F-077, F-078, F-079: 12/12 `nao_entra` com motivo. |
| H-01 suíte | **PASS** | `.venv\Scripts\python.exe -m pytest tests -q` → `82 passed, 1 warning` (cache não gravável, não é falha). |
| H-02 commit | **PASS** | `git show --name-only c0161ce` = só `documentacao/fontes/inventario.csv` e `.../verificar_inventario.py`; `git diff --stat c0161ce^ c0161ce -- . ':(exclude)documentacao'` vazio. Observação: a árvore de trabalho tem `M ESTUDOS_BIBLICOS/GSI_EBD` (gitlink a6c5b80→ac712dd) e `?? estudos/`, anteriores/fora do commit; não são alterações do c0161ce. |
| H-03 contradições ADR | **PASS** | 0 contradições (F-06). |
| C-01 código/banco | **PASS** | Commit não toca `gsi_ebd/`, banco nem corpus; só documentação. Ver observação de árvore suja em H-02. |
| N-01 banco | **PASS** | Nenhuma migração/tabela/script de persistência no diff. |
| N-02 ingestão | **PASS** | Nenhum importador/ingestão no diff; F-082 declara a ingestão como DEM-C. |
| N-03 busca/tela | **PASS** | Nenhuma tela/rota/busca no diff. |
| N-04 léxico/original | **PASS** | Nenhum léxico/original ingerido; F-065..F-067 só inventariados. |
| N-05 `a confirmar` por suposição | **PASS (com B-01)** | 14 `a confirmar` preservados com gatilho; nenhuma licença trocada por suposição. F-082 é um caso de licença híbrida que não foi marcada, mas não é uma resolução por suposição. |
| G-01 aceite humano | **N-A** | ARQUITECT. |

## 5. Veredito

```
hash: c0161ce9ad2c45af838ca31b86fbcf249d8a1008
F: FAIL (1 defeito de conformidade: F-082; os demais casos F passam)
H: PASS
C: PASS
N: PASS
G: N-A (ARQUITECT)
agregado: FAIL
```

**Por categoria:**

- **F — FAIL.** F-01, F-02, F-03, F-05, F-06, F-07, F-08, F-09, F-10 passam; F-04 falha no critério de escolha do regime (§6.1) por causa de F-082. O enum de F-04 está correto; a classificação não.
- **H — PASS.** 82 testes; commit só em `documentacao/`; 0 contradições com a ADR-012.
- **C — PASS.** O commit não toca código nem banco. (A árvore de trabalho tem um gitlink sujo de `GSI_EBD` e `estudos/` untracked, mas não no c0161ce.)
- **N — PASS.** Nenhuma persistência, ingestão, busca, léxico ou resolução de `a confirmar` por suposição.
- **G — N-A.** Aceite do ARQUITECT.

## 6. Concordância com o verificador do autor

**Não concordo com o PASS como validação da entrega.** Concordo com ele apenas nos itens mecânicos que reproduzi de forma independente (BOM, 17 colunas, 86 linhas, enums, 46 ids do Sensus, 12 exclusões, gatilho das 14 linhas `a confirmar` exatas, motivo das não-entradas). Discordo de:

1. tratar as 3 checagens de identidade como prova das 18 correções — elas não comparam identidade com o disco;
2. tratar a cobertura inversa como cobertura das 7 linhas — ela não pega 4 delas;
3. tratar o nome parecido como detector do erro original — ele não pega o mesmo nome repetido;
4. aceitar F-082 com `regime=curto` e sem gatilho porque a licença não é a string exata `a confirmar`.

## 7. Ressalvas não bloqueantes

- **R-01:** F-005 é a linha **EN** e o `titular` acrescenta "tradução: Editora Vida Nova"; a tradução PT é F-004. O ponto pedido (Zondervan 1994) está atendido, mas a linha mistura as duas edições.
- **R-02:** F-004: "gerada por IA (Grok)" não tem rastro no disco; o README só não nomeia tradutor humano. A afirmação é do ARQUITECT, não do arquivo.
- **R-03:** F-008: organizadores e Loyola não aparecem nos 17 arquivos; o título "Dicionário de Paulo e suas cartas" e a origem CETEP aparecem. O resto é testemunho do ARQUITECT (7.1).
- **R-04:** F-086: a licença omite o MIT de OpenFreeMap e do maplibre; a linha cobre OSM/OpenMapTiles.
- **R-05:** F-080: `licenca_verificada=sim` sem página de copyright no PDF; "direito reservado" é o default seguro, mas o "sim" não está evidenciado no disco.
- **R-06:** F-082 diz "14 arquivos dados-*.js"; o glob `dados-*.js` tem 13, e `dados*.js` tem 14 (inclui `dados.js`). A contagem de 14 é a do conjunto, o rótulo do glob é impreciso.
- **R-07:** F-083 usa `atribuicao_exigida=a confirmar`, que não é "texto a exibir, ou `nao`" (§4). Como a decisão é `depende`, não há exibição hoje; fica registrado.

## 8. N-A

- **G-01** — aceite humano do ARQUITECT: N-A.
- **H-02** — produção/HTTP 200/"João 3:16": não se aplica a esta DEM (sem produção envolvida); o que se verifica é o diff, e o diff é só em `documentacao/`.
