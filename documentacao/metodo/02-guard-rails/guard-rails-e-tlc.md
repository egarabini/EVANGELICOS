# Guard-rails de agentes & o ritual TLC

> Delegar implementação a agentes (IA ou humanos) sem limites explícitos leva a três falhas: **alucinação** (inventar fora da spec), **quebra de alinhamento** (trocar stack, refatorar fora de escopo, "melhorar" o não pedido) e **escalada de privilégio** (decidir arquitetura/negócio sozinho). Estes mecanismos contêm as três.

## 1. Princípio constitucional

> **O código serve à documentação, não o contrário.**

- O que não está na **spec** não pode entrar no código.
- O que não está no **visual** não pode chegar à tela.
- Divergência detectada → **atualiza o documento antes do código.**

## 2. Os quatro guard-rails comportamentais (todo agente de IA)

- **Think Before Coding** — declare assunções e ambiguidades; **nunca escolha em silêncio**.
- **Simplicity First** — código mínimo que resolve; sem flexibilidade não pedida.
- **Surgical Changes** — toque só o necessário; **não "melhore"** código adjacente fora do escopo.
- **Goal-Driven Execution** — não termine até os testes provarem os critérios de aceite da DEM.

> **Estilo é julgamento, não regra.** Escreva código que **lê como o código ao redor** (densidade de comentário, nomes, idioma). Não se listam regras de estilo de propósito — o agente decide pelo contexto. Os guard-rails acima são de **escopo/verificação** (governança), não de estilo.

## 3. O fluxo TLC (Think → List → Code)

Em **toda** sessão de implementação, nesta ordem — nada de código antes do **List aprovado**:

1. **Identifique a DEM** (a pasta da demanda, ou a fornecida no handoff).
2. **Leia, nesta ordem:** o perfil do projeto / contexto → as convenções → o plano da DEM em `planner/` (`intent.md` → `prd.md` → `spec.md` → `design.md` → `plano-testes.md`) → o **seu** `dev/briefing.md`.
3. **Think** — declare assunções, ambiguidades e conflitos com ADRs.
4. **List** — liste os arquivos que serão criados/modificados, os riscos e a **ordem dos passos**. **Aguarde aprovação.**
5. **Code** — só então implemente, **um passo por vez**, registrando na `jornada.md` em tempo real.

**Dúvida ANTES de executar:** sem dúvida → execute; com dúvida → registre na jornada e **devolva ao PLANNER** (nova Tarefa no `briefing.md`); só então prossiga. Nunca execute sobre assunção não confirmada — escolha em silêncio aqui gera retrabalho.

## 4. Arquivos de guarda obrigatórios (por repositório)

Todo repo de código do projeto **deve** conter, e todo agente de código **deve** ler antes de escrever:

| Arquivo | Conteúdo |
|---|---|
| **`AGENTS.md`** | Manifesto comportamental do agente de código: guard-rails + TLC + restrições absolutas + ponteiro para a DEM atual. |
| **`CLAUDE.md`** | Equivalente comportamental para agentes Claude (aponta para os demais). |
| **`CONVENTIONS.md`** | Padrões de código/teste/segurança, commit, rastreio requisito↔teste, Definition of Ready/Done. |
| **`PROJECT_CONTEXT.md`** *(recomendado)* | Stack, ADRs vigentes e a seção **"o que NÃO mudar"**. |

Modelos neutros prontos em [`../arquivos-de-guarda/`](../arquivos-de-guarda/README.md) — copie para a raiz do repo e complete com o [perfil do projeto](../perfil-do-projeto/perfil-do-projeto.template.md).

## 5. Registrar como decisão

Estes guard-rails, o TLC e a exigência dos arquivos de guarda devem ser **registrados como uma ADR** no seu projeto (é a decisão que autoriza delegar código a agentes com segurança). Ver [`../05-decisoes-adr/como-usar-adr.md`](../05-decisoes-adr/como-usar-adr.md).
