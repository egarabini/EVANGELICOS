# Design — DEM-202610-005 / a v1 na base nova

> Nível 3. Este design cobre os **marcos 1-2** com o detalhe necessário para começar; os marcos 3-6
> ganham o detalhe quando o anterior estiver verde (a regra do processo ágil).

## 1. A estrutura

```
ESTUDOS_BIBLICOS/GSI_EBD/
  gsi_ebd/            # o DOMÍNIO (reaproveitado): models/, services/, scripts/, ai/
  v1/                 # A APLICAÇÃO NOVA
    main.py           # o FastAPI: os routers, o middleware, o static
    auth.py           # a sessão de servidor, o CSRF, o login/logout, a dependência de papel
    routers/          # login, admin, revisor, coordenador, instrutor, aluno
    templates/        # Jinja2 (o layout + as páginas)
    static/           # o HTMX, o Alpine, o CSS (sem Node/TS na app)
    tests/            # a suíte da v1 (a matriz, os rendes, os fluxos)
  deploy/             # o compose + o subir (a v1 ganha o serviço/imagem)
```

**A v0 (o Reflex) fica intocada** enquanto a v1 é construída. O `gsi_ebd/` é importado pela v1
(a sessão é a única troca: `rx.session` → a sessão do `sqlmodel`).

## 2. O marco 1 (o esqueleto)

- **`auth.py`**: a sessão de servidor (o `SessionMiddleware` com o secret do `.env`; o cookie
  `httponly`, `secure`, `samesite=lax`); o login (o `services/auth_service` reaproveitado); o
  logout; a **dependência única** `usuario_atual(request) -> User` e o `exige(papel)`.
- **A matriz papel × rota**: a mesma da DEM-002 (`gsi_ebd/utils/rbac.py`), aplicada como
  **dependências** do FastAPI — o teste que renderiza todas as rotas por papel (o H-04/H-05).
- **O CSRF**: o token por sessão, o campo oculto nos formulários, o header no HTMX.
- **A imagem e o compose**: um serviço `app` da v1 (o mesmo `deploy/docker-compose.producao.yml`,
  um serviço novo ou o mesmo trocando a imagem) — decide-se no marco 1, com o teste local.
- **A homologação**: o subdomínio (o Traefik com um `Host` novo; o DNS e o certificado são do
  ARQUITECT — avisar quando o marco 1 estiver pronto, com o nome do subdomínio e a porta).

## 3. O marco 2 (o fluxo admin/revisor/obras)

- As telas: a lista das obras (os estados), a importação (a fonte do inventário), o parecer do
  revisor, a liberação do admin, a alteração (a nova versão), o "contestar".
- As ações chamam o **`gsi_ebd/services/flow.py`** (a fatia 1 da DEM-011) — **nenhuma transição no
  template**.
- O **`exec -e SEED_PASSWORD`** entra no `deploy/subir.sh` (a A-2); o seed é rodado sob demanda,
  não no deploy.

## 4. O deploy (a RF07)

- A imagem da v1: `deploy/app-v1.Dockerfile` (ou o mesmo Dockerfile com um entrypoint novo).
- O pipeline: a tag dispara; o entry script da v1 faz o backup → o checkout → o compose da v1 →
  o HTTP. **O mesmo `restrict,command`** e a mesma cadeia de chaves (ADR-015/016).
- O **`exec -e SEED_PASSWORD`** no `subir.sh` (o valor do ambiente do script; nunca da linha).
- **Não** gravar a variável no `environment:` do Compose.

## 5. A virada (o marco 6) e o retorno

- O Traefik: o host principal → o serviço da v1; a v0 de pé (o serviço antigo) para o retorno.
- **O período estável**: um tempo com a v1 no subdomínio, com o EVAL e o ARQUITECT usando (o plano
  de virada define: recomendo 2 semanas ou o "estudo completo por 3 papéis").
- **Os dados reais** só entram **depois** do período estável — e a partir daí "voltar à v0" **perde
  dados**: a correção é **para a frente**. O plano de virada escreve isso e o teste do retorno é
  feito **antes**.

## 6. Riscos

- **A migração de dados**: os modelos do `gsi_ebd/` (o `create_all`) — a v1 com o mesmo banco (as
  tabelas novas do `ObraVersao`/o `Adendo.ambiente_id`; sem alembic, o `create_all` não altera a
  tabela existente — o design da migração é o marco 1/2, com o `pg_dump` antes).
- **A sessão**: a do Reflex e a da v1 são independentes (a RF01) — não há ponte.
- **As telas**: a matriz de rotas precisa cobrir **todas** as rotas da v1 (o teste que renderiza).
- **O tempo**: a v1 é o maior item do projeto; os marcos dão resultado visível a cada um.

## 7. O que o EVAL julga em cada marco

O plano de testes **por marco** (o `plano-testes.md` da DEM-005, escrito antes do marco 1 e
acrescentado por marco): a matriz, os rendes, os fluxos, as dívidas (H-14/H-15), o deploy e a
virada.
