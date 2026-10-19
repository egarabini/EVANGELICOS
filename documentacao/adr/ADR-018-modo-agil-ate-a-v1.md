# ADR-018: Modo ágil até a v1 (processo proporcional ao risco)

- **Status:** **Proposed** — aguarda o aceite do ARQUITECT.
- **Data:** 2026-10-19
- **Decisores:** ARQUITECT (Eduardo) · redação do PLANNER (a partir da proposta do AUXILIAR-ARCHITECT)
- **Gatilho:** Operação — a cerimônia do método passou a custar mais do que protege na fase de construção
- **Emenda (explícita):** **[ADR-006](ADR-006-guard-rails-tlc-arquivos-de-guarda.md)** e **[ADR-007](ADR-007-estrutura-dem-gate-intent.md)**, no que exigem o processo completo para **toda** DEM
- **Não altera:** ADR-002 (corpus), ADR-003 (Escritura), ADR-008 (segredos), ADR-009 (GitFlow), ADR-011 (aprovação de conteúdo), ADR-012 (fontes), ADR-016 (deploy) e o **CI como porteiro de merge**

---

## Contexto

O método foi desenhado para risco alto. Aplicado **igual** a toda mudança, gera atrito sem
retorno: a **DEM-003** (um inventário em CSV) teve **5 rodadas de EVAL**; a **DEM-002** teve 3
rodadas e 2 correções de teste; toda DEM passa por intent, PRD, spec, design, plano de testes,
List e aceite — mesmo quando é pequena. O deploy, em contraste, já foi simplificado pela ADR-016.

O ambiente hoje é **de teste**: os dados são descartáveis e serão limpos na virada da v1. O
ARQUITECT decidiu priorizar **agilidade** até lá e **fechar as proteções depois**.

## Decisão

Até a **v1 estar no ar e testada**, o processo é proporcional ao risco, em **três níveis**.

| Nível | Quando | Processo |
|---|---|---|
| **1 — leve** | documentação, texto, ajuste visual de tela, correção pequena, refatoração local **sem efeito em dado** | **uma página** (o quê e por quê) + **CI verde**. Sem EVAL cego. O DEVS **não** aguarda "segue" |
| **2 — normal** | funcionalidade nova **sem dado sensível** nem efeito em deploy | **intent curto + spec enxuta** + **no máximo uma rodada** de EVAL |
| **3 — cheio** | segurança e papéis, schema/migração, importação com escrita, infra de deploy/chaves/Traefik, **tudo irreversível** | processo completo, como hoje |

**Cortes adicionais**
- **EVAL:** no máximo **duas rodadas** por DEM; a terceira só por decisão do ARQUITECT.
- **Release por lote:** um PR de release agrupa várias DEMs aceitas.
- **Classificação:** o **PLANNER** diz o nível ao abrir a DEM; **na dúvida, sobe um nível**. O ARQUITECT pode reclassificar.

### O que NÃO muda no modo ágil

- **CI verde** para mesclar; **backup antes do deploy**; **HTTP 200** ao final.
- Nada de **exclusão de dados, restauração de banco, migração ou importação com escrita** sem o ARQUITECT (ADR-016).
- A **regra do porquê**: se o objetivo mudou, reabre o intent.

## Fim do modo ágil (gatilho)

O modo ágil termina quando **a v1 for declarada pelo ARQUITECT** como no ar e testada. Nesse dia:

1. fecha-se a lista de **dívidas aceitas** ([`DIVIDAS-ACEITAS-ATE-A-V1`](../visao/DIVIDAS-ACEITAS-ATE-A-V1.md), D-01 a D-09), item por item;
2. os dados de teste são limpos e entram os dados reais;
3. as **ADR-006 e ADR-007 voltam a valer integralmente**, salvo decisão em contrário;
4. as decisões adiadas por causa da agilidade são reavaliadas — **incluindo a ADR-017 (publicação como serviço)**.

A **definição da v1** (escopo, critério de pronto e o que fecha na virada) está em
[`DEFINICAO-DA-V1`](../visao/DEFINICAO-DA-V1.md) — sem ela, "a v1" não tem fim.

## Consequências

**Positivas**
- Menos rodadas e menos documentos nas mudanças pequenas; mais entregas por semana.
- A proporcionalidade fica **registrada**: o atrito que sobra está onde o risco está.

**Negativas / trade-offs**
- Menos rede de proteção nos níveis 1 e 2: erros pequenos podem passar. O CI mitiga.
- O nível é uma **classificação humana**: pode ser errada. A regra "na dúvida, sobe" mitiga.
- As dívidas aceitas ficam abertas por tempo definido — e com gatilho escrito.

**Neutras**
- O método não morre: ele fica **proporcional**. A partir da v1, o nível 3 volta a ser o padrão.

## Mensagem ao perfil DEPLOY

O DEPLOY (ADR-016) continua publicando nos termos de hoje: CI verde, backup antes, HTTP 200
ao final. **Não** corrige dívida sozinho; risco novo → registra na jornada e avisa o ARQUITECT.
Na dúvida sobre nível ou escopo, **para e devolve ao PLANNER**.

## Referências

- Proposta original: [`PROPOSTA-ADR-017-modo-agil-aux-architect.md`](../visao/PROPOSTA-ADR-017-modo-agil-aux-architect.md)
- Dívidas aceitas: [`DIVIDAS-ACEITAS-ATE-A-V1`](../visao/DIVIDAS-ACEITAS-ATE-A-V1.md)
- Definição da v1: [`DEFINICAO-DA-V1`](../visao/DEFINICAO-DA-V1.md)
