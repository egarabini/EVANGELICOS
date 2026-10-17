# Levantamento de fatos para o inventário de fontes (DEM-202610-003)

> Autor: AUXILIAR-ARCHITECT (IA) · Para: PLANNER · Data: 2026-10-17
> **Só leitura.** Este documento não classifica nada: não decide `entra` / `nao_entra`, não preenche
> `adequacao_doutrinaria` e não contradiz a ADR-012. Ele entrega **fatos com o caminho onde foram
> lidos**, para o PLANNER escrever o `inventario.csv` sem suposição.
>
> Convenção: **[F]** = fato lido no arquivo citado · **[I]** = inferência minha, a confirmar ·
> **[?]** = não foi possível determinar.

---

## 1. Achados que mudam o inventário (leia primeiro)

1. **O Dicionário de Paulo é cópia de páginas web.** `ESTUDOS_BIBLICOS/DICIONARIO_PAULO_CARTAS/`
   tem 17 arquivos `.md` (~1,1 MB). **[F]** Todos trazem o título "… :: CETEP - Teologia e
   Psicanálise"; 5 (Adoção, Angústias, Eleição, Graça, Ressurreição) são **HTML bruto** de um site
   Webnode (`teologia-online8.webnode.page`); 11 são texto convertido do mesmo site, com menus e
   links; só `Cruz.md` está em Markdown limpo. O breadcrumb diz "Estudos > Dicionário de Paulo e suas
   cartas". **[I]** O conteúdo parece ser a obra *Dicionário de Paulo e suas Cartas* (ed. Hawthorne,
   Martin e Reid; em português, Vida Nova) reproduzida por um terceiro (CETEP). **[?]** Nenhum arquivo
   registra autor, editora ou licença. → `titular = a confirmar`, `licenca = a confirmar`; gatilho
   sugerido: identificar a obra-origem e o titular antes de qualquer exibição.
2. **O texto ACF vem de cópia de terceiro.** **[F]** `PASTOR_IA/rag/biblia/load_biblia.py` carrega de
   `github.com/ameisehaufen/BibleMarkdown` ("ACF 2007 … única disponível no repo"). **[F]** O
   `biblia-plataforma/docs/LICENCA-TEXTO-ACF.md` registra que a página de direitos da **SBTB**
   (Sociedade Bíblica Trinitariana do Brasil) trata a ACF como protegida, com limite de citação e
   autorização por escrito acima dele. A ADR-012 (10.10) aceitou o risco; o inventário precisa só
   registrar titular provável (SBTB **[I]**), `licenca_verificada = nao` e o gatilho da ADR.
3. **O Sensus lista 46 ids de fonte, não 31.** **[F]** `estudos/sensus/DATA_LICENSES.md` e o README
   dizem "31 fontes", mas `grep` das linhas de tabela devolve **46 ids distintos**. O
   `data-manifest.json` já aponta a versão de dados 2026.10.18 (o documento cita 2026.10.11).
   **[I]** O documento está desatualizado em relação ao pipeline. O inventário deve usar a
   lista de ids (seção 4), não o número.
4. **Obras de terceiros com tradução/exposição por IA ou por terceiros.** Ver seção 3: Grudem
   (Zondervan; tradução Vida Nova), Sire (Hagnos), Clark, Edwards (PDF traduzido por Rodrigo Reis de
   Faria, 2015). Os `.md` do repositório são "estudo / exposição" feitos sobre essas obras.
   **[?]** Não está registrado se os `.md` são resumo próprio, trecho, ou tradução integral.
5. **Há fonte com restrição não comercial dentro de acervo "aberto"** (Robertson, `sword-rwp`).
   Caso previsto na spec §6; a ADR-012 10.4 aceita enquanto não houver lucro.

---

## 2. Fontes internas já no projeto

| Fonte | Titular / origem | Licença declarada | Onde está | Observações |
|---|---|---|---|---|
| **Corpus bíblico ACF 2007** | **[I]** SBTB (titular da ACF); cópia de terceiro `ameisehaufen/BibleMarkdown` **[F]** | **[?]** nenhuma registrada. **[F]** SBTB limita citação | indexado no ChromaDB; fonte em `PASTOR_IA/rag/biblia/sources/BibleMarkdown`; 31.102 versículos | ADR-002 (local, `:ro`, não versionado); ADR-012 10.10 (risco aceito, com gatilho) |
| **Referências cruzadas OpenBible** | OpenBible.info | **[F]** CC BY 4.0, atribuição obrigatória | `DADOS_EXTERNOS/openbible/cross_references.txt` e `_openbible/` (344.799 pares); gerado 2026-10-12 | Base: *Treasury of Scripture Knowledge* (domínio público) + votos da comunidade. **[F]** README exige preservar o cabeçalho de atribuição. ADR-004 |
| **Grudem — Doutrina Bíblica** (fonte de verdade) | **[F]** Wayne Grudem; Zondervan (1994); tradução Editora Vida Nova (`TEOLOGIA_SISTEMATICA/README.md`) | **[?]** direito reservado **[I]** | `Grudem_Doutrina_Biblica/` — 450 arquivos; por capítulo: `_EN.md` (original), `_PT.md` ("tradução histórica") e `_PT_v1.md` (texto para estudo) | **[?]** quem traduziu `_PT` e `_PT_v1`. O `DOUTRINAS_CRISTAS/README` fala em "tradução de obra protegida por direitos autorais" fora do versionamento |
| **Doutrinas Cristãs** (derivada) | derivada do Grudem | idem | `DOUTRINAS_CRISTAS/` — 522 arquivos (planos, decks, estudo dirigido) | **[F]** README: "esta árvore é DERIVADA". Conteúdo disponível ao aluno vem daqui |
| **Teologia Sistemática** (derivada) | derivada do Grudem | idem | `TEOLOGIA_SISTEMATICA/` — 133 arquivos | **[F]** reorganização pelo template |
| **Cosmovisão — James W. Sire** | **[F]** Sire; obra *O Universo ao Lado*, Ed. Hagnos | **[?]** direito reservado **[I]** | `COSMOVISAO_JAMES_SIRE/` — 4 arquivos | **[F]** "estudo estruturado e exposição" de um ensaio; não é a obra inteira |
| **Deus e o Mal — Gordon H. Clark** | **[F]** Clark (1902–1985) | **[?]** | `DEUS_E_O_MAL_GORDON_CLARK/` — 8 arquivos | **[F]** "estudo detalhado, capítulo por capítulo". **[?]** edição/tradução de origem não registrada |
| **O Fim para o qual Deus criou o mundo — Jonathan Edwards** | **[F]** Edwards (séc. XVIII, obra em domínio público); **tradução** de Rodrigo Reis de Faria (2015) | obra: domínio público **[I]**; **tradução: direito do tradutor [I]** | `JONATHAN_EDWARDS_.../` — 5 `.md` + **PDF da tradução** no próprio diretório | O PDF é da tradução (2015): linha própria, regime mais restritivo |
| **Dicionário de Paulo e suas cartas** | ver seção 1, item 1 | **[?]** | `DICIONARIO_PAULO_CARTAS/` — 17 arquivos, ~1,1 MB | cópia de páginas do site CETEP |
| **Docs de apoio** (Paulo, dons, escatologia) | **[?]** | **[?]** | `ESTUDOS_BIBLICOS/docs/` — 2 PDFs (um sobre escatologia paulina, um sobre dons) + `.md` | **[?]** autoria dos PDFs |
| **PASTOR_IA / RAG** | projeto interno | interna | `PASTOR_IA/` (4.977 arquivos, em maior parte o BibleMarkdown) | o grosso dos arquivos é a cópia da Bíblia (ver ACF) |

**Fontes dos originais** (ADR-012 10.9; entram no primeiro corte), conforme `estudos/estudos-biblicos/README.md`:

| Fonte | Licença **[F]** | Observação |
|---|---|---|
| SBL Greek New Testament | CC BY 4.0 | |
| Westminster Leningrad Codex + morfologia OpenScriptures | CC BY 4.0 | hebraico/aramaico |
| MorphGNT (morfologia do grego) | CC BY-SA 3.0 | share-alike — ADR-012 10.3 |

---

## 3. Projetos de `estudos/` (seis, por artefato)

Regra da spec (RF02): **uma linha por artefato** quando as licenças diferem.

| Projeto | Artefato | Titular **[F]** | Licença **[F]** | Observações |
|---|---|---|---|---|
| **atlas-biblico** | código | Noé de Lima Bezerra | MIT (`LICENSE`) | não entra como código; ADR-012 |
| | dados do grafo (`dados-*.js`, 12 arquivos) | autor do atlas **[I]** | "conteúdo de terceiros conforme tabela de fontes" (README) | identificações marcadas com confiança; **[?]** licença própria do grafo não declarada |
| | texto integral — Bíblia Livre (66 livros) | Diego Santos, Mario Sérgio, Marco Teles | CC BY 3.0 BR | atribuição obrigatória |
| | texto — Figueiredo (deuterocanônicos) | domínio público (ed. 1950) **[F]** | domínio público | **fora do cânon** (10.6): linha `nao_entra` |
| | Natural Earth (basemap) | — | domínio público | |
| | Pleiades (gazetteer, links) | — | **[?]** não registrada no README | |
| | Bíblia de Jerusalém (overlay) | **[F]** o README diz "overlay **privado**, por direito autoral" | direito reservado | |
| **mapas-biblicos-e-panorama** | cópia de site WordPress comercial | terceiro | **[?]** | **[F]** contém link de pagamento; imagens de terceiros. ADR-012: `nao_entra` |
| **estudos-biblicos** | ferramenta (`estudos.py`, `ferramentas/`) | autor do repositório | **[?]** sem `LICENSE` | |
| | dados SBL/WLC/MorphGNT | ver seção 2 | CC BY 4.0 / CC BY 3.0-SA | |
| | `lff`, `lff-en`, `lffe`, `sangue` | **[?]** | **[F]** README: terceiros, "mantenha privado" | ADR-012 10.7: `nao_entra`. **[F]** há `dados/livros/{lff,lff-en,lffe}` e `dados/temas/sangue`; **[F]** `referencias/` ignorada pelo git |
| **biblia-plataforma** | código | LoadCG | MIT | stack Expo/TS: `nao_entra` (ADR-001) |
| | `assets/biblia.json` (ACF) | cópia de `thiagobodruk/bible` **[F]** | **[?]** | **[F]** o próprio projeto escreve que a licença está pendente |
| | `resumos-biblicos/` (66 resumos: `antigo-testamento`, `novo-testamento`) | **[?]** | **[?]** | **[?]** quem escreveu (IA? humano?) e com que fonte |
| | `docs/AVALIACAO-BUSCA-EDITORIAL.md` | projeto | MIT **[I]** | triagem editorial de busca |
| **sensus** | código | alvarosw **[I]** (URL do manifest) | **AGPL-3.0-or-later** | `nao_entra` como código; ideia/esquema apenas |
| | dados (46 ids, seção 4) | vários | **uma licença por fonte** | linha por fonte |
| | tiles/mapa (OpenFreeMap, OSM, OpenMapTiles) | vários | MIT / ODbL / CC BY 4.0 | não são dados do banco do Sensus; só se o Didasko usar mapa |
| **top-skills** | skills `book-to-skill`, `humanizer`, `last30days`, `notebooklm` | autores nomeados em `CREDITOS.md` | MIT | uso só de processo; não entra no produto |
| | skills `criar-skill-ouro`, `gerador-de-prompt`, `elliott-jaques` | curadoria | **[F]** "a fonte não especificava licença" | |
| | skill `jesus-cristo` | curadoria | **[F]** sem licença especificada | ADR-012: `nao_entra` |

---

## 4. Fontes do Sensus — 46 ids (de `DATA_LICENSES.md`)

Licenças e condições **[F]** conforme o documento do próprio projeto; "PD" = domínio público
declarado. Marcadas as que o documento diz **Verificar**.

| Grupo / licença | ids | Observações **[F]** |
|---|---|---|
| **CC BY-SA 4.0** | `theographic` | share-alike; descrições incluem Easton (1897, PD) |
| **CC BY 4.0 — STEPBible / Tyndale House** | `tagnt`, `grc-tr`, `tahot`, `hbo-wlc`, `stepbible-tbesg`, `stepbible-tbesh`, `stepbible-tflsj`, `stepbible-tipnr` | atribuição "STEP Bible"; `tipnr` tem coordenadas via OpenBible (ver ODbL) |
| **CC BY 4.0 — OpenBible.info** | `openbible-geo`, `openbible-xref` | `openbible-geo`: **Verificar ODbL** (parte das coordenadas pode vir do OpenStreetMap) |
| **CC BY 3.0 BR** | `blivre` | atribuição obrigatória; eBible cita 4.0 BR |
| **Não comercial** | `sword-rwp` (Robertson's Word Pictures) | **só uso não comercial**; vols. 5–6 © 1932/1933 Broadman; "se comercializado, remover" |
| **GPL declarada no módulo (texto PD)** | `kjv` | texto PD; pacote declara GPL |
| **PD — comentários** | `gill`, `sword-barnes`, `sword-calvincommentaries`, `sword-clarke`, `sword-jfb`, `sword-kd`, `sword-mhc`, `sword-scofield`, `sword-wesley`, `sword-abbott`, `sword-burkitt`, `sword-catena`, `sword-lightfoot`, `sword-luther`, `sword-pnt`, `sword-tfg` | **Verificar:** `gill` (edição original?), `sword-luther` (partes de 1892–1932), e-mails de terceiros em `calvincommentaries` e `jfb` |
| **Sem licença de redistribuição do conjunto** | `patristic` | só trechos conferidos em edições PD |
| **PD — adventistas** | `egw-great-controversy`, `egw-patriarchs`, `egw-prophets`, `egw-acts`, `egw-object-lessons`, `egw-steps`, `egw-thoughts`, `smith-daniel` | autora † 1915, edições anteriores a 1929; **Verificar** edições; **[I] adequação doutrinária a revisar** (linha adventista, não evangélica reformada) |
| **PD — dicionários** | `sword-easton`, `sword-hitchcock`, `sword-isbe`, `sword-smith` | **Verificar:** `isbe` (edição de 1915?) |
| **PD — tópicos/referências** | `sword-nave`, `sword-torrey`, `sword-tsk` | |

**Pontos que o PLANNER deve decidir como tratar** (não decido eu): se as 46 entram como 46 linhas, se
as adventistas e patrísticas recebem `adequacao_doutrinaria = atencao`, e se as fontes que o
Didasko **não pretende ingerir** (ex.: Luther, Lightfoot) entram como `depende` ou `nao_entra`.

---

## 5. O que o PLANNER ainda precisa de uma resposta do ARQUITECT

Nenhuma destas eu fecho. Estão aqui porque **travam um "a confirmar"**:

1. **Dicionário de Paulo:** qual é a obra-origem e quem é o titular? (Eduardo provavelmente sabe
   de onde copiou.)
2. **Grudem `_PT` e `_PT_v1`:** quem traduziu? É tradução própria, da Vida Nova ou de terceiro?
3. **Sire, Clark, Edwards:** os `.md` são resumo/estudo próprio ou reprodução? O PDF do Edwards é
   da tradução de Rodrigo Reis de Faria (2015)?
4. **PDFs em `ESTUDOS_BIBLICOS/docs/`:** de quem são?
5. **`resumos-biblicos` do biblia-plataforma:** quem escreveu? Entram ou só inspiram?
6. **Licença do conteúdo do grafo do atlas:** o ARQUITECT quer pedir confirmação ao autor?
7. **Gatilho padrão para "a confirmar":** sugiro uma frase única (ex.: "confirmar titular e
   licença antes de qualquer exibição ao usuário"), para o CSV não ter 30 gatilhos diferentes.

---

## 6. Rastro (o que li)

Lido: `estudos/*/README.md`, `estudos/sensus/DATA_LICENSES.md` (integral), `data-manifest.json`,
`estudos/atlas-biblico/README.md` (tabela de fontes), `estudos/biblia-plataforma/docs/LICENCA-TEXTO-ACF.md`,
`estudos/estudos-biblicos/README.md` e `referencias/LEIA-ME.md`, `estudos/top-skills/CREDITOS.md`,
READMEs de Grudem, Doutrinas, Teologia, Sire, Clark, Edwards, `DADOS_EXTERNOS/openbible/README.md`,
`PASTOR_IA/rag/biblia/load_biblia.py`, cabeçalho dos 17 arquivos do Dicionário de Paulo.

**Não lido:** capítulos de Grudem, Sire, Clark e Edwards; conteúdo do atlas (`dados-*.js`) e dos resumos
do biblia-plataforma; PDFs (nenhum aberto); `ESTUDOS_BIBLICOS/docs/` além dos nomes.
Contagens de arquivos são de `find`/`ls`, sem filtro de binários.

---

## 7. Respostas do ARQUITECT (2026-10-17) e o que elas implicam para o CSV

> Respostas dadas pelo ARQUITECT às perguntas da seção 5. A coluna "efeito no CSV" é
> **sugestão** do AUXILIAR-ARCHITECT; a classificação final é do PLANNER.

| # | Pergunta | Resposta do ARQUITECT | Efeito no CSV (sugestão) |
|---|---|---|---|
| 1 | Obra-origem do Dicionário de Paulo | *Dicionário de Paulo e suas Cartas*, de **Gerald F. Hawthorne, Ralph P. Martin e Daniel G. Reid** | `fonte` = a obra; `titular` = os organizadores e a editora da edição (**editora ainda a confirmar**); `licenca = direito reservado`. O arquivo é **reprodução de terceiro** (site CETEP), então a procedência da cópia é parte da linha |
| 2 | Quem traduziu Grudem `_PT` e `_PT_v1` | **IA (Grok)** | `titular` da tradução: **sem titular humano**; obra-base: Grudem/Zondervan (tradução oficial: Vida Nova). `licenca_verificada = nao`. Ver alerta A |
| 3 | `.md` de Sire, Clark e Edwards | **Reprodução** (não resumo) | Linhas com `regime_exibicao` no máximo `integral_interno`. Ver alerta A. Edwards: separar obra (domínio público) de tradução (Rodrigo Reis de Faria, 2015) |
| 4 | PDFs em `docs/` | **Web — revista.fajopa.org** | `titular` = autores/revista; licença **a confirmar** (a página da revista costuma declarar a licença do periódico); gatilho: ler a política da revista |
| 5 | Resumos do biblia-plataforma | **Disponibilizados no GitHub** | Herdam a MIT do repositório (titular LoadCG **[I]**). **A autoria real (humano ou IA) segue sem resposta** — registrar em `observacoes`; o projeto fala em "gate de revisão humana", o que sugere rascunho por IA |
| 6 | Confirmar licença do grafo do atlas com o autor | **Não precisa** | `licenca = MIT (código) / conforme tabela de fontes (dados)`, `licenca_verificada = nao`, e em `observacoes`: "risco aceito pelo ARQUITECT em 2026-10-17" |
| 7 | Frase única de gatilho para "a confirmar" | *não respondida* | Proposta: **"confirmar titular e licença antes de qualquer exibição ao usuário"** |

### Alertas ao PLANNER

**A. Tensão com a ADR-012 (10.2), que o ARQUITECT precisa ver.**
A decisão 10.2 diz: *texto integral só para papel interno e **nunca em superfície do aluno***.
Mas o conteúdo atual do aluno nasce de uma tradução por IA do Grudem (34 capítulos, `content_md` do
`Study`) e há arquivos que são **reprodução** de Sire, Clark, Edwards e do Dicionário de Paulo.
**Não verifiquei** quanto texto do Grudem aparece literalmente na lição do aluno — pode ser
plano de estudo próprio, e não tradução. Essa verificação define se há conflito real. O inventário
**registra** o fato; ele não resolve a tensão. Quem decide (e eventualmente reabre a ADR-012) é o ARQUITECT.

**B. Tradução por IA não cria titular.**
Uma tradução gerada por IA de obra protegida não tem autor humano que a licencie, e continua
sendo derivada da obra original. Em `titular`, não colocar "Grok"; colocar a obra-base e deixar
`licenca_verificada = nao`.

**C. Reprodução de obra de terceiros no repositório.**
`regime_exibicao = integral_interno` é o teto defensável com o que se sabe; `nao_exibir` é o piso
seguro. O PLANNER escolhe, citando a ADR-012 10.2.

### Ainda em aberto

- Editora exata do Dicionário de Paulo (para o campo `titular`).
- Autoria dos resumos do biblia-plataforma.
- Frase única de gatilho (item 7) — falta o OK do ARQUITECT.

### 7.1 Atualizações de 2026-10-17 (segunda rodada)

- **Editora do Dicionário de Paulo:** **Edições Loyola** (informado pelo ARQUITECT). Fecha o `titular`
  do item 1: *Hawthorne, Martin e Reid (orgs.) / Edições Loyola*; `licenca = direito reservado`.
- **Verificação do alerta A (feita em leitura de código e arquivos):**
  - **[F]** O que o aluno vê hoje na lição é o `content_md` da `StudyVersion`, e o importador
    (`importar_estudo_dirigido.py`) o preenche com o **`plano-de-estudo.md`** de cada capítulo
    (Cap. 21: **4.727 bytes**), não com o texto do Grudem. O texto integral do capítulo (`estudo/…md`,
    **25.565 bytes**; `_PT_v1` no Grudem_Doutrina_Biblica) não é renderizado na lição.
  - **[F]** Não existe, no código da lição (`pages/lesson.py`, `states/aluno.py`), nenhum recurso
    "detalhar" / "ver completo". A única exibição de contexto é `current_question_context`
    (`pages/lesson.py:128`); **[?]** não verifiquei o que ele contém por questão.
  - **[F]** O texto do Cap. 21 em `estudo/` reproduz fielmente a prosa de Grudem (o mesmo
    parágrafo de abertura aparece em `docs/base/Capitulo_21/*_PT.md`).
  - **Conclusão:** hoje **não há conflito** com a ADR-012 10.2. **Passaria a haver** se o "detalhar"
    mostrasse ao aluno o texto integral do capítulo.

### 7.2 Decisão do ARQUITECT sobre o "detalhar" (2026-10-17)

**Decisão:** o "detalhar" da lição mostra ao aluno **trechos curtos com a fonte exibida**.
O texto integral de obra de terceiros **não** vai à superfície do aluno. É a aplicação direta da
ADR-012 10.2; **a ADR não muda**.

**Efeito no inventário (sugestão ao PLANNER):**
- Grudem, Sire, Clark, Edwards (tradução) e Dicionário de Paulo: `regime_exibicao = curto` para
  o que o aluno pode ver; o integral permanece só para papéis internos (`integral_interno`).
  Quando uma linha cobre os dois usos, registrar o regime mais restritivo para a superfície do aluno.
- Nenhuma linha nova de CSV nasce desta decisão; ela vira **requisito** das DEMs seguintes.

**Requisitos para as DEMs seguintes (não são desta DEM-A):**
1. A lição precisa de um recurso "detalhar" que **não existe hoje** (verificado em 7.1). É escopo
   de uma DEM futura (lição/busca), não da DEM-003.
2. O trecho exibido carrega a **fonte** (obra, capítulo) e, onde a licença exigir, a atribuição.
3. **"Curto" ainda não tem medida.** Para a SBTB, a página de direitos fixa um limite próprio para
   a ACF; para Grudem, Sire etc. nada está definido. O PLANNER deve propor uma medida objetiva
   (palavras ou % do capítulo) e o ARQUITECT fecha — pergunta aberta para a DEM de busca/lição.

### Ainda em aberto (após 7.2)

- Autoria dos resumos do biblia-plataforma.
- OK do ARQUITECT à frase única de gatilho para "a confirmar".
- Medida objetiva de "curto".
