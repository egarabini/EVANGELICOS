# ADR-015: Acesso operacional do agente à VPS (escopo restrito)

- **Status:** **Accepted** — aceite do ARQUITECT em **2026-10-19**
- **Data:** 2026-10-19
- **Decisores:** ARQUITECT (Eduardo) · redação do PLANNER
- **Gatilho:** Operação — a instalação da chave de deploy não é deploy, mas hoje está coberta pelo "nunca" da ADR-010
- **Emenda**: **a ADR-010 parcialmente** (ver §"O que muda na ADR-010")

---

## Contexto e Problema

A **ADR-010** proíbe o agente de executar deploy em produção — e está certa: o deploy é
publicação, tem portões (CI, EVAL, aprovação) e já derrubou o site uma vez.

Mas a operação real tem ações que **não são deploy** e que hoje ficaram cobertas pelo
"nunca": instalar a chave pública de deploy no `authorized_keys`, conferir a permissão
de um arquivo, rodar um `docker ps`, ver por que o container reiniciou. Sem uma política
explícita, sobram duas saídas ruins:

1. o ARQUITECT faz **tudo** à mão — inclusive o que é trivial e verificável; ou
2. o agente contorna a regra em silêncio, sem registro e sem limite — **pior**.

Uma regra absoluta que obriga o humano a ser o único shell do projeto não é governança;
é gargalo. O que protege não é o "nunca", é **a lista fechada do que pode**.

## Decisão

**O agente PODE, sem autorização adicional:**

1. **Instalar e conferir chave PÚBLICA de deploy e suas permissões** — acrescentar entrada
   no `authorized_keys`, ajustar dono/modo, conferir o conteúdo;
2. **Inspecionar configuração e executar diagnósticos READ-ONLY** — `docker ps`/`logs`,
   `systemctl status`, `df`, `free`, `git status`, `curl` local, leitura de arquivos de
   configuração, `ssh -T` para testar autenticação.

**O agente NÃO PODE, em nenhum caso:**

- **gerar, guardar, ler ou usar chave PRIVADA**;
- **executar deploy** — a ADR-010 continua valendo, inteira, para publicação;
- **executar ação destrutiva** sem autorização **específica e escrita** do ARQUITECT para
  aquela ação, naquele atendimento.

### Lista fechada do que é destrutivo

Não é interpretação: **é a lista**. Cada item exige autorização específica.

| Ação | Exemplo |
|---|---|
| Ciclo de vida dos containers | `docker compose up/down/restart`, `docker rm`, `docker system prune` |
| Remoção ou sobrescrita de arquivo | `rm`, `mv`, edição de arquivo de produção, `>` em arquivo existente |
| Escrita no banco | `psql` com `INSERT/UPDATE/DELETE/DDL`, migração, seed, importador |
| Publicação | `subir.sh`, `git checkout` na VPS, qualquer caminho que troque a versão no ar |
| Configuração de infra | `docker-compose.producao.yml`, `.env`, regras do Traefik, firewall, DNS |

## Condições

1. **A chave pública é do ARQUITECT** (ou por ele fornecida e identificada). O agente
   **copia** um arquivo; **não gera par**. Se o agente gerasse a chave, ele teria acesso
   de deploy e a ADR-010 cairia por baixo do pano.
2. **A entrada acrescentada leva o mesmo `restrict,command="/usr/local/bin/didasko-deploy-entry"`
   das existentes.** Chave sem `restrict` é shell na VPS.
3. **Backup do arquivo antes de editar**, e o **comando de reversão** registrado na jornada.
4. **Toda ação registrada** na jornada da DEM: comando, saída e motivo.
5. **Preservar as entradas existentes** — acrescentar, nunca reescrever o arquivo.

## O que muda na ADR-010

A ADR-010 **continua Accepted** e **inteira no que importa**: publicação é do CI, o agente
não faz deploy, o aceite de release é do ARQUITECT. O que muda é apenas a leitura do
**acesso operacional**: ele deixa de ser "nunca" e passa a ser a **lista fechada** desta
ADR. A ADR-010 ganha a nota: *"acesso operacional restrito: ver ADR-015; a proibição de
deploy permanece"*.

## Consequências

**Positivas**
- O agente resolve o que é operação sem esperar o humano; o humano fica com as decisões.
- O que o agente pode fazer vira **lista**, não interpretação — auditável.
- O deploy continua com portão humano e com o CI.

**Negativas / riscos**
- **Superfície nova**: o agente passa a ter acesso SSH. Mitigação: a chave é restrita por
  `command=`, a lista é fechada e tudo é registrado.
- **Risco de "só mais um comando"**: a lista fecha a porta para a interpretação elástica.
- Requer disciplina de registro; sem jornada, a ADR vira licença.

**Neutras**
- A instalação da chave pública passa a ser operação de rotina; a privada continua fora do
  contexto da IA.

## Referências

- [`ADR-010`](ADR-010-publicacao-por-ci.md) — publicação por CI (emendada em parte)
- [`RUNBOOK-CHAVE-DE-DEPLOY`](../visao/RUNBOOK-CHAVE-DE-DEPLOY-aux-architect.md) — o procedimento
