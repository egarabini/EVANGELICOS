# Spec — DEM-202610-003 / inventário de fontes

> Dono: PLANNER. Cada capacidade cita um **outcome** (intent §2), um **non-goal**
> (§4 Out) ou uma **constraint** (§5). Capacidade órfã = a spec inflou.

## 1. Referência

PRD: [`prd.md`](prd.md) · Intent: [`intent.md`](intent.md) — **signed** em 2026-10-17

## 2. Requisitos funcionais

- [ ] **RF01:** O inventário é um **CSV UTF-8**, delimitado por `;`, com as colunas do §4.
  — *(intent §2 · §8.1)*
- [ ] **RF02:** Toda fonte do acervo tem **uma linha por artefato** — código e dados são
  linhas separadas quando as licenças diferem. — *(intent §4 In · §2)*
- [ ] **RF03:** Toda linha traz **licença** identificada ou a marca `a confirmar`, e nesse
  caso um **gatilho de revisão** na coluna `motivo`/`observacoes`. — *(intent §5 · ADR-012)*
- [ ] **RF04:** Toda linha traz **regime de exibição** ∈ `{curto, integral_interno, nao_exibir}`.
  — *(intent §2 · ADR-012 10.2)*
- [ ] **RF05:** Toda linha traz **decisão** ∈ `{entra, nao_entra, depende}`; quando a decisão
  não é `entra`, o **motivo** é obrigatório. — *(intent §2)*
- [ ] **RF06:** Nenhuma linha contradiz as 12 decisões da ADR-012. — *(intent §5)*
- [ ] **RF07:** A coluna de **adequação doutrinária** é preenchida pelo PLANNER e marcada
  como pendente de revisão do ARQUITECT. — *(intent §8.3)*
- [ ] **RF08:** Fontes **internas** (Grudem, Sire, dicionários) têm o **mesmo peso** das
  externas, na mesma tabela. — *(intent §8.2)*
- [ ] **RF09:** O inventário vive em `documentacao/fontes/inventario.csv`, acompanhado de
  `documentacao/fontes/README.md` explicando colunas e manutenção. — *(intent §4 In)*
- [ ] **RF10:** Fontes **excluídas por decisão** (`lff`, `lff-en`, `lffe`, `sangue`,
  `mapas-biblicos-e-panorama`, deuterocanônicos, skill `jesus-cristo`) aparecem como
  `nao_entra` **com motivo** — não desaparecem do inventário. — *(intent §4 In · ADR-012)*

## 3. Requisitos não funcionais

- **Cobertura:** 100% das fontes do acervo. Fonte conhecida sem linha é FAIL.
- **Consistência:** as colunas de enum só aceitam os valores do §4.
- **Legibilidade:** aberturas em planilha e em editor de texto, sem caracteres corrompidos
  (UTF-8, e sem `;` dentro dos campos — usar vírgula no texto quando precisar).
- **Rastreabilidade:** cada linha cita a ADR ou a decisão que a rege, quando houver.
- **Estabilidade:** o inventário é versionado no git; alteração de linha é mudança
  documentada, não edição silenciosa.

## 4. Contrato do arquivo (CSV)

Delimitador `;`, cabeçalho obrigatório, uma linha por artefato:

| Coluna | Tipo | Obrigatório | Valores |
|---|---|---|---|
| `id` | texto | sim | `F-001`, `F-002`… (único) |
| `fonte` | texto | sim | nome legível |
| `tipo` | enum | sim | `corpus` `referencia_cruzada` `obra` `adendo` `dados_originais` `codigo` `conteudo` `ferramenta` |
| `titular` | texto | sim | quem detém o direito, ou `a confirmar` |
| `licenca` | texto | sim | ex.: `CC BY 4.0`, `CC BY-SA 3.0`, `AGPL-3.0`, `MIT`, `direito reservado`, `uso interno`, `a confirmar` |
| `licenca_verificada` | enum | sim | `sim` `nao` |
| `regime_exibicao` | enum | sim | `curto` `integral_interno` `nao_exibir` |
| `atribuicao_exigida` | texto | sim | texto a exibir, ou `nao` |
| `versao_data` | texto | sim | versão/edição ou data do material |
| `adequacao_doutrinaria` | enum | sim | `ok` `atencao` `fora` `a_revisar` |
| `decisao` | enum | sim | `entra` `nao_entra` `depende` |
| `motivo` | texto | quando `decisao` ≠ `entra` | motivo objetivo |
| `localizacao` | texto | sim | caminho no repositório, ou `fora do git` |
| `adr_referencia` | texto | não | `ADR-002`, `ADR-004`, `ADR-012 10.7`… |
| `observacoes` | texto | não | gatilho de revisão, pendência |
| `revisado_por` | texto | não | vazio hoje; preenchido quando o ARQUITECT revisar |
| `revisado_em` | data | não | `AAAA-MM-DD` |

## 5. Modelo do dado (lógico)

O inventário é **tabela**, não prosa: é o embrião do registro de fontes que a DEM-B vai
persistir. Cada linha é um **artefato** (código, dados ou conteúdo), porque um mesmo
projeto pode ter regimes diferentes por artefato.

## 6. Edge cases

- **Licença desconhecida** → `licenca = a confirmar`, `licenca_verificada = nao` e gatilho
  em `observacoes`.
- **Projeto com licença de código diferente da de dados** → **duas linhas**.
- **Titular desconhecido** → `titular = a confirmar`, com motivo.
- **Fonte que não entra** → linha `nao_entra` com motivo (não desaparece).
- **Material de terceiro dentro de projeto de terceiro** (ex.: uma fonte não comercial
  dentro de um acervo aberto) → linha própria, com o regime mais restritivo.
- **Deuterocanônicos** → linha `nao_entra` com `adequacao_doutrinaria = fora` e motivo
  (cânon, 10.6), mesmo estando dentro de um pacote que "entra".

## 7. Critérios de aceitação

- [ ] **CA01:** o CSV abre em planilha e em editor sem corrupção; todas as linhas têm as
  colunas obrigatórias preenchidas.
- [ ] **CA02:** toda fonte do acervo tem linha — conferido contra a lista do intent §4 In.
- [ ] **CA03:** toda linha com `decisao ≠ entra` tem `motivo` não vazio.
- [ ] **CA04:** zero linhas contradizendo a ADR-012.
- [ ] **CA05:** as fontes internas estão na mesma tabela das externas.
- [ ] **CA06:** as exclusões conhecidas (10.7, mapa comercial, deuterocanônicos,
  `jesus-cristo`) aparecem como `nao_entra` com motivo.
