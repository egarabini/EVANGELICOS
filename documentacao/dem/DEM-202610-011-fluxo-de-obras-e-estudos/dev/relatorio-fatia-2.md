# DEM-202610-011 — relatório da fatia 2 (etapas A e B)

- **Branch:** `feature/DEM-202610-011-fatia2-telas`, criada de `develop` em `7670aec` (fatia 1 mergeada).
- **Commit:** `3b5f56c8964b7efcb10de085617717038abd2930`.
- **PR:** https://github.com/egarabini/gsi_ebd/pull/5 → `develop`, sem merge.
- **Alvo:** briefing/design da fatia 2, design v7/plano v4 e ADRs 002/003/008/020; estrutura mínima da DEM-005.
- **Escopo do código:** nova pasta `v1/`, três chaves adicionais de rota em `gsi_ebd/utils/rbac.py` e passo da suíte v1 em `.github/workflows/ci.yml`. **flow.py e models da fatia 1 não foram alterados; nenhum campo novo foi necessário.**

## A — esqueleto e login local

App FastAPI por factory; SQLModel com uma sessão por request; create_all no boot; templates Jinja2 com StrictUndefined/autoescape; layout, login, logout e troca obrigatória. O engine vem de DATABASE_URL e rejeita o banco PostgreSQL com nome diferente de `didasko_v1`; SQLite local usa `didasko_v1.db`. Não foi aberto ou alterado o banco da v0.

Cookie `didasko_v1` assinado contém apenas SID opaco; identidade, CSRF e expiração ficam no servidor, em memória de **um processo**. HttpOnly/SameSite=Lax, Secure por padrão (false somente no HTTP local). SESSION_SECRET obrigatório, sem fallback, mínimo 32 caracteres. Login/troca rotacionam a sessão; logout revoga o SID; troca revoga as outras sessões do usuário. TTL de uma hora.

Papel/status/flag são consultados no banco a cada request. AuthService verifica a permissão contra a matriz fonte única; UserStatusService atualiza os metadados de sucesso do login. O auth_service legado não tem verificação de credenciais: a v1 verifica o mesmo bcrypt, sem importar estados Reflex. Troca exige senha atual, confirmação, não reutilização e nova senha válida; limpa a flag, sem fluxo de email/reativação nesta etapa local.

H-14 é dependência global: com a flag, recusa 403 em todas as rotas da app exceto perfil/logout. CSRF global em **todo POST**, inclusive login/logout: campo oculto ou header X-CSRF-Token do HTMX. O layout recebe um resumo de identidade, sem manter objeto ORM expirável após rollback de dependência.

`v1/criar_usuario.py` é bootstrap explícito local, com getpass: não tem senha fixa, não redefine conta existente, não roda no boot e marca troca obrigatória. Instruções completas em `v1/README.md` e configuração sem valores secretos em `v1/.env.example`.

## B — telas e fluxo

Admin: lista com estado/disponibilidade/publicação, importação com ID de fonte, detalhe publicado × trabalho, parecer/ajustes, histórico/assinaturas/diferenças, liberação com edição da base, nova versão, aceitar/dispensar solicitação e cancelar ciclo.

Revisor: fila em revisão/aguardando Admin, publicadas para solicitação, detalhe com hash_esperado, parecer/recusa, solicitação e posição. POST com hash desatualizado mostra erro 409, sem sucesso falso. Motivo de dispensa aparece na trilha ao Revisor.

Os handlers autorizados chamam flow.py; cada ação confirma **um commit**. Em recusa há rollback, incluindo conteúdo de trabalho anexado ao POST. A adaptação de formulários escreve apenas capítulos/adendos da base nos campos existentes, sem decidir transição. A seleção do formulário de liberação/reenvio fica no apresentador; template apenas exibe a ação. O conteúdo Markdown é escapado e mostrado como texto de revisão, sem executar HTML.

Além das rotas expressas na §3, foi incluída **POST /admin/obras/{id}/reenviar**, necessária para operar a transição já existente após recusa. Não acrescenta campo, operação ou regra ao domínio. A importação anexa a base depois de criar a obra, preservando o contrato existente (hash de importação vazio até o parecer, já registrado pelo EVAL da fatia 1).

A matriz conserva todas as permissões da v0 e acrescenta:

| Chave da fonte única | Papéis |
|---|---|
| rota:/admin/obras | Admin |
| rota:/revisor/obras | Revisor |
| rota:/obras | Admin/Revisor, os papéis de leitura do catálogo |

Perfil/logout são comuns aos cinco papéis. Coordenador/instrutor/aluno não ganham telas nesta fatia. Negação de papel é 403 no servidor; não depende de ocultar botão.

## Testes

| Suíte | Diretório | Resultado local |
|---|---|---|
| `..\.venv\Scripts\python.exe -m pytest tests -q --basetemp=C:/Windows/Temp/dem011-fatia2-v1-final2` | `v1/` | **157 passaram**, 329 avisos de depreciação (serviço legado utcnow e TestClient/Starlette) |
| `.venv/Scripts/python.exe -m pytest tests -q --basetemp=C:/Windows/Temp/dem011-fatia2-regressao` | raiz do app | **269 passaram**, 18 avisos existentes |
| Integração/render após simplificar o apresentador | `v1/` | **7 passaram** |

A matriz cobre as **20 rotas protegidas × cinco papéis (100 casos)**; inventário via schema interno cobre também GET/POST login. GET autorizado renderiza 200; papel negado recebe 403. POST autorizado pode retornar 303 ou recusa do domínio 409; os testes de integração verificam as transições positivas, não tratam 409 como sucesso de negócio.

Mais cobertura: 14 POSTs sem CSRF, token de outra sessão, cookie adulterado/revogado, header HTMX, rotação, senha errada/status inativo, cookie Secure/HttpOnly/SameSite, StrictUndefined, HTML escapado, bootstrap seguro, banco legado recusado, H-14 em todas as rotas e troca real para os cinco papéis. Integração: importação/parecer/liberação com ajustes/nova versão, hash obsoleto, gates de licença/rollback, solicitação/aceite/dispensa com motivo, posição, cancelamento e recusa/reenvio.

Sem corpus ou credenciais reais nos testes. Python local 3.14.6; CI existente roda Python 3.12. `git diff --check` e ASCII no Python/JS próprio passaram. Texto de interface/documentação em pt-BR.

## Provas de mutação (implementação final)

Reprodução: de `v1/`, `python tools/mutacoes.py --evidencias <pasta-nova>`. Cópias fiéis fora do app; em cada cópia, o mesmo seletor roda antes/depois. Não modifica original. Evidências finais: [`evidencias-fatia2-mutacao-final/`](evidencias-fatia2-mutacao-final/).

| Remoção | Baseline | Mutante |
|---|---|---|
| Dependência de papel de GET /admin/obras, mantendo login obrigatório | 100 passaram | **4 falharam** |
| CSRF global | 14 passaram | **14 falharam** |
| H-14 global | 22 passaram | **19 falharam**, três exceções previstas permaneceram permitidas |

Todos os baselines exit 0, mutantes exit 1 por comportamento, sem erro de coleta. A pasta sem sufixo `-final` preserva o ensaio anterior ao ajuste de contexto do render; a evidência final é a indicada acima.

## HTTP local real

`v1/tools/smoke_local.py` iniciou Uvicorn em loopback/porta efêmera, com SQLite e credenciais geradas só para essa execução: login GET **200**, autenticação **303**, acesso bloqueado pelo H-14 **403**, troca **303**, Admin **200**, HTMX **200**. Processo encerrado após a verificação. Resultado: [`evidencia-fatia2-http-local.json`](evidencia-fatia2-http-local.json). Nenhuma senha/cookie/secret foi gravada na evidência.

## Integração, requisitos e limites

- Sessões em memória exigem **um processo** e são perdidas ao reiniciar. Armazenamento compartilhado e operação com múltiplos workers pertencem à implantação da v1; não foi criada tabela de sessão no domínio.
- SQLite é o ambiente local/teste. Provisão e integração real com PostgreSQL didasko_v1, baseline de schema e homologação são da DEM-005; esta fatia valida a configuração e o create_all com banco descartável, sem usar credenciais de infraestrutura.
- `CAMINHO_INVENTARIO` precisa estar acessível na v1; ambos os gates continuam no domínio, com leitura fresca. Corpus não foi lido, copiado ou incluído.
- HTMX **2.0.4**, licença incluída e servido localmente; SHA-256 do asset: `e209dda5c8235479f3166defc7750e1dbcd5a5c1808b7792fc2e6733768fb447`. Sem CDN em runtime, Node ou TS. Alpine não foi adicionado porque os formulários só exigem melhoria progressiva leve.
- Sem deploy, imagem, DNS, homologação, Alembic, segredo no repositório, telas instrutor/aluno ou fatia 3 (desvincular/adendo do ambiente/planejar). Não foi executado fluxo de email.
- Avisos/transições históricas e limites do domínio, como cancelamento lógico/cópia de trabalho, continuam conforme a fatia 1; sem correções adjacentes.

CI foi ampliado apenas para instalar dependências e executar a suíte da v1 no seu próprio diretório, preservando a regressão da raiz. Relatório/jornada/evidências ficam no repositório pai, fora do Git do app. EVAL cego e aceite permanecem posteriores ao PR.


CI confirmado no commit `3b5f56c8964b7efcb10de085617717038abd2930`: **269 testes de regressao + 157 testes da v1 passaram**, com a suite da v1 executada de `v1/`. [Execucao verde](https://github.com/egarabini/gsi_ebd/actions/runs/39339058255). PR #5 permanece aberto para develop; EVAL e aceite pendentes.
