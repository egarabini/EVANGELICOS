# Runbook — chave de deploy do CI/CD (DEM-004, Etapa 2)

> Autor: AUXILIAR-ARCHITECT (IA) · Para: ARQUITECT (executa) e PLANNER (incorpora ao design) · Data: 2026-10-18
> **Proposta.** Nenhum comando foi executado por mim e **nenhum segredo aparece aqui**.
> Quem executa todos os passos é o ARQUITECT, na máquina e na VPS dele.
> Base: ADR-008 (segredos), ADR-010 (agente não publica), DEM-004 intent §9.3.

## Princípio

**A chave privada nasce na máquina do ARQUITECT e vai direto para o GitHub Secret.**
Nunca passa por chat, por arquivo versionado, por log de agente nem pelo contexto de uma IA.
Se o PLANNER "gera o par", a privada passa pelo contexto dele; por isso este runbook tira essa etapa dos agentes.

> Nota: o texto do intent (9.3) diz que a privada vai "via `gh secret set` lendo de arquivo". Ele não diz
> quem gera o arquivo. Este runbook responde: **o ARQUITECT**.

## 0. Pré-requisitos

- `gh` autenticado como `egarabini` (já está).
- Usuário de deploy já existente na VPS: `didasko-deploy`, com acesso ao Docker por `sudo -n /usr/bin/docker` (NOPASSWD), como descreve `deploy/subir.sh`.
- Decidir o **host e a porta SSH** da VPS (aqui, `<VPS_HOST>` e `<PORTA>`).

## 1. Criar o Environment de produção (uma vez)

No GitHub: *Settings → Environments → New environment* `producao`.

- **Required reviewers:** `egarabini` (você aprova cada deploy).
- **Deployment branches:** *Selected branches* → só `main`.
- Os secrets de deploy ficam **neste Environment**, não no repositório. Assim só um job que passe pela sua aprovação os lê.

## 2. Gerar o par de chaves (na sua máquina)

Em um terminal seu, numa pasta temporária fora de qualquer repositório:

```powershell
mkdir $env:TEMP\didasko-ci
ssh-keygen -t ed25519 -C "didasko-ci-deploy" -f $env:TEMP\didasko-ci\didasko_ci -N '""'
```

Sem senha na chave, porque o CI não digita senha. A proteção vem das restrições do passo 3 e do Environment.

## 3. Instalar a chave pública na VPS (restrita)

Na VPS, no `~didasko-deploy/.ssh/authorized_keys`, uma linha com o conteúdo de `didasko_ci.pub` precedido de opções:

```text
restrict,command="/usr/local/bin/didasko-deploy-entry" ssh-ed25519 AAAA... didasko-ci-deploy
```

- `restrict` desliga shell interativo, port forwarding, agent forwarding e TTY.
- `command=` força um único ponto de entrada. O script `didasko-deploy-entry` é desenhado na Etapa 2 da DEM-004: deve aceitar só ações previstas (atualizar o código, rodar `subir.sh`, checar saúde) e rejeitar o resto lendo `$SSH_ORIGINAL_COMMAND`.
- IP de origem **não** dá para restringir: os runners do GitHub usam faixas variáveis.

## 4. Guardar a privada como Secret do Environment

Na sua máquina, lendo do arquivo. A chave **não** é exibida:

```powershell
Get-Content -Raw $env:TEMP\didasko-ci\didasko_ci | gh secret set DEPLOY_SSH_KEY --env producao --repo egarabini/gsi_ebd
```

Fixe também a **identidade do servidor** para evitar interceptação (`known_hosts`). Gere-a de dentro da VPS ou confira a impressão digital por outro canal, e então:

```powershell
gh secret set DEPLOY_KNOWN_HOSTS --env producao --repo egarabini/gsi_ebd --body "<linha do known_hosts conferida>"
```

Confira que existem, sem ver o valor:

```powershell
gh secret list --env producao --repo egarabini/gsi_ebd
```

## 5. Apagar a privada local

```powershell
Remove-Item -Recurse -Force $env:TEMP\didasko-ci
```

Se houver dúvida de que a chave vazou, revogue-a (passo 7) e gere outra; é barato.

## 6. Primeiro teste: sem deploy de verdade

Antes de qualquer publicação, rode o workflow (`workflow_dispatch`) com uma ação inofensiva (por exemplo, o script de entrada só devolver "ok" e a saúde do site). Ele deve:
1. pedir a sua aprovação do Environment `producao`;
2. conectar por SSH com a chave nova;
3. recusar qualquer comando fora da lista.

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

## Para o PLANNER incorporar ao design da Etapa 2

- Workflow de deploy em job com `environment: producao`, disparado a partir de `main`.
- `pg_dump` com checksum antes do deploy, guardado como artifact (decisão 9.2).
- Falha fechada: qualquer passo com erro para o deploy.
- Desenhar o `didasko-deploy-entry` e a sua lista de ações permitidas.
- Teste do próprio runbook: um dry-run documentado no passo 6.
