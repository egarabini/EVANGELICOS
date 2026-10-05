# Avaliação do Fundamento da Plataforma

Data: 2026-07-18

## 1. Contexto

Este documento registra a avaliação técnica do "fundamento" da plataforma conforme descrito por Eduardo: uma **plataforma de estudo bíblico assistido e acompanhado**, fechada (não aberta ao público geral), estruturada em **4 níveis de acesso** e **5 módulos funcionais**.

Não se trata de um produto novo: o fundamento descrito **já corresponde, em grande parte, ao que está implementado no subprojeto `GSI_EBD`** (Reflex + SQLModel). Este diagnóstico cruza a visão de negócio recebida com o que já existe em código, para servir de base ao plano de desenvolvimento.

## 2. Modelo de Acesso Proposto vs. Implementado

| Nível (visão de negócio) | Papel no código (`gsi_ebd/models/user.py`) | Situação |
|---|---|---|
| 1. Administrativo | `Role.ADMIN` | Implementado (cadastro, seed) |
| 2. Gestor | `Role.GESTOR` | Implementado como entidade, painel parcial |
| 3. Coordenador | `Role.SUPERVISOR` | Implementado só como papel; **sem painel/estado próprio** |
| 4. Aluno | `Role.ALUNO` | Implementado (fluxo de lição funcional) |

### Achado crítico — inconsistência de hierarquia no enum

```python
class Role(IntEnum):
    ADMIN = 1
    SUPERVISOR = 2
    GESTOR = 3
    ALUNO = 4
```

A ordem numérica (`ADMIN < SUPERVISOR < GESTOR`) **contradiz** a hierarquia real descrita nos próprios comentários do código e confirmada agora pelo fundamento de negócio:

```
Administrador → Gestor → Coordenador (hoje "Supervisor") → Aluno
```

O relacionamento `gestor_id`/`supervisor_id` em `User` já reflete a hierarquia correta (Coordenador pertence a um Gestor, Aluno pertence a um Coordenador), mas o **enum não está alinhado semanticamente**, o que é uma fonte provável de bugs em qualquer verificação futura baseada em `role >` ou `role <`.

**Recomendação:** renomear `SUPERVISOR` → `COORDENADOR` e reordenar o enum:

```python
class Role(IntEnum):
    ADMIN = 1
    GESTOR = 2
    COORDENADOR = 3
    ALUNO = 4
```

Isso é uma migração de dados simples (o valor 2 vira 3 e vice-versa), mas deve ser feita **antes** de construir novas regras de autorização em cima do enum, para não herdar a inconsistência.

## 3. Módulos Propostos vs. Estado Atual do Código

| Módulo (visão de negócio) | Onde já existe no `GSI_EBD` | Lacunas |
|---|---|---|
| **1. Administrativo** (gestão da plataforma, planos, dashboard, financeiro) | `pages/admin.py`, `states/admin.py`, `models/study.py`, `models/subscription.py` | Dashboard geral não confirmado; módulo financeiro tem modelo (`Subscription`, `PaymentMethod`) mas pagamento é só `SIMULADO` (sem gateway real) |
| **2. Desenvolvimento de Estudos** (livro → capítulos → plano dirigido → aprovação → publicação) | `models/study.py` (`Study`, `StudyVersion`, `StudyStatus`) | Não há evidência de fluxo de **aprovação** nem de proposta de plano pelo Gestor → Admin |
| **3. Gestão de Equipes** (Gestor gerencia Coordenadores + turmas, dashboard restrito) | `pages/gestor.py`, `states/gestor.py` | Não existe entidade "Turma/Equipe/Classe" — hoje a relação é direta `user.gestor_id`, sem agrupamento formal de alunos em turmas coordenadas |
| **4. Coordenação de Alunos** (Coordenador acompanha evolução/assiduidade) | Papel `SUPERVISOR` existe no modelo | **Não há `pages/coordenador.py` nem `states/coordenador.py`** — este módulo ainda não tem interface própria |
| **5. Estudos Dirigidos** (Aluno estuda e vê seu dashboard) | `pages/aluno.py`, `states/aluno.py`, `models/progress.py` (`Progress`, `UserResponse`, `QuestionType`) | Fluxo de lição já funciona; falta dashboard indicativo de evolução mais rico (mencionado como lacuna também no `Diagnostico` técnico do `GSI_EBD`) |

## 4. Pontos Fortes do Fundamento Recebido

- **Modelo de acesso fechado e hierárquico é coerente** com o que já foi modelado no banco (`gestor_id`, `supervisor_id`), reduzindo o risco de retrabalho estrutural.
- **Separação clara entre "quem estuda" e "quem administra conteúdo"**: o fluxo Livro → Capítulos → Plano de Estudo Dirigido → Aprovação → Publicação é uma boa prática editorial, evita que qualquer Gestor publique conteúdo sem curadoria doutrinária.
- **Módulo financeiro já antecipado no modelo de dados** (`Subscription`, `PaymentMethod` com PIX/Boleto/Cartão/Mercado Pago), o que facilita a evolução futura sem redesenho de schema.
- **Granularidade de dashboards por papel** (visão restrita para Gestor/Coordenador/Aluno) é consistente com o RBAC já parcialmente implementado.

## 5. Pontos Fracos / Riscos

1. **Inconsistência de hierarquia no enum `Role`** (detalhado na seção 2) — deve ser corrigido antes de avançar.
2. **Falta o módulo/entidade "Turma" ou "Equipe"**: hoje um Aluno se vincula diretamente a um `supervisor_id`, mas não há um objeto explícito de "turma/classe" com nome, plano de estudo associado, data de início, etc. Isso limita relatórios de "todas as equipes que o Gestor coordena".
3. **Ausência de fluxo de proposta/aprovação de planos de estudo**: o Gestor, segundo o fundamento, pode propor referências de novos planos ao Admin. Não há hoje modelo nem tela para isso (poderia reaproveitar `models/lead.py` ou exigir um novo modelo `StudyProposal`).
4. **Coordenador ainda não tem interface**: é o papel menos maduro tecnicamente, apesar de estar completo no fundamento de negócio.
5. **Financeiro em modo simulado**: sem gateway de pagamento real, o módulo "controle de inscrições pagas" não está operacional de fato.
6. **Terminologia divergente entre negócio e código** (`Supervisor` vs `Coordenador`) precisa ser unificada em todas as camadas (models, states, pages, textos de UI) para evitar confusão em manutenção futura.

## 6. Sugestões para o Plano de Desenvolvimento

1. **Corrigir o enum `Role`** e renomear `SUPERVISOR` → `COORDENADOR` em todo o código (models, states, pages, testes) antes de qualquer nova feature.
2. **Modelar a entidade `Equipe`/`Turma`** (nome, gestor responsável, coordenador responsável, plano de estudo, lista de alunos, datas) para sustentar os módulos 3 e 4 com precisão.
3. **Criar o módulo `Coordenação de Alunos`** (`pages/coordenador.py`, `states/coordenador.py`) com dashboard de evolução e assiduidade — hoje é o maior vazio entre negócio e código.
4. **Desenhar o fluxo de proposta de plano de estudo** (Gestor propõe → Admin avalia/aprova/rejeita → se aprovado, entra no pipeline de "Desenvolvimento de Estudos").
5. **Formalizar o pipeline editorial** Livro → Capítulos → Plano Dirigido → Revisão → Aprovação → Publicação, provavelmente reaproveitando `StudyStatus` já existente em `models/study.py`.
6. **Priorizar o módulo financeiro real** apenas depois da estabilização de RBAC e do módulo de equipes — hoje está em modo simulado e não é bloqueante para o MVP de acompanhamento pedagógico.
7. **Manter os dashboards com visão restrita por papel** desde o início das telas do Coordenador e do Gestor, usando a mesma política central de autorização já recomendada no `GSI_EBD/Diagnostico/plano-de-acao.md`.

## 7. Conclusão

O fundamento de negócio recebido **não exige um novo projeto do zero** — ele formaliza e refina o que já está em construção no `GSI_EBD`. O maior valor deste diagnóstico é expor:
(a) uma inconsistência técnica real no enum de papéis que precisa ser corrigida antes de crescer o sistema, e
(b) as lacunas estruturais (Turma/Equipe, Coordenador, fluxo de proposta/aprovação de planos) que precisam entrar no plano de desenvolvimento para que o código passe a refletir fielmente a visão de negócio.

## Documentos Relacionados

- `GSI_EBD/Diagnostico/README.md`
- `GSI_EBD/Diagnostico/arquitetura-atual.md`
- `GSI_EBD/Diagnostico/plano-de-acao.md`
- `GSI_EBD/gsi_ebd/models/user.py`
