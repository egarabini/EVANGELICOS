# Briefing do EVAL cego — DEM-005, **marco 1** (o esqueleto da v1)

> Você julga **sem ver a implementação pela mão do autor** e **sem confiar no relatório** — a régua
> é o spec, o plano de testes e as condições da autorização. A saída é um **veredito com evidência**:
> PASS/FAIL por critério, com o comando e a saída que o provam.

## 1. O alvo

- o **PR #7**, o head **`59abcf8`**, a branch `feature/DEM-202610-005-marco1`;
- o **CI verde** (o run `39581630194`);
- a **homologação** no `homolog.didasko.app.br`.

## 2. O que ler (a régua)

1. `documentacao/dem/DEM-202610-005-saida-do-reflex/planner/spec.md` — os **RF01–RF15**, os CA.
2. `.../planner/design.md` — o **marco 1** (a estrutura, a auth, o banco, o deploy).
3. `.../planner/plano-testes.md` e `.../planner/plano-testes-marco-1b.md` (o que o 1b vai cobrar —
   não é o alvo deste EVAL).
4. `.../dev/briefing-marco-1.md` — o que o DEVS foi instruído a fazer.
5. As **condições da autorização** do ARQUITECT (a–g), no briefing e no relatório.
6. As ADRs **002** (o corpus), **003** (a Escritura), **008** (os segredos), **014 v3** (a v1),
   **018** (o nível), **021** (o provedor — o 1b, não este marco).
7. `documentacao/metodo/templates/briefing-eval.md` — o formato da sua jornada.

## 3. O ambiente (não o toque além de ler)

- a **homologação** `homolog.didasko.app.br`: o `/login` 200, o cert LE, o Postgres **próprio**
  (`didasko_v1`, o volume `homolog-v1_didasko_v1_data`), o usuário `didasko_v1`;
- a **produção** `didasko.app.br` 200 — e os 5 contêineres da v0 com o `StartedAt` de antes do
  marco 1 (a prova de que nada da v0 foi tocado);
- a **VPS** é read-only para você (o `sudo -n docker ps`/`logs`/`inspect`; **nada** de `up`, `down`,
  `rm`, `restart`, nem de tocar no Traefik).

## 4. O que julgar — os critérios

| O critério | O que o prova |
|---|---|
| **RF01** (a v1 FastAPI + Jinja2/HTMX) | a estrutura, as rotas, o render |
| **RF02** (a sessão, o CSRF, o H-14) | o login, o CSRF, a flag bloqueando (e as rotas abrindo após a troca) |
| **RF05/RF06** (a matriz e a guarda) | o `exigir(chave)`, o 403 por papel, o servidor decidindo |
| **RF10** (o banco próprio) | o `didasko_v1` no Postgres **próprio**; o `0001_baseline`; o seed |
| **RF13/RF14** (o issuer e o certificado) | o `extra_hosts` versionado; o cert do `homolog`; o procedimento (recriar o contêiner, nunca o Traefik) |
| **as condições a–g** | o Traefik da v0 sem restart; nada no `didasko_postgres`; os limites; os segredos na VPS (sem imprimir); o `exec -e` **a partir da próxima tag**; o escopo fechado |
| **os testes** | a suíte (as 37 + a regressão 269) — rode; e a **prova de mutação** (a que você quiser) |
| **o quase-acidente** | o `StartedAt` dos 5 da v0 **antes e depois** (o relatório tem a tabela) |

## 5. A régua do veredito

- **PASS** por critério, com a **evidência** (o comando e a saída);
- **FAIL** por critério, com o **o que faltou** e o **que faria passar**;
- o veredito **não** é do relatório: **você** confere o que dá para conferir (o código, os testes, a
  homologação, a VPS em leitura) e **declara o que não deu** — não inventa.
- **nada de "o autor disse"**: o relatório é uma pista, não a prova.

## 6. O que **não** fazer

- tocar na **produção** (a v0), no **Traefik** ou em qualquer contêiner da v0;
- o `down`/o desmonte da homologação;
- alterar o código do PR (a correção é do DEVS);
- inventar ambiente/valores — se não der para testar, diga.
