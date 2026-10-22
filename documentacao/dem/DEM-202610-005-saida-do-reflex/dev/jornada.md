# Jornada — DEM-005, marco 1 (o esqueleto da v1)

## 2026-10-22 — as 3 correções do ARQUITECT (hash no nome, ETag, fonte única)

Despacho relido em `dev/despacho-menu.md` (data 22/10). O porte visual já estava
na v1 (`0c8f0ef` + `a753222`); o `?v=` no query string **não** cumpria a correção 1
(hash no **nome**, CSS/WebP imutáveis só com URL versionada, HTML com ETag).

Think:
- a v1 (`feature/DEM-202610-005-landing`) é a única fonte; o `landing-prototipo/`
  já está CONGELADO (README) — não editei HTML/CSS/WebP de lá;
- o hash tem de sair do **conteúdo no build** (`python -m v1.landing_assets` no
  Dockerfile); nos testes, a subida do app versiona em dir temporário;
- o DEPLOY roda `subir.sh --v1`; este perfil não publica (ADR-016).

List (executado):
1. `v1/landing_assets.py` — `logo-88.<hash>.webp`, `landing.<hash>.css`;
2. `v1/landing.py` — HTML `no-cache` + ETag/304; assets com hash no nome
   recebem `max-age=31536000, immutable`; sem hash → 404;
3. `deploy/app-v1.Dockerfile` — `RUN python -m v1.landing_assets`;
4. testes: cabeçalhos, URL que muda com o conteúdo (inclusive `srcset`);
5. decisões já cobertas: yaml vazio, depoimentos só `ativo`, canais só se
   existirem, compose sem `DATABASE_URL` e sem rede `interna`.

Validação local: **60 testes da v1** + **269 da v0**. Commit `02eff4a` na
branch da landing, push para o origin. Não rodei `subir.sh`.

## 2026-10-21 — adendo despacho-menu: cache e testes do porte completo

Adendo lido em `dev/despacho-menu.md`. O porte dos quatro arquivos do
protótipo já estava no commit `0c8f0ef`; complementado no `a753222` com:

- hash SHA-256 do conteúdo em todas as URLs de assets dos templates;
- HTML e CSS com `Cache-Control: no-cache`;
- WebP com URL versionada válida: `public, max-age=31536000, immutable`;
  URL sem versão ou com hash antigo revalida, sem cache longo;
- testes parametrizados nas duas páginas para `srcset` 90w, topo 45 px,
  rodapé 34 px, imagem nova, versionamento, cabeçalhos e CSS com ETag/304.

Think/List: `landing.py`, dois templates e `tests/test_landing.py`;
risco de cache antigo mitigado por versão derivada do conteúdo; sem alteração
de YAML, rotas ou acesso ao banco. Adendo autoriza implementação e homologação.
Validação local: **58 testes da v1 + nove de páginas passaram**.
CI: https://github.com/egarabini/gsi_ebd/actions/runs/39698536189.

## 2026-10-21 — complemento do protótipo e atualização de assets

O ARQUITECT informou logo pequeno e hambúrguer à direita após o redeploy.
Diagnóstico: o head publicado continuava `74e3ee3`; o protótipo local tinha
alterações adicionais não commitadas (logo novo de 90 px, exibição em 45 px,
botão de 40 px e `justify-content: flex-start` no cabeçalho mobile).
O HTML/CSS consultado por HTTPS na homologação já tinha o botão antes da marca
e `order: -1`; cache no navegador é hipótese, não causa comprovada.

Porte restrito dessas alterações à v1, preservando os arquivos de autoria do
protótipo. URLs do CSS e logo receberam `?v=20261021-menu2` para nova busca
no navegador. Conteúdo, YAML, rotas e isolamento do banco preservados.
Commit `0c8f0ef`, enviado ao PR #8. Testes: 54 da v1 e nove do gate de páginas
passaram. Chrome em ambas as páginas, viewport 360 px: botão em x=22,4 px,
logo em x=78,4 px com largura 45 px, imagem carregada, sem overflow.
Capturas `menu-logo2-landing-360.png` e `menu-logo2-homenagens-360.png`.
CI disparado: https://github.com/egarabini/gsi_ebd/actions/runs/39698022094.

## 2026-10-21 — fix visual do menu mobile (marco 2L)

Despacho do ARQUITECT: portar o protótipo corrigido no commit `1135930`.
Think/List: alteração restrita aos dois templates e ao bloco CSS mobile;
riscos de ordem dos irmãos quebrar o checkbox e de regressão no desktop.
O despacho especificou e autorizou o porte.

- Input e label antes da marca em ambas as páginas, com URLs preservadas.
- CSS mobile copiado do protótipo: hambúrguer à esquerda, painel lateral
  `min(320px, 86vw)`, branco opaco, sombra e canto arredondado; hover no botão
  e painel, com checkbox como fallback.
- Conteúdo, YAML, rotas e regra sem banco preservados.
- Commit `74e3ee3`, enviado à branch `feature/DEM-202610-005-landing` do PR #8.
- Venv do projeto: **269 testes da base + 54 da v1 passaram**. Tentativas
  iniciais falharam por Python global sem dependências e permissão nos
  temporários; resolvido usando o venv e acesso aos temporários.
- Chrome local em ambas as páginas: 360 px, painel de 309,6 px, fundo branco,
  opacidade final 1, hover e checkbox funcionais, sem overflow horizontal.
  Em 1440 px o botão mobile fica oculto. Capturas:
  `capturas-landing/menu-fix-landing-360.png` e
  `capturas-landing/menu-fix-homenagens-360.png`.
- CI disparado por `workflow_dispatch`: o PR aponta para marco1, fora dos
  filtros automáticos develop/main.
  Run https://github.com/egarabini/gsi_ebd/actions/runs/39694772157:
  **success**, ambas as suítes verdes, duração do job 1m22s.
- Homologação pendente do DEPLOY: o atendimento foi atribuído ao DEVS, que
  não abre SSH operacional nem executa `subir.sh` pelo AGENTS.md do código.

## 2026-10-20 — Think

Branch `feature/DEM-202610-005-marco1`, criada de `develop` (`7670aec`), no worktree
`.worktrees/DEM-005-marco1`. O checkout da fatia 2 não foi alterado.

O marco entrega a interface `usuario_atual`, `exigir` e `ambiente_atual` com uma
implementação própria. O marco 1b troca a implementação sem trocar as telas. As rotas
deste marco são login, logout, troca de senha e a raiz. As casas `/admin`,
`/coordenador`, `/revisao` e `/aluno` ficam para os marcos seguintes.

## Assunções registradas

- `exigir` recebe a chave da matriz (`rota:/...`), não um `Role`. O texto do design diz
  `exigir(papel)`. A matriz admite um conjunto de papéis por rota, então o argumento que
  as telas usam é a chave. O 1b precisa conservar essa assinatura. Se o PLANNER quiser
  outro contrato, as telas mudam — isso está fora do que este marco pode decidir sozinho.
- A troca de senha do H-14 não chama `UserStatusService.on_password_changed`. Esse método
  suspende quem não é admin, e a rota continuaria fechada depois da troca. A implementação
  própria zera `must_change_password`, mantém o status `ativo`, revoga as sessões e renova
  a sessão corrente. O login continua chamando `on_login_success` e `on_login_failure`.
- Enquanto a casa do papel não existe na v1, o login autenticado cai em `/`. Quem está com
  a flag vai para `/perfil/alterar-senha`.
- O IP do hairpin não entra no git. O Compose versiona `extra_hosts` com
  `TRAEFIK_EDGE_IP`, lido na hora na rede de borda e gravado só no `.env` da VPS.
- Limites escolhidos: `app-v1` e `postgres-v1` com `mem_limit: 512m` e `cpus: 0.50`.
- O plano de testes ainda fala em 128 testes da v0. A suíte viva desta base tem 269. O
  documento do PLANNER não foi reescrito para caber no número.

## O que quebrou no caminho

- O FastAPI 0.150 tratava o `request` sem anotação de `sessao` como query obrigatória.
  Toda rota respondia 422. A correção foi anotar `request: Request`.
- Imagem nova, com Starlette 1.9, não traz `itsdangerous`. O `SessionMiddleware` precisa
  dele. Entrou em `v1/requirements.txt`.
- O primeiro `subir.sh --v1` entrou no projeto Compose `deploy` — o mesmo da produção —
  porque o arquivo mora em `deploy/` e não tinha nome de projeto. O aviso de órfãos
  listou os containers da v0. O comando não usou `--remove-orphans` e não reiniciou o
  Traefik. Em seguida os containers `didasko_v1_app` e `didasko_v1_postgres`, a rede
  `deploy_interna` e o volume `deploy_didasko_v1_data` foram removidos por nome, e a v1
  subiu de novo no projeto `homolog-v1`. O `down` do projeto `deploy` não foi executado.

## Validação local

- `v1/`: 37 testes passaram (FastAPI 0.150 no venv e FastAPI 0.153 dentro da imagem).
- Raiz do worktree: 269 testes da v0 passaram.
- `docker build -f deploy/app-v1.Dockerfile` concluiu. Com `--memory 512m`, `GET /login`
  respondeu 200 e o processo ficou em cerca de 76 MiB.

## Homologação

Diretório na VPS: `/home/didasko-deploy/homolog-v1`. Não é `/home/eduardo/didasko` nem
`~/didasko`. O `didasko-deploy-entry` não foi usado: ele faz checkout de tag em `~/didasko`
e dump do banco da v0.

- `https://homolog.didasko.app.br/login` respondeu 200.
- Certificado: `C = US, O = Let's Encrypt, CN = YR2`, `CN = homolog.didasko.app.br`.
  Já existia antes deste marco (válido desde 2026-10-20 09:40 GMT). O roteador da v1
  reutilizou esse certificado. Não houve segundo obtain e o Traefik não foi reiniciado
  (`StartedAt` 2026-10-18T17:27:43Z antes e depois).
- `alembic_version` = `0001_baseline`. O seed criou 5 usuários.
- `https://didasko.app.br/` continuou 200. `https://homolog.didasko.app.br/experimento`
  continuou 401.
- Projeto Compose do container da v1: `homolog-v1`.

## Fora deste marco

Marco 1b, telas dos marcos 2–6, pin do Traefik, Ollama, desmonte da homologação.

## 2026-10-21 — marco 2L (a landing)

Branch `feature/DEM-202610-005-landing` a partir do marco 1 (`3d28934`), worktree
`.worktrees/DEM-005-landing`. O despacho do ARQUITECT autoriza a execução; a fatia 2
e o checkout `feature/DEM-202610-011-fatia2-telas` nao foram alterados.

### Think

- A landing e um **servico separado** (`v1.landing:create_app`): o EVAL exige o
  conteiner **sem** `DATABASE_URL` e **sem** rede para o banco. Colocar `/` na app-v1
  quebraria essa prova, porque a app-v1 precisa do Postgres.
- A base e o marco 1 (o compose da homologacao vive la, PR #7 ainda aberto). `develop`
  ainda nao tem a v1. Assuncao registrada: a branch da landing sai do marco 1.
- O `GET /` autenticado da app-v1 deixa de ser alcancavel pelo Traefik — a raiz publica
  passa a ser a landing. O `/login` continua na app-v1. Nao mexo no `destino()`.
- O `landing.yaml` entra vazio. Depoimentos so com `ativo: true`. Contato so com
  `email`/`whatsapp`. Homenagens: lista vazia, sem cartoes de exemplo.
- O porte e o HTML/CSS do prototipo; o Jinja so entra nos `{% if %}`.
- Publicar na VPS e do DEPLOY (ADR-016). Este marco entrega o codigo, os testes, as
  capturas locais e o compose; o `subir.sh --v1` fica pronto para o executor.

### List

1. `v1/landing.py` + `v1/landing_conteudo.py` + `v1/landing.yaml` — app sem banco.
2. Templates Jinja2 (porte do `index.html` e do `homenagens.html`) + CSS + WebP.
3. Servico `landing` no `docker-compose.v1-homolog.yml` (so a rede `borda`) e o
   `subir.sh --v1` (recria a landing; confere `/` 200 e ausencia de `DATABASE_URL`).
4. Testes do render (yaml vazio e preenchido), do compose e do orcamento.
5. Suite da v1 + regressao 269; capturas 360/768/1024/1440 e o LCP.

### Execucao

- App em `v1.landing:create_app`. Recusa `DATABASE_URL`. Le `v1/landing.yaml`.
- Porte do prototipo nos templates `v1/templates/landing/` e em `v1/static/landing/`.
- Compose: servico `landing` so na rede `borda`, prioridade Traefik 100, sem Postgres.
- `subir.sh --v1` recria a landing e confere `/`, `/homenagens` e `/login` em 200.
- Testes: 54 na v1 (inclui yaml vazio e preenchido) e 269 na v0.
- Capturas em `dev/capturas-landing/`. LCP 1064 ms (hero logo, 4G simulado). Peso 2x ~92 KB.
- Nao publiquei na VPS (ADR-016). A raiz da homologacao continua 401 ate o DEPLOY subir a branch.

## 2026-10-22 — fix do parecer do EVAL (marco 2L): contraste e placeholder

Despacho do ARQUITECT com o parecer do EVAL cego (`eval/jornada-landing.md`): **FAIL**,
dois bloqueios. Worktree `.worktrees/DEM-005-landing`, sobre o `02eff4a`.

### Think

- A "nota do contato" aparece em dois pontos do despacho (o contraste dela e a
  decisao de remove-la). Removendo o placeholder inteiro (`{% else %}` + o CSS
  `.contato__nota`), o problema de contraste desaparece por construcao — nao fiz
  as duas coisas em separado.
- As capturas 768/1024/1440 no head, a captura do painel aberto e o LCP no head
  exigem navegador real; o perfil do projeto diz que **nao ha navegador
  automatizado disponivel** (VISION e o Eduardo). Nao fabriquei essas provas.
- Esta estacao (Windows, Python 3.14) nao tem o venv do projeto (Python 3.12 +
  Reflex + sqlalchemy completos); o `conftest.py` da v1 importa `gsi_ebd.models`
  e `v1.main`, que arrastam a pilha inteira. Verifiquei com um script direto
  contra `v1.landing` (sem o conftest) e deixei a suite oficial para o CI, que
  ja roda com o ambiente certo (confirmado no `02eff4a`, run `39771652866`).

### List (aprovada pelo ARQUITECT antes do code)

1. `v1/static/landing/landing.css` — var `--roxo-escuro`; `.botao--primario` com
   as duas pontas escuras; remove `.contato__nota`; checkbox do menu focavel
   (sr-only) so no breakpoint mobile, com foco visivel no hamburguer.
2. `v1/templates/landing/index.html` e `homenagens.html` — remove o `{% else %}`
   do placeholder.
3. `v1/landing.py` — `mimetypes.add_type("image/webp", ".webp")`.
4. `v1/tests/test_landing.py` — remove o assert do placeholder; cobre o
   `content-type: image/webp` no teste de cache existente.

### Execucao

- Commit `a703389` (`fix(landing): escurece o botao primario e remove o
  placeholder de contato`), push, CI disparado via `workflow_dispatch`
  (procedimento ja usado no `02eff4a`): run `39835747275`, **success**.
- DEPLOY (ADR-016): `subir.sh --v1` no clone `/home/didasko-deploy/homolog-v1`,
  fast-forward `02eff4a..a703389`. `/`, `/homenagens`, `/login` 200; Traefik e
  app de producao com os mesmos horarios de inicio (nao reiniciados).
- Verificado em homologacao: 0 ocorrencias do placeholder; CSS novo
  (`landing.e8784ecbc0f4a9c1.css`) com `linear-gradient(120deg,
  var(--roxo-escuro), var(--roxo))`; `Content-Type: image/webp` no logo.
- **Pendente**: as capturas 768/1024/1440 e do painel aberto no head, e a
  remedicao do LCP — dependem de navegador (o ARQUITECT ou um proximo EVAL).
  O teclado do menu (foco no checkbox + Espaco) nao foi confirmado em browser
  real, so pela leitura do CSS/HTML.
