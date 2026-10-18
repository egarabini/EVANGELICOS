# Jornada EVAL — DEM-202610-003 / rodada 5

- **Agente:** EVAL
- **Data:** 2026-10-17 (America/Sao_Paulo)
- **DEM:** DEM-202610-003-inventario-de-fontes
- **Hash avaliado:** `6d9d1ccedc9bc643711dbdc05439ebd67b75b969` (branch `develop`)
- **Escopo:** rodada 5 estreita — H-01 (rastreabilidade do gitlink) e a mensagem
  da regra do §6.1 do verificador; regressão de F, C e N no hash novo.
- **Regras cumpridas:** não corrigi nada; não mudei critério. Li os três arquivos
  exigidos do planner (`intent.md`, `spec.md` §6.1/§6.3, `plano-testes.md`); para
  evidência, li o README do artefato (`documentacao/fontes/README.md`), a
  ADR-012 e os READMEs das fontes amostradas. Não li `dev/`, o README da DEM nem
  as jornadas das rodadas 1–4. Escrevi somente em `eval/`.

---

## 1. H-01 — o conteúdo aponta para o merge?

### 1.1 Ponteiro no hash novo

```
$ git ls-tree 6d9d1cc ESTUDOS_BIBLICOS/GSI_EBD
160000 commit ba165d933f997b3d193be7b45fb552a1f21796b5	ESTUDOS_BIBLICOS/GSI_EBD
```

O gitlink aponta para **`ba165d933f997b3d193be7b45fb552a1f21796b5`** — o merge
(`parents=4ad1e0d ac712dd`), não mais o `4ad1e0d`. O working tree do submódulo
está em `ba165d9` e limpo (`git status --porcelain` vazio).

### 1.2 Suíte no commit pinado

Exportei o commit pinado, sem tocar no repositório de código:

```
$ git -C ESTUDOS_BIBLICOS/GSI_EBD archive ba165d933f997b3d193be7b45fb552a1f21796b5 | tar -x -C <temp>
$ <venv>\python.exe -m pytest tests -q
82 passed, 1 warning in 1.95s
```

O warning é do cache do pytest no diretório temporário (o sandbox nega a escrita do
diretório de cache); nenhum teste falhou. Com `-p no:cacheprovider`, o resultado é
`82 passed in 3.11s`.

- `tests/test_estudo_aplicado.py` **existe** no commit exportado (o merge o trouxe;
  o `4ad1e0d` não o tinha).
- O arquivo contém **6 funções `test_`** — exatamente o delta 76 → 82.
- Controle: o commit anterior `4ad1e0d`, exportado do mesmo jeito, dá
  **76 passed in 3.07s**.

| Medida | Resultado |
|---|---|
| Pin em `6d9d1cc` | `ba165d933f997b3d193be7b45fb552a1f21796b5` |
| `tests/test_estudo_aplicado.py` no commit pinado | presente (6 testes) |
| `pytest tests -q` em `ba165d9` | **82 passed** |
| `pytest tests -q` em `4ad1e0d` (controle) | 76 passed |
| Working tree do submódulo | `ba165d9`, limpo |

**H-01: OK.** A contagem esperada (82) foi obtida no commit que o repositório
realmente pina.

---

## 2. Mensagem do verificador (§6.1)

Código no hash novo (`documentacao/fontes/verificar_inventario.py`, linhas 129–133):
a decisão é lida da própria linha (`decisao_da_linha = (linha.get("decisao") ...)`)
antes de compor a mensagem.

### 2.1 Caso forçado — decisão da própria linha

Copiei o CSV para um temp e forcei **só a F-082** (linha 83) para
`regime_exibicao=curto`; ela já tem `licenca_verificada=nao` e `decisao=depende`.
A linha anterior (F-081) tem `decisao=nao_entra` — é o caso que discriminava o
defeito. O original não foi editado (blob continua `e3d23c5`).

Saída do verificador atual contra a cópia:

```
FAIL (1 problema(s)):
  - linha 83 (F-082): licenca nao confirmada com decisao 'depende' exige regime
    integral_interno ou nao_exibir, nunca curto (spec §6.1)
```

**A mensagem cita `depende`, a decisão da linha 83**, e não `nao_entra`
(a da linha anterior). Exatamente 1 falha; exit code 1.

Controle com a versão anterior do verificador (blob do commit `3018146`,
exportado para temp, original intocado), contra a mesma cópia:

```
- linha 83 (F-082): licenca nao confirmada com decisao 'nao_entra' exige regime ...
```

Ou seja, o defeito descrito (imprimir a decisão da linha anterior) **é
reproduzível na versão antiga e não ocorre na nova**.

### 2.2 Primeira linha do arquivo disparando

Montei outra cópia com a F-082 como **primeira linha de dados** (linha 2).

- Verificador novo: mensagem `linha 2 (F-082): ... com decisao 'depende' ...`;
  **0 ocorrências de `Traceback`**, exit 1 (falha normal da regra).
- Verificador antigo (mesma cópia): `UnboundLocalError: cannot access local
  variable 'decisao' where it is not associated with a value` — o `NameError`
  que o defeito causava.

**Mensagem: correta.** Lê a decisão da linha avaliada e não quebra quando a
primeira linha é a que dispara.

---

## 3. Verificador no hash novo

```
$ python documentacao\fontes\verificar_inventario.py
linhas: 86
AVISO fontes internas na mesma tabela: 11 linha(s)
AVISO autores com nome parecido: 'Clark' ['F-009'] x 'Clarke' ['F-030'] - conferir identidade
AVISO autores com nome parecido: 'House' [...] x 'Rouse' ['F-012'] - conferir identidade
AVISO autores com nome parecido: 'Reid' ['F-008'] x 'Reis' ['F-080'] - conferir identidade

PASS — estrutura, enums, motivo, gatilho e cobertura do Anexo A
```

Conferência independente do CSV:

- BOM: `efbbbf` presente; 87 quebras CRLF; 17 colunas únicas na ordem; 86 linhas
  de dados; 0 linha com número de campos ≠ 17; ids únicos.
- Sensus: **46 linhas** `Sensus — ...`, **46 ids únicos** (bate com o Anexo A).
- RF10: **12/12 exclusões** presentes como `nao_entra` com `motivo` não vazio.
- `licenca` contendo `a confirmar`: 15 linhas, todas com `licenca_verificada=nao`
  e com o gatilho completo (o quê / com quem / quando).
- `adequacao_doutrinaria` preenchida nas 86 linhas; `revisado_por` e `revisado_em`
  vazios em todas (revisão do ARQUITECT ainda pendente, como manda o RF07).

---

## 4. Amostra das correções de identidade

| Linha | O que o CSV diz | Evidência na fonte |
|---|---|---|
| **F-009** | `Gordon H. Clark (1902-1985)`; `atencao`; obs. diz que é o filósofo calvinista de Westminster e **não** Adam Clarke (F-030) | `DEUS_E_O_MAL_GORDON_CLARK/01_Introducao...md`: "Dr. Gordon H. Clark", "calvinista", "Westminster"; F-030 é `Adam Clarke` |
| **F-005** | `Wayne Grudem / Zondervan (1994) - tradução: Editora Vida Nova`; obs. confirma Zondervan | `TEOLOGIA_SISTEMATICA/README.md` l. 175–176: "Editora original: Zondervan (1994)" / "Tradução: Editora Vida Nova" |
| **F-010** | obra original de Jonathan Edwards, **domínio público**, uma linha | Edwards (1703–1758); a obra original não tem titular de tradução |
| **F-080** | tradução de 2015, `Rodrigo Reis de Faria`, **direito reservado**, linha separada | `.../README.md`: PDF "Tradução de Rodrigo Reis de Faria, 2015" |
| **F-082** | `regime_exibicao=integral_interno`, `licenca=a confirmar`, `licenca_verificada=nao`, `decisao=depende`; obs. diz que o MIT é do código, não dos dados | coerente com a ADR-012 e com o §6.1 (licença a confirmar nunca em `curto`) |

F-010 e F-080 são linhas distintas, com regimes distintos (obra x tradução) e
observações que se referenciam. F-005 separa obra (Zondervan, 1994) de tradução
(Vida Nova). F-009 e F-030 são autores diferentes, sem colisão.

---

## 5. F-01..F-10 no hash novo

| ID | Veredito | Evidência |
|---|---|---|
| F-01 | PASS | BOM `efbbbf`; `;`; 17 colunas na ordem; 86 linhas; 0 malformada; verificador PASS |
| F-02 | PASS | 46 linhas do Sensus, 46 ids únicos |
| F-03 | PASS | 15 linhas `a confirmar`, todas com gatilho completo; verificador PASS |
| F-04 | PASS | `regime_exibicao` só em `{curto, integral_interno, nao_exibir}`; verificador PASS |
| F-05 | PASS | `decisao` só em `{entra, nao_entra, depende}`; toda decisão ≠ `entra` tem `motivo` |
| F-06 | PASS | 0 contradições na matriz das 12 decisões (abaixo); CSV idêntico ao da rodada 4 (blob `e3d23c5`) |
| F-07 | PASS | `adequacao_doutrinaria` preenchida nas 86; `revisado_por/em` vazios (revisão pendente) |
| F-08 | PASS | 11 linhas internas (`ESTUDOS_BIBLICOS`) e 70 de `estudos/` no mesmo arquivo |
| F-09 | PASS | `documentacao/fontes/{inventario.csv,README.md,verificar_inventario.py}` presentes; README explica colunas, critérios e manutenção |
| F-10 | PASS | 12/12 exclusões `nao_entra` com motivo |

Matriz H-03/F-06 (12 decisões da ADR-012; 0 contradições):

| Decisão | Linha/evidência |
|---|---|
| 10.1 público | n/a — não é linha de fonte; regime não declara público do primeiro corte |
| 10.2 trecho curto / integral interno | F-004, F-005, F-007, F-008, F-009, F-010, F-080, F-084 em `curto`; F-085 em `integral_interno` |
| 10.3 CC BY-SA | F-012 (CC BY-SA 4.0) e F-067 (CC BY-SA 3.0), com share-alike registrado em `observacoes` |
| 10.4 sem lucro | F-024 (não comercial) em `integral_interno`/`depende`, com gatilho de jurisdição |
| 10.5 ADR de política | n/a — a própria ADR-012 existe |
| 10.6 deuterocanônicos | F-060 `nao_entra`, `fora` |
| 10.7 linha doutrinária | F-068, F-069, F-070, F-071 e F-076 `nao_entra`, `nao_exibir` |
| 10.8 mapa | F-086 (`depende`, ADR-013) |
| 10.9 originais | F-065, F-066, F-067 `curto`/`entra` |
| 10.10 ACF | F-001 `a confirmar`/`curto`/`entra`, com a exceção explícita e o risco aceito |
| 10.11 resumo por IA | n/a — não há linha de fonte de resumo; nada gerado é armazenado |
| 10.12 Jev/Laya | F-078 e F-079 `nao_entra`, reavaliar na DEM-E |

---

## 6. C-01 — código e banco

- O commit `6d9d1cc` toca **3 caminhos**: o gitlink, `eval/jornada-rodada4.md`
  (documentação) e `verificar_inventario.py`. Nenhum arquivo de código ou banco.
- O repositório de código está em `ba165d9`, limpo; nenhum arquivo de `gsi_ebd/`
  foi escrito por esta DEM. A mudança do gitlink é ponteiro de rastreabilidade,
  não alteração de código.
- `git grep -i inventario` no commit `ba165d9` do submódulo: nenhuma ocorrência.
- `git grep "class Fonte"` no mesmo commit: nenhuma ocorrência.

**C-01: PASS.**

---

## 7. N-01..N-05

| ID | Veredito | Evidência |
|---|---|---|
| N-01 | PASS | Nenhuma tabela/modelo/persistência criada; `documentacao/fontes` só tem CSV, README e verificador; código sem `inventario`/`class Fonte` |
| N-02 | PASS | Nenhum importador; nenhum caminho do inventário é lido por código de ingestão |
| N-03 | PASS | Nenhuma tela, rota ou busca nova; a entrega é documental |
| N-04 | PASS | Nenhum léxico ou original ingerido; os 3 arquivos de `documentacao/fontes` são metadados |
| N-05 | PASS | As 15 linhas `a confirmar` seguem `licenca_verificada=nao`, com gatilho; nenhuma licença foi "resolvida" por suposição |

---

## 8. H-02 e H-03

- **H-02:** o commit toca só `documentacao/`, o gitlink e o verificador; não há
  escrita em corpus, conteúdo ou produção. A sonda HTTP 200 + "João 3:16" em
  produção **não foi executada** neste ambiente — não há deploy neste commit e a
  mudança é documental. Veredito pelo escopo: **PASS**.
- **H-03:** matriz das 12 decisões acima, **0 contradições**. O CSV é
  byte-idêntico ao do hash da rodada 4 (blob `e3d23c5`), então não houve
  regressão de conteúdo.

---

## 9. O que regrediu

Nada.

- CSV: blob `e3d23c562efa943544e9e48d0a7e280ce3aeda06` em `3018146` e em
  `6d9d1cc` — inalterado.
- Verificador: blob `1e90930d07555260894ab2e38165d050705a81b5` no HEAD e no
  commit; a única diferença de comportamento é a mensagem do §6.1, agora correta.
- Gitlink: corrigido de `4ad1e0d` para `ba165d9`; suíte **82 passed**.
- Verificador no CSV original: **PASS**, 86 linhas.

---

## Veredito

```
hash: 6d9d1ccedc9bc643711dbdc05439ebd67b75b969
F: PASS · H: PASS · C: PASS · N: PASS · G: N-A (ARQUITECT)
agregado: PASS
```

- **H-01: OK** — pin em `ba165d9`; `pytest` = **82 passed**; `test_estudo_aplicado.py`
  presente; controle em `4ad1e0d` = 76.
- **Mensagem do verificador: correta** — cita a decisão da própria linha
  (`depende` na F-082, com a anterior em `nao_entra`) e não dá `NameError` quando
  a primeira linha dispara.
- **Regressão: nenhuma.**

### Limitações declaradas

- A sonda de produção (H-02) não foi executada; o veredito de H-02 é pelo escopo
  do diff (nenhuma escrita em corpus/produção).
- F-06/H-03 foram conferidos por amostragem das 12 decisões e pela imutabilidade
  do CSV (blob idêntico ao da rodada 4); não substituem o aceite do ARQUITECT.
- O console do Windows exibe `§` como `�` (code page); o arquivo é UTF-8 e o
  caractere está correto no CSV e no verificador.
