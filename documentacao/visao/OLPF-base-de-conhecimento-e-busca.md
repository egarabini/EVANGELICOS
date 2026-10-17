# OLPF — Base de conhecimento bíblico e busca por assunto

> **Opportunity · Loss · Pain · Future**
> Autor: AUXILIAR-ARCHITECT (IA) · Destinatário: PLANNER · Aprovador: ARQUITECT (Eduardo)
> Data: 2026-10-17 · Status: **proposta para o PLANNER** — não é intent, não é PRD, não decide nada.
>
> Observação de nome: o pedido chamou este documento de "OPLR". O repositório usa **OLPF**
> (Opportunity, Loss, Pain, Future) — ver `ESTUDOS_BIBLICOS/PASTOR_IA/fases/fase-0-fundacao/olpf.md`.
> Adotei a mesma estrutura de quatro blocos para o PLANNER reconhecer o formato.

---

## 0. Como o PLANNER deve usar este documento

1. Este documento **alimenta** o `planner/intent.md` e o `planner/prd.md` de uma ou mais DEMs novas.
   Ele não os substitui.
2. Segundo o método, o **intent não leva stack, schema nem UX detalhada** (intent §9). Por isso as
   seções 6 a 9 abaixo são **subsídios do AUXILIAR-ARCHITECT**: servem para o PLANNER não
   redescobrir o que já foi levantado, e o PLANNER decide o que sobe para o intent, o PRD e o design.
3. Toda decisão que cabe ao ARQUITECT está na **seção 10 (perguntas abertas)**. O PLANNER lista e
   nunca responde.
4. Nada aqui contraria as ADRs 001 a 011. Onde há tensão, ela está marcada na seção 8.
5. **Regra do ARQUITECT para esta frente:** não se copia código de nenhum projeto de terceiros.
   Aproveitam-se **ideias, esquemas e aplicabilidade**, reescritos no stack do Didasko.

---

## 1. Opportunity — a oportunidade

O Didasko está formando, além dos estudos, uma **base de conhecimento bíblico ampla**. Ela já tem
ativos que raramente aparecem juntos numa plataforma de igreja:

| Ativo | Volume / estado | Onde está |
|---|---|---|
| Corpus bíblico (ACF 2007) indexado | 31.102 versículos, no ChromaDB | corpus local, `:ro`, não versionado (ADR-002) |
| Referências cruzadas (OpenBible, CC BY 4.0) | 344.799 pares; 29.364 versículos de origem; 66 livros | PostgreSQL (ADR-004) |
| Obra + capítulos + adendos | modelo Obra → Estudo (ADR-005); Fase 1 importada | PostgreSQL |
| Estudo aplicado com capítulos próprios e mapa de origem | 34 capítulos do Grudem em rascunho (DEM-202610-001, em EVAL) | PostgreSQL |
| Teologia sistemática (Grudem PT/EN), Dicionário de Paulo, Cosmovisão (Sire), outros | em Markdown | `ESTUDOS_BIBLICOS/*` |

Existe também um acervo de **estudos externos** (pasta `estudos/`, seis projetos) que traz ideias
maduras de **proveniência, grafo de conhecimento, hermenêutica por camadas e busca** (seção 5).

**A oportunidade:** transformar esse acervo de "arquivos e tabelas" em **conhecimento consultável**.
Um coordenador ou instrutor digita um **assunto em pauta** (ex.: "justificação", "aliança", "o Espírito
Santo na vida do crente") e recebe **material verificado, com a origem de cada item visível** —
versículos do corpus, passagens relacionadas, trechos de capítulos e adendos, verbetes, lugares,
pessoas e cronologia. Isso apoia o preparo de aulas e a escolha do que estudar.

O diferencial coerente com o projeto: a busca devolve **fonte, não opinião do modelo**. Mantém o
princípio inegociável do projeto — *a Escritura vem do corpus, nunca do modelo* (ADR-003).

---

## 2. Loss — o que se perde se não for feito

- **Conhecimento preso em arquivos.** O instrutor precisa saber em qual livro e capítulo está o
  assunto. Quem não conhece o acervo não o aproveita.
- **Trabalho duplicado.** O preparo de aula refaz buscas manuais em PDFs e Markdown a cada vez.
- **Proveniência frágil.** Sem um registro de fontes com licença e atribuição, o acervo cresce sem
  saber o que pode ser exibido, citado ou redistribuído. O risco jurídico (direitos autorais,
  CC BY-SA, uso não comercial) aumenta a cada fonte adicionada.
- **A DEM-001 fica subaproveitada.** Os capítulos próprios do estudo e o mapa de origem são a base
  natural de contexto para busca; sem a busca, viram só uma tela de leitura.
- **O assistente do aluno nasce sem alicerce.** A ideia de uma IA que ajuda o aluno (texto ou voz) só
  é segura se houver uma camada de recuperação confiável por baixo. Sem ela, a tentação é deixar o
  modelo responder de memória — o oposto da ADR-003.
- **Ideias valiosas ficam esquecidas** na pasta `estudos/`, sem triagem de licença e adequação
  doutrinária.

---

## 3. Pain — a dor atual

**Coordenador e instrutor**
- Não têm como perguntar "o que o acervo tem sobre X?". Navegam estudo por estudo.
- Não veem de relance de qual obra e capítulo um tema vem, nem quais passagens se relacionam.
- Não conseguem montar uma aula temática reunindo capítulos, versículos e verbetes dispersos.

**Revisor e admin**
- Não há onde registrar o **grau de confiança** de uma afirmação (atestado, provável, debatido) —
  o que existe é "aprovado ou não" por conteúdo (ADR-011).

**ARQUITECT**
- Não existe hoje um **inventário de fontes e licenças**: o que está no repositório, de quem é, o que
  pode ser exibido e o que não pode. Decidir o que entra na base depende disso.
- Há material em `estudos/` que **não pode ou não deve** entrar (seção 7), misturado com material
  aproveitável.

**Plataforma**
- Cada nova fonte exigiria um importador próprio, sem um contrato comum de dados.

---

## 4. Future — o futuro que queremos construir

Quando esta frente existir, o ARQUITECT deve conseguir confirmar, olhando a tela:

1. **Busca por assunto** para coordenador e instrutor: digita um tema e recebe resultados agrupados
   por tipo (Escritura, passagens relacionadas, capítulos da obra/estudo, adendos, verbetes,
   lugares, pessoas), **cada um com a origem exibida** (obra, capítulo, fonte).
2. **Toda afirmação rastreável.** Nenhum item aparece sem dizer de onde vem. Onde houver controvérsia
   (cronologia, rota do Êxodo, autoria), o sistema mostra o **grau de confiança** em vez de esconder o debate.
3. **Registro de fontes com licença.** Cada fonte tem licença, atribuição e condição de uso
   registradas, e a interface exibe a atribuição quando a licença exige.
4. **Material sem permissão não aparece.** Fonte de uso restrito (não comercial, direito reservado)
   só é exibida dentro do que a licença permite — ou não entra.
5. **Mapas e linha do tempo** alimentados por dados próprios e abertos (lugares, jornadas, eventos),
   ligados às passagens do estudo.
6. **Base pronta para o assistente do aluno** (fase posterior): a mesma camada de recuperação serve de
   contexto. Texto primeiro; voz depois, como camada separada.
7. **Nada do que já funciona regride**: lição do aluno, Escritura verificada, corpus intocado.

**Sinal de sucesso sugerido (para o PLANNER lapidar no intent):** o ARQUITECT digita um assunto real
e confere que (a) os resultados fazem sentido, (b) cada um mostra a origem, (c) a lição do Cap. 21
continua idêntica.

---

## 5. O que há em `estudos/` e o que se aproveita (ideia, não código)

Avaliação feita lendo README, documentos de licença e estruturas de dados. **Não foi lido o conteúdo
integral** de capítulos, verbetes e resumos. Itens marcados *a confirmar* dependem de checagem.

### 5.1 sensus — **modelo conceitual** (código AGPL-3: não copiar)

O que se aproveita como **ideia e esquema**:

- **Painel hermenêutico por camadas** para um trecho selecionado: texto, contexto literário, contexto
  histórico, língua original, intertextualidade, história da interpretação. Serve de **roteiro de
  agrupamento de resultados** da busca.
- **A IA só afirma citando a fonte.** Cada afirmação carrega um identificador de citação que aponta
  para o registro de origem. É a ADR-003 estendida a qualquer afirmação, não só a versículos.
- **Tabela de fontes com licença e atribuição por fonte**, e atribuição visível na interface.
- **Contrato de dados comum** por tipo de conhecimento. Tabelas conceituais observadas:
  `source`, `book`, `verse_text`, `text_division`, `token`, `lexicon_entry`, `commentary`,
  `dictionary_entry`, `entry_ref`, `xref`, `entity`, `entity_ref`, `meta`.
- **Um ingestor por fonte**, todos produzindo o mesmo formato intermediário antes de gravar.
- **"Nada gerado por IA é armazenado"**: princípio útil para a trilha de conteúdo aprovado (ADR-011).

Aplicabilidade ao Didasko: o PLANNER pode usar a **lista de tipos de conhecimento** acima para
decidir o recorte do primeiro corte (seção 9), reescrevendo tudo no stack do Didasko (Python,
SQLModel/PostgreSQL).

**Cuidados de licença** (do `DATA_LICENSES.md` do próprio projeto): dados com CC BY-SA 4.0
(share-alike) e uma fonte (Robertson) com restrição **não comercial**. O código é AGPL-3: por isso
nenhum trecho dele entra no Didasko.

### 5.2 atlas-biblico — **grafo de conhecimento com confiança** (código MIT)

O que se aproveita:

- **Afirmação como cidadã de primeira classe:** toda identificação, data ou localização carrega
  **fonte** e **grau de confiança** (atestado · provável · debatido · derivado).
- **Entidades:** pessoas, lugares, eventos, perícopes, jornadas, cronologia, genealogia.
- **Cobertura:** Gênesis 1–11, patriarcas, Êxodo, conquista e juízes, monarquia, reino dividido,
  exílio, Evangelhos, Atos, Cartas, Escritos e Profetas (um arquivo de dados por bloco).
- **Duas ideias de apresentação:** leitura corrente sempre visível com camadas opcionais por cima;
  e o debate declarado (ex.: rota do Êxodo, cronologia) em vez de escondido.
- **Guia de voz** que separa texto de especificação de texto de interface.

Aplicabilidade: importar o **conteúdo** (não a interface) como dados do Didasko, mantendo fonte e
confiança por registro. A licença MIT cobre o código; o conteúdo segue a tabela de fontes do próprio
atlas (*a confirmar registro a registro*).

Observação doutrinária: o atlas inclui texto de deuterocanônicos (cânon católico). Isso é decisão
editorial do ARQUITECT (pergunta 10.6).

### 5.3 estudos-biblicos — **dados de língua original** (aproveitamento parcial)

- Aproveitável: o **desenho** de interlinear (grego, hebraico, aramaico, siríaco) e as **fontes de
  dados abertas** que ele cita (SBL GNT e Westminster Leningrad Codex em CC BY 4.0; MorphGNT em
  CC BY-SA 3.0).
- **Não aproveitável como está:** os cadernos `lff` / `lff-en` ("Seja Feliz Para Sempre!" / "Enjoy Life
  Forever!") e `sangue`. Pelos títulos, parecem pertencer a outra linha doutrinária (material das
  Testemunhas de Jeová) — **inferência do AUXILIAR-ARCHITECT, não verificada no conteúdo**. O próprio
  repositório avisa que o material é de terceiros e deve permanecer privado.
- O fluxo LaTeX/PDF não se aplica ao Didasko.

### 5.4 biblia-plataforma — **ideias de produto** (código MIT, stack Expo/TypeScript)

- Planos de leitura com **reflexão e pergunta diária**; retomada persistente.
- Sequência de dias e medalhas (engajamento do aluno).
- Documentos de **plano técnico de busca** e de **auditoria de UX de visitante novo**.
- Alerta útil: o projeto registra que a **licença da cópia da ACF ainda não está confirmada** e que
  não se deve afirmar domínio público. O mesmo vale para o corpus ACF do Didasko (ver ADR-002).
- Stack Expo/TS é incompatível com a ADR-001 para a aplicação. Só **ideias** são reaproveitáveis.
- Resumos bíblicos: *a confirmar autoria e licença antes de qualquer uso.*

### 5.5 top-skills — **baixo valor para o produto**

- Skills de apoio a agentes (criar skill, gerar prompt, humanizar texto etc.). Úteis, no máximo, ao
  processo de desenvolvimento.
- **Não usar** a skill `jesus-cristo` no produto: ela faz a IA falar **em primeira pessoa como Jesus**.
  Numa plataforma pastoral, o risco de atribuir palavras a Cristo supera o ganho, mesmo com a regra
  de não inventar versículos.

### 5.6 mapas-biblicos-e-panorama — **não usar**

- É uma cópia de um site WordPress comercial ("BíbliaTeca Mapeada"), com imagens de terceiros e
  link de pagamento. Não ingerir. No máximo, referência de **o que** construir com dados próprios.

### 5.7 Quadro-resumo

| Pasta | Decisão sugerida | Natureza do aproveitamento |
|---|---|---|
| sensus | Aproveitar ideias e esquema | Modelo conceitual; **zero código** |
| atlas-biblico | Aproveitar ideias e **dados** | Grafo com confiança; conferir licença do conteúdo |
| estudos-biblicos | Aproveitar só interlinear | Ideia + fontes abertas; descartar cadernos `lff`/`sangue` |
| biblia-plataforma | Aproveitar ideias de produto | Planos, engajamento, busca |
| top-skills | Ignorar no produto | Apoio ao processo, no máximo |
| mapas-biblicos-e-panorama | Excluir | Direitos de terceiros |

---

## 6. Subsídios do AUXILIAR-ARCHITECT — o que a base de conhecimento precisa ter

> Não são requisitos. São as **capacidades** que a frente parece exigir; o PLANNER decide o que
> vira RF, o que é intent e o que é design.

**6.1 Registro de fontes**
Cada fonte do acervo com: identificação, autor/titular, licença, condição de uso (exibir trecho,
exibir integral, só interno, não comercial), atribuição exigida e versão/data. Toda linha de
conhecimento referencia sua fonte.

**6.2 Proveniência e confiança por afirmação**
Cada item da base (identificação, data, localização, verbete) carrega fonte e, quando aplicável, grau
de confiança (atestado · provável · debatido · derivado).

**6.3 Tipos de conhecimento, com contrato comum**
Escritura (corpus), passagem relacionada, capítulo/adendo de obra, capítulo de estudo, verbete,
entidade (pessoa, lugar, evento), jornada, cronologia, e — num segundo momento — léxico e original.

**6.4 Recuperação**
Busca por assunto que combina: igualdade para Escritura (ADR-003), busca textual no acervo e busca
semântica onde fizer sentido. A parte semântica precisa tratar **português e inglês** (parte do
acervo está em inglês).

**6.5 Apresentação com origem**
Resultados agrupados por tipo, com a origem visível e a atribuição quando exigida pela licença.

**6.6 Papéis**
Primeiro corte para **coordenador e instrutor** (público mais controlado). O aluno só consome por meio
do assistente, em fase posterior.

**6.7 Trilha de aprovação**
Conteúdo ingerido nasce em rascunho; só vira consultável com aprovação assinada e amarrada ao
conteúdo (ADR-011).

**6.8 Resumo gerado (opcional e posterior)**
Se houver resumo por IA, ele só pode afirmar o que está nos resultados recuperados e cita a fonte de
cada afirmação. Nada gerado é armazenado como conteúdo aprovado.

---

## 7. Restrições e riscos

**7.1 Licenças e direitos autorais**
- Cada fonte precisa de licença verificada **antes** de entrar. Há mistura de CC BY, CC BY-SA
  (share-alike), uso não comercial e direito reservado.
- **CC BY-SA:** incorporar dados com essa licença pode obrigar a distribuir derivados sob a mesma
  licença. O ARQUITECT precisa decidir o efeito sobre o banco do Didasko (pergunta 10.3).
- **Uso não comercial:** o Didasko é multi-tenant para igrejas e escolas. Se houver cobrança
  (SaaS pago), fontes não comerciais ficam fora (pergunta 10.4).
- **Obras de terceiros** (Grudem, Sire, Clark, Edwards): uso interno por coordenadores é diferente de
  exibir ou redistribuir trechos longos. Definir o limite de citação.
- **Texto ACF 2007:** licença a confirmar (ADR-002 já trata de não redistribuição).
- **Atribuição:** OpenBible exige crédito (CC BY).

**7.2 Doutrinário**
- Conteúdo de linha doutrinária diferente não entra na base sem decisão explícita do ARQUITECT.
- Nenhuma fala da IA em primeira pessoa como Cristo.

**7.3 LGPD**
- As perguntas dos alunos (fase do assistente) são dado pessoal. Nenhum serviço externo recebe
  pergunta ou dado do aluno; o LLM local recebe só a Escritura já recuperada, sem dado pessoal.

**7.4 Técnico**
- A VPS não tem GPU. Qualquer geração em linguagem natural roda em CPU (`gemma2:9b`); a busca em si
  deve ser leve.
- Cobertura bilíngue exige embeddings multilíngues.

**7.5 Escopo**
- Esta frente **não pode** reabrir a DEM-001 nem alterar a lição do aluno.

---

## 8. Relação com ADRs e DEMs existentes

| Item | Relação |
|---|---|
| ADR-001 (stack fixa) | Dados externos entram como **dados**, não como código. Mapa interativo em JavaScript pode exigir ADR nova. |
| ADR-002 (corpus local, não redistribuído) | A busca não pode expor o corpus além do permitido; trechos curtos com origem. |
| ADR-003 (Escritura por igualdade) | Pilar da busca: versículo sempre do corpus. Estende-se a "afirmação sempre com fonte". |
| ADR-004 (referências cruzadas e curadoria) | Já define tratamento das passagens relacionadas; reaproveitar o teto/curadoria. |
| ADR-005 (Obra + Adendos → Estudo) | A busca percorre obra, adendo e estudo conforme o mapa de origem. |
| ADR-008 (segredos) | Qualquer serviço externo exigiria chave; hoje fora do desenho. |
| ADR-010 (publicação por CI) | Entrega por PR; agente não publica. |
| ADR-011 (aprovação assinada) | Conteúdo ingerido nasce rascunho; consultável só após aprovação. |
| DEM-202610-001 | **Dependência leve:** capítulos próprios do estudo são a unidade de contexto. A frente nova começa **depois** do fechamento da DEM-001. |

**Possível ADR nova** (decisão do ARQUITECT, antes da DEM): política de fontes e licenças do acervo
(o que entra, em que condições, como a atribuição aparece).

---

## 9. Sugestão de decomposição em DEMs (ordem proposta)

> Sugestão. O PLANNER numera e escreve os intents.

1. **DEM-A — Inventário de fontes e política de licenças.** Cataloga o acervo (inclusive `estudos/`),
   classifica por licença e adequação doutrinária e fecha o que entra e o que não entra.
   Saída: registro de fontes + decisão sobre ADR de política de fontes.
2. **DEM-B — Registro de fontes e proveniência no sistema.** Modelo de fonte, atribuição e (quando
   aplicável) grau de confiança por registro; contrato comum de ingestão.
3. **DEM-C — Ingestão do grafo (lugares, pessoas, eventos, jornadas).** A partir de dados abertos e do
   conteúdo aproveitável do atlas; tudo em rascunho até aprovação.
4. **DEM-D — Busca por assunto para coordenador e instrutor.** Resultados agrupados por tipo, com
   origem visível. Só leitura.
5. **DEM-E (futura) — Assistente do aluno.** Texto primeiro; voz depois. Usa a DEM-D como contexto.
   Fora do escopo de agora; registrada para não se perder a ideia.

**Health metrics candidatos** (baseline atual, para o PLANNER confirmar no disco):
- suíte de testes verde (baseline: 82 testes na branch da DEM-001; 76 antes dela);
- lição do Cap. 21 continua com Escritura e passagens relacionadas;
- nada apagado: 39 estudos, 31.102 versículos, 344.799 referências cruzadas.

---

## 10. Perguntas abertas — só o ARQUITECT fecha

- [ ] **10.1 Público do primeiro corte.** Confirma coordenador + instrutor, e o aluno só depois, via assistente?
- [ ] **10.2 Limite de citação.** Quanto de obra de terceiros (Grudem etc.) a busca pode exibir (trecho curto com fonte? integral só interno?).
- [ ] **10.3 CC BY-SA.** Aceita incorporar dados share-alike, ou prefere só fontes sem essa obrigação?
- [ ] **10.4 Modelo comercial.** O Didasko será cobrado? Se sim, fontes de uso não comercial ficam fora.
- [ ] **10.5 ADR de política de fontes.** Quer que ela seja escrita antes da DEM-A?
- [ ] **10.6 Cânon.** Deuterocanônicos entram na base ou ficam fora por decisão editorial?
- [ ] **10.7 Linha doutrinária.** Confirma que os cadernos `lff`/`sangue` ficam fora da base?
- [ ] **10.8 Mapa interativo.** Aceita abrir ADR para um componente de mapa em JavaScript, ou o primeiro corte é só lista/tabela de lugares e jornadas?
- [ ] **10.9 Original (grego/hebraico).** Entra já no primeiro corte ou numa DEM posterior?
- [ ] **10.10 Texto ACF.** Quem confirma a licença do corpus ACF 2007 e quando?
- [ ] **10.11 Resumo por IA.** Entra na busca (com citação por afirmação) ou só depois?
- [ ] **10.12 Modelos de classificação (Jev, Laya).** Foram citados como candidatos. Sem caso de uso definido, ficam fora desta frente; reavaliar na DEM-E?

---

## 11. Fora de julgamento deste documento

Stack, nomes de tabela e coluna, telas detalhadas, escolha de modelo de IA, motor de busca e
decomposição em tarefas. Tudo isso é do PLANNER (spec e design) e do DEVS.

---

## 12. Rastro do levantamento (para o PLANNER verificar)

- Lido: `documentacao/visao/projeto.md`, ADRs 001–011 (índice), `perfil-do-projeto.md`, intent e
  briefing da DEM-001, `estudos/*/README.md`, `DATA_LICENSES.md` e `schema.sql` do Sensus,
  tabela de fontes do atlas, `ESTADO-DO-PROJETO.md` e `TODO.md` do biblia-plataforma,
  `CREDITOS.md` e skill `jesus-cristo` do top-skills.
- **Não lido integralmente:** capítulos e verbetes de `ESTUDOS_BIBLICOS/*`, dados do atlas,
  resumos do biblia-plataforma, `PASTOR_IA` além do README e do OLPF, `MCP-VOICE-FRAMEWORK.md` além do início.
- **Não verificado:** licença de cada registro de conteúdo do atlas; autoria dos resumos; conteúdo
  dos cadernos `lff`/`sangue`; licença do texto ACF.
