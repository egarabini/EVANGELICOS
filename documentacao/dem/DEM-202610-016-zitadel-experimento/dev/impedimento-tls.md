<!-- DEM016-E01-E05 -->
## E-01..E-05 sem CA local — 20/10, cerca de 12:30 UTC

**Executados. E-05 falhou na mediana.** O mapeamento privado foi aplicado só no FastAPI do experimento, depois que a obtenção pública já tinha saído. Não houve nova tentativa de certificado.

- `extra_hosts` do contêiner `experimento-oidc-identity-app-1`: `oidc.homolog.didasko.app.br:172.18.0.4` (IP do Traefik na rede `deploy_didasko`). DNS público, certificados e o processo do Traefik da v0 intactos. Verificação TLS da confiança do sistema permaneceu ligada. Discovery interno: 200, issuer `https://oidc.homolog.didasko.app.br`.
- E-01 PASS: coordenador `395936739576774663`, papel `coordenador`, ambiente `ambiente-dem016`.
- E-02 PASS: `POST /experimento/instructors` 201; instrutor `395948201938518023` entrou com papel `instrutor`.
- E-03 PASS: a UI do provedor em `/ui/v2/login/password/change` apareceu antes do callback. A app não implementa a troca.
- E-04 PASS: repouso do provedor até 343,199 MB. Pico na série de logins 401,888 MB.
- E-05 FAIL: 10 logins com `gemma2:9b` gerando; mediana 2,474 s; máximo 3,247 s; sobreposição em todas as tentativas.
- Recomendação registrada no relatório: adiar. Evidência: [evidencias-e01-e05-20261020.json](evidencias-e01-e05-20261020.json).

---

<!-- DEM016-CLIENTE-REDE-PENDENTE -->
## Retomada LE e estado atual da homologação

**Registro anterior, superado pela seção de cima.** Naquele momento o `extra_hosts` ainda não tinha sido aplicado.

- Uma única recriação dos três serviços do provedor às10:22 UTC resultou em certificado Let's Encrypt YR1 para oidc.homolog e discovery200 com confiança pública verificada. O Traefik da v0 não foi reiniciado. A CA local não foi usada.
- O FastAPI foi iniciado isoladamente, com Basic Auth:401/challenge sem credencial;200 em /experimento/health com credencial. Homolog também recebeu certificado Let's Encrypt YR2. Nenhum novo force-recreate do provedor.
- Organização, projeto, papéis coordenador/instrutor, appOIDC e conta de serviço configurados pela API. Serviço recebeu ORG_USER_MANAGER e ORG_USER_PERMISSION_EDITOR somente na organização experimental; sem IAM_OWNER no cliente. Senhas/tokens permanecem em .env/.runtime privados na VPS.
- O login do administrador no provedor impôs troca e a API confirmou passwordChanged atualizado; novo login com a senha alterada concluiu o console. Isso é evidência parcial de E-03, não substitui o teste do instrutor criado pela app.
- E-01 ponta a ponta parou em /experimento/login com500/httpx.ConnectTimeout: do contêiner app, conexão ao IP público do issuer e gateway expira. A conexão ao IP privado do Traefik na rede existente, preservando server_hostname=oidc.homolog.didasko.app.br, passou com certificado LE validado. Não é um novo bloqueio LE.
- Proposta submetida ao ARQUITECT: mapeamento extra_hosts somente na app experimental para alcançar esse mesmo servidor HTTPS interno, preservando URL/issuer/SNI e verificação pública. **Não aplicado**, pois a restrição de DNS exige esclarecimento. Sem mudar Traefik, DNS público ou certificados.

### Memória real já medida (MB decimais)

10 amostras em repouso,20/10 10:45:37–10:46:06 UTC: API+Login+Postgres dedicado **318,767–343,199MB**; máximo do experimento com FastAPI **393,499MB**. Limites configurados não foram usados como consumo.

Login real no console do provedor,10:47:03–10:47:07 UTC, sem CA local:10 amostras na janela; somente1 caiu estritamente entre início e conclusão do login. Pico amostrado nesse intervalo **321,074MB**; máximo na janela completa, incluindo depois do login, **336,048MB**. Amostragem de alguns segundos não garante pico instantâneo. Não confundir este login com E-05, que ainda não teve carga Ollama ou dez medidas.

[Amostras reais e tempos de coleta](evidencias-memoria-real-20261020.json). Ferramentas de navegador/dependências instaladas somente no venv/diretório privado do experimento, sem apt install ou mudança de pacotes do sistema.

Estado às 10:50 UTC, antes da retomada: E-01/E-02 e o E-03 do instrutor ainda não concluídos; E-05 ainda não executado. Ollama só tinha sido consultado (api/tags 200, gemma2:9b presente), sem geração. Esse parágrafo não descreve o estado atual.

---

<!-- DEM016-LE-CONTROLADO-OK -->
## Tentativa controlada de 20/10 — certificado público emitido

**O impedimento TLS do issuer foi resolvido após uma única recriação dos serviços do experimento. CA local não usada.** Discovery retornou200 com issuer exato e verificação TLS pela confiança pública normal.

### Atribuição corrigida

- Traefik/CA: **duas mensagens de falha real**, 00:05:10 UTC (identity-api@docker, DNS/CAA) e00:05:34 UTC (identity-login@docker, DNS A/AAAA). Mesmo ciclo inicial de subida; não se deve afirmar uma única tentativa/ordem real apenas pela proximidade.
- Let's Debug: **dois marcadores explícitos**, letsdebug-test às00:43:23 UTC e08:46:25 UTC. Os tokens opacos de00:43:27 e08:46:29 são compatíveis com as duas sondas auxiliares informadas pelo ARQUITECT (~00:41/~08:45), mas não há correlação de ordem CA no log. Registrar como provável auxiliar, não obtenção real do Traefik.
- Três pedidos teste às09:14/09:15 são as sondas HTTP desta equipe; não são emissão LE.

### Única ação executada

Usada .provider.compose.yml já existente na VPS: somente identity-db, identity-api e identity-login. O Compose principal ainda tinha a app não configurada; por isso não foi usado para recriar um quarto serviço. Mesmo projeto autorizado, sem down, sem remover volumes, sem reiniciar Traefik.
```bash
sudo -n docker logs --since 24h didasko_traefik > /tmp/t24.log 2>&1
grep -n 'Unable to obtain' /tmp/t24.log
grep -n -i 'letsdebug' /tmp/t24.log
cd ~/experimentos/didasko/experiments/zitadel
timeout 125s sudo -n docker logs --follow --tail 3 --timestamps didasko_traefik > /tmp/t24-new-attempt.log 2>&1 &
sudo -n docker compose -p experimento-oidc -f .provider.compose.yml up -d --force-recreate
```

Ciclo iniciado10:22:19 UTC e observação encerrada10:24:24 UTC. Exit124 é o término esperado do timeout do observador, não erro do Compose. Não houve segunda recriação. O log começa com três linhas históricas (--tail3); nenhuma linha nova de falha apareceu durante a janela.
```text
watch_exit=124
CONTROLLED_ATTEMPT_END_UTC: 2026-10-20T10:24:24Z

COMPLETE OBSERVATION WINDOW
2026-10-20T09:14:47.261845148Z 2026-10-20T09:14:47Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
2026-10-20T09:14:47.282738246Z 2026-10-20T09:14:47Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
2026-10-20T09:15:10.962400430Z 2026-10-20T09:15:10Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme

PUBLIC CERTIFICATE ISSUER
issuer=C = US, O = Let's Encrypt, CN = YR1
subject=CN = oidc.homolog.didasko.app.br
notBefore=Oct 20 09:24:15 2026 GMT
notAfter=Jan 18 09:24:14 2027 GMT

VERIFIED HTTPS DISCOVERY
{"status": 200, "issuer": "https://oidc.homolog.didasko.app.br", "system_trust_verified": true}
```

### Inferência e risco do marco1

O resultado é compatível com a hipótese de que a recarga dos roteadores disparou nova obtenção depois da falha inicial. Na janela observada não houve novas mensagens de obtenção entre00:05 e a recarga10:22. Isso não prova regra universal de que Traefik nunca retenta, nem elimina a possibilidade de backoff/estado não registrado no nível de log atual. Nenhuma repetição foi feita para testar a hipótese e pressionar o limite da CA.

Registrar para o marco1: **fixar versão e digest do Traefik** (atualmente latest, execução3.7.14), tratar a ausência observada de retentativa após falha e ter procedimento de recuperação com limite de tentativas. Recomendação operacional ao ARQUITECT; nenhuma modificação do Traefik da v0 foi feita.

[Log completo pré-tentativa](evidencias-le-t24-20261020.log); [evidência da tentativa](evidencias-le-tentativa-controlada.json). Risco detalhado em DEM-005/dev/risco-tls-marco-1.md. E-01..E-05 seguem em execução sem CA local; não foram marcados PASS por esta prova de TLS.

---

<!-- DEM016-CA-LOCAL-PREPARADA -->
## Contorno com CA local autorizado — preparação e lacunas de rota

**CA e certificado gerados; suporte do cliente publicado no PR#6, commit320bdf5. Terminador e /experimento não iniciados.** O veredito continua dependente da homologação, sem medidas reais ou recomendação.

### Executado dentro da autorização

Na VPS, tls/ excluído do Git antes da criação, diretório700, todos os arquivos600, dono didasko-deploy. OpenSSL criou CA RSA2048 e certificado para o único host autorizado oidc.homolog.didasko.app.br, válidos por dois dias. Nenhuma chave foi exibida, copiada ao repositório ou montada em cliente. Configurados CA:TRUE/keyCertSign na CA e CA:FALSE/serverAuth/SAN no certificado do host. Validação explícita:

```text
server.pem: OK
subject=CN = Experiment CA
notBefore=Oct 20 09:29:27 2026 GMT
notAfter=Oct 22 09:29:27 2026 GMT
sha256 Fingerprint=42:00:B8:DA:BA:97:F0:5A:85:3A:5A:D0:38:94:86:E2:C1:3B:90:45:F4:12:23:D9:EE:61:4E:7B:9A:51:D8:06
issuer=CN = Experiment CA
subject=CN = oidc.homolog.didasko.app.br
X509v3 Subject Alternative Name:
    DNS:oidc.homolog.didasko.app.br
ca.key 600 didasko-deploy
ca.pem 600 didasko-deploy
server.key 600 didasko-deploy
server.pem 600 didasko-deploy
```

Comando de validação: `openssl verify -CAfile ca.pem -verify_hostname oidc.homolog.didasko.app.br server.pem`. Isso valida arquivos e hostname, sem afirmar que existe endpoint publicado com esse certificado. Expiração local:22/10/2026 06h29 BRT.

Cliente: CA_BUNDLE configura SSLContext com CERT_REQUIRED e check_hostname=True tanto no Authlib quanto na provisão. CA inválida/ausente no caminho configurado falha; não existe verify=False nem fallback permissivo. Com CA_BUNDLE vazio preserva a confiança pública normal do sistema. Testes fazem handshake TLS em memória com certificado sintético e conferem: CA correta aceita, CA desconhecida recusada, hostname incorreto recusado, arquivo ausente falha e contexto efetivamente aplicado ao Authlib. **47 testes locais passaram**; certificados sintéticos não são a CA real nem dados de homologação.

### Lacunas devolvidas ao ARQUITECT antes da publicação

Leitura sem alteração:

```bash
sudo -n docker inspect didasko_traefik --format '{{json .HostConfig.PortBindings}}'
openssl s_client -connect homolog.didasko.app.br:443 -servername homolog.didasko.app.br -verify_return_error -showcerts </dev/null 2>/dev/null | openssl x509 -noout -issuer -subject -ext subjectAltName
```

```text
{"443/tcp":[{"HostIp":"","HostPort":"443"}],"80/tcp":[{"HostIp":"","HostPort":"80"}]}
issuer=CN = TRAEFIK DEFAULT CERT
subject=CN = TRAEFIK DEFAULT CERT
X509v3 Subject Alternative Name:
    DNS:69c0444f7fea4d8c7f41599a1d0a6ab8.c2e2fade5307021c368b6a70128bb359.traefik.default
```

1. O443 público pertence ao Traefik da v0. Um terminador restrito à rede interna pode atender clientes dessa rede, mas não passa a receber o navegador externo automaticamente. Falta definir como o navegador alcançará o terminador mantendo o issuer, sem alterar o DNS público nem o Traefik da v0.
2. O host da app homolog.didasko.app.br também apresenta certificado default sem SAN homolog. O certificado autorizado somente para oidc.homolog não pode validar https://homolog.didasko.app.br/experimento. Falta definir a confiança/rota desse host, preservando a exigência de /experimento passar pelo Traefik.

Pergunta enviada ao ARQUITECT com essas evidências. Não foi inventado outro hostname, porta pública, certificado para homolog, proxy alternativo ou desativação de verificação. Montagem da CA no cliente exige arquivo legível pelo UID da app dentro do container; não se deve montar a chave privada da CA nem assumir que caminho do host é caminho do container.

O provedor anterior continua saudável; não foi alterado Traefik, DNS ou certificado da v0. Nenhum desmonte, terminador ou app iniciado. Basic Auth existente permanece protegida na VPS. E-01..E-05 reais continuam não testados.

### Registro exigido para futuras medidas

**Método previsto, ainda não executado:** E-05 será medido com a CA do experimento; a produção usará LE; o bloqueio do LE é risco do marco1, incluindo a emissão de homolog.didasko.app.br. Somente quando existirem as dez medidas registrar no passado "o E-05 medido com a CA do experimento". Não afirmar que medições aconteceram nesta preparação.


---

<!-- DEM016-ESTADO-ACME-20261020 -->
## Estado ACME — diagnóstico somente de leitura de 20/10/2026, 06h23 BRT

**Coleta concluída e interrompida para decisão do ARQUITECT.** Não houve reinício, alteração de infraestrutura ou nova tentativa de emissão/login. A hipótese de redirect permanece refutada pelo diagnóstico HTTP anterior. Esta coleta não comprova uma falha interna de estado ACME; registra o estado observável e os erros disponíveis.

### Achados

1. **Erros completos de emissão nas 14h:** às 00:05:10 UTC, HTTP400/urn:ietf:params:acme:error:dns durante validação secundária, erro de rede ao consultar CAA. Às 00:05:34 UTC, também erro DNS na validação secundária, ao consultar A/AAAA. São os erros completos retornados pela CA que aparecem na coleta.
2. **08:46 UTC:** mensagens Cannot retrieve the ACME challenge com letsdebug-test e um token opaco. No contexto coletado não há mensagem Invalid response, URL de ordem, the pending order ou erro de autorização associado a esse horário. Não atribuir automaticamente essas sondas a uma ordem de emissão do Let's Encrypt.
3. **Versão em execução:** Traefik 3.7.14, build 2026-10-06T07:42:27Z, linux/amd64. Image ID e RepoDigest: sha256:b588cb566045e1ebb185948a8e2456f9705cb915b5f0fb5ee698184233997817. Imagem criada em 06/10 17:48:04 UTC; contêiner criado em 07/10 18:00:38 UTC, iniciado em 18/10 17:27:43 UTC, RestartCount=0. O Compose consultado no clone autorizado fixa traefik:latest, não um digest.
4. **Comparação com 7/out:** o certificado da v0 tem notBefore=07/10 17:02:27 UTC. O contêiner atual data do próprio dia7, portanto não se evidencia recriação/troca de imagem após sua criação em7/out; reinício/início em18/out não equivale a atualização de imagem. Não há nesta coleta o digest histórico do processo que emitiu o certificado. Como notBefore antecede Created do contêiner, não é possível provar igualdade de imagem no instante da emissão somente com esses metadados. A tag latest no arquivo também não prova que houve atualização.
5. **acme.json:** 16048 bytes, modo600, root. Resolver le, apenas um certificado: didasko.app.br, SAN www.didasko.app.br; emissor Let's Encrypt YR1; validade 07/10/2026–05/01/2027. Nenhum certificado para oidc.homolog na lista. A busca literal por Main não retornou linhas; extração JSON posterior encontra o campo domain.main em minúsculas.
6. **Ordens persistidas:** nenhuma chave contendo order/pending encontrada na estrutura JSON. Isso não prova ausência de ordens em memória ou qual era o estado do token às08:46. Não foi coletado nem exibido conteúdo de chaves privadas, conta ou tokens de credencial.
7. **Resolvedor efetivo:** le usa storage /letsencrypt/acme.json e httpchallenge no entrypoint web. Há redirect global web→websecure, porém o teste anterior demonstrou404 no desafio. Não há opção caserver nas linhas efetivas; os logs de emissão identificam explicitamente a CA de produção https://acme-v02.api.letsencrypt.org/directory.

### Comandos e saídas exatas — coleta principal

Executados via SSH didasko-vps. A ordem de redirecionamento foi corrigida para > /tmp/traefik.log 2>&1, capturando stdout e stderr; 2>&1 > arquivo deixaria stderr fora do arquivo. Apenas um arquivo temporário de diagnóstico foi escrito na VPS, com umask077; nenhuma configuração foi alterada.
```bash
set -eu
printf 'UTC: '; date -u '+%Y-%m-%dT%H:%M:%SZ'
umask 077
sudo -n docker logs --since 14h didasko_traefik > /tmp/traefik.log 2>&1
printf '\nCONTEXT 08:46\n'
grep -n -B5 -A10 '08:46' /tmp/traefik.log || test "$?" -eq 1
printf '\nACME ORDER ERRORS LAST 40\n'
grep -n -i -E 'invalid response|urn:ietf|order|authorization|acme' /tmp/traefik.log | tail -40
printf '\nRUNNING CONTAINER IMAGE\n'
sudo -n docker inspect didasko_traefik --format 'image={{.Image}} criado={{.Created}}'
printf '\nRUNNING IMAGE DIGEST\n'
image_id=$(sudo -n docker inspect didasko_traefik --format '{{.Image}}')
sudo -n docker image inspect "$image_id" --format 'digest={{index .RepoDigests 0}} criado={{.Created}}'
printf '\nCOMPOSE TRACKED IN AUTHORIZED EXPERIMENT CLONE\n'
grep -n -A3 'traefik:' "$HOME/experimentos/didasko/deploy/docker-compose.producao.yml"
printf '\nACME FILE METADATA\n'
sudo -n docker exec didasko_traefik stat -c '%s bytes %a %U' /letsencrypt/acme.json
printf '\nACME MAIN DOMAIN MATCHES\n'
sudo -n docker exec didasko_traefik sh -c 'tr -d "\n" < /letsencrypt/acme.json | grep -o "\"Main\":\"[^\"]*\""' | head -20
printf '\nEFFECTIVE RESOLVER COMMAND\n'
sudo -n docker inspect didasko_traefik --format '{{join .Config.Cmd "\n"}}' | grep -i -E 'acme|entrypoint|storage|caserver|httpchallenge'
```

Somente códigos ANSI de cor removidos para exibição. Texto integral bruto da saída preservado no JSON de evidência.
```text
UTC: 2026-10-20T09:23:36Z

CONTEXT 08:46
1-2026-10-20T00:05:10Z ERR Unable to obtain ACME certificate for domains error="unable to generate a certificate for the domains [oidc.homolog.didasko.app.br]: resolver: one or more domains had a problem: [oidc.homolog.didasko.app.br: invalid authorization: acme: error: 400 :: urn:ietf:params:acme:error:dns :: During secondary validation: While processing CAA for oidc.homolog.didasko.app.br: DNS problem: networking error looking up CAA for oidc.homolog.didasko.app.br]" ACME CA=https://acme-v02.api.letsencrypt.org/directory acmeCA=https://acme-v02.api.letsencrypt.org/directory domains=["oidc.homolog.didasko.app.br"] providerName=le.acme routerName=identity-api@docker rule=Host(`oidc.homolog.didasko.app.br`)
2-2026-10-20T00:05:34Z ERR Unable to obtain ACME certificate for domains error="unable to generate a certificate for the domains [oidc.homolog.didasko.app.br]: resolver: one or more domains had a problem: [oidc.homolog.didasko.app.br: invalid authorization: acme: error: 400 :: urn:ietf:params:acme:error:dns :: During secondary validation: DNS problem: networking error looking up A for oidc.homolog.didasko.app.br; DNS problem: networking error looking up AAAA for oidc.homolog.didasko.app.br]" ACME CA=https://acme-v02.api.letsencrypt.org/directory acmeCA=https://acme-v02.api.letsencrypt.org/directory domains=["oidc.homolog.didasko.app.br"] providerName=le.acme routerName=identity-login@docker rule="Host(`oidc.homolog.didasko.app.br`) && PathPrefix(`/ui/v2/login`)"
3-2026-10-20T00:43:23Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "letsdebug-test") providerName=acme
4-2026-10-20T00:43:27Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "lo0rHAgSg3YsLf4Ddlm9h3iConjkbk8HeZhQRUbRTP4") providerName=acme
5:2026-10-20T08:46:25Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "letsdebug-test") providerName=acme
6:2026-10-20T08:46:29Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "ODZW1Rhveickin-gIz_I6YQSawWkmyoUGGqJo6iS5R4") providerName=acme
7-2026-10-20T09:14:47Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
8-2026-10-20T09:14:47Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
9-2026-10-20T09:15:10Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme

ACME ORDER ERRORS LAST 40
1:2026-10-20T00:05:10Z ERR Unable to obtain ACME certificate for domains error="unable to generate a certificate for the domains [oidc.homolog.didasko.app.br]: resolver: one or more domains had a problem: [oidc.homolog.didasko.app.br: invalid authorization: acme: error: 400 :: urn:ietf:params:acme:error:dns :: During secondary validation: While processing CAA for oidc.homolog.didasko.app.br: DNS problem: networking error looking up CAA for oidc.homolog.didasko.app.br]" ACME CA=https://acme-v02.api.letsencrypt.org/directory acmeCA=https://acme-v02.api.letsencrypt.org/directory domains=["oidc.homolog.didasko.app.br"] providerName=le.acme routerName=identity-api@docker rule=Host(`oidc.homolog.didasko.app.br`)
2:2026-10-20T00:05:34Z ERR Unable to obtain ACME certificate for domains error="unable to generate a certificate for the domains [oidc.homolog.didasko.app.br]: resolver: one or more domains had a problem: [oidc.homolog.didasko.app.br: invalid authorization: acme: error: 400 :: urn:ietf:params:acme:error:dns :: During secondary validation: DNS problem: networking error looking up A for oidc.homolog.didasko.app.br; DNS problem: networking error looking up AAAA for oidc.homolog.didasko.app.br]" ACME CA=https://acme-v02.api.letsencrypt.org/directory acmeCA=https://acme-v02.api.letsencrypt.org/directory domains=["oidc.homolog.didasko.app.br"] providerName=le.acme routerName=identity-login@docker rule="Host(`oidc.homolog.didasko.app.br`) && PathPrefix(`/ui/v2/login`)"
3:2026-10-20T00:43:23Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "letsdebug-test") providerName=acme
4:2026-10-20T00:43:27Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "lo0rHAgSg3YsLf4Ddlm9h3iConjkbk8HeZhQRUbRTP4") providerName=acme
5:2026-10-20T08:46:25Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "letsdebug-test") providerName=acme
6:2026-10-20T08:46:29Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "ODZW1Rhveickin-gIz_I6YQSawWkmyoUGGqJo6iS5R4") providerName=acme
7:2026-10-20T09:14:47Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
8:2026-10-20T09:14:47Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
9:2026-10-20T09:15:10Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme

RUNNING CONTAINER IMAGE
image=sha256:b588cb566045e1ebb185948a8e2456f9705cb915b5f0fb5ee698184233997817 criado=2026-10-07T18:00:38.564701495Z

RUNNING IMAGE DIGEST
digest=traefik@sha256:b588cb566045e1ebb185948a8e2456f9705cb915b5f0fb5ee698184233997817 criado=2026-10-06T17:48:04.120233275Z

COMPOSE TRACKED IN AUTHORIZED EXPERIMENT CLONE
23:  traefik:
24:    image: traefik:latest
25-    container_name: didasko_traefik
26-    restart: unless-stopped
27-    # CORRECAO (fonte: forum oficial do Traefik, "make sure to use Traefik latest"):

ACME FILE METADATA
16048 bytes 600 root

ACME MAIN DOMAIN MATCHES

EFFECTIVE RESOLVER COMMAND
--entrypoints.web.address=:80
--entrypoints.websecure.address=:443
--entrypoints.web.http.redirections.entrypoint.to=websecure
--entrypoints.web.http.redirections.entrypoint.scheme=https
--certificatesresolvers.le.acme.email=egarabini@gmail.com
--certificatesresolvers.le.acme.storage=/letsencrypt/acme.json
--certificatesresolvers.le.acme.httpchallenge.entrypoint=web
```

### Comandos e saídas exatas — versão e metadados JSON

O conteúdo bruto do arquivo passou somente por um pipe para um extrator com saída limitada a domínios, datas públicas de certificados e nomes/tipos/contagens de campos order/pending. Não foi copiado para documento nem exibido. Chaves privadas nunca são selecionadas para saída.
```bash
set -eu
printf 'RUNNING VERSION\n'
sudo -n docker exec didasko_traefik traefik version
printf '\nCONTAINER LIFETIME\n'
sudo -n docker inspect didasko_traefik --format 'criado={{.Created}} iniciado={{.State.StartedAt}} reinicios={{.RestartCount}}'
printf '\nACME STRUCTURAL METADATA ONLY\n'
sudo -n docker exec didasko_traefik cat /letsencrypt/acme.json | python3 -c '
import sys,json,base64,subprocess
root=json.load(sys.stdin)
for resolver,value in root.items():
    if not isinstance(value,dict): continue
    certs=value.get("Certificates",value.get("certificates",[])) or []
    print(json.dumps({"resolver":resolver,"certificate_count":len(certs)}))
    for cert in certs:
        domain=cert.get("domain",cert.get("Domain",{}))
        print(json.dumps({"main":domain.get("main",domain.get("Main")),"sans":domain.get("sans",domain.get("SANs",[]))}))
        encoded=cert.get("certificate",cert.get("Certificate"))
        if encoded:
            result=subprocess.run(["openssl","x509","-noout","-issuer","-dates"],input=base64.b64decode(encoded),capture_output=True)
            if result.returncode==0: sys.stdout.write(result.stdout.decode())
            else: print("certificate_metadata_parse_failed")
found=[]
def scan(value,path):
    if isinstance(value,dict):
        for key,child in value.items():
            if "order" in key.lower() or "pending" in key.lower():
                found.append({"path":path+"/"+key,"type":type(child).__name__,"count":len(child) if isinstance(child,(list,dict)) else None})
            scan(child,path+"/"+key)
    elif isinstance(value,list):
        for index,child in enumerate(value): scan(child,path+"/"+str(index))
scan(root,"")
print(json.dumps({"pending_or_order_sections":found,"values_not_printed":True}))
'
```
```text
RUNNING VERSION
Version:      3.7.14
Codename:     langres
Go version:   go1.26.8
Built:        2026-10-06T07:42:27Z
OS/Arch:      linux/amd64

CONTAINER LIFETIME
criado=2026-10-07T18:00:38.564701495Z iniciado=2026-10-18T17:27:43.522467189Z reinicios=0

ACME STRUCTURAL METADATA ONLY
{"resolver": "le", "certificate_count": 1}
{"main": "didasko.app.br", "sans": ["www.didasko.app.br"]}
issuer=C = US, O = Let's Encrypt, CN = YR1
notBefore=Oct  7 17:02:27 2026 GMT
notAfter=Jan  5 17:02:26 2027 GMT
{"pending_or_order_sections": [], "values_not_printed": true}
```

### Devolução

Sem evidência suficiente para determinar por que um token não estava disponível naquele instante. Nenhuma correção proposta foi aplicada. Decisão e eventuais investigações adicionais são do ARQUITECT. Não alterados Traefik do v0, DNS, certificados ou verificação TLS; não iniciado /experimento; não executado down -v.

[Evidência bruta da coleta](evidencias-estado-acme-20261020.json). O código está pronto; o veredito depende da homologação.

---

<!-- DEM016-DIAGNOSTICO-20261020 -->
## Diagnóstico somente de leitura — 20/10/2026, 06h15 BRT (09h15 UTC)

**Resultado: desafio ACME retorna 404 por dentro e por fora; raiz HTTP retorna 308.** Não foi observado redirect no caminho do desafio. Certificado permanece CN = TRAEFIK DEFAULT CERT. Aplica-se o ramo 4 do pedido: registrar e devolver ao PLANNER; causa da emissão indeterminada.

### Comandos na VPS e stdout

Via SSH didasko-vps, usuário didasko-deploy. --max-time 20 somente limita a espera; curl não seguiu redirects.
```bash
date -u '+%Y-%m-%dT%H:%M:%SZ'
sudo -n docker ps --format '{{.Names}} {{.Image}}' --filter ancestor=traefik
curl --max-time 20 -sS -o /dev/null -w 'local: %{http_code}\n' http://127.0.0.1/.well-known/acme-challenge/teste -H 'Host: oidc.homolog.didasko.app.br'
curl --max-time 20 -sS -o /dev/null -w 'externo: %{http_code}\n' http://oidc.homolog.didasko.app.br/.well-known/acme-challenge/teste
curl --max-time 20 -sS -I http://oidc.homolog.didasko.app.br/ | head -3
openssl s_client -connect oidc.homolog.didasko.app.br:443 -servername oidc.homolog.didasko.app.br -verify_return_error -showcerts </dev/null 2>/dev/null | openssl x509 -noout -issuer -subject -dates -fingerprint -sha256
```

Saída remota com os marcadores de coleta:
```text
UTC: 2026-10-20T09:14:47Z
didasko_traefik traefik:latest

LOCAL CHALLENGE
local: 404

PUBLIC CHALLENGE FROM VPS
externo: 404

PUBLIC HTTP HEAD FROM VPS
HTTP/1.1 308 Permanent Redirect

Location: https://oidc.homolog.didasko.app.br/

Date: Tue, 20 Oct 2026 09:14:47 GMT


CERTIFICATE METADATA ONLY
issuer=CN = TRAEFIK DEFAULT CERT
subject=CN = TRAEFIK DEFAULT CERT
notBefore=Oct 20 00:05:29 2026 GMT
notAfter=Oct 20 00:05:29 2027 GMT
sha256 Fingerprint=8B:5F:54:C6:5A:70:27:F3:DA:D3:1D:8C:D4:AB:77:F1:E5:0E:D8:B8:35:FA:20:E8:F2:FE:91:18:07:BC:01:77
```

O comando de certificado extrai somente metadados; -verify_return_error permaneceu ativo. A extração não afirma que o certificado foi aceito. Uma falha local de sintaxe PowerShell (identificador textResult, antes do SSH) emitiu diagnóstico separado e não impediu o SSH (exit0); não integra o stdout remoto acima.

### Teste externo, fora da VPS — estação Windows
```powershell
curl.exe --max-time 20 -sS -o NUL -w 'externo: %{http_code}\n' http://oidc.homolog.didasko.app.br/.well-known/acme-challenge/teste
curl.exe --max-time 20 -sS -I http://oidc.homolog.didasko.app.br/ | Select-Object -First 3
```
```text
externo: 404

HTTP/1.1 308 Permanent Redirect

Location: https://oidc.homolog.didasko.app.br/

Date: Tue, 20 Oct 2026 09:15:11 GMT
```

### Logs ACME das últimas 8 horas
```bash
date -u '+%Y-%m-%dT%H:%M:%SZ'
sudo -n docker logs --since 8h --timestamps didasko_traefik 2>&1 | python3 -c 'import sys; [sys.stdout.write(line) for line in sys.stdin if "acme" in line.lower()]'
```

Coleta às 09:15:13 UTC; janela aproximada 01:15:13–09:15:13 UTC de 20/10. Todas as linhas retornadas estão abaixo. Somente sequências ANSI de cor foram removidas da exibição; stdout bruto preservado no JSON.
```text
UTC: 2026-10-20T09:15:13Z
2026-10-20T08:46:25.234352630Z 2026-10-20T08:46:25Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "letsdebug-test") providerName=acme
2026-10-20T08:46:29.207131994Z 2026-10-20T08:46:29Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "ODZW1Rhveickin-gIz_I6YQSawWkmyoUGGqJo6iS5R4") providerName=acme
2026-10-20T09:14:47.261845148Z 2026-10-20T09:14:47Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
2026-10-20T09:14:47.282738246Z 2026-10-20T09:14:47Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
2026-10-20T09:15:10.962400430Z 2026-10-20T09:15:10Z ERR Cannot retrieve the ACME challenge for oidc.homolog.didasko.app.br (token "teste") providerName=acme
```

### Achado e limites

- **404 no desafio** em loopback com Host correto, hostname público da VPS e estação externa: o caminho chega ao handler ACME. Os pedidos com token teste aparecem nos horários das sondas.
- **308 apenas em /** não comprova captura/redirecionamento do desafio. Não se aplica o ramo 3 (301/308 no próprio caminho ACME); aplica-se o ramo 4.
- Cannot retrieve... com token teste é esperado para uma sonda de token inexistente. As entradas anteriores de 08:46 incluem letsdebug-test e um token opaco. Sem correlação com uma ordem ACME real, não é possível atribuir todas essas entradas à emissão do Let's Encrypt, nem determinar por que o token não foi encontrado.
- O certificado default permanece. Não foi determinada a causa raiz da emissão.
- **PARE/devolução ao PLANNER:** nenhum ajuste no Traefik do v0, DNS ou certificados; nenhuma verificação TLS desligada; /experimento não iniciado; nenhum down -v. DNS-01 ou CA local continuam decisões do ARQUITECT, sem execução.

Evidência bruta: [evidencias-diagnostico-tls-20261020.json](evidencias-diagnostico-tls-20261020.json). **O código está pronto; o veredito depende da homologação.** Nenhum login, medição E-01..E-05 ou recomendação de adoção resultou deste diagnóstico.

---

## Historico anterior ao diagnostico acima

# DEM-016 — devolução ao PLANNER: validação TLS

**O código está pronto; o veredito depende da homologação.** Nenhuma recomendação de adoção antes das medidas reais.

## Resolvido

O clone foi criado no caminho autorizado, como didasko-deploy, e fixado em dcf136a. Não há impedimento de clone/acesso SSH. Configuração local da VPS sem o FastAPI permite iniciar os três serviços de provedor enquanto a Basic Auth aguarda o arquivo do ARQUITECT.

## Evidência

- Postgres dedicado, API e Login V2 observados healthy no projeto experimento-oidc.
- Discovery HTTPS: `URLError`, reason_type=`SSLCertVerificationError`.
- Login health público HTTPS: mesmo erro.
- Readiness limitada: `public_provider_health_not_ready_stop_for_planner`, exit1.
- Login inspecionado: exit0, OOM=false, restarts=0.

Não se conclui a causa raiz apenas pelo tipo da exceção. PLANNER/ARQUITECT devem confirmar certificado, cadeia/emissão/roteamento e trust store conforme o ambiente esperado, antes de autorizar retomada. Nenhuma verificação TLS foi desativada, nenhum host/porta alternativo usado e nenhum ajuste de infraestrutura foi tentado após a divergência.

Serviços continuam rodando; não houve desmonte, que exige confirmação específica na hora. Nunca executar DROP no didasko_postgres. A Basic Auth foi gerada conforme nova autorização, sem exibir valores; ver atualização ao final. E-01..E-05 reais continuam não testados; nenhuma carga Ollama ou login de usuário foi executado.


## Retomada: Basic Auth gerada; TLS ainda bloqueado

O ARQUITECT autorizou gerar credencial aleatória na VPS. Clone existente conferido em dcf136a; não foi recriado. OpenSSL gerou senha e hash APR1 sem exibir valores. Senha gravada exclusivamente em `/home/didasko-deploy/experimentos/didasko/experiments/zitadel/basic-auth-password.txt`, modo600; registro `EXPERIMENTO_BASIC_USERS` acrescentado ao .env600. Arquivo de senha excluído do Git por configuração local antes da gravação. Hash protegido com aspas simples no .env para preservar os caracteres $ na interpolação do Compose. Nenhuma senha/hash no chat, log ou repositório.

Nova verificação pública, ainda com validação TLS habilitada: discovery e Login health falham com **SSLCertVerificationError, verify_code=18, verify_message=self-signed certificate**. Readiness terminou `tls_preflight_failed_stop_for_planner`, exit1. Logo, o impedimento TLS persiste; a Basic Auth deixou de ser pendência de fornecimento.

**PARE aplicado novamente conforme instrução expressa:** sem iniciar /experimento, sem login, sem carga Ollama, sem desativar verificação TLS, sem alterar Traefik/DNS/certificados e sem desmonte. O middleware ativo de /experimento ainda não foi criado; sua configuração local da VPS deve referenciar `EXPERIMENTO_BASIC_USERS` quando TLS permitir retomar. O Compose versionado anterior usa outro nome; não se deve subir a app sem a adaptação local autorizada.

PLANNER/ARQUITECT: regularizar/esclarecer o certificado apresentado pelo endpoint antes de retomar E-01..E-05. O código está pronto; o veredito depende da homologação. Sem recomendação antes das medidas reais. Serviços do provedor permanecem em execução; down -v somente após confirmação na hora.


CA explicita: commit `320bdf56095cfb7340723aaf367b3d54e1bc55a4`, mesmo [PR#6](https://github.com/egarabini/gsi_ebd/pull/6). [CI do experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39401372787): **47 testes passaram**; [regressao](https://github.com/egarabini/gsi_ebd/actions/runs/39401372798): **269 passaram**. Ambos verdes. Nao equivalem a logins reais; terminador e app pendentes da definicao de rota.
