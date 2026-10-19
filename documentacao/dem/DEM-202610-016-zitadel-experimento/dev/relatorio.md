# DEM-016 — relatório parcial: fase 1, infraestrutura pendente

**Recomendação atual: ADIAR a decisão de adoção até o ensaio autorizado.** Não é um descarte técnico do provedor. Nenhum resultado mockado é evidência de funcionamento na VPS. Nada foi adotado, publicado ou alterado na v0/v1, no RF01 ou no domínio. O prazo é de 1–2 dias; esta entrega prepara o ensaio e explicita o que ainda falta medir.

## Critérios e evidência

| Critério | Resultado real | Evidência disponível / falta |
|---|---|---|
| E-01: login + papel do token | **NÃO TESTADO em homologação** | PASS local: Authlib com discovery, JWKS RSA, ID token assinado, PKCE/state/nonce/issuer/aud/exp; identidade/ambiente vêm do token. Falta login real no Login V2. |
| E-02: Didasko cria instrutor e ele entra | **NÃO TESTADO em homologação** | PASS local: rota de coordenador chama CreateUser e grant; mocks verificam org/role e falha parcial. Falta criação real e login desse instrutor. |
| E-03: troca obrigatória pelo provedor | **NÃO TESTADO em homologação** | PASS local do contrato: changeRequired=true enviado ao provedor, sem lógica própria de troca. Não prova comportamento da UI; falta confirmar antes do callback. |
| E-04: provedor <1 GB em repouso | **NÃO TESTADO** | Consumo real: **N/D MB** repouso; **N/D MB** pico no login. Coletor por projeto pronto. Limites não são medição. |
| E-05: p95 de 3 logins ≤5s com Ollama ocupado | **NÃO TESTADO** | Tempos: **N/D, N/D, N/D s**; p95 **N/D s**. Ferramenta aguarda geração e confere sobreposição; sessão nova por tentativa. Sem carga na VPS nesta fase. |
| E-06: esforço restante | **PASS documental** | Estimativa abaixo: **5–9 dias**, exclui a decisão, migração da v0 e implantação de produção. Incerteza depende do ensaio. |
| E-07: independência | **PASS no cliente, ressalva de interpretação documentada** | issuer/client_id/secret e nomes de claims/scopes vêm do ambiente. Código em experiments/identity_client e ferramentas em experiments/tools, sem nome do fornecedor nos caminhos/rotas do cliente. O diretório experiments/zitadel contém somente configuração de implantação, dependências e documentação, conforme exigência explícita do briefing. Esse diretório obrigatório não pode ao mesmo tempo ter nome neutro; se o EVAL considerar também a configuração, registrar FAIL literal, não ocultar a exceção. A API administrativa continua adaptador específico e mudar de provedor requer implementá-la novamente. |

## Validação fase 1

Comando da raiz do worktree: `python -m pytest experiments/tests -q`: **40 passaram** (23 avisos de depreciação upstream: root_path, Starlette/httpx e integração Authlib/httpx). Testes de memória/latência usam entradas sintéticas somente para verificar cálculo/limites; não viraram números do experimento. `docker compose -f experiments/zitadel/docker-compose.yml config --no-interpolate --quiet`: exit 0, sem daemon/infra e sem interpolar segredos. CI e PR confirmados ao final deste relatório.

O cliente usa somente identificador opaco em cookie assinado; tokens/sessão em memória de um worker, expiram em 10 minutos; CSRF + Origin da app nos POSTs; provisionamento só coordenador. Não há senha local. Logout só local, não revoga sessão do provedor. A sessão de experimento não é a solução definitiva da v1. Grant após CreateUser não é transação: falha parcial visível 502, sem exclusão automática.

## Esforço restante E-06

Estimativa de engenharia para integrar o fluxo completo da v1, em dias úteis de uma pessoa (não são horas já trabalhadas nem promessa):

| Bloco | Dias | Trabalho restante |
|---|---:|---|
| Papéis e ambientes | 1–2 | Todos os papéis da matriz, grants por organização, vínculo de identidade e testes de isolamento multiambiente. |
| Convites | 1–2 | Convite real/SMTP, expiração, reenvio, aceite e mensagens de erro; teste atual marca email sintético verificado. |
| Ciclo de vida | 2–3 | Recuperação, desativação, bloqueio/tentativas, revogação/logout global, sessão da app, auditoria e conciliação de provisão parcial. |
| Tema | 0,5–1 | Branding suportado, acessibilidade, responsividade, revisão das telas hospedadas e limites do plano/licença. |
| Integração final e regressão | 0,5–1 | Trocar implementação da interface, testes reais, operação/retorno e documentação. |
| **Total** | **5–9** | Sem migração de usuários da v0; produção limpa somente se o ARQUITECT decidir adotar. |

Não justifica adoção pela economia sem comparar esse custo ao restante da auth própria. A fase 1 mostra viabilidade do contrato OIDC, não do consumo da pilha.

## Arquitetura e licença verificadas

Tag oficial encontrada: **v4.19.5** (API GitHub releases/latest); imagens da API e Login V2 fixadas nessa tag. Disponibilidade e digests confirmados por consulta pública de manifests GHCR, sem baixar camadas. API: sha256:a586456a208e0db4c633db0ba43c427c24b37846138b8b13ff16ad8e003a18d3; Login: sha256:2f8e57672fcd4f9a285d99355fae9f85fd7495768c090c07c3bbc2d84fc06617. Dockerfiles oficiais confirmam usuários zitadel e nextjs (Login UID1001). Pull e startup ainda não foram executados. API em h2c e UI separada em /ui/v2/login, atrás do mesmo host neutro. [Proxy oficial](https://zitadel.com/docs/self-hosting/manage/reverseproxy/reverse_proxy), [defaults da tag](https://github.com/zitadel/zitadel/blob/v4.19.5/cmd/defaults.yaml), [contrato CreateUser](https://github.com/zitadel/zitadel/blob/v4.19.5/proto/zitadel/user/v2/user_service.proto). O exemplo oficial na main foi usado como referência de arquitetura, não como versão executada.

O núcleo é **AGPL-3.0-only**, e apps/login tem exceção **MIT**, confirmado na [LICENSING.md da tag](https://github.com/zitadel/zitadel/blob/v4.19.5/LICENSING.md) e [licença do Login](https://github.com/zitadel/zitadel/blob/v4.19.5/apps/login/LICENSE). Plano: serviços separados e não modificados, sem incorporar fonte do núcleo ao Didasko. Interpretação técnica: integração por OIDC/HTTP não incorpora o núcleo por si só; isso não é dispensa geral das obrigações de licença. Modificação do núcleo acessível pela rede aciona oferta de fonte correspondente (seção 13); distribuição exige cumprir os avisos e as condições aplicáveis. MIT permite modificar/distribuir preservando licença/aviso. A avaliação jurídica/adopção permanece do ARQUITECT; não foi emitida conclusão de compatibilidade de todo o produto.

## Infraestrutura: revisão necessária antes da fase 2

Configuração: `experiments/zitadel/docker-compose.yml`; roteiro: README do mesmo diretório; segredos: `.env.example` só chaves vazias, gerador com caminho fixo e criação exclusiva 600 na VPS, nunca executado aqui.

- **a**: API e Login V2 em oidc.homolog.didasko.app.br; app em homolog.didasko.app.br/experimento. Três routers internos para dois destinos públicos (o provedor precisa separar API e Login). TLS websecure/le, aproveitando httpchallenge existente. Sem alterar configuração global do Traefik.
- **b**: papel/banco zitadel no Postgres existente. Não basta CREATE ROLE: conferir PUBLIC CONNECT e HBA; não revogar privilégio do banco da v0. Se necessário, autorização específica para regra HBA restrita a esse papel; sem isolamento comprovado, não subir.
- **c**: API 512 MiB + Login 256 MiB + FastAPI 128 MiB = 896 MiB / 939,52 MB de teto. E-04 usa memória observada do provedor, não teto. Registrar OOM/restarts. Confirmar também autorização de três gerações para E-05; se Ollama compartilhado não puder receber carga sem impacto na produção, não executar e registrar impossibilidade.
- **d**: gerar chave mestra de exatamente 32 caracteres, senha admin, senha DB e segredos de cookies na VPS; `.env` 600, dono didasko-deploy. PAT Login em volume nomeado próprio. API UID1000:1000 e Login UID1001:1001; diretório do volume UID1000/GID1001 modo 2750, PAT gerado depois pela API com leitura ao GID1001 em 0640. Volume novo exige preparação única de ownership, sem root permanente.
- **e**: autorização destrutiva separada para down -v do projeto e DROP do banco/papel criados neste ensaio. Conferir recursos e ownership antes; não apagar preexistentes. Clone/arquivo .env somente conforme autorização específica.

A revisão automática rejeitou a alternativa de processos permanentemente root. Configuração final preparada sem esse downgrade; inicialização única do volume e compatibilidade dos UIDs ainda dependem da revisão/ensaio. Nenhum SSH, criação de banco, geração de segredo, carga Ollama, deploy ou desmonte foi feito nesta fase.

## Recomendação e decisão pendente

**ADIAR a adoção, prosseguir somente com o experimento autorizado.** O cliente e os contratos testados não mostraram impedimento, mas E-01/E-02/E-03 reais e E-04/E-05 não têm evidência. Ausência de autorização/infra é **não consegui testar**, não **o provedor não serve**. Se o prazo terminar sem infra, este permanece o resultado, com recomendação adiar; não há base para adotar nem para descartar tecnicamente.

Depois do ensaio, preencher PASS/FAIL real, valores/horários/digests, falhas e atualizar a recomendação. Nada altera RF01 ou prepara produção automaticamente; somente o ARQUITECT decide, por ADR posterior.


## Entrega da fase 1 e CI

Commit `8d894aad283b2cb6a9639a63d6cc0d528a7f3d3f`; [PR #6 draft aberto](https://github.com/egarabini/gsi_ebd/pull/6). [CI do experimento](https://github.com/egarabini/gsi_ebd/actions/runs/39343258566): **40 testes passaram**, Python 3.12, e Compose validado. [CI de regressão](https://github.com/egarabini/gsi_ebd/actions/runs/39343258578): **269 testes passaram**. Ambos verdes no commit entregue. Diff limitado a experiments/ e um workflow isolado; gsi_ebd/, v1/ e deploy/ sem alterações. Worktree limpo.

Autorização a–e solicitada com configuração revisável; nenhuma resposta de aprovação recebida nesta etapa. Fases 2–3 não executadas. Não marcar E-01..E-05 reais como PASS.
