# Revisão doutrinária do inventário de fontes (DEM-202610-003)

> Para o **ARQUITECT**. O EVAL cego deu **PASS** na rodada 5; o aceite é seu.
>
> ## Duas folhas, dois papéis — não são concorrentes
>
> - **A forma de decidir** é o quadro do AUXILIAR-ARCHITECT:
>   [`visao/QUADRO-REVISAO-DOUTRINARIA-aux-architect.md`](../visao/QUADRO-REVISAO-DOUTRINARIA-aux-architect.md).
>   Ele reduz as 22 linhas a **8 decisões** (opções A/B/C/D) e mostra o efeito de cada opção no CSV.
>   **É o que você preenche.**
> - **Este documento** é o **mapa de aplicação**: qual `id` está em qual grupo, o que o PLANNER
>   escreve no CSV para cada opção A/B/C/D, a correção de contagem e a assinatura.
>
> Das **86 linhas**, **64 têm `adequacao_doutrinaria = ok`** e não pedem nada de você. As **22
> restantes** pedem o seu olhar — e uma delas (F-077) é questão **legal**, não doutrinária.

## O que o PLANNER grava no CSV, por opção

| Opção | O que muda no CSV |
|---|---|
| **A. Entra, com rótulo** | nada (já está `atencao` + `curto`); a interface identifica a tradição |
| **B. Só papel interno** | `regime_exibicao = integral_interno`; o aluno não vê |
| **C. Não entra** | `decisao = nao_entra` + `motivo` obrigatório (verificador CA05) |
| **D. Entra sem rótulo** | `adequacao_doutrinaria = ok` |
| Em todas | `revisado_por` e `revisado_em` preenchidos; verificador reexecutado; EVAL confirma |

## 1. A que mais importa (1)

| # | Fonte | Hoje | Por que pede olhar | Sua decisão |
|---|---|---|---|---|
| **F-009** | **Gordon H. Clark**, *Deus e o Mal: O Problema Resolvido* (ed. a identificar) | `atencao` · entra | Calvinista (Westminster), **mas** houve a controvérsia **Clark–Van Til** sobre a incompreensibilidade de Deus. Foi o erro de identidade mais grave do inventário (estava como "Adam Clarke, metodista"). O `atencao` é para identificar ao exibir — **não** é objeção doutrinária do projeto | ☐ ok · ☐ mudar · ☐ fora |

## 2. Adventistas (8)

Todas `atencao` · entram, com identificação ao exibir e sem misturar com o material doutrinário do estudo.

| # | Fonte | Sua decisão |
|---|---|---|
| F-043 | Ellen G. White, *The Great Controversy* (1911) | ☐ ok · ☐ mudar · ☐ fora |
| F-044 | Ellen G. White, *Patriarchs and Prophets* (1913) | ☐ ok · ☐ mudar · ☐ fora |
| F-045 | Ellen G. White, *Prophets and Kings* (1917) | ☐ ok · ☐ mudar · ☐ fora |
| F-046 | Ellen G. White, *The Acts of the Apostles* (1911) | ☐ ok · ☐ mudar · ☐ fora |
| F-047 | Ellen G. White, *Christ's Object Lessons* (1900) | ☐ ok · ☐ mudar · ☐ fora |
| F-048 | Ellen G. White, *Steps to Christ* (1892) | ☐ ok · ☐ mudar · ☐ fora |
| F-049 | Ellen G. White, *Thoughts from the Mount of Blessing* (1896) | ☐ ok · ☐ mudar · ☐ fora |
| F-050 | Uriah Smith, *Daniel and the Revelation* (1907) — adventista, **não** é EGW | ☐ ok · ☐ mudar · ☐ fora |

## 3. Comentaristas históricos de outras tradições (7)

Todas `atencao` · entram, com identificação da tradição ao exibir.

| # | Fonte | Tradição | Sua decisão |
|---|---|---|---|
| F-030 | Adam Clarke, *Commentary and Critical Notes* | metodista/arminiana — **não confundir com a F-009** | ☐ ok · ☐ mudar · ☐ fora |
| F-034 | C. I. Scofield, *Reference Notes* (1917) | dispensacionalista | ☐ ok · ☐ mudar · ☐ fora |
| F-035 | John Wesley, *Notes on the Bible* | arminiana/metodista | ☐ ok · ☐ mudar · ☐ fora |
| F-040 | Luther's Commentary (coletânea 1892–1932) | luterana | ☐ ok · ☐ mudar · ☐ fora |
| F-041 | B. W. Johnson, *The People's New Testament* | Movimento de Restauração | ☐ ok · ☐ mudar · ☐ fora |
| F-042 | McGarvey e Pendleton, *The Fourfold Gospel* | Movimento de Restauração | ☐ ok · ☐ mudar · ☐ fora |
| F-056 | Torrey, *New Topical Textbook* | dispensacionalista | ☐ ok · ☐ mudar · ☐ fora |

## 4. Sem classificação (1)

| # | Fonte | Hoje | Por que pede olhar | Sua decisão |
|---|---|---|---|---|
| **F-083** | Materiais da revista **FAJOPA** (escatologia paulina, dons do Espírito, Paulo/história) | `a_revisar` · `depende` | Não há classificação doutrinária **nem** política de licença da revista. É a única linha sem os dois | ☐ ok · ☐ mudar · ☐ fora |

## 5. Fora do produto — só uma conferência (6)

| # | Fonte | Hoje | Por que está fora | Sua decisão |
|---|---|---|---|---|
| F-060 | Bíblia Figueiredo (Vulgata) | `fora` · `nao_entra` | Deuterocanônicos e adições gregas, fora do cânon (ADR-012 10.6) | ☐ confirmo · ☐ reabrir |
| F-068 | Caderno *lff* (JW) | `fora` · `nao_entra` | Linha doutrinária excluída (ADR-012 10.7) | ☐ confirmo · ☐ reabrir |
| F-069 | Caderno *lff-en* (JW) | `fora` · `nao_entra` | idem | ☐ confirmo · ☐ reabrir |
| F-070 | Caderno *lffe* (JW) | `fora` · `nao_entra` | idem | ☐ confirmo · ☐ reabrir |
| F-071 | Caderno "sangue" (JW) | `fora` · `nao_entra` | idem | ☐ confirmo · ☐ reabrir |
| F-077 | mapas-biblicos-e-panorama | `ok` · `nao_entra` | **Legal, não doutrinário**: cópia de site comercial com imagens de terceiros | ☐ confirmo · ☐ reabrir |

> **Contagem**: o levantamento do AUXILIAR-ARCHITECT falou em "22". São **23**: 22 de conteúdo
> doutrinário + a F-077, cuja questão é legal. As 4 linhas JW (F-068..F-071) somam 4, não 3.

## Assinatura

```
revisado_por: ______________________  (ARQUITECT)
revisado_em:  ______________________  (AAAA-MM-DD)
lote das 64 linhas sem atenção: ☐ sem objeção
```

Depois da assinatura, o PLANNER grava as duas colunas no CSV e reemite o verificador. A DEM-003
fecha com aceite (o EVAL já deu PASS).

## Pendências que **não** são desta revisão

- **Origem do Matthew Henry "tradução PT"** (F-002) — fonte não localizada no disco; o Henry em
  inglês é a F-033.
- **Medida de "curto"** — proposta pendente de fechamento (300 palavras / 10% do capítulo / 2
  trechos por tela; o limite da SBTB prevalece).
- **Política de licença da revista FAJOPA** — pergunta aberta (afeta a F-083).
