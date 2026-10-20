# Risco TLS do marco 1 — evidencia DEM-016

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

Registrar para o marco1: **fixar versão e digest do Traefik** (atualmente `latest`, execução 3.7.14, digest `sha256:b588cb566045e1ebb185948a8e2456f9705cb915b5f0fb5ee698184233997817`), tratar a ausência observada de retentativa após falha e ter procedimento de recuperação com limite de tentativas. Recomendação operacional ao ARQUITECT; nenhuma modificação do Traefik da v0 foi feita.

O E-05 da DEM-016 foi medido depois, com o certificado público Let's Encrypt, não com a CA local. A mediana ficou em 2,474 s e o critério não passou. Isso não altera o risco desta nota: a imagem segue sem digest fixo, e a obtenção que falhou às 00:05 UTC só voltou a ocorrer quando os roteadores do experimento foram recarregados.

[Log completo pré-tentativa](../../DEM-202610-016-zitadel-experimento/dev/evidencias-le-t24-20261020.log); [evidência da tentativa](../../DEM-202610-016-zitadel-experimento/dev/evidencias-le-tentativa-controlada.json); [E-01..E-05](../../DEM-202610-016-zitadel-experimento/dev/evidencias-e01-e05-20261020.json). A prova de TLS não marca esses critérios; os resultados estão no relatório da DEM-016.

Os links de evidencia acima referem-se a pasta dev da DEM-016. Nenhuma alteracao no RF01, no design ou na infraestrutura da v0. A decisao de fixar imagem e de procedimento operacional e do ARQUITECT.
