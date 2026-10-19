# Definição da v1 (revisada em 19/10)

> Ligada à [ADR-018](../adr/ADR-018-modo-agil-ate-a-v1.md) e à [ADR-014 v3](../adr/ADR-014-saida-do-reflex.md).
> **Revisão de 19/10**: a v1 **não é em Reflex** — a base nova é o núcleo da v1.

## 1. O que é a v1

**A plataforma na base nova** (FastAPI + Jinja2 + HTMX), com o **fluxo de obras e estudos**, as
proteções fechadas, os dados de teste limpos e a **virada** feita. A v0 (o Reflex de teste) sai de
cena.

## 2. Escopo da v1 (o que entra)

| # | Item | Estado hoje |
|---|---|---|
| 1 | **A base nova** — login/sessão, telas (admin, coordenador, instrutor, aluno, lição, pareceres, perfil) | **a construir** (DEM-005) |
| 2 | A **matriz papel × rota** migrada inteira (o que a DEM-002 fez) | a construir na v1 |
| 3 | O **fluxo de obras e estudos** (admin → revisor → admin → liberada; adendos do coordenador) | **a construir** (DEM-011) |
| 4 | O **domínio reaproveitado** (`models/`, `services/`, `scripts/`, `ai/`) | a adaptar (a sessão) |
| 5 | O **pipeline** publicando a base nova | a adaptar (o `deploy.yml`) |
| 6 | A **virada** (o Traefik para a v1) **com retorno** | a executar |
| 7 | As **dívidas fechadas**: D-01, D-02, D-05, D-09, D-10 (as demais reclassificadas) | ver o checklist |

## 3. Fora da v1 (explicitamente)

- a **busca** (DEM-B/C/D) e o **DAVID** (DEM-E) — nascem **na base nova**, depois;
- o **multi-ambiente real** (D-06) — o adendo por ambiente nasce com um ambiente; o isolamento
  completo tem gatilho próprio;
- a **publicação como serviço** (DEM-013) — adiada (ADR-017 Deferred);
- o **Reflex** — a v0 é desligada na virada.

## 4. Critério de pronto (o que o ARQUITECT verifica)

1. A v1 **na base nova** com o fluxo completo: importar → revisar → ajustar → liberar → vincular →
   a lição do aluno.
2. A **matriz papel × rota** testada na base nova (a mesma garantia da DEM-002).
3. As **dívidas críticas fechadas** (D-01, D-02, D-05, D-09, D-10) e as demais com gatilho escrito.
4. **Dados de teste limpos** e os dados reais entrando com procedimento.
5. O **release `v1.0.0`** na base nova, publicado pelo pipeline, com o backup verificado e o HTTP 200.
6. A **virada testada**, com o retorno à v0 funcionando.

## 5. Checklist de fechamento (na virada)

- [ ] **D-01** — senha de seed fora do código; o admin e os demos com troca obrigatória; a senha de produção trocada
- [ ] **D-02** — `diag` no script + chave com `restrict`; a operacional revogada
- [ ] **D-03** — ruleset de tags `v*`; a conta única revisada
- [ ] **D-04** — Environment `producao` com aprovador (ou decisão escrita de manter sem)
- [ ] **D-05** — cópia do dump **fora da VPS**, com checksum
- [ ] **D-06** — reclassificar (o adendo por ambiente nasce com um ambiente)
- [ ] **D-07** — **fechada pela DEM-011** (o fluxo com o hash)
- [ ] **D-08** — **fechada por construção**: o `AdminState` é do Reflex; a v1 tem auth própria
- [ ] **D-09** — limpar `eval/tmp-*`, usuários demo e o histórico de teste
- [ ] **D-10** — o `create_gestor` e a tela sem a senha conhecida
- [ ] **declarar o fim do modo ágil** (ADR-018) e voltar as ADR-006/007 ao processo cheio

## 6. Candidatas de produto pós-v1 (ordem recomendada, não decisão)

| Ordem | Candidata | Nível | Dependência |
|---|---|---|---|
| **a** | **Novos estudos a partir de Sire, Clark e Edwards** — piloto no **Clark** (8 arquivos), **plano próprio**, não o texto do livro | 2 | a DEM-003 aceita; o fluxo (DEM-011) para a revisão |
| **b** | **DEM-B → C → D** (registro de fontes, grafo, busca) | 2 · 3 · 2 | a DEM-003; a base nova |
| **c** | A **publicação como serviço** (DEM-013) — reavaliada na virada | 3 | a ADR-017 + a virada |

**Por que o Clark primeiro**: é o menor acervo (8 arquivos), tem plano de estudo dirigido como
formato — o que a plataforma consome — e está na base editorial reformada. E o estudo é
**derivado** (o mesmo regime da F-084), não reprodução.

## 7. Como se declara a v1

O ARQUITECT declara, com o checklist fechado. O PLANNER registra a data, o hash do release e o
fechamento das dívidas no painel; a ADR-018 ganha o status de encerrada (o nível 3 volta a ser o
padrão) e o modo ágil termina.
