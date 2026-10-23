# A proposta de autorização da produção — a landing (o marco 2L)

> **O ato é do ARQUITECT.** Esta proposta descreve o que será feito; o aceite é o seu. **Nada é
> executado sem ele.**

## 1. O roteador (o Traefik)

O serviço da **landing** (a v1) ganha um **roteador próprio**, com a prioridade **maior** que a da v0:

```yaml
# no serviço da landing (o Compose da v1 na produção), os labels:
traefik.http.routers.landing-prod.rule=Host(`didasko.app.br`) && (Path(`/`) || PathPrefix(`/static/landing/`))
traefik.http.routers.landing-prod.priority=200          # > a prioridade da v0
traefik.http.routers.landing-prod.entrypoints=websecure
traefik.http.routers.landing-prod.tls=true
traefik.http.routers.landing-prod.tls.certresolver=le
```

- **O que a landing atende**: **só o `/` (o exato) e o `/static/landing/*`**.
- **O que continua na v0**: o `/login`, o `/aluno`, o `/admin` e **todo o resto** — porque o
  `Path(/)` é **exato** (`/login` não é `/`) e o `PathPrefix(/static/landing)` não os alcança.
- **O roteador da v0 não muda** (o `didasko_app` continua com o catch-all dele); o novo serviço
  entra com a prioridade maior no **mesmo host**.

## 2. Os limites

- O serviço da landing: **sem banco** e sem a rede interna; só na rede de borda.
- Os limites: a **memória** e a **CPU** definidos (o serviço é estático, só serve o HTML/CSS/WebP).
- O disseram os limites **de acordo com o que a aplicação consome** — o valor final no relatório.

## 3. A volta atrás

- **Remover o rótulo** do serviço da landing (ou o `docker compose -p … down` do **serviço** da
  landing) e **recriar só ele** — o **`--force-recreate --no-deps landing`**.
- **NUNCA** reiniciar o Traefik: ele relê os rótulos sozinho (o docker provider).
- **O efeito**: o `/` volta a servir a landing da v0 — **a substituição é reversível em uma linha**.

## 4. O teste (depois da mudança)

- o **`/`** → 200 e é a landing da v1 (o `<title>` e o CSS `landing.<hash>.css`);
- o **`/login`** → 200 (a v0, o login);
- o **`/homenagens`** → 200 (a v0 — a página própria dela);
- o **`/aluno`** (ou o app da v0) → 200/redireciona como hoje;
- a **v0 intocada** (o `StartedAt` dos 5 contêineres da produção **inalterado**).

## 5. A substituição

A landing nova **substitui** a atual no `/` desde a primeira publicação (a decisão do ARQUITECT) —
**não há convivência**: o `/` é a nova, o resto é a v0.

## O que **não** muda

- o **`/login`** e o app (a v0) — o roteador novo não os toca;
- o **`/homenagens`** — a v0 tem a própria (a v1 não entra, pela decisão do ARQUITECT);
- o **Traefik** (sem restart) e o **domínio** (o mesmo `didasko.app.br`).

## O pedido

**A sua aprovação**, com o VISION revisando antes: (1) o roteador preserva o `/login` e o resto na
v0 **pela prioridade**; (2) a **volta atrás nunca reinicia o Traefik**; (3) a substituição do `/`.
