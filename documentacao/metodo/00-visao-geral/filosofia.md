# Filosofia — O que rege o método

> **O projeto não é estático; é um organismo em evolução.** A arquitetura cresce por **decisões estruturais** (ADRs) e a plataforma é entregue por **ciclos táticos** (DEMs). O método separa com rigor **"o que somos / para onde vamos"** de **"o que faremos agora"**.

## 1. Os dois pilares

### Pilar A — ADRs: a Constituição

As ADRs são o conhecimento consolidado e as **leis** do projeto. Não descrevem tarefas; registram **decisões** que mudam o curso da plataforma.

- **Gatilhos:** novo conhecimento (técnico/negócio), mudança de regra de negócio (legal/regulatória), ou novo horizonte (expansão para uma área nova).
- **Características:** longa duração (uma vez aceita, é lei até ser substituída) e impacto transversal (afeta muitas DEMs futuras).
- **Regra dura:** nenhuma DEM pode contrariar uma ADR `Accepted`. Se uma DEM precisa quebrar uma ADR, o ARQUITECT cria uma nova ADR que a substitui **antes** de a DEM começar.

Como registrar: [`../05-decisoes-adr/como-usar-adr.md`](../05-decisoes-adr/como-usar-adr.md).

### Pilar B — DEMs: a Ação

As DEMs são as **unidades de trabalho tático** — implementar uma feature, corrigir um defeito, fazer um ajuste técnico.

- **Características:** curta duração (ciclo definido), foco específico (resolve um problema pontual), paralelizável (várias DEMs simultâneas, respeitando dependências).
- Cada DEM é um **pacote de pastas por agente** — ver [`../04-estrutura-dem/estrutura-da-dem.md`](../04-estrutura-dem/estrutura-da-dem.md).

## 2. A camada de objetivo: intent → spec → DEM

A especificação **não** é o primeiro artefato. Antes dela vem o **intent** — o *porquê*, assinado pelo ARQUITECT. Sem essa camada, o especificador e o dono convergem cedo demais numa spec que **já é uma solução**, e ninguém no fim consegue responder *"isso ainda é o que queríamos?"*.

```
INTENT   →   SPEC    →   DEM / TASKS   →   código
porquê       o quê        o como            evidência
outcome      contrato     decomposição
limites      aceitação
```

- **Intent** é **julgamento** (cabe ao ARQUITECT assinar); **spec** é **contrato** (cabe ao PLANNER redigir). São jobs diferentes — não os misture no mesmo arquivo nem no mesmo dono.
- Detalhe completo em [`../03-camada-intent/camada-intent.md`](../03-camada-intent/camada-intent.md).

## 3. A evolução das cercas (por que o método é assim)

O método existe porque agentes de IA, sem limites, **alucinam** (inventam fora da spec), **quebram alinhamento** (trocam stack, refatoram fora de escopo, "melhoram" o não pedido) e **escalam privilégio** (decidem arquitetura/negócio sozinhos). As cercas contra isso amadureceram em quatro estágios:

1. **Textuais** — regras escritas ("não faça X").
2. **Estruturais** — a organização dos arquivos garante o controle (um dono por arquivo; pastas por papel). O que era pedido por texto passa a ser imposto pela estrutura.
3. **Verificadas** — nada existe até estar no disco/git, conferido. Veredito amarrado a hash; jornada materializada é pré-condição.
4. **De objetivo** — o *porquê* vira artefato assinado (intent), não memória de sessão. Fecha o **drift de objetivo** (implementar a feature certa para o problema errado), que as três anteriores não cobriam.

## 4. Princípio constitucional

> **O código serve à documentação, não o contrário.**
> O que não está na **spec** não entra no código. O que não está no **visual** não chega à tela. Divergência detectada → **atualiza o documento antes do código**.

## 5. O que faz este método funcionar (resumo operacional)

- **Cada arquivo tem um dono único.** Briefing é do PLANNER; jornada é do próprio agente que executa.
- **A cerca de papel é bidirecional.** Tarefa fora do papel devolve-se; ninguém executa o trabalho de outro papel.
- **O ARQUITECT é a origem e o destino.** Nenhum gate humano é bypassável (intent, spec, aceite de entrega, aceite de release, decisões sensíveis).
- **O ciclo termina no disco.** Todo fechamento de DEM acaba em snapshot git da documentação e atualização do painel.

> Próximo: [`ciclo-de-vida.md`](ciclo-de-vida.md) — como isso vira um fluxo executável.
