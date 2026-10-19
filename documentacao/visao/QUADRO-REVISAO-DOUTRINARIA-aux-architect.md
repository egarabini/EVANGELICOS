# Quadro de revisão doutrinária do inventário (DEM-003)

> Autor: AUXILIAR-ARCHITECT (IA) · Para: ARQUITECT (preenche) · Data: 2026-10-18
> Base: `documentacao/fontes/inventario.csv`, 86 linhas, após o PASS da rodada 5 do EVAL.
> **Eu não decido doutrina.** Este quadro só reduz 22 linhas a 8 decisões e põe os fatos do CSV ao lado.
> Marque uma opção por grupo, escreva sua nota se quiser, e entregue ao PLANNER, que aplica nas
> linhas do CSV e preenche `revisado_por` / `revisado_em` com o que você indicar.

## Como decidir cada grupo

Todas as linhas abaixo estão hoje com `decisao = entra` e `regime_exibicao = curto` (o aluno pode
ver trechos curtos com a fonte), exceto o grupo FAJOPA (`depende`) e os excluídos.

| Opção | Efeito no CSV |
|---|---|
| **A. Entra, com rótulo** | `adequacao_doutrinaria = atencao` mantido; a interface identifica a tradição ao exibir ("comentário de tradição X") |
| **B. Só papel interno** | `regime_exibicao = integral_interno`; o aluno não vê |
| **C. Não entra** | `decisao = nao_entra`, com `motivo` |
| **D. Entra sem rótulo** | `adequacao_doutrinaria = ok` |

Lembrete de contexto: a base editorial atual é **reformada** (Grudem, Clark, Edwards). A ADR-012 10.7 já
excluiu uma linha doutrinária inteira (`lff`, `lffe`, `sangue`). Nenhum grupo abaixo está nessa categoria
por si só; a questão é se o aluno vê esses comentários e com que aviso.

---

## Grupo 1 — Clark, *Deus e o Mal* (F-009)

- Fato: Gordon H. Clark (1902–1985), filósofo calvinista, linha da Confissão de Westminster. 8 arquivos. Reprodução de obra de terceiro (você confirmou). Titular da edição ainda a identificar.
- Já corrigido: não confundir com Adam Clarke (F-030).
- Decisão: ☐ A  ☐ B  ☐ C  ☐ D
- Nota: ____________________

## Grupo 2 — Tradição arminiana / metodista (F-030 Adam Clarke · F-035 John Wesley)

- Fato: ambos domínio público (Sensus). A obra de Wesley é *Notes on the Bible*; a de Clarke é comentário crítico.
- Decisão: ☐ A  ☐ B  ☐ C  ☐ D
- Nota: ____________________

## Grupo 3 — Tradição dispensacionalista (F-034 C. I. Scofield · F-056 R. A. Torrey)

- Fato: domínio público. Scofield é a edição de **1917** das notas; Torrey é um livro de tópicos.
- Decisão: ☐ A  ☐ B  ☐ C  ☐ D
- Nota: ____________________

## Grupo 4 — Tradição luterana (F-040 Lutero e outros)

- Fato: o módulo reúne edições de **1892 a 1932** (Lenker, Hay, Holman); o CSV pede conferir cada parte antes de exibir ao usuário. O próprio levantamento do Sensus marca a licença como "Verificar".
- Decisão: ☐ A  ☐ B  ☐ C  ☐ D
- Nota: ____________________

## Grupo 5 — Movimento de Restauração (F-041 B. W. Johnson, *People's New Testament* · F-042 McGarvey e Pendleton, *Fourfold Gospel*)

- Fato: ambos domínio público. Tradição do Movimento de Restauração, com ensino próprio sobre o batismo.
- Decisão: ☐ A  ☐ B  ☐ C  ☐ D
- Nota: ____________________

## Grupo 6 — Adventistas (F-043 a F-049 Ellen G. White, 7 obras · F-050 Uriah Smith)

- Fato: domínio público pelo critério do Sensus (autora † 1915, edições anteriores a 1929); só Project Gutenberg e archive.org. O CSV já pede "não misturar com o material doutrinário do estudo".
- Fato relevante para a decisão: são obras de uma tradição com autoridade profética própria, e **não são comentário versículo a versículo** (o Sensus só gera linha para parágrafos com referência explícita).
- Decisão: ☐ A  ☐ B  ☐ C  ☐ D
- Nota: ____________________
- Se preferir decidir por obra: ☐ mesma opção para as 8 · ☐ separar (Ellen White × Uriah Smith)

## Grupo 7 — Materiais da revista FAJOPA (F-083)

- Fato: escatologia paulina, dons do Espírito e Paulo/história da Igreja; origem `revista.fajopa.org` (resposta sua). Está `a_revisar` e `depende`; a política de licença da revista não foi verificada.
- Esta linha **não** depende só de doutrina: falta ler a licença da revista.
- Decisão doutrinária: ☐ A  ☐ B  ☐ C  ☐ D  ☐ aguardar a licença
- Nota: ____________________

## Grupo 8 — Já excluídos, só conferência (F-060 · F-068 · F-069 · F-070 · F-071)

- F-060 Bíblia do Pe. Figueiredo (deuterocanônicos) — fora do cânon adotado (ADR-012 10.6).
- F-068, F-069, F-070, F-071 — `lff`, `lff-en`, `lffe`, `sangue` — excluídos pela ADR-012 10.7; **titular inferido pelo título**, ainda sem confirmação.
- Decisão: ☐ confirmo as 5 como `nao_entra` / `fora`   ☐ mudar: ____________________

---

## Registro da revisão (você preenche)

- `revisado_por`: **ARQUITECT**
- `revisado_em`: **2026-10-19**
- Observação geral: o ARQUITECT **aceitou a revisão doutrinária** em 19/10, mantendo o **estado
  atual** das 22 linhas (`entra` / `curto` / `atencao` = opção **A**, com o rótulo de tradição na
  exibição). A **F-083 (FAJOPA)** permanece `depende` — a licença da revista ainda não foi lida, e
  pela decisão 9.4 do fluxo de obras ela **bloqueia na liberação**, não na importação.
  As 8 opções por grupo **não foram marcadas** — se você quiser trocar algum grupo (B, C ou D), é
  só indicar que eu aplico e reenvio ao EVAL.

## O que o PLANNER faz com isto

1. Aplica a opção de cada grupo às linhas listadas.
2. Preenche `revisado_por` e `revisado_em` **somente nas 22 linhas revisadas**. As outras 64 (`ok`) ficam
   para uma revisão por amostragem ou por você depois; o quadro não as cobre.
3. Reenvia ao EVAL e registra no changelog da DEM-003 o que mudou.

## Limites

Revisão doutrinária é sua. Os rótulos de tradição usados aqui (arminiana, dispensacionalista, luterana,
Restauração, adventista) vêm das observações que o PLANNER já colocou no CSV; não os reexaminei obra por obra.
Não verifiquei se algum desses comentários entrará na primeira ingestão (DEM-C): vale perguntar ao PLANNER, porque
se não entrar, a decisão pode esperar.

