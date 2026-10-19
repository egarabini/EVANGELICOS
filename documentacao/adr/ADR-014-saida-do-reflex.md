# ADR-014: Saída do Reflex — a v1 na base nova (FastAPI + Jinja2 + HTMX)

- **Status:** **Accepted** — aceito pelo ARQUITECT em **2026-10-19** (a v3: a v1 na base nova).
- **Data:** 2026-10-18 (v1) · 2026-10-18 (v2 — emendas da revisão) · **2026-10-19 (v3 — a v1 é a base nova)**
- **Decisores:** ARQUITECT (Eduardo) · redação e emendas pelo PLANNER
- **Gatilho:** Novo Horizonte (troca de framework)
- **v3 (decisão do ARQUITECT, 19/10):** a **v1 não é em Reflex**. A saída do Reflex deixa de ser
  "pós-v1" e passa a ser **o núcleo da v1**. A estratégia muda de **migração por rotas com
  convivência** para **v1 construída ao lado, com uma única virada**.

---

## Contexto e Problema

O Reflex foi a base da aplicação (ADR-001) e entregou o produto em produção. Mas acumulou
evidências de que o custo de mantê-lo passou o ganho:

1. **16/10** — concatenar `Var` com texto dentro de `rx.foreach` **derrubou o app em produção**;
   o erro só aparecia na **compilação da página**.
2. **DEM-001** — duas funções com o mesmo nome fizeram a **aba de Aprovação mostrar a tela errada**,
   sem aviso.
3. A ferramenta exige **regras compensatórias** que não existem em Python normal.

**A v0 é o Reflex atual, de teste.** O ARQUITECT decidiu (19/10) que **a v1 é a base nova** — e que
os dados de teste serão limpos na virada. Isso **remove a necessidade de convivência**: não há
usuário em produção a preservar durante uma migração longa.

## Opções Consideradas

| Opção | Descrição | Custo / risco | Veredito |
|---|---|---|---|
| A | Ficar no Reflex e endurecer as cercas | baixo e imediato; mantém a classe de erro e a UI datada | Descartada |
| **B** | **FastAPI + Jinja2 + HTMX** — **v1 construída ao lado** | **o custo é a v1 inteira** (não um pedaço); sem convivência, sem sessão compartilhada | **Escolhida** |
| C | Django | reescrita de modelos/ORM | Descartada |
| D | Outro framework full-stack Python | mesmo risco, sem o ganho do HTML servido | Descartada |

## Decisão (v3)

Adotar **FastAPI + Jinja2 + HTMX** como base **da v1**, com **uma única virada**:

1. **A v1 é construída ao lado**, em paralelo à v0 (que continua rodando para testes).
2. **O domínio é reaproveitado** — `models/`, `services/`, `scripts/`, `ai/`, ajustando o que usa
   `rx.session` para a sessão do SQLModel. Não se reescreve o domínio.
3. **Telas novas** em FastAPI + Jinja2 + HTMX — nenhuma tela nova nasce em Reflex (a decisão 8.3
   passa a ser **consequência natural**, não uma regra à parte).
4. **A virada é uma só**, pelo Traefik: a v1 assume o domínio; a v0 fica como retorno rápido.
5. **Nada de migração de dados**: os dados são de teste e serão limpos na virada (ADR-018).

## O que a v3 remove da v2

- **A migração por rotas com convivência** — não há mais o que conviver.
- **O bloqueio da sessão compartilhada** (achado A da revisão) — a v1 tem **a própria
  autenticação desde o início** (sessão de servidor no Jinja2), sem nada a compartilhar com o
  Reflex. O *spike* de sessão deixa de ser necessário.
- A "primeira rota só migra depois da Etapa 2 do CD" — o CD já está entregue e a virada é única.

## O que permanece da v2 (e continua valendo)

- **Cláusulas da ADR-001 que ficam**: Python 3.12, PostgreSQL, ChromaDB, Ollama, Docker/Traefik,
  "sem Node/TS na aplicação" (HTMX/Alpine são arquivos estáticos; Tailwind pela CLI), o corpus
  `:ro`. A ADR-001 é **substituída só na cláusula do framework**.
- **As classes de risco novas** e as mitigações: `StrictUndefined` no Jinja; teste que **renderiza
  todas as rotas por papel**; CSRF em formulários/HTMX; cookie de sessão (flags, expiração);
  autorização por dependência única, testada pela matriz papel × rota.
- **Os baselines que faltam**: inventário das rotas e a **matriz papel × rota** (H-04/H-05).

## Consequências

**Positivas**
- A v1 nasce **sem dívida de framework** e sem convivência: mais simples que a rota a rota.
- O domínio inteiro sobrevive; o esforço é a camada de UI/HTTP.
- A classe de erro do `Var` deixa de existir.

**Negativas / trade-offs**
- **O custo é a v1 inteira** (as telas + o auth), não um pedaço: é o maior item do projeto até aqui.
- **Duas bases rodando até a virada** (a v0 de teste); exige disciplina de não criar tela na v0.
- **Um único evento de virada**: se falhar, o retorno é a v0 inteira (que fica de pé).

## Impacto nas DEMs

- **A DEM-005 passa a ser a v1** — construída ao lado, com a virada única.
- **A DEM-002 (guarda de papel) continua valendo**: a matriz papel × rota migra inteira para a v1.
- **O fluxo de obras/estudos (DEM-011)** é construído **já na v1** — não há o que migrar.
- **Depende de**: o inventário (H-04/H-05), a ordem das telas, e a decisão de **quando** é a virada.

## Referências

- Revisão original: `documentacao/visao/REVISAO-ADR-014-e-DEM-005-aux-architect.md`
- Intent: `documentacao/dem/DEM-202610-005-saida-do-reflex/planner/intent.md`
- Definição da v1: `documentacao/visao/DEFINICAO-DA-V1.md`

