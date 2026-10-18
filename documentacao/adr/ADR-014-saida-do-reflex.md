# ADR-014: Saída do Reflex — FastAPI + Jinja2 + HTMX

- **Status:** **Proposed** — aguarda aceite do ARQUITECT. Quando aceita, **substitui a ADR-001**.
- **Data:** 2026-10-18
- **Decisores:** ARQUITECT (decisão 8.1 do intent da DEM-005) · redação do PLANNER
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

| Opção | Descrição | Veredito |
|---|---|---|
| A | Ficar no Reflex e endurecer as cercas | Descartada: as cercas são compensação de framework, não solução |
| **B** | **FastAPI + Jinja2 + HTMX** (Alpine.js para interações pequenas) | **Escolhida** (decisão 8.1) |
| C | Django | Descartada: reescrita de modelos/ORM |
| D | Outro framework full-stack Python | Descartada: mesmo risco de framework opinativo |

## Decisão

Adotar **FastAPI + Jinja2 + HTMX** como base da aplicação, **mantendo Python e PostgreSQL**.
Muda a camada de UI/HTTP; o domínio (`models/`, `services/`, `scripts/`, `ai/`) é reaproveitado.

A migração é **por rotas, com convivência** — o Traefik já está na frente e pode direcionar rota
a rota. **Paridade primeiro**: nenhuma função nova durante a migração. Telas novas, busca
(DEM-D) e assistente (DEM-E) **já nascem na base nova** (decisão 8.3).

## Consequências

**Positivas**
- HTML servido pelo servidor: erro de template aparece no teste, não em produção.
- Sem `Var`: o estado é Python comum — a classe de erro do dia 16/10 deixa de existir.
- UX mais atual (HTMX) sem SPA.

**Negativas / trade-offs**
- **~3.300 linhas** a reescrever (`states/`, `pages/`, `components/`).
- `services/` tem **8 de 13** arquivos com `import reflex`, quase só por `rx.session` — troca
  mecânica para `Session` do SQLModel.
- Dois stacks vivos durante a migração: disciplina de rota é obrigatória.

**Neutras**
- A produção continua no Reflex até a última rota migrar.
- `models/` (753), `scripts/` (898) e `ai/` (87) **não** importam Reflex: ficam como estão.

## Impacto nas DEMs

- **Substitui a ADR-001** quando aceita: a ADR-001 passa a `Superseded by ADR-014`.
- **Depende da DEM-004**: sem CI não há rede de segurança para migrar rota a rota.
- **DEM-005** implementa a migração — **admin e telas novas primeiro; lição do aluno por
  último** (decisão 8.2, protege H-02).
- **DEM-002** (guarda de papel no `/admin`) deve ser feita **agora, no Reflex**: o furo existe
  hoje e não vale esperar a base nova.

## Restrições

- **Nenhuma** mudança de schema ou de dado.
- Volta atrás possível **a cada rota**.
- Nenhum código de terceiros copiado.
- **Baselines que faltam antes da DEM-005:** matriz papel × rota e inventário das rotas atuais
  (a serem levantados na spec da DEM-005).
