# Proposta — ADR-017: Modo ágil até a v1 (com dívidas aceitas registradas)

> Autor: AUXILIAR-ARCHITECT (IA) · Para: PLANNER (redige e numera) e ARQUITECT (aceita) · Data: 2026-10-19
> **Rascunho.** O texto da ADR segue o formato do projeto, mas o número, a redação final e o
> aceite são do PLANNER e do ARQUITECT. Nada aqui foi commitado nem aplicado.
> Motivação do ARQUITECT (19/10): "estamos iniciando um desenvolvimento e essas burocracias estão
> atrasando o progresso… depois que a versão 1 estiver rodando e testada, fechamos a proteção."

---

# ADR-017: Modo ágil até a v1

- **Status:** **Proposed** — aguarda aceite do ARQUITECT
- **Data:** 2026-10-19
- **Decisores:** ARQUITECT (Eduardo) · redação do PLANNER
- **Gatilho:** Operação — a cerimônia do método passou a custar mais do que protege na fase de construção
- **Emenda (explícita):** **[ADR-006](ADR-006-guard-rails-tlc-arquivos-de-guarda.md)** e **[ADR-007](ADR-007-estrutura-dem-gate-intent.md)**, no que exigem o processo completo para toda DEM
- **Não altera:** ADR-002 (corpus), ADR-003 (Escritura), ADR-008 (segredos), ADR-009 (GitFlow), ADR-011 (aprovação de conteúdo), ADR-012 (fontes) e o CI como porteiro de merge

## Contexto

O método foi desenhado para risco alto. Aplicado igual a toda mudança, gera atrito sem retorno:
a DEM-003 (um inventário em CSV) teve **5 rodadas de EVAL**; a DEM-002 teve 3 rodadas e 2
correções de teste; toda DEM passa por intent, PRD, spec, design, plano de testes, List e aceite,
mesmo quando é pequena. O deploy, em contraste, já foi simplificado pela ADR-016.

Hoje o ambiente é **de teste**: os dados são descartáveis e serão limpos na virada da v1.
O ARQUITECT decidiu priorizar agilidade até lá e **fechar as proteções depois**.

## Decisão

Até a **v1 estar no ar e testada**, o processo é proporcional ao risco, em três níveis.

| Nível | Quando | Processo |
|---|---|---|
| **1 – leve** | documentação, texto e ajuste visual de tela, correção pequena, refatoração local sem efeito em dado | uma página (o quê e por quê) + **CI verde**. Sem EVAL cego. O DEVS segue sem aguardar "segue" |
| **2 – normal** | funcionalidade nova sem dado sensível nem efeito em deploy | intent curto + spec enxuta + **no máximo uma rodada** de EVAL |
| **3 – cheio** | segurança e papéis, schema/migração de dado, importação com escrita, infra de deploy/chaves/Traefik, tudo irreversível | processo completo, como hoje |

Cortes adicionais:
- **EVAL:** no máximo **duas rodadas** por DEM; a terceira só com decisão do ARQUITECT.
- **Release por lote:** um PR de release agrupa várias DEMs aceitas.
- **Classificação:** o PLANNER diz o nível ao abrir a DEM; na dúvida, sobe um nível. O ARQUITECT pode reclassificar.

### O que NÃO muda no modo ágil
- **CI verde** para mesclar; **backup antes do deploy**; **HTTP 200** ao final.
- Nada de **exclusão de dados, restauração de banco, migração ou importação com escrita** sem o ARQUITECT (ADR-016).
- A **regra do porquê**: se o objetivo mudou, reabre o intent.

### Fim do modo ágil (gatilho)
O modo ágil termina quando **a v1 for declarada pelo ARQUITECT** como rodando e testada. Nesse dia:
1. fecha-se a lista de **dívidas aceitas** (abaixo), item por item;
2. os dados de teste são limpos e entram dados reais;
3. as ADRs 006 e 007 voltam a valer integralmente, salvo decisão em contrário.

## Consequências

**Positivas**
- Menos rodadas e menos documentos nas mudanças pequenas; mais entregas por semana.
- A proporcionalidade fica registrada: o atrito que sobra está onde o risco está.

**Negativas / trade-offs**
- Menos redes de proteção em níveis 1 e 2: erros pequenos podem passar. O CI mitiga.
- O nível é uma classificação humana: pode ser errada. A regra "na dúvida, sobe" mitiga.
- As dívidas aceitas ficam abertas por tempo definido.

---

## Registro de dívidas aceitas até a v1

> Cada item tem **dono**, **risco** e **gatilho de fechamento**. O ARQUITECT aceitou conscientemente
> (19/10: "tudo é teste até a v1; a partir da v1 fechamos, bloqueamos e entramos com dados reais").

| # | Dívida | Risco aceito | Gatilho de fechamento |
|---|---|---|---|
| D-01 | **Credencial de seed pública** (`admin@gsi.ebd` / `senha123`, DEM-012) | quem ler o repositório público pode entrar como admin no site; ver leads, aprovar estudos | **antes de dados reais ou de divulgação** (ADR-008 já bloqueia a divulgação) |
| D-02 | **Chave operacional com shell completo** (ADR-016, §dívida 1) | um agente com a chave tem acesso de root-equivalente à VPS | **na virada da v1**: comando `diag` no script de entrada + chave com `restrict` |
| D-03 | **Sem ruleset de tags `v*`** e conta admin única | qualquer sessão autenticada como o dono publica por tag | na virada da v1, ou quando entrar um segundo colaborador |
| D-04 | **Environment `producao` sem aprovador** (ADR-016) | deploy sem pausa humana | revisar na virada da v1 |
| D-05 | **Dump do banco só na VPS** (manifesto, não cópia) | perda da VPS = perda do backup | **antes de dados reais**: cópia fora do servidor |
| D-06 | **`can_manage` sem ambiente / posse por id do cliente** (DEM-010) | um coordenador age sobre usuário de outro ambiente | **antes de ter mais de um ambiente real** |
| D-07 | **Aprovação de estudo por uma só assinatura** (DEM-011, ADR-011 não implementada) | o admin sozinho libera estudo; sem hash de conteúdo | antes de liberar estudos a coordenadores reais |
| D-08 | **`logout` não limpa `AdminState`** (WARN da DEM-002) | resíduo de sessão na mesma aba | na migração do admin (DEM-005) |
| D-09 | **Dados de teste e lixo de EVAL** (`eval/tmp-*`, usuários demo) | confusão e vazamento de dado de teste | **na virada da v1**: limpeza de histórico antes de dados reais |

### Cuidado de contexto (não é dívida, é premissa)
A premissa "tudo é teste" **vale enquanto nenhum dado real de pessoa entrar** na plataforma. O
formulário de contato público, se estiver ativo, **coleta dados reais de visitantes**: esses leads
são acessíveis por qualquer um que entre como admin (D-01). Se houver leads reais no banco hoje, tratar
esse item como exceção e adiantar o D-01.

---

## Mensagem curta ao perfil DEPLOY (Codex)

```markdown
PARA: DEPLOY (Codex)
DE: ARQUITECT (via AUXILIAR-ARCHITECT)
DATA: 2026-10-19
ASSUNTO: modo ágil até a v1

1. O ARQUITECT prioriza agilidade até a v1. Haverá uma ADR-017 (proposta) com três níveis de
   processo; publicar continua sendo seu, nos termos da ADR-016.
2. O que continua: CI verde, backup antes do deploy, HTTP 200 ao final, e nada de exclusão de
   dados, restauração de banco, migração ou importação com escrita sem o ARQUITECT.
3. Dívidas aceitas até a v1 estão registradas (D-01 a D-09) com gatilho. Não corrija sozinho
   nenhuma delas fora da lista; se encontrar risco novo, registre na jornada e avise o ARQUITECT.
4. Na dúvida sobre nível ou escopo, pare e devolva ao PLANNER.
```
