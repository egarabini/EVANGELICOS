# Intent: DEM-202610-004 / ci-cd-fase-a3

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: ADR-009 + ADR-010 + bloqueio do aceite de release da DEM-202610-001
signed_at:
supersedes: —
open_questions_open: 7
spec_citations: —

> **Rascunho do AUXILIAR-ARCHITECT para o PLANNER lapidar.** O número `004` é sugestão
> (a 002 está reservada à guarda de papel do `/admin`). O PLANNER renumera, corta e assina com o ARQUITECT.

## 1. Problema

Hoje **não existe pipeline**: nenhum dos dois repositórios tem `.github/workflows`. Consequências
medidas:

- A DEM-001 está **aceita e com changelog fechado**, mas o aceite de release ficou
  **pendente** — o próprio changelog diz "bloqueado no `gh`" e "sem CI (ADR-010) não há publicação".
- O merge de um PR em `develop` ou `main` **não roda teste nenhum**: o PR #1 abriu com
  **0 checks**. O portão de merge da ADR-009 existe no papel, não na prática.
- O deploy ainda depende de um humano ou de um agente com acesso SSH, caminho que a
  ADR-010 manda aposentar (já derrubou o site uma vez, por erro de tipagem que só aparecia na
  compilação da página).

Quem sente: o ARQUITECT (publica à mão, sem rede de segurança) e a plataforma (nada impede um
PR quebrado de chegar à produção).

## 2. Outcome

Um PR no repositório de código **mostra, antes do merge, se a suíte passa e se as páginas
compilam**; e a **publicação em produção acontece pelo pipeline**, a partir de um merge ou de
um acionamento autorizado — **sem que nenhum agente tenha acesso à produção**.

## 3. Afetados

ARQUITECT (aprova e aciona), DEVS e agentes (abrem PR e leem o resultado), a VPS (recebe o deploy),
os dois repositórios (código e conteúdo).

**Intocáveis:** a lição em produção, o corpus (`:ro`, ADR-002), o banco e o backup do banco.

## 4. Escopo

**In**
- **Etapa 1 — CI de verificação:** a cada PR, rodar a suíte e a compilação das páginas, e
  mostrar o resultado como check do PR.
- **Etapa 2 — CD:** publicar pelo pipeline, com a chave de deploy como **segredo do GitHub**
  (ADR-008, ADR-010) e a verificação HTTP ao final.
- proteção de branch para `main` e `develop`, exigindo o check da Etapa 1 (ADR-009)
- a **aposentadoria** do deploy por SSH e a **revogação** da chave atual (`didasko_deploy`)

**Out (non-goals)**
- rodar o importador de conteúdo em produção — **continua manual do ARQUITECT**, após `pg_dump`
- ambiente de homologação — hoje não existe (perfil §5); outra DEM
- observabilidade e alerta de site fora do ar — outra DEM
- troca das senhas de demonstração — pendência própria da ADR-008
- publicar o repositório de **conteúdo** por pipeline (a DEM trata só o repositório de código;
  o conteúdo continua sendo clonado na VPS)

## 5. Constraints (duras)

- **IA não executa deploy em produção** (ADR-010): o agente abre PR e lê resultado; no máximo
  aciona o workflow, **quando autorizado**.
- **Segredos nunca no repositório** (ADR-008): chave e senhas só como Secret; token nunca em chat.
- O deploy **não pode perder dado**: backup `pg_dump` pareado com checksum antes do release (perfil §5).
- Nada que contrarie as ADRs 001, 002, 009 e 010.
- O pipeline **falha fechado**: erro em qualquer passo para o deploy; o site não fica "meio no ar".

## 6. Health metrics

- **H-01** · a suíte continua verde · baseline **82 testes** (`pytest tests`) · porteiro **EVAL**
- **H-02** · a lição do Cap. 21 em produção intacta · baseline **HTTP 200 + "João 3:16"** · porteiro **EVAL**
- **H-03** · nenhum segredo no repositório · baseline **0 ocorrências** (varredura) · porteiro **EVAL**
- **H-04** · o site não fica fora do ar além do reinício normal do container · baseline **a medir no 1º deploy** · porteiro **DEPLOY**

## 7. Sinal de sucesso

O ARQUITECT abre um PR, vê o check verde ou vermelho **antes** de mesclar, mescla, e a versão
nova está no ar **sem ele entrar na VPS**. Um PR com teste quebrado **não consegue ser mesclado**.
Isso é o aceite; os workflows são a evidência.

## 8. Perguntas abertas — só o ARQUITECT fecha

- [ ] **8.1** O deploy dispara em **merge em `main`/tag**, ou só por **acionamento manual** do workflow?
- [ ] **8.2** **Copilot Enterprise** (revisor do PR, ADR-009) está disponível na conta? Entra nesta DEM ou depois?
- [ ] **8.3** O pipeline roda em **runner do GitHub** (precisa alcançar a VPS por SSH) ou em runner próprio na VPS?
- [ ] **8.4** O **backup `pg_dump`** antes do release passa a ser parte do pipeline ou continua manual?
- [ ] **8.5** Quem **cria e guarda** a nova chave de deploy, e quando a antiga (`didasko_deploy`) é revogada?
- [ ] **8.6** **Rollback:** voltar por reimplantação da tag anterior basta, ou há migração de banco a reverter?
- [ ] **8.7** Etapa 1 e Etapa 2 viram **duas DEMs** ou uma só com duas entregas?

## 9. Fora de julgamento

Stack dos workflows, estrutura dos arquivos YAML, escolha de actions, nomes de secrets e
decomposição em tarefas. Também não decide a política de versionamento SemVer das tags.
