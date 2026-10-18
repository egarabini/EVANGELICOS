# ADR-014: Saída do Reflex — FastAPI + Jinja2 + HTMX

- **Status:** **Proposed** — aguarda aceite do ARQUITECT. Quando aceita, **substitui a ADR-001 na
  cláusula do framework** (ver §"O que permanece da ADR-001").
- **Data:** 2026-10-18 (v1) · **2026-10-18 (v2 — emendas A, C, D e F da revisão do AUXILIAR-ARCHITECT)**
- **Decisores:** ARQUITECT (decisão 8.1 do intent da DEM-005) · redação e emendas pelo PLANNER
- **Gatilho:** Novo Horizonte (troca de framework)

---

## Contexto e Problema

O Reflex foi a base da aplicação (ADR-001) e entregou o produto em produção. Mas acumulou três
evidências de que o custo de mantê-lo passou o ganho:

1. **16/10** — concatenar `Var` com texto dentro de `rx.foreach` **derrubou o app em produção**;
   o erro só aparecia na **compilação da página**, não no import nem na suíte.
2. **DEM-001** — duas funções com o mesmo nome (`_estudos_tab`) fizeram a **aba de Aprovação
   mostrar a tela errada, sem aviso**: Python não reclama de redefinição.
3. A ferramenta exige **regras compensatórias** que não existem em Python normal: nunca
   `Var + str`, listas planas no estado, teste de compilação de cada página.

O ARQUITECT perdeu a confiança no Reflex como base e pediu algo mais sólido, leve e com UX
mais atual.

## Opções Consideradas

| Opção | Descrição | Custo / risco | Veredito |
|---|---|---|---|
| A | Ficar no Reflex e endurecer as cercas | **Baixo e imediato**; mantém a classe de erro de `Var`, o acoplamento ao framework e a UI datada | Descartada: as cercas são compensação, não solução |
| **B** | **FastAPI + Jinja2 + HTMX** (Alpine.js para interações pequenas) | **~3.300 linhas** a reescrever; **dois stacks vivos durante meses**; risco novo de sessão compartilhada (§ abaixo) | **Escolhida** (decisão 8.1) |
| C | Django | Reescrita de modelos/ORM + curva de admin | Descartada |
| D | Outro framework full-stack Python | Mesmo risco de framework opinativo, sem o ganho do HTML servidor | Descartada |

## Decisão

Adotar **FastAPI + Jinja2 + HTMX** como base da aplicação, **mantendo Python e PostgreSQL**.
Muda a camada de UI/HTTP; o domínio (`models/`, `services/`, `scripts/`, `ai/`) é reaproveitado.

A migração é **por rotas, com convivência** — o Traefik já está na frente e pode receber
roteadores por caminho. **Paridade primeiro**: nenhuma função nova durante a migração. Telas
novas, busca (DEM-D) e assistente (DEM-E) **já nascem na base nova** (decisão 8.3).

## Decisão pendente e BLOQUEANTE: sessão compartilhada

Levantado na revisão do AUXILIAR-ARCHITECT (achado A) e **confirmado no código**:

- o login vive em **estado do Reflex** (`gsi_ebd/states/auth.py`); **não existe** cookie
  assinado, JWT, `SessionMiddleware` nem `set_cookie` em nenhum lugar do backend;
- o Traefik tem **um** roteador (`Host(didasko.app.br)`) apontando para a porta **3000**
  (frontend do Reflex).

Consequência: **uma rota servida pela base nova não sabe quem está logado.** Isso afeta a
**primeira** rota migrada, não a última, e afeta a matriz papel × rota (H-04).

**Antes da primeira rota migrada**, o PLANNER deve registrar na spec da DEM-005:
1. o **mecanismo de sessão compartilhado** (ex.: cookie assinado emitido no login, lido pelas
   duas bases), com flags, expiração e revogação;
2. um **spike descartável**: uma rota trivial na base nova, atrás do Traefik, autenticada pela
   sessão do login atual. **Se o spike falhar, esta ADR precisa ser reaberta** — a convivência
   por rotas não se sustenta;
3. a coluna **"base que serve a rota"** na matriz papel × rota.

## O que permanece da ADR-001 (a substituição é só da cláusula do framework)

A ADR-001 **não é revogada por inteiro**. Substitui-se **apenas** a cláusula "framework de
aplicação = Reflex". Permanecem, e continuam lei:

- **Python 3.12** como linguagem da aplicação;
- **PostgreSQL** como banco;
- **ChromaDB** e **Ollama** como estão;
- **Docker Compose + Traefik** como infraestrutura;
- **"Nada de Node/TS na aplicação"** — e aqui a clareza importa: **HTMX e Alpine.js são arquivos
  estáticos servidos pelo próprio app, não uma stack Node**. Se o Tailwind for usado, entra pela
  **CLI independente**, gerando CSS estático no build — nunca um `package.json` de aplicação;
- o **corpus `:ro`**, fora do git e da imagem (ADR-002).

Quando a 014 for aceita, a ADR-001 passa a **"Superseded in part by ADR-014"** — não
`Superseded` inteira.

## Consequências

**Positivas**
- HTML servido pelo servidor: erro de template aparece no teste, não em produção.
- Sem `Var`: **a classe de erro do dia 16/10 deixa de existir**.
- UX mais atual (HTMX) sem SPA.

**Negativas / trade-offs**
- **~3.300 linhas** a reescrever (`states/`, `pages/`, `components/`).
- `services/` tem **8 de 13** arquivos com `import reflex`, quase só por `rx.session` — troca
  mecânica para `Session` do SQLModel.
- **Dois stacks vivos durante meses**: disciplina de rota e sessão compartilhada são obrigatórias.
- **Classes de risco novas**, que a spec da DEM-005 deve cobrir desde o dia 1:

| Risco novo | Mitigação a exigir na spec |
|---|---|
| Variável inexistente no Jinja renderiza **vazio**, sem erro | `StrictUndefined` |
| Template quebrado só aparece ao renderizar | teste que **renderiza todas as rotas por papel** (substitui `test_paginas.py`) |
| CSRF em formulários e trocas HTMX | token por sessão, validado em toda requisição que altera estado |
| Cookie de sessão (flags, expiração) e cabeçalhos de segurança | decisão registrada na spec |
| Autorização repetida em cada rota | dependência única de papel, testada pela matriz papel × rota |

**Neutras**
- A produção continua no Reflex até a última rota migrar.
- `models/` (753), `scripts/` (898) e `ai/` (87) **não** importam Reflex: ficam como estão.

## Impacto nas DEMs

- **Substitui, em parte,** a ADR-001 (só a cláusula do framework) quando aceita.
- **Depende da DEM-004 — Etapa 1 **e** Etapa 2**: a migração publica o tempo todo; sem deploy
  por pipeline, cada rota migrada seria um deploy manual. **A primeira rota só migra depois da
  Etapa 2.** (emenda D)
- **DEM-002 antes da DEM-005**: a guarda de papel no `/admin` é feita **agora, no Reflex** — o
  furo existe hoje e a migração do admin vem primeiro.
- **DEM-005** implementa a migração — **admin e telas novas primeiro; lição do aluno por
  último** (decisão 8.2, protege H-02).

## Restrições

- **Nenhuma** mudança de schema ou de dado.
- Volta atrás possível **a cada rota**.
- Nenhum código de terceiros copiado.
- **Baselines que faltam antes da DEM-005:** matriz papel × rota (**com a coluna "base que
  serve a rota"**) e inventário das rotas atuais.

## Referências

- Revisão que originou as emendas: `documentacao/visao/REVISAO-ADR-014-e-DEM-005-aux-architect.md`
- Intent: `documentacao/dem/DEM-202610-005-saida-do-reflex/planner/intent.md`
