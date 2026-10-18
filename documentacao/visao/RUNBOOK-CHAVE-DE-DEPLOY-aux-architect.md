# Runbook — chave de deploy do CI/CD (DEM-004, Etapa 2)

> Autor: AUXILIAR-ARCHITECT (IA) · Para: ARQUITECT (executa) e PLANNER (incorpora ao design) · Revisado em 2026-10-18
> **Proposta.** Nenhum comando foi executado por mim e **nenhum segredo aparece aqui**.
> Quem executa os passos 2 a 5 é o ARQUITECT, na máquina e na VPS dele.
> Base: ADR-008 (segredos), ADR-010 (agente não publica), DEM-004 intent §9.3.
> Revisão: ajustada ao que existe de fato em `GSI_EBD`: `.github/workflows/deploy.yml` e
> `deploy/didasko-deploy-entry.sh` (commit `3bf67af`).

## Princípio

**A chave privada nasce na máquina do ARQUITECT e vai direto para o GitHub Secret.**
Nunca passa por chat, por arquivo versionado, por log de agente nem pelo contexto de uma IA.
O PLANNER escreveu o workflow e o script de entrada; **ninguém além do ARQUITECT gera ou toca a privada**.

## O que já existe (não refazer)

| Peça | Estado |
|---|---|
| Workflow `deploy.yml` | pronto. Dispara em **tag `v*`** e em **`workflow_dispatch`**; job com `environment: producao` |
| Script de entrada `deploy/didasko-deploy-entry.sh` | pronto. Só aceita `deploy <tag>` (tag com `A-Za-z0-9._-`); faz `pg_dump` → checkout da tag → `subir.sh --pular-import` → verificação HTTP 200 |
| Environment `producao` | existe, com `egarabini` como aprovador obrigatório; branches restritas a `main` (ver aviso na seção "Pendência de tags") |
| Secrets `DEPLOY_SSH_KEY`, `DEPLOY_KNOWN_HOSTS` | **faltam** (são o objeto deste runbook) |
| Variáveis `DEPLOY_HOST`, `DEPLOY_USER`, `DEPLOY_PORT` | opcionais; padrões do workflow: `didasko.app.br`, `didasko-deploy`, `22` |

## Pendência de tags (leia antes de criar o primeiro `v*`)

O `deploy.yml` dispara em **tag `v*`**, mas o Environment `producao` hoje aceita **só a branch `main`**
(política aplicada em 2026-10-18). Uma execução disparada por tag vem com ref `refs/tags/v…` e, **se o
Environment não tiver regra para tags, a aprovação nunca é pedida e o job é recusado**.
Resolver antes do primeiro release, com **uma** das opções (decisão do ARQUITECT):
1. acrescentar ao Environment a regra de **tag** `v*` (mantém o disparo por tag); ou
2. publicar sempre por `workflow_dispatch` a partir de `main`, informando a tag no campo `tag`, e
   considerar remover o gatilho `push: tags` do workflow.

## Pré-requisitos na VPS (conferir uma vez)

O script de entrada assume, **para o usuário `didasko-deploy`**:
- clone do repositório de código em `~didasko-deploy/didasko` e o arquivo `~didasko-deploy/didasko/.env`;
- o repositório de conteúdo clonado ao lado (`conteudo/`), como pede `deploy/DEPLOY.md`;
- `sudo -n docker` liberado por NOPASSWD (como descreve `deploy/subir.sh`);
- `curl` instalado, e saída para o GitHub (para `git fetch --tags`);
- escrita em `~/backups` e `~/` (logs `deploy-*.log`).

Se o clone e o `.env` hoje estão no home de outro usuário (por exemplo `eduardo`), o script aborta com
"clone não encontrado" ou ".env não encontrado". Resolver antes do teste.

## 1. Environment de produção (já feito)

Conferir em *Settings → Environments → producao*: aprovador `egarabini`; branches permitidas. Os
secrets ficam **neste Environment**, não no repositório.

## 2. Gerar o par de chaves (na sua máquina, em Git Bash)

Numa pasta temporária fora de qualquer repositório:

```bash
mkdir -p /tmp/didasko-ci
ssh-keygen -t ed25519 -C "didasko-ci-deploy" -f /tmp/didasko-ci/didasko_ci -N ""
```

Sem senha na chave, porque o CI não digita senha. A proteção vem das restrições do passo 3 e do
Environment. Use **Git Bash** (não PowerShell) neste passo e no 4: ele preserva o arquivo byte a byte;
quebras de linha CRLF podem fazer o `ssh-keygen -y` do workflow rejeitar a chave.

## 3. Instalar a chave pública na VPS (restrita)

Na VPS, copie `didasko-deploy-entry.sh` para `/usr/local/bin/didasko-deploy-entry` (dono `root`, modo
755; o script já documenta isso) e, no `~didasko-deploy/.ssh/authorized_keys`, acrescente uma linha com
o conteúdo de `didasko_ci.pub` precedido de opções:

```text
restrict,command="/usr/local/bin/didasko-deploy-entry" ssh-ed25519 AAAA... didasko-ci-deploy
```

- `restrict` desliga shell interativo, port forwarding, agent forwarding e TTY.
- `command=` força o script de entrada, que **só aceita `deploy <tag>`** e recusa qualquer outro pedido.
- IP de origem não dá para restringir (faixas variáveis do GitHub).

## 4. Guardar a privada como Secret do Environment

Ainda em Git Bash, lendo do arquivo. A chave **não** é exibida:

```bash
gh secret set DEPLOY_SSH_KEY --env producao --repo egarabini/gsi_ebd < /tmp/didasko-ci/didasko_ci
```

Fixe também a **identidade do servidor** (`known_hosts`) para evitar interceptação. Gere a linha e
**confira a impressão digital por outro canal** (na própria VPS):

```bash
# na sua máquina
ssh-keyscan -t ed25519 didasko.app.br > /tmp/didasko-ci/known_hosts
ssh-keygen -lf /tmp/didasko-ci/known_hosts
# na VPS: a impressão digital deve ser idêntica
ssh-keygen -lf /etc/ssh/ssh_host_ed25519_key.pub
```

Se a porta SSH não for 22, use `-p <PORTA>` no `ssh-keyscan` (a linha sai no formato `[host]:porta`)
e defina a variável `DEPLOY_PORT`. Depois:

```bash
gh secret set DEPLOY_KNOWN_HOSTS --env producao --repo egarabini/gsi_ebd < /tmp/didasko-ci/known_hosts
```

Conferir que existem, sem ver o valor:

```bash
gh secret list --env producao --repo egarabini/gsi_ebd
```

## 5. Apagar a privada local

```bash
rm -rf /tmp/didasko-ci
```

Se houver dúvida de que a chave vazou, revogue-a (passo 7) e gere outra; é barato.

## 6. Primeiro teste

**Atenção:** o script de entrada tem **um único comando** (`deploy <tag>`), e ele faz o deploy de
verdade (backup, checkout da tag, `subir.sh`). **Não existe hoje um teste inofensivo de conectividade.**
Duas saídas:
- **Recomendada:** pedir ao PLANNER/DEVS um comando `ping` (ou `status`) no script de entrada, que
  só confirme usuário, host e acesso ao Docker, sem alterar nada. O teste do passo 6 usa esse comando.
- **Alternativa:** aceitar que o primeiro teste é um deploy real de uma tag já existente e conhecida
  (que não muda nada de relevante), com o `pg_dump` como rede de segurança e você presente para aprovar.

Em qualquer caso o resultado esperado é: (1) a pipeline pede a sua aprovação do Environment;
(2) conecta por SSH com a chave nova; (3) recusa qualquer comando que não seja `deploy <tag>`.

## 7. Revogar a chave antiga

Só **depois** de um deploy completo bem-sucedido pelo pipeline:

- remover da VPS a linha de `authorized_keys` da chave `didasko_deploy`;
- apagar a chave antiga dos locais onde existia (máquina do agente, segredos antigos);
- registrar a data no changelog da DEM-004.

## 8. Rotina

- Girar a chave a cada 90 dias, ou ao trocar de máquina ou de pessoa.
- Se qualquer log do Actions mostrar o valor do segredo, tratar como vazamento: revogar e gerar outra.

## O que NUNCA fazer

- Colar a chave (pública sim, privada nunca) em chat, issue, PR ou comentário.
- Colocar a privada em variável do repositório, no `.env` ou no código.
- Usar `pull_request_target` em qualquer workflow que veja secrets.
- Usar `set -x` ou imprimir variáveis no script de deploy.
- Pedir a um agente que gere, leia ou guarde a privada.

## Lacunas que o PLANNER deve fechar no design

1. Comando `ping`/`status` no script de entrada (seção 6).
2. Regra de tag no Environment, ou remoção do gatilho por tag (seção "Pendência de tags").
3. Verificação de pré-requisitos da VPS (clone, `.env`, `conteudo/`) antes do primeiro deploy.
4. O script de entrada roda `subir.sh --pular-import`: o **importador do conteúdo (inclusive o da
   DEM-001) continua manual** do ARQUITECT, depois do `pg_dump`, como decidido.
