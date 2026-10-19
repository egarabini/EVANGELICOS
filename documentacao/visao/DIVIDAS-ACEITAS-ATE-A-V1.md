# Dívidas aceitas até a v1 (D-01 a D-09)

> Documento ligado à [ADR-018](../adr/ADR-018-modo-agil-ate-a-v1.md) · Decisão do ARQUITECT, 2026-10-19:
> *"Tudo é teste até a v1; a partir da v1 fechamos, bloqueamos e entramos com dados reais."*
> Cada item tem **dono**, **risco aceito** e **gatilho de fechamento**. Não se corrige por conta própria.

| # | Dívida | Risco aceito | Gatilho de fechamento | Dono |
|---|---|---|---|---|
| **D-01** | **Credencial de seed pública** (`admin@gsi.ebd` / `senha123`) — DEM-012 | quem ler o repositório público entra como admin; vê leads, aprova estudos | **antes de dados reais ou de divulgação**; a DEM-012 tirou a senha do código — o fechamento exige a **rotação manual** (o ARQUITECT) e o **A-2** (o `exec -e SEED_PASSWORD` no `subir.sh`, autorização do ARQUITECT); o **A-1 é local** (em produção o seed roda no container, sem `.env`) e não é pré-requisito | ARQUITECT (decisão) · Codex (implementação, DEM-012) |
| **D-02** | **Chave operacional com shell completo** (ADR-016) | um agente com a chave tem acesso root-equivalente à VPS | **na virada da v1**: comando `diag` no script + chave com `restrict` | ARQUITECT |
| **D-03** | **Sem ruleset de tags `v*`** e conta admin única | qualquer sessão autenticada como o dono publica por tag | na virada da v1, ou quando entrar um segundo colaborador | ARQUITECT |
| **D-04** | **Environment `producao` sem aprovador** (ADR-016) | deploy sem pausa humana | revisar na virada da v1 | ARQUITECT |
| **D-05** | **Dump do banco só na VPS** (manifesto, não cópia) | perda da VPS = perda do backup | **antes de dados reais**: cópia fora do servidor | ARQUITECT |
| **D-06** | **`can_manage` sem ambiente / posse por id do cliente** (DEM-010) | um coordenador age sobre usuário de outro ambiente | **antes de ter mais de um ambiente real** | PLANNER (intent) |
| **D-07** | **Aprovação de estudo por uma só assinatura** (ADR-011 não implementada) | o admin sozinho libera estudo; sem hash de conteúdo | **em implementação pela DEM-011** (o fluxo com o parecer e o hash por versão) | PLANNER (intent) |
| **D-08** | **`logout` não limpa `AdminState`** (WARN da DEM-002) | resíduo de sessão na mesma aba | **fecha por construção na v1**: o `AdminState` é do Reflex; a base nova tem auth própria (DEM-005) | PLANNER |
| **D-09** | **Dados de teste e lixo de EVAL** (`eval/tmp-*`, usuários demo) | confusão e vazamento de dado de teste | **na virada da v1**: limpeza de histórico antes de dados reais | PLANNER + ARQUITECT |
| **D-11** | **A troca obrigatória é só um redirect**: `guarda_rota`/`exige` não verificam `must_change_password` — o usuário novo navega e executa ações sem trocar | a flag vira decoração; serve para o admin recém-criado e para o coordenador do `create_gestor` | **fecha por construção na v1** (DEM-005): a flag bloqueia rota/evento protegido **antes** da troca (só a troca de senha e o logout passam) | PLANNER (intent) |
| **D-10** | **Coordenador criado com senha conhecida**: `create_gestor` (`gsi_ebd/states/admin.py`) cria com `senha123` fixa, e a tela (`gsi_ebd/pages/admin.py`) exibe "Senha inicial: senha123" | quem cria/entrevê a tela sabe a senha inicial de todo coordenador novo | **fecha por construção na v1** (DEM-005): criação de coordenador **sem senha fixa** — token de uso único com expiração ou senha aleatória nunca exibida | PLANNER (intent) |

## Premissa (não é dívida, é limite)

A premissa "tudo é teste" **vale enquanto nenhum dado real de pessoa entrar**. O **formulário
de contato público**, se estiver ativo, **coleta dados reais de visitantes** — e esses leads ficam
acessíveis por qualquer um que entre como admin (D-01).

**Se houver leads reais no banco hoje, o D-01 sai da lista de dívidas e vira exceção a tratar
agora.** Verificar é do ARQUITECT.

## Quando este documento fecha

Na **virada da v1** ([`DEFINICAO-DA-V1`](DEFINICAO-DA-V1.md)): cada item é fechado **ou**
reclassificado com um novo gatilho. O documento não some — ele vira o **registro do fechamento**.




