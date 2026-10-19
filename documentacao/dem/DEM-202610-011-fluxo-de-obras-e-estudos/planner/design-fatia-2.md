# Design — DEM-202610-011, **fatia 2: as telas do fluxo (na v1)**

> Nível 3 (as telas de segurança: a auth, a matriz, a liberação). **Depende da fatia 1** (o domínio,
> mergeado em `7670aec`) e da **DEM-005** (a v1: o FastAPI + Jinja2 + HTMX; o seu design tem a
> estrutura e o marco 1). Esta fatia faz a **primeira tela da v1** — e a fronteira com o marco 1 da
> DEM-005 é declarada na §1.

## 1. O que a fatia 2 é (e o que não é)

| Etapa | O quê | O resultado visível |
|---|---|---|
| **A — o esqueleto mínimo da v1** | a app FastAPI, o Jinja2/HTMX, a **auth** (a sessão, o CSRF, a matriz), o `didasko_v1` com o `create_all` dos modelos, o layout e o login | **o login funcionando local**, com a matriz bloqueando |
| **B — as telas do fluxo** | o admin (as obras, a importação, a liberação, a alteração, a solicitação, o cancelamento) e o revisor (a fila, o parecer, a recusa, a solicitação, a posição) | **o fluxo completo na tela**, chamando o `flow.py` da fatia 1 |

**Não é**: as telas do instrutor e do aluno (os marcos 4/5 da DEM-005); a imagem/o pipeline/o
endereço de homologação (o resto do marco 1, a DEM-005); o deploy (a ADR-016); a fatia 3 (o
`desvincular`, o CRUD do adendo do ambiente, o `planejar`).

## 2. A arquitetura (na v1)

```
ESTUDOS_BIBLICOS/GSI_EBD/v1/
  main.py          # o FastAPI: o app, o middleware, o static, o include dos routers
  auth.py          # a sessão (SessionMiddleware), o CSRF, o login/logout, o `usuario_atual`, o `exige(papel)`
  db.py            # a engine do SQLModel (o DATABASE_URL; o create_all no boot)
  routers/         # login, admin_obras, revisor_obras, obra_detalhe
  templates/       # base.html, login.html, perfil_senha.html, admin/..., revisor/..., obra.html
  static/          # htmx.min.js, alpine, o css
  tests/
```

- **O domínio é reaproveitado**: os routers chamam o `gsi_ebd/services/flow.py` (a fatia 1) e usam
  os `gsi_ebd/models/` — **nenhuma regra no template**.
- **A matriz**: o `gsi_ebd/utils/rbac.py` (a DEM-002) — a **fonte única**; a v1 a aplica como as
  dependências do FastAPI (`Depends(exige("rota:/admin"))`). O teste que renderiza **todas** as rotas
  por papel (o H-04/H-05).
- **A sessão do SQLModel**: uma factory por request; o banco `didasko_v1` (o `.env` local; o
  `create_all` no boot — o baseline de Alembic é do marco 1 da DEM-005).

## 3. As rotas

| Rota | Papel | O quê |
|---|---|---|
| `GET /login`, `POST /login`, `POST /logout` | público / os 4 | a auth (o `auth_service` da fatia 1) |
| `GET/POST /perfil/alterar-senha` | os 4 | a troca (a **D-11**: o bloqueio até a troca — o H-14) |
| `GET /admin/obras` | admin | a lista: o estado, a disponibilidade, a versão liberada |
| `GET /admin/obras/nova`, `POST /admin/obras` | admin | a importação (a fonte do inventário; o gate `nao_entra`) |
| `GET /admin/obras/{id}` | admin | o detalhe + o histórico (os eventos) + as ações |
| `POST /admin/obras/{id}/liberar` | admin | a liberação (o gate `depende`) |
| `POST /admin/obras/{id}/alterar` | admin | a nova versão + a `suspensa_para_novos` |
| `POST /admin/obras/{id}/aceitar` · `/dispensar` | admin | a solicitação (a dispensa com o motivo) |
| `POST /admin/obras/{id}/cancelar` | admin | o cancelamento do ciclo |
| `GET /revisor/obras` | revisor | a fila (as `em_revisao` e as `aguardando_admin`) |
| `GET /revisor/obras/{id}` | revisor | o conteúdo + o parecer + o `hash_esperado` |
| `POST /revisor/obras/{id}/revisar` · `/recusar` · `/solicitar` · `/posicionar` | revisor | as ações do revisor |
| `GET /obras/{id}` | os papéis autorizados | o detalhe (o publicado × o em revisão) |

## 4. A segurança das telas

- **O CSRF** em todo POST (o campo oculto + o header do HTMX); **o cookie** (httponly, secure em
  produção, samesite).
- **O `hash_esperado`**: a tela do revisor carrega o hash do conteúdo que ele abriu; o POST o
  devolve; o conteúdo mudou desde então → a **recusa** (o F-06 da fatia 1) — a tela mostra o erro,
  não um sucesso falso.
- **O H-14 (a D-11)**: com a `must_change_password`, só `/perfil/alterar-senha` e `/logout`; as
  demais rotas **recusam** (uma dependência/middleware, não um redirect).
- **A autorização é do servidor**: os botões condicionados ao papel são conveniência; a regra é a
  dependência.
- **O `StrictUndefined`** no Jinja (o bug de produção do Reflex não se repete).

## 5. Os testes (o plano)

- **A matriz**: cada rota × cada papel → o 200/403 (o teste parametrizado; o H-04/H-05).
- **O CSRF**: o POST sem o token → o 403.
- **O H-14**: o usuário com a flag → só a troca e o logout.
- **O render**: todas as rotas renderizam (o `StrictUndefined`).
- **A integração**: as ações das telas chamam o `flow.py` e o estado muda (o F-06/F-12 da fatia 1
  pela tela).
- **A mutação**: remover a dependência de papel de uma rota → a matriz falha; remover o CSRF → o
  teste falha.

## 6. Riscos

- **A v1 é nova**: a etapa A entrega o mínimo local; a imagem/o pipeline/a homologação = o marco 1
  da DEM-005 (o **DNS é do ARQUITECT**).
- **O volume**: a etapa B pode ser entregue em dois commits (o admin; o revisor) — a tela do admin
  primeiro (é ela que cria o conteúdo).
- **O `didasko_v1`**: o `create_all` no boot (o baseline de Alembic = o marco 1); o banco local no
  `.env` (sem segredo no repositório).
- **O tempo**: a fatia 2 é maior que a 1; o design acima é o **contrato**, e o escopo não cresce.

## 7. O DoD

- o login local com a matriz (a etapa A);
- as telas do admin e do revisor com o fluxo completo (a etapa B), chamando o `flow.py`;
- a suíte da v1 verde + a matriz + o CSRF + o H-14 + o render; a mutação;
- o CI verde; o `README` da DEM atualizado.
