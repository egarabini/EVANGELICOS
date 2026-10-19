# Jornada operacional — 2026-10-19

Autorização: ADR-015 Accepted e autorização explícita do ARQUITECT neste atendimento para o cliente SSH usar a credencial local sem leitura da privada pelo agente.

## Diagnóstico e instalação da pública

- `ssh -o BatchMode=yes -o StrictHostKeyChecking=yes -o ConnectTimeout=10 didasko-vps 'id; sudo -n -l'`: acesso como `didasko-deploy`; sudo limitado a `/usr/bin/docker`. Nenhuma privada lida ou exibida.
- `stat -c "%U %a %n" /home/didasko-deploy/.ssh /home/didasko-deploy/.ssh/authorized_keys`: dono `didasko-deploy`, modos 700 e 600.
- `ls -l /usr/local/bin/didasko-deploy-entry`: arquivo inexistente. Bloqueio para o pipeline; nenhuma publicação executada.
- Pública fornecida: arquivo temporário `didasko_ci_nova.pub` do ARQUITECT. Somente a pública foi lida.
- Instalação via SSH com `set -eu`: receber a linha pública em stdin, verificar existência com `grep -Fqx`, fazer `cp -p` do arquivo e acrescentar com `printf '\n%s\n'` em modo append. Prefixo obrigatório: `restrict,command="/usr/local/bin/didasko-deploy-entry"`. Entradas existentes preservadas.
- Saída: `backup=/home/didasko-deploy/.ssh/authorized_keys.bak-20261019T101623Z`, `public-key-added`, `didasko-deploy 600 /home/didasko-deploy/.ssh/authorized_keys`. Código 0.

## Reversão (não executada)

Após autorização específica para sobrescrita, na VPS:

```bash
cp -p /home/didasko-deploy/.ssh/authorized_keys.bak-20261019T101623Z /home/didasko-deploy/.ssh/authorized_keys
```

O backup representa o estado anterior desta operação; conferir alterações posteriores antes de restaurá-lo.

## Pendência

Instalar o ponto de entrada ausente com privilégio administrativo, conforme implementação revisada da DEM. Não usar o sudo Docker para contornar a limitação de privilégios. Não reexecutar deploy até resolver essa pendência.

## Correção aprovada do ponto de entrada

- Aprovação explícita do ARQUITECT: preservar backups, gerar/verificar checksum e aceitar `ping` sem deploy.
- Alterado `ESTUDOS_BIBLICOS/GSI_EBD/deploy/didasko-deploy-entry.sh`: ping e rejeição antes de criar log; removida exclusão automática de backups; `gzip -t` e SHA-256 gerado e conferido antes de git/checkout.
- Validação: `bash -n`, `git diff --check`, ping sem arquivos criados, rejeição de `id` e tag com `;`. Ensaio isolado com sudo/git simulados: gzip e checksum válidos, backup antigo preservado, interrupção antes de git real. Nenhum deploy executado.
- Envio por stdin via `ssh didasko-vps`, para diretório exclusivo criado com `mktemp -d /tmp/didasko-entry.XXXXXXXX`; saída: `ok`, stage `/tmp/didasko-entry.0lPmHYJh`.
- SHA-256 na VPS: `23b8e66b1234cf69cd499802bb8301e4960c0d6f7ffbbb0201e0c6f19071b9c0`.
- Candidato temporário, ainda não instalado: `/tmp/didasko-entry.0lPmHYJh/didasko-deploy-entry`.
- Instalação administrativa depende da sessão interativa do ARQUITECT: SSH como eduardo com a credencial disponível foi recusado; sudo desse usuário requer senha. Nenhuma senha solicitada em chat.
- Após instalação inicial, reversão será desabilitar/remover exclusivamente o ponto de entrada novo, com autorização específica; o destino foi constatado ausente anteriormente. Se agora existir, parar e fazer backup antes de qualquer substituição.
- Ainda não inclui exportação do backup como artifact do Actions; não declarar a DEM inteira concluída com base nesta correção.
