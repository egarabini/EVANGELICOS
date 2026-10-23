# A proposta de autorização da produção — a landing (o marco 2L)

> **A revisão do ARQUITECT (23/10)** — os 7 pontos incorporados. **O ato é do ARQUITECT; nada é
> executado sem ele.**

## 1. O roteador (o Traefik) — os rótulos

O serviço da landing (a v1) entra com um roteador próprio, na **mesma rede de borda** da v0, com a
**prioridade explícita** maior:

```yaml
- traefik.enable=true
- traefik.docker.network=deploy_didasko
- traefik.http.routers.landing-prod.rule=Host(`didasko.app.br`) && (Path(`/`) || PathPrefix(`/static/landing/`))
- traefik.http.routers.landing-prod.priority=200
- traefik.http.routers.landing-prod.entrypoints=websecure
- traefik.http.routers.landing-prod.tls=true
```

**O `tls=true` só — sem o `certresolver`** (a revisão, o ponto 5): o certificado do `didasko.app.br`
**já existe** (o Traefik o serve pelos rótulos da v0); o `tls=true` usa o certificado existente, e
**nenhum pedido novo ao Let's Encrypt é feito**.

**A regra**: o `Path(/)` é **exato** (o `/login` não é o `/`) e o `PathPrefix(/static/landing/)` só
alcança os assets da landing. O `/login`, o `/homenagens`, o `/aluno` e o resto **não casam** com a
regra nova → **continuam na v0**, pelo roteador dela.

## 2. Os limites (os números)

- **A memória**: **`mem_limit: 512m`** (512 MiB);
- **A CPU**: **`cpus: 0.50`** (meio vCPU);
- **A rede**: **só a `deploy_didasko`** (a borda); sem a `interna`; **sem `DATABASE_URL`**.

São os mesmos valores da homologação (o §2 do compose `v1-homolog.yml`), e o serviço é estático (só
serve o HTML/CSS/WebP).

## 3. Como o contêiner chega à produção

- **O stack**: o `deploy/app-v1.Dockerfile` (o `python:3.12-slim`), o comando
  `python -m uvicorn v1.landing:create_app --factory`;
- **O projeto do Compose**: o **`deploy`** (o mesmo da v0), com o serviço **`landing`** — o
  `container_name: didasko_v1_landing`;
- **A tag**: o `v*` (o SemVer) **pelo `deploy.yml`** (o GitHub Actions) — o pipeline que já publica a
  v0; **o mesmo processo**, o serviço a mais;
- **Os 5 contêineres da v0 NÃO são recriados**: o deploy sobe **só o serviço `landing`** (o
  `--force-recreate --no-deps landing`) — o `didasko_app`, o `didasko_traefik`, o `didasko_postgres`,
  o `didasko_chromadb` e o `didasko_ollama` **ficam com o `StartedAt` inalterado**.

## 4. As duas etapas (a subida)

**(a) O contêiner SEM os rótulos de roteador** — a subida só do serviço, sem o Traefik o enxergar
(o `traefik.enable=false` na primeira subida); o teste **por dentro** da VPS:
- o `docker exec didasko_v1_landing curl -sS -o /dev/null -w "%{http_code}" http://127.0.0.1:8000/` →
  **200**, o HTML com o `<title>` da landing;
- o `/homenagens` → **200** (o layout, a página sem o link);
- o contêiner sem o `DATABASE_URL` e só na borda.

**(b) Só então os rótulos** — o **ato do ARQUITECT**: a subida com os rótulos do §1. Depois:
- a **base** do §5 (o antes × o depois);
- o **teste** do `/login` (o 307), do `/homenagens` (o 307) e do app da v0;
- o `StartedAt` dos 5 contêineres da v0 **inalterado**.

**A volta atrás** = remover os rótulos (o `traefik.enable=false` ou o down **do serviço** da landing)
e recriar **só** o serviço — **o Traefik nunca reinicia**; ele relê os rótulos sozinho.

## 5. A base (os códigos de hoje — a produção não foi tocada)

| A rota | Hoje (a v0) | Depois (o esperado) |
|---|---|---|
| `/` | **200** | **200** (a landing da v1) |
| `/login` | **307** | **307** (a v0; o redirect) |
| `/homenagens` | **307** | **307** (a v0) |

**A regra do teste (a revisão, o ponto 1)**: **registrar os códigos de hoje ANTES** e comparar os
**mesmos códigos DEPOIS** — o `/` deve mudar de **origem** (a v0 → a v1), **não** de código; o
`/login` e o `/homenagens` devem **continuar iguais**.

## 6. Os rótulos reais do roteador da v0 (a prova do ponto 6)

```
traefik.http.routers.didasko.entrypoints = websecure
traefik.http.routers.didasko.rule = Host(`didasko.app.br`) || Host(`www.didasko.app.br`)
traefik.http.routers.didasko.tls.certresolver = le
```

**Nenhum `priority`** — o roteador da v0 usa a **prioridade padrão** (calculada pelo Traefik pelo
tamanho da regra, não explícita). O `priority=200` da landing **vence** qualquer rota da v0 no `/`.
**A verificação antes de executar**: `docker inspect didasko_app` para conferir que **nenhum** rótulo
da v0 tem a `priority` > 200.

## 7. A ordem (a revisão, o ponto 7)

1. **O DEPLOY** roda o `subir.sh --v1` **com o head `67f0623`** (o fix do hero/o menu a zero/o YAML
   limpo/o `.gitignore`), na homologação;
2. **O ARQUITECT valida em janela anônima** (o 360 sem o logo do hero, o painel encostado, o rótulo
   AA, o link das homenagens ausente);
3. **A proposta** (este documento) — o **ato do ARQUITECT**;
4. **A etapa (a)** — o contêiner sem os rótulos, o teste por dentro;
5. **A etapa (b)** — os rótulos (o ato), o teste do §5 (a base × o depois).

## O que **não** muda

- o **`/login`** e o app da v0 — o roteador novo não os toca;
- o **`/homenagens`** — a v0 tem a própria (a v1 não entra);
- o **certificado** — o `tls=true` usa o existente, **sem** o let's Encrypt novo;
- o **Traefik** (sem restart) e o **domínio** (o mesmo `didasko.app.br`);
- os **5 contêineres da v0** (o `StartedAt` inalterado).
## O aceite do ARQUITECT — 23/10

**O ARQUITECT deu o ACEITE da proposta de autorização da produção** (a revisão dos 7 pontos).

**A execução (a ordem do ARQUITECT):**

1. **A etapa (a)** — o contêiner da landing sobe na produção **SEM os rótulos de roteador** (o
   `traefik.enable=false`) e é **testado por dentro** (o `docker exec curl` → o `/` 200, o HTML da
   landing; o `/homenagens` 200; o contêiner sem o `DATABASE_URL` e só na borda); os **5 contêineres
   da v0 não são recriados**;
2. **A etapa (b)** — **o ato do ARQUITECT**: os rótulos do §1 (o `tls=true` **sem** o
   `certresolver`; o `priority=200`); o teste do **§5** (a base × o depois);
3. **A volta atrás** = remover os rótulos e recriar **só** o serviço da landing; **o Traefik NUNCA
   reinicia**.

**O que NÃO muda**: o `/login` (o 307) e o app da v0; o `/homenagens` (o 307); o certificado (o
`tls=true` usa o existente); os **5 contêineres da v0** (o `StartedAt` inalterado).
