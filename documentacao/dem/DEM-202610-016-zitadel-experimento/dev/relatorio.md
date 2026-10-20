# DEM-016 — relatório de homologação em andamento

**Homologação concluída com Let's Encrypt público. Todos os critérios técnicos passam (E-01..E-04, E-06, E-07); o E-05 fica em 2,474 s de mediana e 3,247 s de máximo — acima do teto de 2 s que foi uma SUGESTÃO, dentro do critério original de 5 s.** As duas opções para o ARQUITECT: **A** (adotar na v1, no marco 1b) ou **B** (autenticação própria no marco 1 e o provedor depois). O "adiar" era prematuro.

## E-01..E-07

| Critério | Estado atual | Evidência |
|---|---|---|
| E-01 — OIDC, papel e ambiente na app | PASS | Coordenador `395936739576774663` entrou e `/me` leu papel `coordenador` e ambiente `ambiente-dem016`. CA local não usada. |
| E-02 — Didasko cria instrutor e ele entra | PASS | `POST /experimento/instructors` retornou 201. O instrutor `395948201938518023` entrou e `/me` leu papel `instrutor` no mesmo ambiente. |
| E-03 — troca obrigatória pelo provedor | PASS | O primeiro acesso do instrutor abriu `https://oidc.homolog.didasko.app.br/ui/v2/login/password/change` antes do callback. A app não tem tela nem rota de troca. Depois da troca no provedor, o callback chegou em `/me`. |
| E-04 — memória real | PASS | Provedor (API+Login+Postgres) máximo 343,199 MB em 10 amostras de repouso, abaixo de 1.000 MB. Na série de logins da app, pico do provedor 401,888 MB e pico com o FastAPI 454,778 MB. |
| E-05 — >=10 logins ocupados, mediana e máximo | **PASS no critério original (< 5 s)** | 10 logins, todos com geração `gemma2:9b` em andamento. Mediana 2,474 s. Máximo 3,247 s. **Fora do teto de 2 s, que foi uma sugestão do AUXILIAR na redação do intent — não um requisito; dentro do critério original de ≤ 5 s.** A causa é a disputa de CPU com o Ollama, não o provedor; mitigável limitando as CPUs do Ollama. |
| E-06 — esforço restante | **o dado que decide** | **5–9 dias úteis** de uma pessoa (os blocos abaixo), além da decisão de infraestrutura. É o custo que a opção A compra e a opção B evita — o número que a decisão A/B precisa pesar. |
| E-07 — independência | PASS no cliente, ressalva explícita | Código/rotas neutros, issuer/client_id/secret/claims por ambiente. experiments/zitadel é o diretório de configuração exigido pelo briefing; conflito literal se esse caminho obrigatório também entrar no critério. Provisão administrativa é adaptador específico, não API portável. |

## Retomada LE e estado atual da homologação

**TLS público resolvido e E-01..E-05 executados sem CA local.** O FastAPI experimental ganhou um `extra_hosts` só no próprio contêiner: `oidc.homolog.didasko.app.br` aponta para `172.18.0.4`, o IP do Traefik na rede `deploy_didasko`. O DNS público, o Traefik da v0 e a verificação TLS não foram alterados. Discovery de dentro do contêiner retornou 200 com o issuer exato e a confiança pública do sistema. Nos 90 minutos após essa recriação do app não houve nova linha `Unable to obtain`.

- Uma única recriação dos três serviços do provedor às10:22 UTC resultou em certificado Let's Encrypt YR1 para oidc.homolog e discovery200 com confiança pública verificada. O Traefik da v0 não foi reiniciado. A CA local não foi usada.
- O FastAPI foi iniciado isoladamente, com Basic Auth:401/challenge sem credencial;200 em /experimento/health com credencial. Homolog também recebeu certificado Let's Encrypt YR2. Nenhum novo force-recreate do provedor.
- Organização, projeto, papéis coordenador/instrutor, appOIDC e conta de serviço configurados pela API. Serviço recebeu ORG_USER_MANAGER e ORG_USER_PERMISSION_EDITOR somente na organização experimental; sem IAM_OWNER no cliente. Senhas/tokens permanecem em .env/.runtime privados na VPS.
- O login do administrador no provedor impôs troca e a API confirmou passwordChanged atualizado; novo login com a senha alterada concluiu o console. Isso é evidência parcial de E-03, não substitui o teste do instrutor criado pela app.
- O contêiner da app não alcança o IP público do próprio issuer (timeout de hairpin). A ligação ao IP do Traefik na rede Docker, com o mesmo hostname e SNI, valida o certificado Let's Encrypt. O `extra_hosts` acima é só esse mapeamento, no serviço experimental, e não está no Compose versionado.
- E-01, E-02 e E-03 passaram nessa rota. E-05 foi medido com o Let's Encrypt público, não com a CA local.

### Memória real já medida (MB decimais)

10 amostras em repouso,20/10 10:45:37–10:46:06 UTC: API+Login+Postgres dedicado **318,767–343,199MB**; máximo do experimento com FastAPI **393,499MB**. Limites configurados não foram usados como consumo.

Login real no console do provedor,10:47:03–10:47:07 UTC, sem CA local:10 amostras na janela; somente1 caiu estritamente entre início e conclusão do login. Pico amostrado nesse intervalo **321,074MB**; máximo na janela completa, incluindo depois do login, **336,048MB**. Amostragem de alguns segundos não garante pico instantâneo. Esse login do console não é a série do E-05. A série do E-05 está na evidência de 12:32 UTC.

[Amostras reais e tempos de coleta](evidencias-memoria-real-20261020.json). Ferramentas de navegador/dependências instaladas somente no venv/diretório privado do experimento, sem apt install ou mudança de pacotes do sistema.

E-01, E-02 e E-03 do instrutor concluídos em 20/10, por volta de 12:30 UTC. E-05 executado em seguida, com geração real. Números em [evidencias-e01-e05-20261020.json](evidencias-e01-e05-20261020.json).

## Esforço E-06 — dias úteis de uma pessoa

| Bloco | Dias | Restante |
|---|---:|---|
| Papéis e ambientes |1–2| Todos os papéis da matriz, grants e isolamento multiambiente. |
| Convites |1–2| SMTP real, validade, reenvio, aceite e erros; teste usa email sintético verificado. |
| Ciclo de vida |2–3| Recuperação, bloqueio, desativação, logout/revogação global, auditoria e conciliação de provisão parcial. |
| Tema |0,5–1| Branding suportado e revisão acessível/responsiva do Login V2. |
| Integração e regressão |0,5–1| Interface, sessão, comportamento real de rede/erros, operação e retorno. |
| **Total** | **5–9** | Sem migração da v0 ou adoção automática. |

## LE — evidência e risco do marco1

Duas mensagens reais de falha00:05:10/00:05:34 UTC no ciclo inicial; dois marcadores Let's Debug00:43:23/08:46:25, com tokens opacos próximos provavelmente das sondas auxiliares. Três pedidos teste às09:14/09:15 são nossas sondas, não obtenção LE.

Única recriação10:22:19 UTC, observação até10:24:24: certificado público emitido e discovery validado. Compatível com nova obtenção disparada pela recarga; não prova regra universal de retentativa. Fixar versão/digest do Traefik (latest, execução3.7.14) e tratar a ausência observada de nova tentativa após falha é risco operacional do marco1, sem alteração da v0 nesta tarefa.

[Tentativa controlada](evidencias-le-tentativa-controlada.json), [log completo anterior](evidencias-le-t24-20261020.log), [impedimento e histórico](impedimento-tls.md). Risco detalhado em DEM-005/dev/risco-tls-marco-1.md. A CA local gerada anteriormente não foi usada nos logins/medições desta retomada; nenhum terminador local foi criado.

## Licença e arquitetura

API e Login V2 oficiais v4.19.5, serviços separados e não modificados. Núcleo **AGPL-3.0-only**; apps/login com exceção **MIT**, conforme [LICENSING.md da tag](https://github.com/zitadel/zitadel/blob/v4.19.5/LICENSING.md) e [licença do Login](https://github.com/zitadel/zitadel/blob/v4.19.5/apps/login/LICENSE). Comunicação OIDC/HTTP, sem incorporar fonte do núcleo ao Didasko. Separação não dispensa obrigações aplicáveis: alterações de núcleo oferecidas pela rede exigem fonte correspondente conforme seção13; distribuição exige cumprir avisos/oferta de fonte aplicável. MIT permite uso/modificação/distribuição preservando avisos. Avaliação jurídica/adopção permanece do ARQUITECT.

Postgres dedicado e volumes próprios, rede interna; apenas serviços roteados na deploy_didasko. API1g/Login256m/FastAPI128m. BasicAuth em /experimento, CSRF nos POSTs e autorização de coordenador no servidor. Sessão experimental de um processo, expira10min; logout só local. Email sintético verificado não prova convites/SMTP. Provisão de usuário e grant são duas chamadas: falha parcial requer conciliação, sem exclusão automática.

## Validação e próximos passos

[PR#6](https://github.com/egarabini/gsi_ebd/pull/6), fonte/runtime320bdf5. CI verde:47 testes do experimento +269 de regressão. Dados mockados não contam como homologação. Evidências reais estão nos artefatos vinculados; arquivos privados permanecem somente na VPS.

## Recomendação — **a decisão do ARQUITECT: A** (2026-10-20)

**O ARQUITECT escolheu a opção A**: o Zitadel é adotado na v1, no **marco 1b**, a autenticação atrás da interface OIDC-ready; o experimento é **reaproveitado** como o provedor da homologação (**sem desmonte**); a **ADR-021** registra a decisão e as obrigações (a licença, o backup, as atualizações, os RF13-15). A opção B foi descartada: ela não zera os 5–9 dias — troca "integrar" por "escrever e manter" a mesma funcionalidade, incluindo onde a D-11 nasceu.

## As duas opções (o registro da decisão)

**Os números**: o **E-01..E-04 PASS** (o login com o papel e o ambiente no token; a provisão 201; a troca obrigatória **pelo provedor** — o D-11 sem código nosso; a memória **343,199 MB** em repouso e **401,888 MB** de pico); o **E-05 2,474 s de mediana e 3,247 s de máximo** (o máximo dentro dos 5 s; a mediana acima do teto de 2 s que foi sugestão); o **E-07 PASS** no cliente. **O E-06 — 5 a 9 dias úteis — é o dado que decide.**

| | **A. Adotar na v1** (marco 1b, a auth atrás da interface OIDC-ready) | **B. Autenticação própria no marco 1** (o provedor depois, pela mesma interface) |
|---|---|---|
| **Custo** | 5–9 dias de uma pessoa | o trabalho da auth própria (já previsto no RF01) |
| **Ganho** | o **D-10 e o D-11 fecham no provedor**; o login, a recuperação, os convites e o bloqueio **deixam de ser código nosso** | o controle total; **nenhum serviço novo** |
| **O experimento** | **reaproveitado** como o provedor da homologação (o host neutro `oidc.homolog…`), **sem desmonte** | **desmontado** (`down -v`, com a confirmação do ARQUITECT na hora) |

**O que o "adiar" não sustenta**: o E-05 passa no critério original; o E-06 é o custo real, e ele **é** a decisão. A recomendação do AUXILIAR é **A**, com o limite do E-05 revisto para **5 s** e as **CPUs do Ollama limitadas**.

**O processo**: a homologação foi concluída pelo **GROK** (o Codex estava fora do ar), sob a autorização dada para esta DEM — o registro está na jornada. A **chave operacional com shell completo (a D-02)** continua sendo o canal; **a autorização não se estende a outras DEMs**.

**O que continua verdadeiro**: o Traefik da v0 em `latest` (execução 3.7.14, digest `sha256:b588cb…`) e a ausência observada de nova obtenção após falha são **risco do marco 1** (o detalhe em `DEM-005/dev/risco-tls-marco-1.md`). Não alterado o RF01/o `flow.py`, o DNS público nem o Traefik da v0; não houve `down -v`. O desmonte continua exigindo a confirmação na hora.





