# Briefing do DEVS — DEM-005, **marco 1b** (a identidade pela ADR-021)

> **Para:** o Codex (o DEVS) — ou outro executor sob a autorização do ARQUITECT.
> **O que este marco entrega**: o login no **Zitadel**, com o papel e o ambiente no token, **atrás da
> interface que o marco 1 já expõe** — sem tocar nas telas do marco 1.
> **O design**: `planner/design-marco-1b.md`. **O plano de testes**: `planner/plano-testes-marco-1b.md`.

## 1. O contrato que não muda (o marco 1 já o usa)

- `usuario_atual(request)` → o `User`;
- **`exigir(chave)`** → a chave da matriz (`rota:/...`), **não o papel** — uma rota admite vários;
- `ambiente_atual(request)`.

**O marco 1b troca a implementação, não a assinatura.** As telas chamam essas três funções e só o
`auth.py` sabe quem responde.

## 2. O escopo

1. **O cliente OIDC** (`authlib`): o `/login` (o `state`, o `nonce`, o PKCE) → o provedor → o
   `/callback` (o `code` → o token) → a sessão; a **verificação explícita** (o issuer, o audience, a
   assinatura, o `exp`/`nbf`, o `nonce`, o `state`).
2. **O mapeamento** (o §1 do design): o `org_id` → o `ambiente_id` e o `role` do provedor → o `papel`
   do Didasko, num **mapa do Didasko**; o não mapeado **recusa** (sem papel/ambiente padrão).
3. **A autorização no servidor** (o §2): a matriz da DEM-002 a cada requisição; o token **não**
   concede nada além do mapeado.
4. **A sessão** (o §3): a expiração, a renovação, o logout **local e global**, a **revogação pelo
   provedor** derrubando a app.
5. **O ciclo de vida** (o §4): inativar/suspender/60 dias → **desativar/revogar no provedor**; a
   **conciliação** da provisão parcial (detecta e registra, **sem exclusão automática**).
6. **O `hash_esperado`** (o §5): o do domínio, viaja com o formulário; a **reautenticação no meio da
   revisão não o perde**.
7. **Os convites, a recuperação e o tema** (o §6): o **SMTP real**, a recuperação **do provedor**, o
   tema do Login V2 — a estimativa separada (o 0,5–1 dia do tema; os 1–2 dos convites).
8. **O deploy** (o §7): o **RF13** (o `host-gateway` — a pista; o `TRAEFIK_EDGE_IP` muda se o
   Traefik for recriado), o **RF14** (recriar os contêineres do serviço, nunca reiniciar o Traefik),
   o **RF15** (as CPUs do Ollama — **com a autorização própria do ARQUITECT**).

## 3. As regras

- a branch `feature/DEM-202610-005-marco1b` a partir do `develop` (depois do marco 1 mesclado);
- **a interface não muda** — o teste do marco 1 continua verde;
- **o domínio não se reescreve**: o `gsi_ebd/` é importado;
- **nada de segredo no repositório**; o `.env`/as chaves na VPS, o 600;
- **não reiniciar o Traefik**; o `--force-recreate` dos contêineres do serviço da v1;
- **a produção (o v0) não é tocada**; a homologação é o ambiente;
- se faltar decisão, **PARE e devolva ao PLANNER**.

## 4. O Definition of Done

- os **20 casos** do `plano-testes-marco-1b` verdes, com os oráculos hardcoded;
- a **prova de mutação** (as 7) quebrando o caso certo;
- o **login no provedor** funcionando na homologação; o `/me` com o papel e o ambiente;
- a **troca obrigatória do provedor** (o D-11) e a **criação sem a senha fixa** (o D-10);
- a **regressão da v0 (269)** verde; o **CI verde**; o relatório com os números e as evidências;
- o **EVAL cego** julga depois — o marco 2 só depois do PASS.

## 5. O que **não** é deste marco

- as telas do fluxo (a fatia 2 da DEM-011) — **depois do PASS**, com o contrato do `rbac.py` aprovado;
- a virada para a produção (o marco 6);
- o desmonte da homologação (a confirmação do ARQUITECT na hora);
- o RF15 **sem** a autorização própria (o horário e a decisão do ARQUITECT).
