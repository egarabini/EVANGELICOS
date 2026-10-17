# Design — DEM-202610-003 / inventário de fontes

> Dono: PLANNER. O **como** técnico. Esta DEM produz **dado e documento**, não código de
> aplicação: o design é curto de propósito.

## 1. Referência

Spec: [`spec.md`](spec.md) — aprovada com 3 ajustes em 2026-10-17 · ADR-012

## 2. Componentes a criar

- `documentacao/fontes/inventario.csv` — o artefato. UTF-8 **com BOM**, `;`, 17 colunas.
- `documentacao/fontes/README.md` — o que é, como manter, e o que a DEM-B consome.
- `documentacao/fontes/verificar_inventario.py` — **instrumento do EVAL**: valida o CSV
  contra a spec (CA01–CA07) e contra a lista fechada do Anexo A, sem ler o código de
  geração. É o que torna o CA02 conferível por comando.

## 3. Fluxo

1. O PLANNER levanta as fontes nos acervos e nos arquivos de licença de cada projeto
   (`estudos/sensus/DATA_LICENSES.md`, README do atlas, `CREDITOS.md`, etc.).
2. Cada fonte vira linha, com os enums do §6 da spec.
3. `verificar_inventario.py` roda três blocos: estrutura (colunas/enums/BOM), obrigatoriedade
   (motivo/gatilho) e **cobertura** (cada item do Anexo A tem linha).
4. O EVAL roda o verificador e confere o relatório contra o Anexo A, item a item.

## 4. Decisões técnicas

- **Uma linha por ocorrência da fonte no acervo.** A normalização (fonte única, N:N com
  projeto) é da **DEM-B**, não desta: aqui o inventário é **catálogo**, e o catálogo precisa
  mostrar a fonte onde ela está.
- **O id do Sensus vai no campo `fonte`** (`Sensus — <id>: <título>`), para o verificador
  conferir cobertura por id sem criar coluna nova.
- **BOM** via gravação `utf-8-sig` — só assim o Excel PT-BR abre certo.
- **Nenhuma verificação jurídica** aqui: `a confirmar` + gatilho é a resposta correta.
- **`adequacao_doutrinaria` provisória**: preenchida pelo PLANNER pelos critérios do §6.4 da
  spec; `revisado_por` fica vazio até a revisão do ARQUITECT.

## 5. Migrations / dados

- [x] Nenhuma. Nenhuma tabela, nenhum banco tocado.

## 6. Impacto em código existente

- Nenhum. Nada é importado, executado ou exibido por esta DEM.

## 7. O que não muda

- Lição, corpus, busca, produção e a DEM-001.
- O código dos projetos de `estudos/` — são lidos, nunca copiados.

## 8. Ordem

1. Escrever o CSV
2. Escrever o `README.md` das fontes
3. Escrever e rodar o verificador
4. Corrigir o que o verificador apontar
5. EVAL

## 9. Riscos

- **Volume de `a confirmar`** (trilha legal real: SBTB, traduções PT, patrística, RWP). Não é
  falha — é o inventário recusando suposição. Cada um tem gatilho.
- **Julgamento doutrinário** em 7 fontes adventistas e nas dispensacionalistas: provisório,
  marcado para revisão do ARQUITECT.
- **Duplicidade de fontes** entre projetos (Bíblia Livre, OpenBible) — resolvida na DEM-B.
