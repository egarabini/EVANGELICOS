# Intent: DEM-202610-016 / zitadel-provedor-de-identidade (o experimento)

status: draft
owner: PLANNER
signed_by: ARQUITECT
origin: decisão do ARQUITECT de 2026-10-19 — o experimento com prazo no marco 1 da v1
signed_at:
supersedes: —
open_questions_open: 2
nivel_agil: 2 — (ADR-018) uma rodada de EVAL; a homologação; **não** altera o RF01 até o resultado
duracao: **1 a 2 dias**
nota: este experimento **não é** a decisão de adotar. É uma prova de viabilidade com critério (o
E-01..E-06) e uma recomendação (adotar/adiar/descartar). A autenticação própria da v1 continua
prevista, atrás de uma interface (§4).

## 1. Problema

A v1 vai ter autenticação própria (o RF01 da DEM-005) — e é justamente onde apareceram os problemas
das dívidas: a troca obrigatória de senha como **redirect** (a D-11), o coordenador criado com a
senha fixa (a D-10), o bloqueio por tentativas, a recuperação de senha. É código nosso, com história
de defeito.

O ARQUITECT conhece o **Keycloak** e se interessou pelo **Zitadel** porque: o modelo **multi-tenant**
(organizações, projetos, a gestão delegada) casa com o "ambiente" do Didasko e com o coordenador
administrando os seus usuários; é certificado **OIDC**, exige **PostgreSQL** (que já temos) e traz a
**tela de login pronta**. E a decisão é mais barata **agora**: nada depende da auth e não há usuários
a migrar.

## 2. Outcome

**Um go/no-go com evidência**: o relatório com os números do E-04/E-05, o esforço do E-06 e a
**recomendação**. Nada muda no RF01 antes do resultado.

## 3. O escopo (os 7 itens do ARQUITECT)

1. **Subir** o Zitadel na homologação, com o banco próprio no mesmo Postgres, atrás do Traefik, com
   HTTPS — registrando os serviços necessários (a versão atual pode exigir o **serviço de login
   separado**: confirmar na **documentação oficial**, não em terceiros).
2. **Login OIDC** (authorization code + PKCE) de um usuário de teste no FastAPI do marco 1, validando
   o token com biblioteca padrão (p. ex. `authlib`) e lendo o **papel** do token.
3. **Mapear** uma organização do Zitadel a um **ambiente** do Didasko e um papel (o coordenador) a um
   papel do Didasko.
4. **Provisionar por API**: o Didasko (como coordenador) cria um instrutor no Zitadel e ele entra.
5. **A troca obrigatória** de senha no primeiro acesso, feita **pelo próprio Zitadel** (o D-11).
6. **Medir**: a memória do(s) contêiner(es) em repouso e durante um login; o tempo de login com o
   **Ollama ocupado** (a VPS de 12 GB, o Ollama em CPU — o hash de senha disputa os núcleos).
7. **Registrar a licença** atual do Zitadel (o AUXILIAR recorda AGPL-3.0) e o que ela implica usando-o
   como **serviço separado e não modificado**.

## 4. Constraints

- **1 a 2 dias**; **a homologação** (`homolog.didasko.app.br`); o banco/serviço próprios da v1.
- **Não toca na v0 nem em produção**; **não altera o RF01** até o resultado.
- A v1 escreve a autenticação **atrás de uma interface** (OIDC-ready: "quem é o usuário, o papel, o
  ambiente") — qualquer que seja o resultado, trocar a implementação não refaz as telas.
- **A infra é do ARQUITECT**: o DNS do host do Zitadel, o roteador do Traefik e o banco no Postgres —
  o Codex prepara e **pede a autorização quando chegar lá** (§7).

## 5. Os critérios de aceite (o E-01..E-06)

| # | Critério | Passa se |
|---|---|---|
| **E-01** | o login OIDC | o usuário de teste entra e o FastAPI lê o papel do token |
| **E-02** | a provisão por API | o Didasko cria um instrutor e ele entra |
| **E-03** | a D-11 | o primeiro acesso exige a troca, **sem código nosso** |
| **E-04** | a memória | o conjunto do Zitadel **abaixo de 1 GB** em repouso |
| **E-05** | a latência com o Ollama ocupado | o login **≤ 5 s** de ponta a ponta (a proposta do PLANNER; o E-05 pede "propor o limite") |
| **E-06** | o esforço | o relatório estima o custo restante, em dias, para o fluxo completo (os papéis, os convites, o ciclo de vida, o tema da tela) |

## 6. Health e sinal

- **O sinal**: o relatório com a **tabela dos E-01..E-06** (o PASS/FAIL de cada), os números do E-04
  e do E-05, o esforço do E-06 e a **recomendação** (adotar/adiar/descartar) — com a justificativa.
- **O porteiro**: o EVAL cego, **uma rodada**, contra os critérios.

## 7. As autorizações de infraestrutura (avisar o ARQUITECT quando necessário)

| Item | De quem | Quando |
|---|---|---|
| o **DNS** do host do Zitadel (p. ex. `zitadel.homolog...`) | ARQUITECT | antes do HTTPS |
| o **roteador do Traefik** para o host | ARQUITECT | antes do HTTPS |
| o **banco/usuário** do Zitadel no Postgres | ARQUITECT | antes de subir |

## 8. Decisões já registradas

| # | Questão | Decisão |
|---|---|---|
| 8.1 | A DEM | **própria, nível 2** (não um item do marco 1 — o resultado pode virar ADR) |
| 8.2 | O executor | **Codex** (branch + PR; a homologação) |
| 8.3 | O limite do E-05 | **≤ 5 s** de ponta a ponta (a proposta; o ARQUITECT pode ajustar) |
| 8.4 | A decisão | **o ARQUITECT**, com o relatório; se adotar, **ADR nova** + o RF01 + os marcos 1/2 |
| 8.5 | A versão e a arquitetura | **v4.19.5**: a API Zitadel + o **Login V2 separado**, com a API encaminhada por **`h2c`** (confirmado na doc oficial pelo DEVS em 2026-10-19) |
| 8.6 | A licença | o núcleo **AGPL-3.0-only**; o login com **exceção MIT** (a `LICENSING.md` oficial da v4.19.5); usado como **serviço separado e não modificado** |
| 8.7 | Os hosts (a proposta do DEVS) | `zitadel.homolog.didasko.app.br` (a API) e `oidc.homolog.didasko.app.br` (o FastAPI experimental) — o **DNS é do ARQUITECT** |
| 8.9 | Os fatos do DNS (2026-10-19) | `didasko.app.br` e `homolog.didasko.app.br` resolvem para **84.46.250.57** (a VPS); **`zitadel.homolog...` e `oidc.homolog...` NÃO têm registro** (sem wildcard) — faltam os dois A records |
| 8.8 | Os fatos da VPS (2026-10-19) | o SSH: `didasko-vps` (`didasko-deploy`); a rede do Traefik: **`deploy_didasko`**; o Postgres: o **`didasko_postgres`** (o projeto `deploy`, a rede `deploy_didasko`, o usuário `didasko`); os bancos hoje: o `didasko`; o **Zitadel** ganha o banco próprio (o `zitadel`) |

## 9. Perguntas abertas — só o ARQUITECT fecha

- [ ] **9.1** O limite do E-05: **≤ 5 s** de ponta a ponta, **p95 de 3 medições** com o Ollama
  ocupado — confirmar.
- [ ] **9.2** **O DNS**: o pai `homolog.didasko.app.br` **já existe** (→ 84.46.250.57); faltam os **dois A records** (`zitadel.homolog...` + `oidc.homolog...` → 84.46.250.57) — ou um wildcard `*.homolog...`. Sem eles, o HTTPS (o LE por httpchallenge) não sobe.
- [ ] **9.3** **O banco do Zitadel**: criar o banco/usuário (`zitadel`) no `didasko_postgres` (o
  mesmo servidor, o banco separado).
- [ ] **9.4** **O roteador do Traefik**: a regra dos dois hosts (o DEVS prepara a config; o
  ARQUITECT aplica).

## 10. Fora de escopo

A migração de usuários da v0 (não há); o deploy/o pipeline da v1; a adoção (a decisão é depois).


