# Design — DEM-005, **marco 1b: a identidade** (o Zitadel, a ADR-021)

> Depois do **marco 1** (o esqueleto: a app, a sessão, o `didasko_v1`, a imagem, a homologação).
> O que este marco entrega: **o login no provedor, com o papel e o ambiente no token — e as regras
> do Didasko conferidas no servidor.** A ADR-021 é o "porquê"; este documento é o "como".

## 1. A arquitetura

- **O provedor**: a API + o Login V2 (o v4.19.5; a ADR-021). A homologação em
  `oidc.homolog.didasko.app.br`; a produção, quando houver, em `oidc.didasko.app.br` (a instância
  nova).
- **A app**: o cliente OIDC (`authlib`); o módulo `v1/identidade.py` com a **interface**:
  `usuario_atual(request) -> User`, **`exigir(chave)`** (a **chave da matriz**, `rota:/...` — uma rota admite vários papéis; a chave é o contrato que as telas já usam), `ambiente_atual(request)`. O fluxo:
  `/login` → o provedor → `/callback?code…` → o token → a sessão da app.
- **O token** (o ID token + o access token): o `sub` (a identidade), o `email`, o `org_id` (a
  organização → o ambiente), os `roles` (o papel do **provedor**). **A verificação é explícita**:
  o issuer, o audience (o `client_id`), a assinatura (o JWKS), o `exp`/`nbf`, o `nonce` e o `state`.
- **O mapeamento** (o ponto 5): o `org_id` → o `ambiente_id` e o `role` do provedor → o `papel` do
  Didasko, num **mapa do Didasko** (uma tabela/config), **não** numa claim livre. O token **não**
  escolhe o papel; ele **informa** o papel do provedor, e o mapa decide o papel do Didasko.

## 2. A autorização — o token identifica, o Didasko decide (o ponto 1)

- A cada requisição: a **sessão** (o usuário do Didasko) → o **papel do Didasko** (o mapa) → a
  **matriz papel × rota** (`rbac.py`, a DEM-002) → o 200/403. **A decisão não vem do cliente** —
  nem do token, nem do formulário, nem do botão.
- **Os papéis do Didasko continuam dele**: o Admin decide (a ADR-020), o Revisor é o auxiliar de
  qualidade, o Coordenador vincula/adenda. O token do provedor **não concede** nada além do mapeado.
- **O contrato da interface (a v1 já o usa)**: o `exigir(chave)` recebe a **chave da matriz**
  (`rota:/...`); o marco 1b **conserva essa assinatura** — o que muda é **quem** põe o papel na
  sessão (a própria × o provedor), não a chave.
- O teste que prova: um token válido com o papel `coordenador` do provedor **não** passa numa rota
  de admin; e um token **forjado/inválido** é recusado antes da matriz.

## 3. A sessão — a da app × a do provedor (o ponto 3)

| Aspecto | A decisão |
|---|---|
| **Onde** | a sessão **da app** (o servidor, o cookie `httponly`/`secure`/`samesite`) — a fonte da verdade da requisição; a do provedor é a **origem** do login |
| **A expiração** | curta na app (a inatividade), com a renovação pelo **refresh** (o token do provedor); o refresh falha → a reautenticação |
| **O logout local** | limpa a sessão da app **e** revoga a do provedor (o RP-initiated; o the the the the) |
| **O logout global** | o botão "sair de todos os dispositivos" → a revogação no provedor; a app invalida as sessões no the |
| **A revogação pelo provedor** | a sessão da app é **verificada contra o provedor** (o introspection/the the the) no the the — a revogação do provedor **derruba** a app no próximo the the the |
| **O CSRF** | o do marco 1 (o token por sessão) continua; o callback OIDC valida o `state` |

## 4. O ciclo de vida do usuário (o ponto 2)

- **Os estados do Didasko** (o `UserStatus`, a assinatura, a inatividade de 60 dias) **mandam**:
  suspender/cancelar/inativar no Didasko → **desativar/revogar no provedor** (a API), senão a pessoa
  continua autenticando. O inverso também: a reativação → o the the the the the the.
- **A provisão**: o convite (o the e-mail) e a criação pelo coordenador (a API). **A conciliação**:
  a falha parcial (criado no provedor e não no Didasko, ou o contrário) é **detectada e registrada**
  — com a operação de compensação (o the the the the) e **sem a exclusão automática** (a the the the
  a the the the).
- O the the: o the the the the the the the the.

## 5. O `hash_esperado` (o ponto 4) — o domínio manda

- O `hash_esperado` que o Revisor envia no `revisar`/`recusar` (a fatia 1) continua sendo o **do
  domínio** — a versão vista; **não** é o token, não é a sessão.
- **A reautenticação no meio da revisão**: o the the the the the the the (a sessão expirou; o
  refresh falhou) → o provedor reautentica o **mesmo usuário**; a app **preserva o estado da
  revisão** (a versão + o `hash_esperado`) no server (o the the the), e o `revisar` recebe o mesmo
  hash. O the the the the: a reauth **não** invalida o formulário; o `hash_esperado` viaja com o
  formulário/o the, não com a sessão.
- O teste: a sessão expira entre o `GET` do parecer e o `POST` do `revisar` → a reauth → o
  `hash_esperado` **ainda** é o da versão vista (e se o conteúdo mudou, a recusa é a mesma de antes).

## 6. Os convites, a recuperação e o tema (o ponto 6)

- **O SMTP real** (o the the the the no provedor; a the the the the the the the) — o the the the
  the the the the.
- **A recuperação de senha**: a do provedor (a the the the); a app não tem tela.
- **O tema do Login V2**: o branding suportado (o the the the the); a revisão acessível/responsiva —
  **estimativa separada** (o the 0,5–1 dia do E-06).

## 7. O deploy (o ponto 7)

- **O RF13** — o issuer alcançável do contêiner: o `extra_hosts` **versionado** no Compose. **O
  `TRAEFIK_EDGE_IP` (o IP do Traefik na rede de borda) muda se o contêiner for recriado** — a
  alternativa estável é mapear o host para **`host-gateway`** (o endereço do host, que publica o
  80/443), ou resolver o IP na subida. O `host-gateway` **não foi testado**; é a pista do marco 1b.
- **O RF14** — a emissão do certificado: **recriar os contêineres do serviço, nunca reiniciar o
  Traefik**; a versão fixa da imagem é decisão do ARQUITECT.
- **O RF15** — as CPUs do Ollama limitadas (a causa dos 2,474 s).

## 8. Os testes do marco 1b

- **O token**: a assinatura/o issuer/o audience/o `exp`/o `nonce`/o `state` — o inválido é recusado.
- **O mapeamento**: o `org_id` → o ambiente; o `role` → o papel; o **não mapeado** → recusa (sem
  papel padrão).
- **A autorização**: a matriz (o token de coordenador não passa em admin; o de revisor não publica).
- **A sessão**: a expiração; a renovação; o logout local/global; a revogação no provedor → a app
  derruba.
- **O ciclo de vida**: o inativar → o provedor desativado; a conciliação da falha parcial.
- **O `hash_esperado`**: a reauth no meio da revisão não o perde (o §5).
- **A prova de mutação**: remover a verificação do token → o teste falha; remover o mapeamento → o
  papel aparece errado; remover o logout global → a revogação não chega.

## 9. A estimativa (o E-06 da DEM-016)

| O bloco | Os dias úteis |
|---|---:|
| Os papéis e os ambientes (a matriz completa, os grants, o isolamento multiambiente) | 1–2 |
| Os convites (o SMTP real, a validade, o reenvio, o aceite, os erros) | 1–2 |
| O ciclo de vida (a recuperação, o bloqueio, a desativação, o logout/revogação, a auditoria, a conciliação) | 2–3 |
| O tema do Login V2 | 0,5–1 |
| A integração e a regressão (a interface, a sessão, a rede/erros, a operação, o retorno) | 0,5–1 |
| **O total** | **5–9** |

## 10. Os riscos

- **O provedor como dependência do login**: a indisponibilidade do provedor derruba o login (o the
  the the the the the). Mitigação: o the the the; o escopo do the the.
- **A sessão da app × a do provedor**: a divergência (a app acha que a pessoa está logada; o
  provedor revogou) → o the the the the the the the.
- **O the the the the the the**: a the the the the the the the.
- O the the the the the the the the the the the the the the the.



