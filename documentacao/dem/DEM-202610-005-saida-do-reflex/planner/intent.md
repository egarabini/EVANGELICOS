# Intent: DEM-202610-005 / saida-do-reflex

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: decisão do ARQUITECT (17/10) + incidentes de 16/10 e da DEM-001
signed_at:
supersedes: —
open_questions_open: 3
spec_citations: — (preenchido ao fechar a spec)

> **Rascunho do AUXILIAR-ARCHITECT para o PLANNER lapidar.** O número `005` é sugestão.
> A palavra "Reflex" aparece porque é o objeto da decisão; **a tecnologia substituta não é
> decidida aqui** (ver §8, decisão 8.1, e §10). O PLANNER pode renumerar, cortar e dividir em DEMs.

## 1. Problema

O ARQUITECT perdeu a confiança no Reflex como base da interface e quer uma solução **mais sólida,
mais leve e com UX mais atual**. Evidências no próprio projeto:

- **Incidente de 16/10:** concatenar uma variável do Reflex com texto dentro de uma lista dinâmica
  derrubou o app em produção; o erro só aparecia na compilação da página (já citado na ADR-010).
- **DEM-001:** duas funções com o mesmo nome fizeram a aba de Aprovação mostrar a tela errada, sem
  nenhum aviso do Python — pego só por conferência manual da fiação.
- **Regras compensatórias já necessárias:** "nunca concatenar `Var` com `+` no componente", teste de
  compilação das páginas, listas planas sem `foreach` aninhado. A ferramenta exige disciplina para
  não quebrar.

Quem sente: o ARQUITECT (risco em produção) e os agentes (cada tela nova repete as armadilhas).

## 2. Outcome

**A interface do Didasko deixa de depender do Reflex, sem que o aluno, o coordenador ou o
admin percebam uma regressão.** Tela por tela, a interface passa a ser servida pela nova base;
quando a última sair, o Reflex é removido. Em qualquer ponto da transição, **voltar atrás é
possível sem perda de dado**.

## 3. Afetados

Todos os papéis (aluno, instrutor, coordenador, revisor, admin), o código de `states/`, `pages/` e
`components/`, o build e a imagem de produção, e as DEMs seguintes que criam tela (DEM-D, DEM-E).

**Intocáveis:** o banco (schema e dados), o corpus (ADR-002), o caminho da Escritura (ADR-003),
a autenticação e o RBAC existentes, os importadores, o pipeline de IA e o domínio público/URLs
que o aluno já usa.

## 4. Escopo

**In**
- decidir e registrar a **nova base de interface** (por ADR, antes de qualquer tela)
- migração **por rotas**, convivendo com o Reflex durante a transição
- reaproveitar `models/`, `scripts/`, `ai/` e a camada de serviços (ajustando só o que depende do Reflex)
- recriar as telas com **visual/UX atual e leve**, mantendo as funções existentes
- remover o Reflex (dependências, build, imagem) ao fim
- ajustar o CI/CD (DEM-004) à nova base

**Out (non-goals)**
- trocar banco, ORM, migrações, ChromaDB ou Ollama
- migrar ou reestruturar dados
- criar funcionalidade nova durante a migração (paridade primeiro) — inclui a busca (DEM-D) e o assistente (DEM-E)
- redesenho do produto ou de conteúdo
- mexer no domínio, na VPS ou no Traefik além do que a convivência exigir

## 5. Constraints (duras)

- **ADR-001 (stack fixa) é lei:** a mudança exige **ADR nova que a substitua na parte do
  framework, escrita antes** de qualquer código. O resto da ADR (Python, PostgreSQL) permanece.
- **A lição em produção não regride** (H-02): é a última tela a migrar.
- **Menor impacto:** nada de migração de dados; **convivência por rota**; cada tela migrada tem
  **volta atrás** documentada.
- **IA não faz deploy** (ADR-010); publicação pelo CI. Por isso **esta DEM depende da DEM-004**.
- Segredos fora do repositório (ADR-008); LGPD preservada (nenhum dado novo ao navegador).
- Nada de código de terceiros copiado (decisão do ARQUITECT para esta frente).

## 6. Health metrics

- **H-01** · a suíte continua verde · baseline **82 testes** · porteiro **EVAL**
- **H-02** · a lição do Cap. 21 idêntica: HTTP 200 + "João 3:16" e passagens relacionadas · baseline **verificado em produção** · porteiro **EVAL**
- **H-03** · nada de dado alterado: **39 estudos · 31.102 versículos · 344.799 referências cruzadas** · porteiro **EVAL**
- **H-04** · login e RBAC com o mesmo resultado por papel · baseline **a medir (matriz papel × rota)** · porteiro **EVAL**
- **H-05** · paridade de telas: nenhuma rota some · baseline **inventário das rotas atuais (a levantar)** · porteiro **EVAL**

## 7. Sinal de sucesso

O ARQUITECT percorre o app como cada papel, vê o visual novo, e **não encontra função que existia e
sumiu**. O repositório já não tem a dependência do Reflex, e o build de produção ficou mais simples.
Isso é o aceite; a suíte é a evidência.

## 8. Decisões já registradas (não são perguntas)

Seguem as recomendações do AUXILIAR-ARCHITECT, adotadas pelo ARQUITECT em 17/10 ("seguir sua sugestão").

| # | Questão | Decisão |
|---|---|---|
| 8.1 | Nova base de interface | **FastAPI + Jinja2 + HTMX** como direção; Alpine.js para interações pequenas. Mantém SQLModel, Alembic e o RBAC atual. **Django + HTMX** fica registrado como alternativa descartada por custo de reescrita de modelos. A ADR formaliza e substitui a ADR-001 só na parte do framework. |
| 8.2 | Ordem das telas | **Admin e telas novas primeiro; lição do aluno por último** (protege H-02). |
| 8.3 | Tela nova em Reflex | **Não.** A DEM-D (busca) e a DEM-E já nascem na base nova; nenhuma tela nova é criada em Reflex a partir daqui. |
| 8.7 | PR #1 da DEM-001 | **Entra antes**, no Reflex, e a tela "Estudo Aplicável" é migrada com o resto do admin. |

## 9. Perguntas abertas — só o ARQUITECT fecha

- [ ] **9.1** A **DEM-002** (guarda de papel no `/admin`) é feita **agora no Reflex** ou já na base nova? **Atenção do AUXILIAR-ARCHITECT:** o furo existe hoje (qualquer usuário logado alcança a área administrativa, conforme o changelog da DEM-001). Esperar a migração do admin deixa o furo aberto por semanas; a opção segura é corrigir agora no Reflex, pequena, e reimplementar o guarda na base nova.
- [ ] **9.2** **Ritmo:** várias DEMs (uma por grupo de telas) ou uma DEM com entregas?
- [ ] **9.3** **Direção de UX:** há referência visual (produto, paleta, exemplos) ou o PLANNER propõe?

## 10. Fora de julgamento

Detalhes da escolha do framework (a direção está em 8.1), estrutura de pastas, bibliotecas de estilo, templates, nomes de rotas,
e a decomposição em tarefas. O PLANNER leva a ADR ao ARQUITECT; o design decide o como.
