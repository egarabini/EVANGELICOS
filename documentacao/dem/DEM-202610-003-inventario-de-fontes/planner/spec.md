# Spec — DEM-202610-003 / inventário de fontes

> Dono: PLANNER. Cada capacidade cita um **outcome** (intent §2), um **non-goal**
> (§4 Out) ou uma **constraint** (§5). Capacidade órfã = a spec inflou.

## 1. Referência

PRD: [`prd.md`](prd.md) · Intent: [`intent.md`](intent.md) — **signed** em 2026-10-17
ADRs: **012** (política de fontes, rege cada linha) · 002 (corpus) · 004 (referências)

## 2. Requisitos funcionais

- [ ] **RF01:** O inventário é um **CSV UTF-8 com BOM**, delimitado por `;`, com as colunas
      do §4. O BOM é obrigatório para o Excel em português não corromper acentos.
      — *(intent §2 · §8.1)*
- [ ] **RF02:** A granularidade é **uma linha por FONTE** — não por projeto, não por
      artefato genérico. Regras:
      (a) cada fonte de dados declarada por um projeto tem a sua linha (as do Sensus são
      ~46, uma cada); (b) o **código** de um projeto é linha própria, separada dos dados,
      quando o regime difere; (c) material de terceiro dentro de acervo de terceiro é
      linha própria com o regime mais restritivo. — *(intent §4 In · §2)*
- [ ] **RF03:** Toda linha traz **licença** identificada ou a marca `a confirmar`; nesse
      caso, `observacoes` é obrigatório e contém os **três elementos do §6.3** (o que
      verificar, com quem, quando). — *(intent §5 · ADR-012)*
- [ ] **RF04:** Toda linha traz **regime de exibição** ∈ `{curto, integral_interno,
      nao_exibir}`, escolhido pelos critérios do §6.1. — *(intent §2 · ADR-012 10.2)*
- [ ] **RF05:** Toda linha traz **decisão** ∈ `{entra, nao_entra, depende}`, pelos
      critérios do §6.2; quando não é `entra`, `motivo` é obrigatório. — *(intent §2)*
- [ ] **RF06:** Nenhuma linha contradiz as 12 decisões da ADR-012. — *(intent §5)*
- [ ] **RF07:** `adequacao_doutrinaria` ∈ `{ok, atencao, fora, a_revisar}`, preenchida pelo
      PLANNER pelos critérios do §6.4 e **marcada como pendente de revisão** do ARQUITECT.
      — *(intent §8.3)*
- [ ] **RF08:** Fontes **internas** e **externas** na mesma tabela, com o mesmo peso.
      — *(intent §8.2)*
- [ ] **RF09:** O inventário vive em `documentacao/fontes/inventario.csv`, com
      `documentacao/fontes/README.md` explicando colunas, critérios e manutenção.
      — *(intent §4 In)*
- [ ] **RF10:** As **exclusões conhecidas** aparecem como `nao_entra` **com motivo** —
      não desaparecem do inventário. Lista completa:
      `lff`, `lff-en`, `lffe`, `sangue` (10.7) · `mapas-biblicos-e-panorama` (direito de
      terceiro) · deuterocanônicos (10.6) · skill `jesus-cristo` (10.7/risco pastoral) ·
      **código do Sensus** (AGPL-3.0) · **código do `biblia-plataforma`** (Expo/TS —
      ADR-001) · fluxo LaTeX do `estudos-biblicos` · **modelos Jev e Laya** (10.12 —
      reavaliar na DEM-E). — *(intent §4 In · ADR-012)*

## 3. Requisitos não funcionais

- **Cobertura:** 100% dos itens do **Anexo A** (lista de referência fechada). Item do Anexo
  A sem linha = FAIL.
- **Consistência:** os enums do §4 só aceitam os valores declarados; valor fora do conjunto
  = FAIL (CA06).
- **Legibilidade:** abre em Excel PT-BR **sem corromper acentos** (BOM presente) e em
  editor de texto.
- **Rastreabilidade:** cada linha cita a ADR ou a decisão que a rege, quando existir.
- **Estabilidade:** versionado no git; alterar linha é mudança documentada.

## 4. Contrato do arquivo (CSV)

UTF-8 **com BOM**, delimitador `;`, cabeçalho obrigatório:

| Coluna | Obrigatório | Domínio de valores |
|---|---|---|
| `id` | sim | `F-001`… único |
| `fonte` | sim | nome legível |
| `tipo` | sim | `corpus` `referencia_cruzada` `obra` `adendo` `fonte_dados` `codigo` `conteudo` `ferramenta` |
| `titular` | sim | quem detém o direito, ou `a confirmar` |
| `licenca` | sim | ex.: `CC BY 4.0`, `CC BY-SA 4.0`, `AGPL-3.0`, `MIT`, `direito reservado`, `uso interno`, `a confirmar` |
| `licenca_verificada` | sim | `sim` `nao` |
| `regime_exibicao` | sim | `curto` `integral_interno` `nao_exibir` |
| `atribuicao_exigida` | sim | texto a exibir, ou `nao` |
| `versao_data` | sim | versão/edição ou data |
| `adequacao_doutrinaria` | sim | `ok` `atencao` `fora` `a_revisar` |
| `decisao` | sim | `entra` `nao_entra` `depende` |
| `motivo` | quando `decisao` ≠ `entra` | motivo objetivo |
| `localizacao` | sim | caminho no repositório, ou `fora do git` |
| `adr_referencia` | não | `ADR-002`, `ADR-004`, `ADR-012 10.7`… |
| `observacoes` | quando `licenca = a confirmar` | o quê + com quem + quando (§6.3) |
| `revisado_por` | não | vazio até a revisão do ARQUITECT |
| `revisado_em` | não | `AAAA-MM-DD` |

## 5. Modelo do dado (lógico)

Uma **tabela de fontes**, embrião do registro que a DEM-B vai persistir. A unidade é a
**fonte licenciada**, não o projeto: é o que permite decidir exibição por fonte e é o que a
DEM-C precisa na hora de ingerir.

## 6. Critérios de classificação (tornam RF04/05/07 objetivos)

### 6.1 `regime_exibicao`

| Valor | Quando |
|---|---|
| `curto` | a licença permite exibir **trecho curto com atribuição** em superfície de aluno/coordenador |
| `integral_interno` | o texto integral só pode circular entre os quatro papéis internos (obra de terceiro, licença restritiva, ou **licença a confirmar**) |
| `nao_exibir` | a licença ou a decisão doutrinária impede qualquer exibição; o material existe como dado não exibível |

**Precedência:** na dúvida entre dois regimes, **o mais restritivo**.

### 6.2 `decisao`

| Valor | Quando |
|---|---|
| `entra` | a licença permite (ao menos internamente) **e** a doutrina não é `fora` |
| `nao_entra` | a licença proíbe, a doutrina é `fora`, ou há decisão explícita do ARQUITECT |
| `depende` | falta licença (`a confirmar`) **ou** falta a decisão doutrinária |

### 6.3 Gatilho de revisão (obrigatório quando `licenca = a confirmar`)

`observacoes` deve conter, nesta ordem: **(1) o que** verificar · **(2) com quem** (titular,
fonte, detentor) · **(3) quando** (ex.: "antes de exibir ao aluno", "antes da DEM-C").
Faltando qualquer um dos três → FAIL no CA07.

### 6.4 `adequacao_doutrinaria`

| Valor | Quando |
|---|---|
| `ok` | sem tensão identificada com o material do projeto |
| `atencao` | tradição diferente, ponto controverso ou autor de linha distinta que **o ARQUITECT aceita com ressalva** |
| `fora` | linha doutrinária já excluída por decisão (10.6, 10.7) |
| `a_revisar` | o PLANNER não conseguiu classificar com segurança (autor desconhecido, conteúdo não lido) |

> O PLANNER preenche (10.8.3) e o ARQUITECT revisa. **`a_revisar` é resposta honesta, não
> falha**: inventário que finge saber é pior que inventário que declara a dúvida.

## 7. Edge cases

- **Licença desconhecida** → `a confirmar` + `licenca_verificada = nao` + gatilho (§6.3).
- **Projeto com licença de código diferente da de dados** → linhas separadas (RF02b).
- **Titular desconhecido** → `titular = a confirmar` com motivo.
- **Fonte que não entra** → linha `nao_entra` com motivo (não desaparece).
- **Material de terceiro dentro de projeto de terceiro** → linha própria, regime mais restritivo.
- **Deuterocanônicos** → linha `nao_entra`, `adequacao_doutrinaria = fora`, motivo "cânon (10.6)",
  mesmo dentro do atlas que inclui os sete livros.
- **Autor de linha doutrinária distinta** (ex.: EGW no acervo do Sensus) → linha própria com
  `atencao` ou `fora` conforme a revisão do ARQUITECT; **nunca diluída no projeto**.

## 8. Critérios de aceitação

- [ ] **CA01:** o CSV abre em Excel PT-BR **sem corromper acentos** (BOM presente) e em
      editor; todas as colunas obrigatórias preenchidas.
- [ ] **CA02:** **todo item do Anexo A** tem linha — conferência item a item.
- [ ] **CA03:** toda linha com `decisao ≠ entra` tem `motivo` não vazio.
- [ ] **CA04:** zero linhas contradizendo a ADR-012 (conferência das 12 decisões).
- [ ] **CA05:** fontes internas e externas no mesmo CSV.
- [ ] **CA06:** todo valor dos enums pertence ao conjunto fechado (§4/§6).
- [ ] **CA07:** toda linha com `licenca = a confirmar` tem o gatilho completo (§6.3).

---

## Anexo A — lista de referência fechada (é contra esta lista que o CA02 confere)

### A.1 Corpus e dados bíblicos
| Fonte | Licença esperada | Onde |
|---|---|---|
| Texto bíblico ACF 2007 | `a confirmar` (ADR-012 10.10) | cópia na VPS, **fora do git** |
| Comentários Matthew Henry (PT) | `a confirmar` | ChromaDB / corpus |
| Referências cruzadas OpenBible.info | CC BY 4.0 | PostgreSQL (ADR-004) |

### A.2 Obra e adendos
| Fonte | Licença esperada | Onde |
|---|---|---|
| Doutrinas Cristãs — Grudem (PT, tradução) | direito reservado | `DOUTRINAS_CRISTAS/docs/base` |
| Doutrinas Cristãs — Grudem (EN) | direito reservado | `DOUTRINAS_CRISTAS/estudo` |
| Adendos de admin/revisor | uso interno | banco (tabela `adendo`) |

### A.3 Fontes internas (mesmo peso das externas — 8.2)
`Cosmovisão` (Sire) · `Dicionário de Paulo` · `Clark` · `Edwards` — todas **direito reservado / uso interno**, em `ESTUDOS_BIBLICOS/*`.

### A.4 Sensus — **código** e **cada fonte de dados**
- **Código** (`estudos/sensus`) — AGPL-3.0 → `nao_entra` (nenhum trecho é copiado).
- **Fontes de dados** — uma linha por id declarado em `estudos/sensus/DATA_LICENSES.md` §2.
  Autoridade da lista: **aquele arquivo**. Os ids na data desta spec:
  - *Clássicos / domínio público / várias tradições:* `gill`, `patristic`, `smith-daniel`,
    `sword-abbott`, `sword-barnes`, `sword-burkitt`, `sword-calvincommentaries`,
    `sword-catena`, `sword-clarke`, `sword-easton`, `sword-hitchcock`, `sword-isbe`,
    `sword-jfb`, `sword-kd`, `sword-lightfoot`, `sword-luther`, `sword-mhc`, `sword-nave`,
    `sword-pnt`, `sword-scofield`, `sword-smith`, `sword-tfg`, `sword-torrey`,
    `sword-tsk`, `sword-wesley`
  - *Ellen G. White (linha adventista):* `egw-acts`, `egw-great-controversy`,
    `egw-object-lessons`, `egw-patriarchs`, `egw-prophets`, `egw-steps`, `egw-thoughts`
  - *STEP Bible / Tyndale House (CC BY 4.0):* `tagnt`, `grc-tr`, `tahot`,
    `stepbible-tbesg`, `stepbible-tbesh`, `stepbible-tflsj`, `stepbible-tipnr`
  - *Texto bíblico:* `blivre`, `kjv`, `hbo-wlc`
  - *CC BY-SA 4.0:* `theographic` · *CC BY 4.0 OpenBible:* `openbible-geo`, `openbible-xref`
  - *Não comercial:* `sword-rwp` (Robertson's Word Pictures — restrição declarada)

### A.5 Atlas bíblico — código e conteúdo
- **Código** (`estudos/atlas-biblico`) — MIT; aproveitamos **ideia e dados**, não código.
- **Conteúdo** — fontes declaradas na tabela "Fontes e licenças de conteúdo" do
  `estudos/atlas-biblico/README.md` (autoridade da lista), **registro a registro a confirmar**.
- **Deuterocanônicos** — `nao_entra` (10.6).

### A.6 `estudos-biblicos` — língua original e cadernos
- **SBL GNT** (CC BY 4.0) · **Westminster Leningrad Codex** (CC BY 4.0) ·
  **MorphGNT** (CC BY-SA 3.0) — entram no primeiro corte (10.9).
- **Cadernos `lff`, `lff-en`, `lffe`, `sangue`** — `nao_entra` (10.7).
- **Fluxo LaTeX/PDF** — `nao_entra` (ferramenta de outro stack).

### A.7 `biblia-plataforma`, `top-skills`, `mapas-biblicos-e-panorama`
- **Código `biblia-plataforma`** (Expo/TS) — `nao_entra` (ADR-001).
- **Resumos do `biblia-plataforma`** — `a confirmar` (autoria e licença).
- **Skills do `top-skills`** — `nao_entra` no produto; no máximo apoio ao processo.
- **Skill `jesus-cristo`** — `nao_entra` (risco pastoral).
- **`mapas-biblicos-e-panorama`** — `nao_entra` (direito de terceiros).

### A.8 Modelos de classificação
- **Jev** e **Laya** — `nao_entra` nesta frente; reavaliar na DEM-E (10.12).
