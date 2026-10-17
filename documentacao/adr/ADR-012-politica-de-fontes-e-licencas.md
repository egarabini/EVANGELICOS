# ADR-012: Política de fontes e licenças do acervo

- **Status:** Accepted
- **Data:** 2026-10-17
- **Decisores:** ARQUITECT (Eduardo) — decisões 10.1 a 10.12 da OLPF; redação e política delegadas ao PLANNER (decisão 10.5)
- **Gatilho:** Novo Horizonte — nova frente: base de conhecimento e busca por assunto

---

## Contexto e Problema

O Didasko deixa de ser só "estudos" e passa a ter uma **base de conhecimento consultável**.
Isso traz para dentro do produto material de terceiros com licenças diferentes — CC BY,
CC BY-SA, uso não comercial, direito reservado — além do texto bíblico cuja licença nunca
foi confirmada (ADR-002).

Sem política, cada fonte seria uma decisão ad hoc e o risco cresceria a cada ingestão. A
OLPF (`documentacao/visao/OLPF-base-de-conhecimento-e-busca.md`) levantou 12 perguntas; esta
ADR fixa as respostas como lei e vale para **toda** ingestão futura.

## Decisão

| # | Pergunta | Decisão |
|---|---|---|
| 10.1 | Público do primeiro corte | **Coordenador e instrutor.** O aluno só depois, via assistente (DEM-E). |
| 10.2 | Limite de citação de obra de terceiros | **Trecho curto com a fonte exibida.** Texto **integral só para papel interno** (ADMIN, REVISOR, COORDENADOR, INSTRUTOR) e nunca em superfície do aluno. |
| 10.3 | CC BY-SA (share-alike) | **Aceito incorporar.** Cada registro derivado carrega a licença de origem; o derivado mantém a mesma licença. |
| 10.4 | Modelo comercial | **Sem lucro:** contribuição simbólica dos coordenadores para custear servidor. Fontes de uso **não comercial** são aceitas nesse regime; se houver lucro, saem (ver gatilhos). |
| 10.5 | ADR de política de fontes antes da DEM-A | **Sim — é esta ADR.** |
| 10.6 | Cânon | **Deuterocanônicos ficam fora.** 66 livros. |
| 10.7 | Linha doutrinária | **`lff`, `lff-en`, `lffe` e `sangue` ficam fora da base** (verificado: 8 pastas em `estudos/estudos-biblicos/`). |
| 10.8 | Mapa interativo em JavaScript | **Aceito abrir ADR** — ver [ADR-013](ADR-013-componente-de-mapa-em-javascript.md). |
| 10.9 | Original grego/hebraico | **Entra já no primeiro corte** (fontes abertas: SBL GNT e WLC em CC BY 4.0; MorphGNT em CC BY-SA 3.0). |
| 10.10 | Texto ACF 2007 | **Risco aceito:** citação hoje, confirmação da licença depois (ver gatilhos). |
| 10.11 | Resumo por IA | **Entra na busca**, com citação por afirmação; nada gerado é armazenado como conteúdo aprovado. |
| 10.12 | Modelos de classificação (Jev, Laya) | **Fora desta frente**; reavaliar na DEM-E. |

**As três interpretações do PLANNER foram confirmadas pelo ARQUITECT em 2026-10-17:**
"interno" = ADMIN, REVISOR, COORDENADOR e INSTRUTOR; fontes de uso não comercial **aceitas**
no regime sem lucro; registros BY-SA **marcados e contidos** na plataforma até parecer.

## O que NÃO entra (e por quê)

| Item | Motivo |
|---|---|
| `lff`, `lff-en`, `lffe`, `sangue` | linha doutrinária diferente — decisão 10.7 |
| `mapas-biblicos-e-panorama` | cópia de site comercial, imagens de terceiros com direito reservado |
| skill `jesus-cristo` (top-skills) | IA falando em primeira pessoa como Cristo — risco pastoral, sem ganho |
| Deuterocanônicos | fora do cânon adotado — decisão 10.6 |
| **Código** do `sensus` | AGPL-3: aproveita-se a ideia e o esquema, **jamais o código** |
| **Código** do `biblia-plataforma` (Expo/TS) | incompatível com a ADR-001 |
| Modelos Jev / Laya | sem caso de uso definido — decisão 10.12 |

## Riscos aceitos, cada um com gatilho de revisão

| Risco | Gatilho |
|---|---|
| **Texto ACF 2007 com licença não confirmada** (10.10) | Se a licença se mostrar restritiva: o corpus passa a **interno** e/ou a tradução é substituída. O texto nunca é redistribuído (ADR-002). |
| **CC BY-SA obriga derivados** (10.3) | Antes de **qualquer** distribuição pública de dados derivados de fonte BY-SA: parecer. Enquanto isso, esses registros ficam marcados e não saem da plataforma. |
| **Contribuição simbólica** (10.4) | Se deixar de ser custeio e passar a haver lucro: fontes não comerciais e de direito reservado são reavaliadas. |
| **Integral "só interno"** (10.2) | Se a interface expuser o integral ao aluno, ou se um dos papéis internos for extinto, o regime quebra e a regra precisa ser refeita. |

## Consequências

**Positivas**
- Uma fonte nova passa a ser uma linha de registro, não uma decisão nova.
- O risco jurídico fica localizado e rastreável — com gatilho, não com esperança.
- A atribuição exigida por licença (OpenBible, CC BY) vira requisito de sistema, não boa vontade.
- O princípio da ADR-003 se estende: **toda afirmação com fonte**, não só versículo.

**Negativas / trade-offs**
- **A decisão 10.9 amplia o primeiro corte**: a OLPF (§6.3 e §9) tratava original e léxico como "segundo momento"; agora o interlinear entra já. Isso aumenta a decomposição, não a reduz.
- O regime BY-SA obriga rastreio **por registro**, o que pesa no modelo de dados e na ingestão.
- O ACF é um risco vivo até a licença ser confirmada.

**Neutras / a observar**
- O acervo fica dividido por regime de exibição (curto / integral interno / atribuição obrigatória). É simples de modelar, mas não é opcional.

## Impacto nas DEMs

- **DEM-A (inventário)** — primeira aplicação: classificar cada fonte por licença, regime e adequação doutrinária.
- **DEM-B (registro de fontes e proveniência)** — precisa de campos: licença, condição de uso, atribuição exigida, versão/data.
- **DEM-C (ingestão do grafo)** — filtro de cânon (66 livros) obrigatório ao ingerir o atlas.
- **DEM-D (busca)** — a exibição obedece ao regime e mostra atribuição quando a licença exige.
- **ADR-002** — refinada no ponto do ACF: o risco agora é declarado e tem gatilho.
