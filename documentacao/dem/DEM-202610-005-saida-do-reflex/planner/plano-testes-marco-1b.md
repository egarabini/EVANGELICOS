# Plano de testes — DEM-005, **marco 1b** (a identidade pela ADR-021)

> O EVAL cego julga o marco 1b com este plano. A saída é o PASS/FAIL por caso, com a evidência.
> **A régua**: o `plano-testes.md` do marco 1 continua valendo para o esqueleto; este cobre o que o
> 1b acrescenta — o token, o mapeamento, a sessão do provedor, o ciclo de vida e o `hash_esperado`.

## 1. Os oráculos (nunca computar com o código sob teste)

| O quê | O oráculo |
|---|---|
| **O token** | um JWT **hardcoded** (o `sub`, o `email`, o `org_id`, os `roles`, o `exp`, o `iss`, o `aud`), emitido com a chave do mock; o **inválido** com a assinatura quebrada, o issuer errado, o audience errado e o `exp` no passado |
| **O mapa** | as chaves da matriz hardcoded: `rota:/admin/obras` → `ADMIN`; `rota:/revisor/obras` → `REVISOR`; `rota:/obras` → `ADMIN`+`REVISOR` |
| **A sessão** | o cookie e o CSRF hardcoded; o `exp` e o `refresh` com valores conhecidos |
| **O `hash_esperado`** | os hashes **da fatia 1** (a `DEM-011`), não recalculados |
| **O provedor** | o `respx`/o mock para o JWKS, o `/token`, o `/introspect` e o `/logout` — o teste nunca fala com a VPS |

## 2. Os casos

| # | O cenário | O esperado | O oráculo |
|---|---|---|---|
| **CT-01** | o login OIDC com o token **válido** | a sessão criada; o `/me` responde com o papel e o ambiente **mapeados** | o token mock |
| **CT-02** | o token com a **assinatura quebrada** | o **401**, sem sessão criada | o token forjado |
| **CT-03** | o token com o **issuer errado** | o **401** | o `iss` hardcoded |
| **CT-04** | o token com o **audience errado** | o **401** | o `aud` hardcoded |
| **CT-05** | o token **expirado** | o **401** | o `exp` no passado |
| **CT-06** | o `state`/o `nonce` **divergente** no callback | o **401**; a sessão não criada | o `state` hardcoded |
| **CT-07** | o `org_id` **não mapeado** para um ambiente | o **403** — sem ambiente padrão | o `org_id` desconhecido |
| **CT-08** | o `role` do provedor **não mapeado** para um papel | o **403** — sem papel padrão | o `role` desconhecido |
| **CT-09** | o token de **coordenador** numa rota de **admin** | o **403** (a matriz; o token não concede) | a chave `rota:/admin/obras` |
| **CT-10** | o token de **revisor** numa rota de **publicação** (a `liberar`) | o **403** (o Revisor não publica — ADR-020) | a chave da matriz |
| **CT-11** | a **sessão expirada** com o refresh válido | a sessão renovada, sem reautenticação | o `exp`/o `refresh` hardcoded |
| **CT-12** | o **logout local** | a sessão da app limpa **e** o `/logout` do provedor chamado | o mock do `/logout` |
| **CT-13** | o **logout global** ("sair de todos os dispositivos") | a revogação no provedor; a app invalida as sessões | o mock da revogação |
| **CT-14** | o provedor **revoga** a sessão (o `/introspect` = `active:false`) | a app derruba a sessão no the the the | o mock do `/introspect` |
| **CT-15** | o usuário **inativado** no Didasko | o provedor **desativado** (a chamada de desativação) | o mock da API do provedor |
| **CT-16** | a **provisão parcial** (criado no provedor, não no Didasko) | a conciliação **detecta e registra**; sem exclusão automática | o mock do estado |
| **CT-17** | a **provisão parcial** (o inverso) | a conciliação detecta e registra | o mock do estado |
| **CT-18** | o **`hash_esperado`** com a sessão expirando **entre o GET e o POST** do parecer | a reautenticação preserva o estado; o `revisar` recebe o **mesmo hash**; se o conteúdo mudou, a recusa é a de sempre | os hashes da fatia 1 |
| **CT-19** | o `SMTP` real (o convite) | o e-mail sai; o token do convite válido; o aceite cria o usuário | o mock do SMTP |
| **CT-20** | a **recuperação de senha** | a tela do provedor; a app não tem tela | o mock |

## 3. A prova de mutação (o que cada remoção deve quebrar)

| A mutação | O que deve falhar |
|---|---|
| Remover a verificação da **assinatura** | o **CT-02** |
| Remover a verificação do **issuer**/do **audience** | o **CT-03**/o **CT-04** |
| Remover o **mapeamento** (usar o `role` do token direto) | o **CT-09**/o **CT-10** |
| Remover a **verificação da revogação** | o **CT-14** |
| Remover o **logout global** | o **CT-13** |
| Remover a **desativação no provedor** | o **CT-15** |
| Remover a **preservação do `hash_esperado`** na reauth | o **CT-18** |

## 4. O que o EVAL entrega

- o **PASS/FAIL por caso** (os 20), com a evidência (a saída do teste);
- a **prova de mutação** (as 7), com o caso que quebrou;
- a **contagem**: a suíte da v1 (a do marco 1 + a do 1b) e a regressão da v0 (269);
- o **ambiente**: a homologação (o `oidc.homolog…`), jamais a produção; o `down`/o desmonte **só** com a confirmação do ARQUITECT.

## 5. O que o EVAL não julga

- o tema do Login V2 além do que o critério pedir (a aparência é o do E-06, o 0,5–1 dia);
- a infraestrutura do provedor (o backup/o the, que é do ARQUITECT);
- o `SMTP` de produção (o teste valida o envio, não o provedor de e-mail real).
