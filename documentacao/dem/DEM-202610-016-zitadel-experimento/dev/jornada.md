# Jornada — DEM-016

## Fechamento da tentativa controlada — 20/10

- A obtenção única das 10:22 UTC já tinha emitido Let's Encrypt YR1. Não foi repetida.
- O Codex parou no E-01 por timeout do FastAPI até o IP público do issuer e no limite de uso, antes de atualizar o PR.
- Retomada: só o contêiner da app foi recriado, com `extra_hosts` para o IP do Traefik na rede existente. Traefik da v0 não reiniciou. `Unable to obtain` continuou em zero nessa janela.
- E-01, E-02 e E-03 passaram. E-04 permanece PASS (343,199 MB em repouso). E-05 FAIL: mediana 2,474 s, máximo 3,247 s, 10 logins com geração sobreposta.
- Recomendação: adiar. Relatório e impedimento atualizados. Sem commit, sem down -v, sem DNS público.



- Leituras: intent, autorização de infra, briefing, documentação oficial de arquitetura/API/licença, design DEM-005, AGENTS, PROJECT_CONTEXT e CONVENTIONS.
- Think/List: usuário autorizou expressamente fase 1 sem espera; experimento, interface, configuração, ferramentas, testes e CI isolados. Nenhuma autorização de infra implícita.
- Worktree preexistente C:/Projetos/EM_ESTUDO/EVANGELICOS/.worktrees/DEM-016, branch feature/DEM-202610-016-zitadel, base develop 7670aec; rascunho não commitado aproveitado. Sem checkout/reset no app da DEM-011.
- Corrigido rascunho: host da app separado do issuer, origem CSRF da app, nomes neutros, erros JOSE devolvem 401, issuer fixado no Authlib.
- Código de cliente movido para experiments/identity_client; experiments/zitadel reservado à configuração. Ressalva E-07 registrada.
- Versão oficial consultada via GitHub: v4.19.5. API por h2c, Login V2 separado, licença na tag. Configuração não executada.
- Tentativa de preparar API/Login root rejeitada pela revisão automática; alternativa final usa UID1000:1000, com preparação do volume pendente de autorização. Nenhum comando de infra executado.
- Primeiro teste: 29 passaram, um falhou por comparação case-sensitive dos flags do cookie. Teste corrigido para atributo HTTP case-insensitive.
- Resultado local final: 40 passaram. Compose config --no-interpolate --quiet exit0. Artefatos/resultados de cálculo sintéticos não são métricas da VPS.
- Relatório parcial registra E-01..E-05 não testados em homologação, E-06 estimado, E-07 com ressalva explícita; recomendação adiar adoção.

- Manifests públicos GHCR confirmam API e Login v4.19.5; digests no relatório. Fonte Dockerfiles oficial identifica Login UID1001: ajuste rootless e fluxo API primeiro / permissão PAT 0640 / Login depois, ainda não executado.


## Entrega da fase 1 e CI

Commit `8d894aad283b2cb6a9639a63d6cc0d528a7f3d3f`; [PR #6 draft aberto](https://github.com/egarabini/gsi_ebd/pull/6). [CI do experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39343258566): **40 testes passaram**, Python 3.12, e Compose validado. [CI de regressão](https://github.com/egarabini/gsi_ebd/actions/runs/39343258578): **269 testes passaram**. Ambos verdes no commit entregue. Diff limitado a experiments/ e um workflow isolado; gsi_ebd/, v1/ e deploy/ sem alterações. Worktree limpo.

Autorização a–e solicitada com configuração revisável; nenhuma resposta de aprovação recebida nesta etapa. Fases 2–3 não executadas. Não marcar E-01..E-05 reais como PASS.

## Autorização condicionada de 19/10 — atualização

- Relidos intent §7/§10 e autorização final. Substituem banco compartilhado por Postgres dedicado interno, API1g e critério >=10 logins/mediana2s/máximo5s. Recomendação anterior retirada do relatório corrente: veredito somente após números.
- Compose, gerador openssl, ferramenta de memória/latência e testes ajustados. Basic Auth obrigatória, fornecida pelo ARQUITECT; não inventada. Pedido por arquivo600/canal seguro feito no chat; nenhum segredo recebido.
- SSH somente de leitura: alias didasko-vps responde didasko-deploy. Rede deploy_didasko confirmada. Clone esperado não identificado pelo teste de diretório .git: clone=absent. Filtros de projeto não retornaram containers/volumes.
- PARE: operações na VPS interrompidas e divergência devolvida ao PLANNER. Nenhum fallback para clone existente, nenhuma criação de recurso/segredo/deploy/carga/exclusão. Apenas conclusão de configuração/testes/relatório locais já autorizados.
- 42 testes locais verdes. Não existe medição real, nem recomendação de adoção.


## CI do ajuste autorizado

Commit `dcf136acdc906b0eec9f3e81a7d3dcfbc3c3e1a6`, no mesmo [PR #6 draft aberto](https://github.com/egarabini/gsi_ebd/pull/6). [Experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39344948691): **42 testes verdes** e Compose validado. [Regressão](https://github.com/egarabini/gsi_ebd/actions/runs/39344948669): **269 testes verdes**. Nenhum diff em gsi_ebd/, v1/ ou deploy/. Nenhum merge. O CI não executa a homologação nem resolve a divergência do clone; permanece a devolução ao PLANNER e a pendência de credencial Basic Auth do ARQUITECT.

## Retomada autorizada: clone criado e serviços de provedor iniciados

- Usuário esclareceu explicitamente que a ausência do clone era preparação autorizada; criado em ~/experimentos/didasko e fixado dcf136a. Sem root no clone, sem segredo de Git (repositório público).
- Preflight: ferramentas disponíveis, rede correta, sem recursos anteriores de experimento. Segredos gerados via OpenSSL na VPS, direto em .env600, sem valores no chat/log.
- .provider.compose.yml local da VPS (600, fora do git), com API+Login+Postgres e sem app/router /experimento; imagens API/Login pelos digests aprovados. Basic Auth não preenchida, aguardando arquivo seguro do ARQUITECT.
- Volume bootstrap criado com labels do projeto; helper temporário sem rede preparou somente seu ownership. API+DB subiram com --wait e ficaram healthy. Permissão do PAT ajustada somente no volume próprio; Login subiu e foi observado healthy. Nenhum acesso ao didasko_postgres.
- HTTPS público rejeitado: URLError/SSLCertVerificationError em discovery e Login health. Readiness limitada terminou exit1. Não foi exposto conteúdo de token/log/segredo.
- PARE: devolução ao PLANNER em impedimento-tls.md. Nenhuma tentativa de contornar TLS, corrigir Traefik/DNS ou realizar login após a divergência. Sem carga Ollama, sem números de E-04/E-05, sem recomendação.
- Containers permanecem ativos; nenhum desmonte sem a confirmação específica na hora. PR#6 continua no commit dcf136a; somente relatórios e configuração própria da VPS mudaram nesta retomada.


## Retomada: Basic Auth gerada; TLS ainda bloqueado

O ARQUITECT autorizou gerar credencial aleatória na VPS. Clone existente conferido em dcf136a; não foi recriado. OpenSSL gerou senha e hash APR1 sem exibir valores. Senha gravada exclusivamente em `/home/didasko-deploy/experimentos/didasko/experiments/zitadel/basic-auth-password.txt`, modo600; registro `EXPERIMENTO_BASIC_USERS` acrescentado ao .env600. Arquivo de senha excluído do Git por configuração local antes da gravação. Hash protegido com aspas simples no .env para preservar os caracteres $ na interpolação do Compose. Nenhuma senha/hash no chat, log ou repositório.

Nova verificação pública, ainda com validação TLS habilitada: discovery e Login health falham com **SSLCertVerificationError, verify_code=18, verify_message=self-signed certificate**. Readiness terminou `tls_preflight_failed_stop_for_planner`, exit1. Logo, o impedimento TLS persiste; a Basic Auth deixou de ser pendência de fornecimento.

**PARE aplicado novamente conforme instrução expressa:** sem iniciar /experimento, sem login, sem carga Ollama, sem desativar verificação TLS, sem alterar Traefik/DNS/certificados e sem desmonte. O middleware ativo de /experimento ainda não foi criado; sua configuração local da VPS deve referenciar `EXPERIMENTO_BASIC_USERS` quando TLS permitir retomar. O Compose versionado anterior usa outro nome; não se deve subir a app sem a adaptação local autorizada.

PLANNER/ARQUITECT: regularizar/esclarecer o certificado apresentado pelo endpoint antes de retomar E-01..E-05. O código está pronto; o veredito depende da homologação. Sem recomendação antes das medidas reais. Serviços do provedor permanecem em execução; down -v somente após confirmação na hora.


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


CA explicita: commit `320bdf56095cfb7340723aaf367b3d54e1bc55a4`, mesmo [PR#6](https://github.com/egarabini/gsi_ebd/pull/6). [CI do experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39401372787): **47 testes passaram**; [regressao](https://github.com/egarabini/gsi_ebd/actions/runs/39401372798): **269 passaram**. Ambos verdes. Nao equivalem a logins reais; terminador e app pendentes da definicao de rota.


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

## Retomada LE e estado atual da homologação

**TLS público resolvido; pendente esclarecimento sobre a resolução privada do cliente FastAPI.** Nenhum extra_hosts ou mudança de DNS foi aplicado.

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

E-01/E-02 e o E-03 do instrutor permanecem não concluídos; E-05 ainda não executado. Ollama foi apenas consultado (api/tags200, gemma2:9b presente), sem geração iniciada. Sem recomendação antes de E-05. O código está pronto; o veredito depende da homologação.
