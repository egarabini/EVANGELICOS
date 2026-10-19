# ADR-019: O fluxo de obras e estudos — e a emenda da ADR-011

- **Status:** **Accepted** — aceita pelo ARQUITECT em **2026-10-19** (inclui a emenda da ADR-011 e a salvaguarda do "contestar"). **EMENDADA pela [ADR-020](ADR-020-autoridade-e-disponibilidade-da-obra.md)**: o `contestar` do Revisor vira **solicitação de revisão**, decidida pelo Admin.
- **Data:** 2026-10-19
- **Decisores:** ARQUITECT (Eduardo) · redação do PLANNER
- **Gatilho:** o fluxo decidido em 19/10 + a dívida **D-07** (a aprovação de uma só assinatura)
- **Emenda (explícita):** **[ADR-011](ADR-011-aprovacao-de-conteudo-assinada.md)** — o "qualquer mudança de conteúdo invalida a aprovação" ganha a **exceção do ciclo de revisão**, com os dois hashes registrados
- **Não altera:** ADR-008, ADR-009, ADR-012, ADR-016, a matriz papel × rota (DEM-002)

---

## Contexto

A **ADR-011** exige a aprovação **assinada** (revisor + data + hash) e diz: "a transição para
liberado é bloqueada sem assinatura válida para o hash **atual**; **qualquer** mudança de conteúdo
invalida a aprovação automaticamente".

O fluxo decidido pelo ARQUITECT em 19/10 tem o **Admin alterando conteúdo no passo 3** — para
cumprir o parecer do Revisor. Ao pé da letra, essa alteração **invalidaria a assinatura** e travaria
o próprio passo que ela deveria habilitar. O conflito é real e precisa de uma decisão.

## Decisão

**1. O fluxo de obras e estudos** (vale para obra **e** estudo):

| Passo | Quem | O quê | Estado |
|---|---|---|---|
| 1 | **Admin** | importa e disponibiliza | `em_revisao` |
| 2 | **Revisor** | avalia, registra parecer **e ajustes propostos**, assina | `aguardando_admin` |
| 3 | **Admin** | lê o parecer, **descreve e implementa** os ajustes, libera | `liberada` |
| 4 | **Coordenador** | vincula/desvincula ao seu ambiente; ajusta os **adendos do ambiente** | — (autonomia dele) |
| 5 | **Admin** | toda alteração é dele; **depois de `liberada`**, volta como **pendente de revisão** | nova versão em `em_revisao` |

**2. A emenda da ADR-011.** A assinatura do Revisor fica amarrada à **versão que ele viu**. Os
ajustes do Admin **dentro do ciclo** **não** a invalidam — mas o registro guarda **os dois hashes**:
o da versão vista pelo Revisor e o da versão liberada pelo Admin. A regra "qualquer mudança
invalida" vale **depois** de `liberada`: a nova versão volta ao fluxo.

**3. O portão de licença, em duas etapas.** A fonte `nao_entra` no inventário **bloqueia a
importação**; a fonte `depende` **bloqueia a liberação** (importa e revisa, mas não libera até virar
`entra`).

**4. As versões e a adoção.** A versão `liberada` **permanece disponível** enquanto a alterada
espera revisão; o coordenador **adota** a nova quando quiser — a versão em uso não muda sozinha.

**5. O adendo do coordenador.** É **sobreposição por ambiente**, identificado como dele; não altera
a obra base nem passa por revisão. O isolamento multi-ambiente completo fica com a **D-06**.

## A salvaguarda do trade-off (revisão de 19/10)

A emenda declara que o Admin pode liberar conteúdo que o Revisor não viu, e que a proteção é o
registro. Duas medidas **baratas, sem bloqueio**, entram no design (spec RF11):

1. **no momento da liberação**, o Admin vê o **tamanho do que mudou** em relação à versão que o
   Revisor viu;
2. **depois da liberação**, o Revisor vê a **diferença final** (só leitura) e tem o botão
   **"contestar"**, que **reabre a revisão**.

Isso não fecha a brecha — mantém o Admin no comando — mas transforma o que era invisível em
visível e contestável.

## Consequências

**Positivas**
- O fluxo funciona sem transformar cada ajuste numa ida e volta ao Revisor.
- A diferença entre o visto e o liberado fica **auditável** — a assinatura vira um intervalo, não
  uma foto.
- A D-07 (a aprovação de uma só assinatura) fecha: são **duas** assinaturas + o hash.

**Negativas / trade-offs**
- A assinatura deixa de ser "do conteúdo exato" e passa a ser "deste intervalo" — exige o registro
  dos dois hashes para não virar fé.
- O Admin continua podendo liberar conteúdo que o Revisor **não** viu: o que o protege é o registro
  e a auditoria, **não** o bloqueio. É uma decisão de risco consciente.

## Impacto

- **A spec da DEM-011** aplica esta ADR (e não pode ser aceita antes dela).
- **A D-07** passa a "em implementação pela DEM-011".
- **A D-06** mantém o gatilho (mais de um ambiente real).

## Referências

- [ADR-011](ADR-011-aprovacao-de-conteudo-assinada.md) · [DEM-011](../../dem/DEM-202610-011-fluxo-de-obras-e-estudos/planner/intent.md) · a spec da DEM-011



