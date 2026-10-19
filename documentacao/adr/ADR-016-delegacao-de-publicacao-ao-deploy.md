# ADR-016: Delegação da publicação ao perfil DEPLOY

- **Status:** **Accepted** — aceite do ARQUITECT em **2026-10-19**
- **Data:** 2026-10-19
- **Decisores:** ARQUITECT (Eduardo) · redação do PLANNER
- **Gatilho:** Operação — o deploy da v0.1.0 passou pelo pipeline e a aprovação manual por deploy virou gargalo sem decisão nova
- **Emenda (explícita):** **[ADR-010](ADR-010-publicacao-por-ci.md)** (a cláusula "o agente no máximo aciona o workflow quando autorizado") e **[ADR-015](ADR-015-acesso-operacional-do-agente.md)** (o acesso operacional, que deixa de ser só leitura + chave pública)
- **Não altera:** ADR-008 (segredos), ADR-009 (GitFlow), o EVAL, o CI como caminho de publicação

---

## Contexto

O deploy da **v0.1.0** terminou com sucesso pelo GitHub Actions — run `39175867118`,
job `118049517557`, todas as etapas verdes, incluindo a verificação HTTP externa. O
pipeline funciona.

O que sobrou não é automação: é **cerimônia**. Cada publicação exige a aprovação humana
do Environment `producao` — uma decisão que o ARQUITECT **já tomou** ao aceitar o release.
Repetir o clique não adiciona verificação; transforma o humano em gargalo e, na prática,
incentiva o "aprova sem olhar".

O método já prevê o perfil **DEPLOY**, mas ele nunca teve autoridade definida: o
`perfil-do-projeto.md` diz "GitHub Actions; o agente só abre PR e lê o resultado". Esta
ADR define a autoridade, os limites e o procedimento.

## Decisão

**O perfil DEPLOY recebe autorização permanente** para conduzir a publicação **dentro do
procedimento aprovado**, sem aprovação humana por passo:

1. **disparar, acompanhar, diagnosticar e reexecutar** o pipeline de deploy;
2. **publicar uma versão já aceita** — a tag criada no processo de release;
3. **executar rollback** para a tag anterior, dentro do procedimento (§"Rollback");
4. **operar o ciclo de vida dos containers na VPS pelo procedimento** — isto é, pelo
   script de entrada (`didasko-deploy-entry`), que faz backup verificado, checkout da tag,
   `subir.sh` e verificação HTTP;
5. **diagnosticar** (read-only) e **corrigir o que o procedimento prevê** (reexecução).

**O GitHub Actions continua sendo o caminho preferencial e auditável.** A atuação direta
do DEPLOY na VPS só é legítima quando:

- o pipeline **não pode** ser usado (runner indisponível, incidente em curso, tag sem
  workflow); **e**
- a operação está na lista do procedimento (§"Ato direto permitido"); **e**
- cada comando e saída fica na jornada da DEM.

## O que muda

| Onde | Antes | Depois |
|---|---|---|
| Environment `producao` | required reviewer (ARQUITECT) | **sem required reviewer**; secrets mantidos |
| `deploy.yml` | aprovação manual por execução | dispara e roda; a origem continua restrita a **tag `v*` ou `main`** |
| ADR-010 | "agente não publica; no máximo aciona quando autorizado" | **DEPLOY publica pelo procedimento**; o CI segue como caminho |
| ADR-015 | acesso operacional só para chave pública + leitura | **estende** à publicação e rollback **pelo procedimento** |
| `AGENTS.md` / `CONVENTIONS.md` | "IA não executa deploy" | "o **DEPLOY** executa pelo procedimento; os demais perfis, não" |
| `perfil-do-projeto.md` | papel DEPLOY sem autoridade | autoridade e limites definidos |

## Os gates que permanecem (não dispensam aprovação)

- **Aceite de release** — o ARQUITECT; a tag nasce do release aceito. O DEPLOY **publica**
  a tag, **não a inventa**.
- **EVAL** por DEM e **CI verde** no PR — o portão de qualidade não mudou.
- **Backup verificado** — `pg_dump` + `gzip -t` + `sha256sum -c` antes de publicar; **falha
  bloqueia o deploy**.
- **Verificação HTTP externa** ao final.
- **Origem da publicação** — só tag `v*` ou `main`.

## O que continua exigindo autorização específica e escrita

Não é interpretação; é a lista. Cada item exige autorização do ARQUITECT **para aquela
ação**, naquele atendimento:

| Ação | Exemplo |
|---|---|
| **Exclusão de dados** | `DROP`, `TRUNCATE`, `DELETE` em massa, remoção de volume |
| **Restauração de banco** | restaurar um `pg_dump` (o rollback **não** restaura dados) |
| **Migração de schema** | `alembic upgrade`, DDL |
| **Seed / importação com escrita** | `seed`, `importar_estudo_aplicado --apply` |
| **Mudança de infraestrutura** | `.env`, compose, Traefik, DNS, firewall, redes |
| **Rotação/revogação de chave** | remover entrada do `authorized_keys` |
| **Exportar ou ler segredo** | qualquer leitura de `.env`/secret |

**Proibido em qualquer caso:** **contornar permissões administrativas usando Docker** (ex.:
`docker run` com mount para ler arquivo que o usuário não pode ler, `docker exec` para
dados). O `sudo -n docker` do operador é para o **procedimento**, não para escalar.

## Acesso SSH não interativo (não depende de sessão do ARQUITECT)

- **Chave operacional dedicada**, com `restrict,command="/usr/local/bin/didasko-deploy-entry"`
  no `authorized_keys` e `known_hosts` fixado (`StrictHostKeyChecking=yes`);
- **a privada nunca entra no contexto da IA**: o cliente SSH lê o arquivo; o agente não lê,
  não copia, não exibe, não exporta;
- **separação de chaves**: a chave do **CI** (secret `DEPLOY_SSH_KEY`) é distinta da chave
  **operacional** do agente; uma não substitui a outra;
- **rotação**: a chave antiga (`dsh-agent-didasko-deploy`, hoje com **shell completo**, sem
  `restrict`) é revogada **depois** que o fluxo pelo pipeline estiver verde; as privadas
  temporárias são removidas; tudo registrado no runbook.

## Backup e integridade (bloqueante)

Antes de qualquer publicação:

1. `pg_dump` do banco de produção;
2. `gzip -t` (o arquivo é gzip válido);
3. `sha256sum` gravado ao lado do arquivo e **verificado** (`sha256sum -c`);
4. **falha em qualquer um → o deploy não começa**.

**Backups existentes nunca são removidos automaticamente** (a retenção é operação
autorizada). O backup **também** deve ser exportado como **artifact do run** — gap
conhecido da DEM-004 (§"Pendências").

## Rollback

**Critério** (qualquer um): HTTP ≠ 200 após o deploy; versão errada no ar; app em loop de
restart; erro que só aparece na execução.

**Procedimento**: checkout da tag anterior pelo script + `subir.sh`; o backup do deploy
que falhou é preservado. **O rollback é de aplicação, não de dados** — restaurar o banco
exige autorização específica.

**Limite**: o rollback não apaga backup, não altera `.env`, não muda infraestrutura.

## Ato direto permitido (quando o CI não puder)

Só estes, e com registro:

- `git fetch --tags` + `git checkout <tag>` no clone do operador;
- `subir.sh` (que faz o ciclo de vida do compose);
- `docker compose ps/logs` (diagnóstico);
- o script de entrada em modo `ping`.

Qualquer outro comando na VPS exige autorização.

## Auditabilidade

- **cada publicação é um run do workflow** — o registro fica no GitHub;
- **ato direto** fica na jornada da DEM, com comando, saída e motivo;
- a cadeia de chaves (qual chave, com qual `command=`, desde quando) fica no runbook.

## Consequências

**Positivas**
- O humano deixa de ser gargalo; a aprovação passa a ser **por release**, não por clique.
- O procedimento fica escrito e auditável — inclusive o que o DEPLOY não pode.
- A operação de rotina vira repetível e testável.

**Negativas / trade-offs**
- **Superfície maior**: sem o reviewer, um workflow alterado poderia publicar. Mitigação:
  branch protection no `main` (PR + CI), a origem restrita a tag/main, os secrets no
  Environment, e a tag só nasce de release aceito.
- Exige disciplina de jornada; sem registro, a delegação vira licença.
- A chave operacional atual tem shell completo — a restrição/rotação é dívida a pagar.

**Neutras**
- O caminho de publicação continua o mesmo (o script de entrada); muda **quem** aprova.

## Pendências que esta ADR assume (integração ao GitFlow)

1. **Commitar** o que a sessão de 19/10 deixou fora do git: a Emenda 1 da ADR-015, o
   `deploy/didasko-deploy-entry.sh` modificado (ping, `gzip -t`, `sha256sum -c`, sem
   exclusão automática de backup) e a `jornada-operacional-2026-10-19.md`;
2. **Exportar o backup como artifact** no `deploy.yml` (gap da DEM-004 §9.2);
3. **Revogar a chave antiga** e limpar as privadas temporárias (após o back-merge);
4. **Back-merge `main` → `develop`** e encerramento do `release/0.1.0`;
5. Atualizar os guardas (`AGENTS.md`, `CONVENTIONS.md`), o `perfil-do-projeto.md`, o
   runbook de deploy e criar o **runbook de rollback e recuperação**.

## Referências

- [ADR-008](ADR-008-segredos-e-senhas-demo.md) · [ADR-009](ADR-009-gitflow.md) ·
  [ADR-010](ADR-010-publicacao-por-ci.md) · [ADR-015](ADR-015-acesso-operacional-do-agente.md)
- DEM-202610-004 — CI/CD (Etapa 2), run `39175867118`
- Jornada operacional: `documentacao/dem/DEM-202610-004-ci-cd-fase-a3/jornada-operacional-2026-10-19.md`
