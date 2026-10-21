# Jornada do EVAL cego — DEM-005, marco 1 (o PR #7, head `59abcf8`)

> O EVAL julgou sem confiar no relatório. O veredito: **FAIL** — dois bloqueios e sete não
> bloqueantes. O que segue é o parecer, reproduzido para o DEVS e para o ARQUITECT.

## O veredito: **FAIL**

### Os dois bloqueios

**1. A matriz não é provada (a segurança).** O guarda **real** funciona: numa sonda com uma rota de
teste `Depends(exigir("rota:/admin"))`, o **ALUNO** recebe **403** e o **ADMIN 200**. Mas, no
**mutante em que o `exigir` deixa de chamar o `pode`**, a suíte da v1 fica **38/38 verde**. A
mutação "matriz ignorada" **sobrevive**. O inventário pega a remoção da dependência (1 falha), mas
não pega o guarda de decisão arrancado. O template do EVAL: **"o teste que passa com o guarda
arrancado é vacuoso"**.

**Falta**: um teste negativo (a rota de teste ou real com `exigir("rota:/admin")`, o ALUNO → 403, o
ADMIN → 200) e a mutação (o `exigir` sem o `pode`) **tendo** de falhar.

**2. O CSRF do HTMX quebrado (o latente).** O `base.html` carrega o `app.js` no `<head>` (linha 10)
e o `app.js` faz `document.body.addEventListener` (linha 2). O `<body>` **ainda não existe**, então o
listener de `htmx:configRequest` **nunca é registrado** e o header `X-CSRF-Token` **nunca é
anexado**. Não há `hx-` no marco 1 (por isso o login funciona), mas o design §2 pede "o header no
HTMX".

**Falta**: o `defer` (ou o `DOMContentLoaded`) e a verificação do header.

### O que **PASS** (com a evidência reobtida)

- **RF01** (sessão/CSRF/cookie/formulários): 38 testes da v1; live o `/login` 200, o `Set-Cookie`
  com `httponly`/`samesite=lax`/`secure`/`Max-Age=3600`; o POST sem token → 403; o token inválido →
  403; o token válido + o usuário inexistente → 401; o `GET /` 401; o `/static/app.css` 200.
- **H-14** (RF06/D-11): 10 testes; a mutação desliga o `verificar_h14` → 5 falham.
- **RF10**: o Postgres próprio (`didasko_v1_postgres`, o volume `homolog-v1_didasko_v1_data`, a rede
  só interna); o `current_database()`/o `current_user` → `didasko_v1|didasko_v1`; o
  `alembic_version=0001_baseline`; os 5 do seed (`must_change_password=t`, ativos); o
  `didasko_postgres` **sem** papel/DB `didasko_v1`.
- **RF13**: o `extra_hosts` versionado; o live `172.18.0.4` = o `didasko_traefik`.
- **RF14**: o cert LE (YR2; 20/10 → 18/01); o Traefik `StartedAt` 2026-10-18T17:27:43Z (sem
  restart); a versão 3.7.14; o aviso: `traefik:latest` sem digest pin.
- **RF07/RF08**: o Dockerfile `python:3.12-slim`; o compose `name: homolog-v1`, o `--env-file
  .env.v1-homolog`, o `--force-recreate --no-deps app-v1`, o `exec -T -e SEED_PASSWORD`, o
  fail-fast; o live `homolog-v1-app-v1`.
- **As condições a–g: PASS** — (a) o cert sem restart; (b) nada no `didasko_postgres`; (c) os
  limites (512 MiB/0,50 CPU); (d) o `.env.v1-homolog` 600, a senha de 30, o `SESSION_SECRET` de 43,
  o `SEED_PASSWORD` de 24, sem valor impresso; (e) o `exec -T -e` no script e ausente do Compose;
  (f) os 5 da v0 inalterados; (g) sem `down`.
- **O quase-acidente**: os `StartedAt` **iguais** à tabela do relatório; o `Created` confirma que
  não houve recriação em 20/10.
- **O CI/PR**: o run `39581630194` `success`, o `head_sha=59abcf8`; o PR aberto, o base `7670aec`,
  os 4 commits, o `mergeable_state=clean`, sem merge.
- **Os testes**: a v1 **38** (não 37 — o `59abcf8` acrescentou o `test_rf07_fail_fast`); a v0 **269**.
  A primeira v0 deu 150 + 119 `PermissionError` (o `tmp_path` com o `mkdir 0700` no sandbox) — ele
  rodou com o `TMP` fora e um plugin local, **sem tocar no código**.
- **As mutações**: o CSRF 1 falha/37 passes; o H-14 5 falhas/33 passes; a dependência removida de
  `/` 1 falha/16 passes; **a matriz ignorada 38/38 passes (o teste vacuoso)**.

### O que ele **não** testou

O login/H-14 **live** (sem credencial; evitar o write no `last_login_at`); a emissão do cert (não
induziu; o Traefik intocado); o build da imagem no head (o live em `7524ac7`; o app é idêntico); o
Python 3.12 local (o CI 3.12 verde); os logs do CI (a API 403); a aleatoriedade da senha; o
`alembic upgrade` do zero (o app usa o `create_all`+`stamp`); o HTMX em browser (a ordem do HTML
prova o defeito).

### O que falta para passar

1. **Um teste negativo da matriz** + a mutação falhando;
2. **O `app.js`** (o `defer`/o `DOMContentLoaded`) + a verificação do header;
3. **Os não bloqueantes**: o 37 → 38 no relatório/PR; o redeploy do head `59abcf8` se a homologação
   tiver de ser exatamente o head; o **pin do Traefik** (decisão do ARQUITECT); o `v1/.env.example`
   com o `didasko_v1`; o `deploy/.env.producao.example` com o `SEED_PASSWORD`; e uma chave
   **`rota:/logout` própria** (hoje o `/logout` reusa a `rota:/perfil/alterar-senha`).

## O que mudou no processo

O EVAL **não** aceitou o relatório: ele reobteve a evidência (a VPS em leitura, os testes, as
mutações) e **pegou os dois defeitos** que o relatório não viu. O primeiro — o teste que passa com o
guarda arrancado — é a **prova de mutação fazendo o seu trabalho**: o teste do marco 1 testava a
**fiação** (a dependência existe), não a **decisão** (o guarda decide).
