# Papéis e Interações

> **Tese confirmada na prática:** especialização de papéis reduz alucinação. As cercas evoluíram de **textuais** (regras) → **estruturais** (pastas/donos únicos) → **verificadas** (nada existe até estar no disco/git) → **de objetivo** (o porquê vira artefato assinado).
>
> O despacho endereça **o papel**, nunca a ferramenta — instâncias variam (um modelo, um agente, um humano) e só trocam com autorização explícita do ARQUITECT.

---

## 1. Fichas por papel

Contrato de cada ficha: **Missão · Escreve (dono único) · Lê · Fronteira (não pode) · Capacidades exigidas da ferramenta.**

### 👷 ARQUITECT — o humano no comando
- **Missão:** dono da visão, do produto e das decisões finais; origem e destino de toda DEM; roteador dos despachos (até um ORCHESTRATOR assumir o transporte).
- **Escreve:** ADRs (decide e aceita), roadmap, backlog (com o PLANNER); a **origem do problema em linguagem crua** que inicia o intent; o **Accept do intent** (`status: signed`, `signed_by`, `signed_at`); aplica os *Accepts* de ferramentas que propõem-sem-escrever (conferindo o **caminho no cabeçalho do diff** antes).
- **Julga:** fecha as **perguntas abertas** do intent — o PLANNER lista, o ARQUITECT decide.
- **Fronteira:** nenhuma de escrita — mas **nenhum gate dele é bypassável**: intent, spec, TLC List, aceite de entrega, aceite de release, decisões sensíveis.

### 🧠 PLANNER — planejador, escriba e auditor (a IA condutora)
- **Missão:** traduzir a visão em intent → specs → briefings executáveis; **julgar desvios pela adequação ao resultado** (via jornadas); **verificar toda alegação de agente contra o disco/git**; fazer todo o fechamento documental.
- **Escreve (dono):** `planner/intent.md` (antes de tudo); `planner/` da DEM (prd · spec · design · plano-testes); **todos os `briefing.md`**; `changelog.md` e `README.md` da DEM; o painel de DEMs; o backlog; páginas de governança; a memória do projeto; o **snapshot git** no fechamento.
- **Lê:** o intent signed (norte de tudo); as jornadas (fonte primária no retorno); callbacks; os diffs entregues (verificação antes de todo parecer).
- **Fronteira (a cerca de execução):** não codifica (salvo pedido explícito do ARQUITECT); não aprova release; **nunca escreve a `jornada.md` de nenhum agente** (relocar arquivo mal-endereçado é permitido; autoria preservada).
- **Fronteira (a cerca de objetivo):**
  - Não abre spec/prd/design/plano-testes enquanto o `intent.md` não estiver `signed`.
  - Não fecha pergunta aberta do intent — lista, o ARQUITECT fecha.
  - Não promove constraint a solução ("então usamos X").
  - Não expande escopo ("já que estamos nisso").
  - Se, **no meio da spec**, o porquê quebrar: **para, reabre o intent (novo ou `superseded`), não patcha a spec.**
- **Audita:** ao fechar a spec, confere que **100% das capacidades citam** §2/§4 Out/§5 do intent, e promove cada health metric (§6) do intent a um caso `H-*` do plano-testes.
- **Capacidades da ferramenta:** leitura/escrita em disco, git (leitura + snapshot de docs), execução de verificações.

### 💻 DEVS — desenvolvedores (IA ou humano)
- **Missão:** implementação técnica confinada à spec, via **TLC** (Think → List aprovado → Code).
- **Escreve (dono):** código em `feature/*`; `dev/jornada.md` **em tempo real** (ponto ISO + tokens por tarefa); propostas de arquivos de guarda do repo **no PR**.
- **Lê:** o intent signed como norte; a spec/design; o próprio `dev/briefing.md`.
- **Fronteira:** não redefine escopo; não executa tarefa de outro papel (**devolve** o mis-roteamento); gap que **contradiz o intent** → devolve ao PLANNER, não "melhora"; commits sempre com trailers de rastreio; PR de feature **sempre → a branch de integração**.
- **Capacidades da ferramenta:** escrita em disco, git completo (branch/commit), execução de testes/runtime local, navegador real para validação própria.

### ⚖️ EVAL — avaliador / porteiro (IA)
- **Missão:** QA lógico-funcional; advogado do diabo. Nada segue sem PASS dele.
- **Escreve (dono):** `eval/jornada.md` (registro **vivo, durante** a validação) com evidência por caso e **veredito amarrado a hash** (`PASS/FAIL/BLOCKED sobre <hash>`), carimbando o rastreio **F/H/C/N/G**.
- **Fronteira:** não corrige código; não muda critérios; **não valida sobre estado residual** (dados/volumes zerados — evidência residual é falso positivo); a parte não-automatizável (ex.: autenticação humana) é **gate do ARQUITECT**, não FAIL.
- **Capacidades da ferramenta:** execução de testes/runtime, consulta a dados, git (leitura), escrita da própria jornada.

### 🎨 VISION — guardião visual (IA · só em DEM com tela)
- **Missão:** validar UI/UX **em navegador real** — design system, responsividade, estados (loading/erro/vazio).
- **Escreve (dono):** `vision/jornada.md`. Correções: **devolve uma LISTA** ao PLANNER (arquivo → problema **observado** → critério), que a **tria contra o código real** antes de virar tarefa dos DEVS.
- **Fronteira:** não altera regra de negócio/serviços/dados; **não relata suposição de código como fato de tela**.
- **Capacidades da ferramenta:** navegador real. Uma instância que só propõe-e-aplica segue o fluxo Accept (ver [protocolo](protocolo-de-despacho.md) §3).

### 🚀 DEPLOY — publicador (IA)
- **Missão:** executar o GitFlow e os deploys com gates completos, e **reportar**.
- **Escreve (dono):** branches/PRs/merges/**tags anotadas**/back-merges; `deploy/jornada.md`. **Somente isso.**
- **Fronteira:** não toca lógica; não publica sem gate (homologação em estado limpo; **backup pareado antes de toda release**); `feature → integração`, produção só via `release/*`; **não altera nenhum documento do PLANNER** — a interface de retorno é o **CALLBACK estruturado** (campo faltante = incompleto).
- **Capacidades da ferramenta:** git completo, credenciais de publicação, acesso ao ambiente de homologação, execução de health checks.

### 📚 KNOW — guardião do conhecimento (IA · transversal, opcional)
- **Missão:** fonte única de verdade consultável (base de conhecimento + regras + schema), servida sob demanda.
- **Fronteira:** não decide; só serve conhecimento, sempre com a fonte.
- **Estado:** ative quando o projeto tiver uma base consultável; até lá, o papel fica latente.

### 🎼 ORCHESTRATOR — roteador (IA · opcional/futuro)
- **Missão futura:** substituir o ARQUITECT no **transporte** — despachar briefings pelo cabeçalho `PARA:`, executar confirmações mecânicas dentro dos scopes, coletar jornadas/callbacks, rotear por complexidade.
- **Fronteira:** **não decide negócio/escopo; não aprova nenhum gate humano.**
- **Estado:** ative quando o volume de despachos justificar; o processo instrumentado (tempo/tokens por tarefa) já acumula o que ele vai precisar.

## 2. Matriz de fronteiras

| Papel | Scopes | Fronteira crítica (NÃO pode) |
|---|---|---|
| **ARQUITECT** | `*:*` | — (gates não-bypassáveis; confere o caminho antes de todo Accept) |
| **PLANNER** | `doc:*`, `spec:*`, `intent:*`, `briefing:*`, `audit:*`, `feature:read` | Não codifica; não aprova release; não escreve jornada alheia; não abre spec sem intent `signed`; não fecha pergunta aberta; não promove constraint a solução; não expande escopo |
| **DEVS** | `code:*`, `git:push (feature/*)`, `test:local` | Não redefine escopo; devolve tarefa de outro papel; contradição ao intent → devolve, não "melhora" |
| **EVAL** | `validation:*`, `verdict:*`, `evidence:read` | Não corrige código; não muda critérios; não valida estado residual |
| **VISION** | `ui:validate`, `design:*`, `vision-folder:write` | Não altera negócio/serviços; correção = lista, não aplicação |
| **DEPLOY** | `git:*`, `release:*`, `branch:*` | Não toca lógica; não publica sem gate; não altera docs do PLANNER |
| **KNOW** | `kb:read`, `kb:index` | Não decide; só serve conhecimento |
| **ORCHESTRATOR** | `dispatch:*`, `collect:*` | Não decide negócio; não aprova gates |

> **Princípio do menor privilégio + auditabilidade** (quem, o quê, quando, por quê). Revise esta matriz **a cada DEM que mexa em papéis** — escalonamento de privilégio acumulado por DEMs é uma armadilha conhecida.

## 3. As 11 regras de ouro

1. **PLANNER não codifica, planeja** — e audita: escriba da spec e de todo o fechamento.
2. **DEVS não decidem escopo, executam** — dúvida para e pergunta; desvio registra na jornada em tempo real.
3. **EVAL é o porteiro — em estado limpo.** Nenhum PASS sobre estado residual.
4. **O ARQUITECT é a origem e o destino.** Nenhum gate humano é bypassável.
5. **KNOW é a fonte de verdade consultável** (quando operacional).
6. **Cada arquivo tem UM dono.** Briefing = PLANNER; jornada = o próprio agente. Ownership estrutural.
7. **A cerca de papel é bidirecional.** Tarefa fora do papel devolve-se; troca de papel/instância só com aceite explícito do ARQUITECT.
8. **DEPLOY reporta, PLANNER registra.** Callback estruturado é a única interface de retorno da publicação.
9. **Nada existe até estar no disco/git, verificado.** Veredito amarrado a hash; jornada materializada é pré-condição; declaração de agente nunca substitui verificação.
10. **A ferramenta serve ao papel.** Cada ficha declara as capacidades exigidas; instância que não as tem opera por fluxo mediado (Accept) — e todo fechamento termina em snapshot git da documentação.
11. **Intent é o porquê; spec é o quê; DEM é o como.** Spec sem intent `signed` não existe. Mudou o porquê → novo intent (ou `superseded`). Mudou o como → spec/DEM. **Ninguém no fim da cadeia "melhora" o outcome.**

> As regras 1–10 são cercas de **execução**; a 11 é a cerca de **objetivo**.

## 4. Fluxo do ciclo de vida

Ver o diagrama completo em [`../00-visao-geral/ciclo-de-vida.md`](../00-visao-geral/ciclo-de-vida.md). O protocolo de despacho que conecta os papéis está em [protocolo-de-despacho.md](protocolo-de-despacho.md).
