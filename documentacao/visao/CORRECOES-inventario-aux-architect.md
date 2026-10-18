# Correções propostas ao `inventario.csv` (DEM-202610-003)

> Autor: AUXILIAR-ARCHITECT (IA) · Para: PLANNER · Data: 2026-10-17
> Base: `documentacao/fontes/inventario.csv` (79 linhas, hash `17fc665`, EVAL rodada 2 PASS) comparado
> com o que está **no disco** e com as respostas do ARQUITECT em
> `LEVANTAMENTO-FONTES-aux-architect.md`, seções 7, 7.1 e 7.2.
>
> **Só leitura.** Nenhuma célula foi alterada por mim. O PLANNER aplica, confere e reenvia ao EVAL.
> Certeza: **A** = lido no disco ou dito pelo ARQUITECT · **B** = inferência minha, confirmar.

## 0. Por que estas correções existem

A estrutura do CSV está correta (campos, enums, regra do §6.1, 46 ids do Sensus). O EVAL e o
verificador conferem **forma**. Os itens abaixo são de **identidade e fato** — o que cada linha
*diz ser* — e só se pega comparando com o disco. Dois deles mudam a classificação.

---

## 1. Erros de fato (aplicar)

| # | Linha | Campo | Valor atual | Valor proposto | Evidência | Certeza |
|---|---|---|---|---|---|---|
| 1 | **F-009** | `fonte` | "Clark - comentário bíblico" | "Clark — *Deus e o Mal: O Problema Resolvido*" | `ESTUDOS_BIBLICOS/DEUS_E_O_MAL_GORDON_CLARK/README.md` (8 arquivos, autor Gordon H. Clark) | A |
| 2 | F-009 | `titular` | "Adam Clarke (1762-1832) / tradução (a identificar)" | "Gordon H. Clark (1902-1985) / editora da edição (a identificar)" | idem. **Adam Clarke** é outra pessoa e já tem linha própria: **F-030** (Sensus, `sword-clarke`) | A |
| 3 | F-009 | `adequacao_doutrinaria` | `atencao` | **`a_revisar`** (o PLANNER reavalia) | Clark é calvinista (README: "Calvinismo bíblico … Confissão de Westminster"). A nota "metodista/arminiana" descreve Adam Clarke, não Gordon Clark. A justificativa do `atencao` não vale mais | A |
| 4 | F-009 | `observacoes` | "tradição metodista/arminiana: …" | substituir por: "reprodução de obra de terceiro (confirmado pelo ARQUITECT, 17/10); integral só interno; 'curto' é o que o aluno vê" | resposta do ARQUITECT, 7 | A |
| 5 | **F-010** | `fonte` | "Edwards - obras selecionadas" | "Edwards — *O Fim para o qual Deus criou o mundo*" | `JONATHAN_EDWARDS_…/README.md`: uma obra, 5 capítulos | A |
| 6 | F-010 | `titular` | "Jonathan Edwards (1703-1758) / tradução (a identificar)" | "Obra: Jonathan Edwards (domínio público). Tradução: Rodrigo Reis de Faria (2015)" | README do diretório cita a tradução e o PDF | A |
| 7 | F-010 | `licenca` | `direito reservado` | **`direito reservado (tradução)`** — ou dividir em duas linhas: obra (domínio público) e tradução (direito reservado), como a spec §6 prevê para "licenças que diferem" | spec RF02 | A |
| 8 | **F-005** | `titular` | "Wayne Grudem / Crossway (a confirmar)" | "Wayne Grudem / Zondervan (1994)" | `TEOLOGIA_SISTEMATICA/README.md` linhas 175-176: "Editora original: Zondervan (1994) · Tradução: Editora Vida Nova" | A |
| 9 | F-005 | `localizacao` | `DOUTRINAS_CRISTAS/estudo` | `Grudem_Doutrina_Biblica/Capitulo_NN/*_EN.md` (fonte de verdade) e `DOUTRINAS_CRISTAS/docs/base/Capitulo_NN/*_EN.md` | os arquivos `_EN.md` estão em `Capitulo_NN/`; `DOUTRINAS_CRISTAS/estudo/` contém só pastas `Capitulo_NN` de estudo | A |
| 10 | **F-004** | `titular` | "Wayne Grudem / editora da tradução (a identificar)" | "Obra: Wayne Grudem / Zondervan. **Tradução PT: gerada por IA (Grok) — sem titular humano**" | resposta do ARQUITECT, 7 | A |
| 11 | F-004 | `observacoes` | "A titularidade da tradução PT ainda não foi identificada." | "Tradução por IA (Grok) de obra protegida: sem titular da tradução; derivada da obra de Grudem (tradução oficial: Vida Nova). Verificar com Zondervan/Vida Nova antes de qualquer uso além de 'curto'." | resposta do ARQUITECT, 7 | A |
| 12 | F-004 | `localizacao` | `DOUTRINAS_CRISTAS/docs/base` | `Grudem_Doutrina_Biblica/Capitulo_NN/*_PT.md` e `*_PT_v1.md` (fonte de verdade); `DOUTRINAS_CRISTAS/docs/base/` (derivada) | `Grudem_Doutrina_Biblica/README.md`: "esta árvore é a FONTE DE VERDADE" | A |
| 13 | **F-008** | `titular` | "Editora da tradução (a identificar)" | "Gerald F. Hawthorne, Ralph P. Martin e Daniel G. Reid (orgs.) / **Edições Loyola**" | resposta do ARQUITECT, 7.1 | A |
| 14 | F-008 | `observacoes` | "A titularidade da tradução PT ainda não foi identificada." | "Arquivos são cópia de páginas do site CETEP (Teologia e Psicanálise), não da edição impressa: 5 em HTML bruto, 11 convertidos, 1 em Markdown. Cópia de terceiro de obra protegida; sem autorização conhecida." | `DICIONARIO_PAULO_CARTAS/*.md` (cabeçalhos) | A |
| 15 | F-008 | `localizacao` | "ESTUDOS_BIBLICOS (localização exata a confirmar)" | `ESTUDOS_BIBLICOS/DICIONARIO_PAULO_CARTAS/` (17 arquivos, ~1,1 MB) | `ls` | A |
| 16 | **F-007** | `localizacao` | "ESTUDOS_BIBLICOS (…a confirmar)" | `ESTUDOS_BIBLICOS/COSMOVISAO_JAMES_SIRE/` (4 arquivos) | `ls` | A |
| 17 | F-007 | `titular` | "James Sire / editora da tradução (a identificar)" | "James W. Sire / Editora Hagnos (*O Universo ao Lado*)" | README do diretório | A (editora) |
| 18 | F-009, F-010 | `localizacao` | "ESTUDOS_BIBLICOS (…a confirmar)" | respectivamente `…/DEUS_E_O_MAL_GORDON_CLARK/` e `…/JONATHAN_EDWARDS_O_FIM_PARA_O_QUAL_DEUS_CRIOU_O_MUNDO/` | `ls` | A |

> Regra geral para a coluna `localizacao`: onde o caminho existe no repositório, **escrever o caminho**.
> "a confirmar" na `localizacao` só vale quando o material está fora do git.

---

## 2. Linhas que parecem faltar (acrescentar)

Conferi as 33 linhas não-Sensus. Não achei linha para os artefatos abaixo. Todos existem no disco.

| Artefato proposto | Onde está | O que se sabe | Sugestão de campos |
|---|---|---|---|
| **Grafo de dados do atlas** (`dados-*.js`, 12 arquivos: pessoas, lugares, jornadas, cronologia, com fonte e confiança) | `estudos/atlas-biblico/dados*.js` | README: "conteúdo de terceiros conforme tabela de fontes"; o ARQUITECT decidiu **não** consultar o autor (7) | `licenca = MIT (código do repositório); dados conforme tabela de fontes`, `licenca_verificada = nao`; `observacoes`: "risco aceito pelo ARQUITECT em 17/10"; `decisao = depende` (DEM-C) |
| **PDFs e textos em `ESTUDOS_BIBLICOS/docs/`** — escatologia paulina (PDF), dons do Espírito (PDF + MD), Paulo/história da Igreja (MD) | `ESTUDOS_BIBLICOS/docs/` | origem: **revista.fajopa.org** (resposta do ARQUITECT, 7) | `titular = autores / revista FAJOPA`, `licenca = a confirmar`, gatilho padrão; `regime = integral_interno`; **verificar a política de licença da revista** |
| **Planos de estudo dirigido** (`plano-de-estudo.md`, 34) — o que o aluno vê | `ESTUDOS_BIBLICOS/DOUTRINAS_CRISTAS/estudo_dirigido/capitulo_NN/` | é o `content_md` da lição (verificado, 7.1); derivam do Grudem | `titular = Didasko (material próprio, derivado de Grudem)`; `regime = curto`; `observacoes`: "o texto integral do capítulo não é renderizado na lição" |
| **Árvore `TEOLOGIA_SISTEMATICA/`** (133 arquivos, derivada) e **`Grudem_Doutrina_Biblica/`** (450, fonte de verdade) | `ESTUDOS_BIBLICOS/` | README do Grudem declara qual é canônica e quais são derivadas | ou linha própria, ou citar nas `observacoes` de F-004/F-005 |
| **Tiles/serviços de mapa** (OpenFreeMap, OpenStreetMap ODbL, OpenMapTiles CC BY 4.0) | `estudos/sensus/DATA_LICENSES.md` §2.8 | só relevantes se o Didasko adotar mapa (ADR-013) | `decisao = depende`, gatilho: ADR-013 |
| **PDF da tradução do Edwards** | `JONATHAN_EDWARDS_…/…pdf` | tradução de Rodrigo Reis de Faria (2015) | se F-010 for dividida (item 7), é a linha de "tradução" |

---

## 3. Linhas para ajustar (menores)

| Linha | Problema | Proposta | Certeza |
|---|---|---|---|
| **F-075** (`top-skills`) | Mistura licenças diferentes numa linha, contra a RF02 (uma linha por artefato quando a licença difere) | Dividir: (a) `book-to-skill`, `humanizer`, `last30days`, `notebooklm` — **MIT**, autores nomeados em `CREDITOS.md`; (b) `criar-skill-ouro`, `gerador-de-prompt`, `elliott-jaques` — **"a fonte não especificava licença"** | A |
| **F-076** (`jesus-cristo`) | `licenca = "MIT (a confirmar)"`; o `CREDITOS.md` diz que a skill **não tem licença especificada** | `licenca = a confirmar`, observação: "sem licença especificada na origem" | A |
| **F-068 a F-071** (`lff`, `lff-en`, `lffe`, `sangue`) | `titular = "Testemunhas de Jeová (titular a confirmar)"` apresenta como fato o que é **inferência** minha pelo título | Prefixar a observação: "titular **inferido pelo título**; o repositório só diz 'publicações estudadas, © dos detentores'" | B |
| **F-002** (Matthew Henry, "tradução PT", no ChromaDB) | Não encontrei essa fonte no disco; o Sensus tem Matthew Henry em **inglês** (F-033). Pode ser uma tradução que não localizei | Pedir à origem a indicação: quem traduziu e onde está. Até lá, manter `a confirmar` com gatilho | B |
| **F-066** (WLC) | `titular = "Westminster Hebrew Seminary / J. Alan Groves Center"` — o README do `estudos-biblicos` diz só "Westminster Leningrad Codex, CC BY 4.0" | Manter como proposta do PLANNER, mas marcar na observação "titular conforme o projeto WLC, não confirmado no repositório" | B |
| **F-078, F-079** (Jev, Laya) | Titulares ("TypeSafe", "Convai") vieram de uma tabela colada no chat, não verificada | `titular = a confirmar`; observação: "citados como candidatos; origem do dado não verificada" | A |
| **F-074** (resumos do biblia-plataforma) | O ARQUITECT disse "disponibilizado no GitHub" | Pode registrar `licenca = MIT (herdada do repositório; autoria dos resumos não confirmada)`; mantém `depende` | B |

---

## 4. Sugestão para o verificador (`verificar_inventario.py`)

O defeito que o EVAL achou na rodada 1 foi *"verificador escrito de memória"*. O de agora repete a classe:
ele valida **forma**, não **identidade**. Há uma checagem mecânica barata que teria pegado a maior parte
do §1:

1. **Existência do caminho.** Para toda linha cuja `localizacao` aponta para o repositório
   (`ESTUDOS_BIBLICOS/…`, `estudos/…`, `DOUTRINAS_CRISTAS/…`), o caminho **precisa existir**. Falha
   para valor genérico do tipo "a confirmar" quando o material está no git.
2. **Duplicidade de autor.** Dois ids com o mesmo sobrenome de autor (F-009 "Clark" × F-030 "Clarke")
   merecem um aviso para revisão humana.
3. **Cobertura inversa.** Listar os diretórios de primeiro nível de `ESTUDOS_BIBLICOS/` e de `estudos/`
   e exigir ao menos uma linha por diretório. Isso pegaria `docs/` e o grafo do atlas ausentes.

Nenhuma dessas verifica *verdade*; elas só reduzem o espaço onde o erro se esconde. A identidade
continua dependendo de alguém comparar com a fonte, que é o que este documento fez.

---

## 5. O que fica em aberto (não é do PLANNER resolver)

- Autoria dos resumos do biblia-plataforma.
- Medida objetiva de **"curto"** (palavras ou % do capítulo).
- Ordem da `revisado_por` / `revisado_em`: o ARQUITECT ainda não revisou nenhuma linha (79/79 vazias).
- Política de licença da revista FAJOPA.

## 6. Rastro

Lido: `documentacao/fontes/inventario.csv` (completo, 79 linhas), `eval/jornada-rodada2.md` (início),
`DEUS_E_O_MAL_GORDON_CLARK/README.md`, `JONATHAN_EDWARDS_…/README.md`, `COSMOVISAO_JAMES_SIRE/README.md`,
`TEOLOGIA_SISTEMATICA/README.md` (editora), `Grudem_Doutrina_Biblica/README.md`, listagens de
`DOUTRINAS_CRISTAS/`, `ESTUDOS_BIBLICOS/docs/`, `estudos/top-skills/CREDITOS.md`.
**Não lido:** conteúdo dos capítulos, dos PDFs e dos 12 arquivos `dados-*.js` do atlas.
