# Jornada — DEM-202610-011, fatia 2

## 2026-10-23 — Recriação a partir da develop `5c0bc3e`

O despacho (`dev/despacho-obras-fatia2.md` no DEM-005) e o plano de testes já estavam escritos no commit `146f374`. A branch do PR #5 (`feature/DEM-202610-011-fatia2-telas`) duplicava o esqueleto do marco 1 e **não** foi despachada.

Worktree isolado `.worktrees/DEM-011-fatia2`, branch `feature/DEM-202610-011-fatia2-obras` a partir de `origin/develop` (`5c0bc3e`). Portadas só as telas: routers admin/revisor/catálogo (`GET /obras` incluído), helpers em `views.py` sem trocar a assinatura do `render`, 3 chaves no `rbac.py`. CSRF e H-14 nas dependências do router, `exigir` (não `exige`) em cada rota.

Matriz de 15 células com as duas asserções; monkeypatch remove as 3 chaves e o permitido vira 403. ADR-020: só o Admin muda publicação/disponibilidade; o Revisor assina e move o editorial; a liberação exige os dois; N imutável e N+1; hash LF+NFC; `aberta | suspensa_para_novos`. Modo estudo com alunos fake no SQLite de teste e seed `v1/seed_homolog_estudo.py` que recusa produção e qualquer banco que não seja `didasko_v1`. O `gsi_ebd.data.seed` de produção não ganhou fake.

Suíte local: 130 v1 + 272 v0. Commit `3f9246e`. [CI verde](https://github.com/egarabini/gsi_ebd/actions/runs/40038005779). [PR #9](https://github.com/egarabini/gsi_ebd/pull/9). Sem `subir.sh`, sem merge, sem tocar no PR #5. EVAL cego pendente (máximo de 2 rodadas, ADR-018).

## 2026-10-19 — Leitura, Think e List

Briefing da fatia 2, design-fatia-2, design v7/plano v4, domínio e modelos lidos na ordem solicitada; depois design/plano da DEM-005, guardas e ADRs 002/003/008/020. A fatia 1 estava mergeada no `develop` em `7670aec`; a v1 não existia. Branch `feature/DEM-202610-011-fatia2-telas` criada desse ponto, com árvore limpa.

Lista informada: criar `v1/` com app/auth/db, routers admin/revisor/detalhe, templates/estáticos e testes; ampliar a matriz fonte única com as rotas específicas da v1; acrescentar suíte ao CI e documentar a operação local. O `/admin` da v0 permite Admin/Revisor; as rotas novas precisam separar Admin e Revisor, portanto foram acrescentadas chaves específicas sem mudar as antigas. `/obras/{id}` usa os papéis de leitura de catálogo existentes, Admin/Revisor. Nenhum campo novo no domínio foi necessário.

## 2026-10-19 — Etapa A

FastAPI/Jinja2 e middleware de sessão, engine exclusiva e create_all no boot. Sessão de servidor em memória de um processo, com identificador opaco no cookie assinado; CSRF por sessão, TTL, rotação/revogação, cookie HttpOnly/SameSite e Secure por padrão. Segredo obrigatório do ambiente. H-14 como dependência global que recusa rotas até a troca. Login, logout, perfil e bootstrap local explícito, sem senha fixa ou usuário automático no boot. Papéis consultados do banco a cada request, pela mesma matriz.

AuthService.can_access_role e UserStatusService.on_login_success reaproveitados; bcrypt compatível com os hashes existentes. O auth_service legado não tem verificador de senha: a verificação da v1 usa o mesmo bcrypt, sem importar os estados Reflex. Troca local exige senha atual, confirmação, nova senha e revogação das sessões, sem fluxo de email/reativação fora desta etapa.

## 2026-10-19 — Etapa B e testes

Admin: lista/importação/detalhe/histórico, liberação com ajustes, alteração, aceite/dispensa e cancelamento. Revisor: fila, detalhe/hash aberto, parecer/recusa, solicitação e posição. Detalhe publicado × cópia de trabalho. A rota `/reenviar` foi incluída para concretizar a operação já existente de recusa/reenvio, sem aumentar o domínio. Os POSTs usam flow.py e um commit por ação, com rollback em recusa, inclusive revertendo os ajustes anexados ao POST.

Domínio/modelos da fatia 1 intactos. Conteúdo digitado e adendos da base são adaptados aos campos existentes; sem ler corpus. Templates escapam conteúdo e usam StrictUndefined. HTMX oficial servido localmente com licença, sem dependência de CDN no runtime; melhorias progressivas mantêm formulários HTML comuns.

O primeiro ensaio de testes encontrou duas falhas: inventário baseado na lista plana de APIRoute não via os routers incluídos do FastAPI 0.150; a fila tinha join ambíguo entre Obra e ObraVersao. Corrigidos com inventário via schema interno e join explícito. Depois foram completados os testes das solicitações, posição, cancelamento, reenvio e bootstrap.

Suíte da v1, de `v1/`: 157 testes passaram. Regressão da raiz do app: 269 passaram. Três mutações em cópias fiéis: remover papel de uma rota causou 4 falhas na matriz; remover CSRF causou 14 falhas; remover H-14 causou 19 falhas. Cada baseline passou antes de mutar. Logs em `evidencias-fatia2-mutacao/`.

Verificação HTTP local por Uvicorn, banco e credenciais descartáveis: login 200, autenticação 303, H-14 403, troca 303, lista Admin 200 e HTMX 200. Servidor encerrado e ausência do processo verificada. A primeira limpeza automática do SQLite temporário encontrou lock no Windows após as respostas válidas; o teste HTTP em si passou, sem arquivo no repositório.

Próximos passos: consolidar evidência HTTP, revisar escopo, commit/PR e CI. Sem deploy, imagem, DNS ou homologação.

## 2026-10-19 — Revisão final, commit e PR

O ajuste para uma única sessão SQLModel por request identificou objeto ORM expirado durante a renderização de um 403 após rollback da dependência. Corrigido com resumo de identidade no request, sem segunda consulta/sessão no render. Suíte repetida e verde: 157 testes. As três provas foram repetidas sobre esse código e guardadas em `evidencias-fatia2-mutacao-final/`.

O smoke HTTP ganhou script reproduzível; banco temporário fica fora do repositório, sem limpeza automática que colida com locks do Windows. A confirmação de término usa o próprio processo iniciado, sem inferir pelo tipo de erro de conexão. Execução final exit 0 e JSON sem credenciais.

Apresentador passou a fornecer a ação do formulário, retirando decisão de estado do template; sete integrações/renders repetidos e verdes. Commit `3b5f56c8964b7efcb10de085617717038abd2930` enviado; PR https://github.com/egarabini/gsi_ebd/pull/5 aberto contra develop. Domínio/modelos da fatia 1 intactos. Documentação final e CI em acompanhamento.


CI confirmado no commit `3b5f56c8964b7efcb10de085617717038abd2930`: **269 testes de regressao + 157 testes da v1 passaram**, com a suite da v1 executada de `v1/`. [Execucao verde](https://github.com/egarabini/gsi_ebd/actions/runs/39339058255). PR #5 permanece aberto para develop; EVAL e aceite pendentes.
