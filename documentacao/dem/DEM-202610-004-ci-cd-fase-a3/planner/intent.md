# Intent: DEM-202610-004 / ci-cd-fase-a3

status: signed
owner: PLANNER
signed_by: ARQUITECT
origin: ADR-009 + ADR-010 + bloqueio do aceite de release da DEM-202610-001
signed_at: 2026-10-17
supersedes: —
open_questions_open: 0
spec_citations: 100% — todo RF de `spec.md` cita §2, §4 In, §5 ou uma decisão do §9
nota_de_assinatura: o ARQUITECT autorizou as recomendações do PLANNER ("segue", 2026-10-17); as cinco decisões estão registradas no §9.

## 1. Problema

Não existe pipeline: nenhum dos dois repositórios tem `.github/workflows`. O que isso custa,
**medido em 2026-10-17 com o `gh` autenticado**:

- O **PR #1** (DEM-001, `feature/…` → `develop`) está aberto, `MERGEABLE`, com **0 checks**.
- O **Copilot Code Review já funciona** e aprovou o PR (run `39067498100`, success, 4m32s).
  Ou seja: **o revisor automático existe; o portão de testes não.**
- **Nenhuma** branch protection (`main` responde 404 "not protected") e **nenhum secret**
  configurado nos dois repositórios.
- Consequência: um PR com a suíte quebrada **mergeia do mesmo jeito**. É o portão da ADR-009
  existindo pela metade.
- A **DEM-001 está aceita e com changelog fechado**, mas o aceite de **release** ficou
  pendente: sem CI não há publicação (ADR-010).
- O deploy ainda depende de SSH humano ou de agente — caminho que já derrubou o site uma vez,
  por erro que só aparecia na compilação da página.

## 2. Outcome

Um PR **mostra, antes do merge, se a suíte passa e se as páginas compilam**; e a publicação em
produção acontece **pelo pipeline**, a partir de um merge ou de um acionamento autorizado —
**sem que nenhum agente tenha acesso à produção**.

## 3. Afetados

ARQUITECT (aprova e aciona), DEVS e agentes (abrem PR e leem o resultado), a VPS (recebe o
deploy), os dois repositórios.

**Intocáveis:** a lição em produção, o corpus (`:ro`, ADR-002), o banco e o backup do banco.

## 4. Escopo

**In**
- **CI de verificação:** a cada PR, rodar a suíte e a compilação das páginas, com o resultado
  como check do PR.
- **CD:** publicar pelo pipeline, com a chave de deploy como **segredo do GitHub** e
  verificação HTTP ao final.
- proteção de `main` e `develop` exigindo o check da CI (ADR-009).
- **aposentar** o deploy por SSH e **revogar** a chave atual (`didasko_deploy`).

**Out (non-goals)**
- rodar o importador de conteúdo em produção — segue **manual do ARQUITECT**, após `pg_dump`
- ambiente de homologação — não existe (perfil §5); outra DEM
- observabilidade e alerta de site fora do ar — outra DEM
- troca das senhas de demonstração — pendência da ADR-008
- publicar o repositório de **conteúdo** por pipeline — o conteúdo continua clonado na VPS

## 5. Constraints (duras)

- **IA não executa deploy em produção** (ADR-010): abre PR e lê resultado; no máximo aciona o
  workflow, quando autorizado.
- **Segredos nunca no repositório** (ADR-008): chave e senhas só como Secret; token nunca em chat.
- O deploy **não pode perder dado**: `pg_dump` pareado com checksum antes do release (perfil §5).
- O pipeline **falha fechado**: erro em qualquer passo impede o deploy; o site não fica "meio no ar".
- Nada que contrarie as ADRs 001, 002, 009 e 010.

## 6. Health metrics

- **H-01** · a suíte continua verde · baseline **82 testes** (`pytest tests`) · porteiro **EVAL**
- **H-02** · a lição do Cap. 21 em produção intacta · baseline **HTTP 200 + "João 3:16"** · porteiro **EVAL**
- **H-03** · nenhum segredo no repositório · baseline **0 ocorrências** (varredura no commit) · porteiro **EVAL**
- **H-04** · após o deploy, o site volta a responder 200 em **≤ 2 min** · baseline **200 hoje** (medido) · porteiro **DEPLOY**

## 7. Sinal de sucesso

O ARQUITECT abre um PR, vê o check verde ou vermelho **antes** de mesclar, mescla, e a versão
nova está no ar **sem ele entrar na VPS**. Um PR com teste quebrado **não consegue ser
mesclado**. Isso é o aceite; os workflows são a evidência.

## 8. Decisões já registradas (não são perguntas)

| # | Questão | Decisão e origem |
|---|---|---|
| 8.1 | Copilot Enterprise entra nesta DEM? | **Sim, como revisor do PR.** Está ativado na conta — informação do ARQUITECT em 17/10; a ADR-009 já o prevê. |
| 8.2 | Runner do GitHub ou runner próprio na VPS? | **GitHub-hosted + SSH para a VPS.** Runner próprio na VPS foi descartado: os repositórios são públicos e runner self-hosted permitiria execução de código de terceiro na VPS. O ARQUITECT aceitou a recomendação em 17/10. |

## 9. Perguntas abertas — fechadas pelo ARQUITECT em 2026-10-17

**Nenhuma aberta.** As cinco foram decididas (autorizadas com "segue").

| # | Pergunta | Decisão |
|---|---|---|
| 9.1 | Disparo do deploy | **Merge em `main`** (via `release/*`, com aceite) **+ `workflow_dispatch`** para republicar sem release, em emergência |
| 9.2 | `pg_dump` no pipeline | **Sim, no pipeline**, antes do deploy, com checksum e guardado como artifact |
| 9.3 | Chave de deploy | **Par novo (ed25519).** Pública no `authorized_keys` da VPS (tarefa do ARQUITECT); privada como secret `DEPLOY_SSH_KEY` via `gh secret set` lendo de arquivo — **nunca no chat**. A `didasko_deploy` antiga é revogada **depois** do primeiro deploy pelo pipeline funcionar |
| 9.4 | Rollback | **Reimplantar a tag anterior.** Nenhuma migração de schema é feita pelo pipeline |
| 9.5 | Uma ou duas DEMs | **Uma DEM com duas entregas**: CI (Etapa 1) e CD (Etapa 2) |

## 10. Fora de julgamento

Stack dos workflows, YAML, escolha de actions, nomes de secrets, decomposição em tarefas e a
política de versionamento SemVer das tags.
