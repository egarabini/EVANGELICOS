# ADR-013: Componente de mapa em JavaScript — exceção pontual à ADR-001

- **Status:** Proposed — aguarda aceite do ARQUITECT
- **Data:** 2026-10-17
- **Decisores:** ARQUITECT (Eduardo) — autorizou abrir a ADR (decisão 10.8 da OLPF); termos técnicos pelo PLANNER
- **Gatilho:** Novo Horizonte

---

## Contexto e Problema

A ADR-001 fixa Python/Reflex e proíbe Node/TS **na aplicação**. A frente de base de
conhecimento prevê mapas e linha do tempo de lugares e jornadas (OLPF §4.5). Um mapa
interativo não tem equivalente em Python puro no navegador: exige JavaScript.

A decisão 10.8 autoriza abrir esta ADR. O problema é permitir o mapa **sem** abrir a
porta para uma segunda stack — que é o que a ADR-001 existe para impedir.

## Opções consideradas

| Opção | Descrição | Veredito |
|---|---|---|
| **A** | Sem JS: listas e tabelas de lugares/jornadas + imagens estáticas | Atende a busca, não atende o mapa. É o **fallback** se esta ADR for rejeitada. |
| **B** | **Um** componente de mapa isolado, em JavaScript, servido como asset, consumindo JSON do backend | Exceção mínima e contida. **Recomendada.** |
| **C** | Mapa renderizado no servidor como imagem | Sem interação; não resolve |
| **D** | Migrar o frontend para JS/TS | Proibido pela ADR-001 |

## Decisão proposta

Adotar **B, com fronteiras duras** — e registrar que é **exceção**, não precedente:

- **Exatamente um** componente de mapa. Nenhum outro widget JS.
- Vive em pasta própria e isolada; **não** importa código da aplicação, **não** acessa
  banco, **não** lê sessão nem token, **não** decide regra de negócio.
- Recebe os dados **prontos** do backend (JSON: lugares, coordenadas, jornadas, referências
  de passagem) e só desenha.
- Node continua existindo **apenas** para o build do frontend do Reflex, como já acontece —
  nenhuma toolchain nova no repositório.
- Se o componente falhar, a tela degrada para a opção **A** (lista/tabela). O mapa é
  enriquecimento, nunca o único caminho para a informação.
- A biblioteca de mapa é escolha do **design** da DEM, não desta ADR — e precisa de licença
  compatível com a ADR-012.

## Consequências

**Positivas**
- O mapa deixa de ser uma contradição silenciosa da ADR-001 e passa a ter fronteira escrita.
- A degradação para lista garante que a informação nunca depende de JS.

**Negativas / trade-offs**
- Introduz a primeira (e única) superfície JS na aplicação: um lugar a mais para revisar.
- Exige disciplina de revisão: qualquer segundo widget JS passa a contrariar esta ADR.

**Neutras**
- Se rejeitada, a opção A entrega a mesma informação da busca sem interação — a frente não
  fica bloqueada.

## Impacto nas DEMs

- **DEM-C / DEM-D** — só a DEM que de fato tiver mapa usa esta exceção.
- Qualquer outra DEM que queira JS precisa de **nova ADR** que substitua esta.
- Não altera a ADR-001 para o resto do produto: a stack segue Python/Reflex.
