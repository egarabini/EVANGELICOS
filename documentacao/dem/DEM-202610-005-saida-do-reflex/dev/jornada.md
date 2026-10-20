# Jornada — DEM-005, marco 1 (o esqueleto da v1)

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
