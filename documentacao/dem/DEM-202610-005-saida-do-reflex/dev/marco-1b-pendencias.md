# O marco 1b (o Zitadel) — o que falta e o que depende do ARQUITECT

> **SÓ CONFERIR — NÃO DESPACHAR.** A frente das obras vem antes. O 1b depende de decisões do
> ARQUITECT que **não são técnicas**.

## O que já existe (o commit `ff0d0b7`)

- o **design** do provedor de identidade (o ADR-021, Accepted: o Zitadel adotado);
- o **plano de testes** (os 20 casos);
- o **briefing** (o `documentacao/adr/ADR-021-...` + o `dev/briefing-...`).

## O que falta conferir (o PLANNER, sem despachar)

- o **design** cobre o **fluxo inteiro** (o login, o refresh, o logout, o MFA, o convite, o
  provisionamento, a sincronização de papéis)?
- o **plano de testes** tem os **20 casos** com o **DoD** de cada um (o caminho felizes + os erros:
  o sessão expirada, o papel removido, o usuário desativado, o token revogado)?
- o **briefing** define o **o quê/o porquê/o DoD/o risco** do marco 1b?

## As pendências do ARQUITECT (NÃO são técnicas — são decisão)

1. **A autorização da infraestrutura do Zitadel em produção** (o `oidc.didasko.app.br`) — a nova
   entrada no Traefik, o certificado, o DNS;
2. **A avaliação da licença AGPL-3.0-only pelo jurídico dele** — o Zitadel é AGPL; a implicação
   jurídica do uso interno/exposto;
3. **A ordem**: **as obras antes do 1b** (a decisão do ARQUITECT);
4. **A rotação das contas e da senha `senha123` do admin de produção** (o D-01) — o 1b é o momento
   natural, mas a decisão é do ARQUITECT.

## O entregável do 1b (quando despachado)

- o **EVAL cego** do design + do plano de testes;
- o **despacho** ao DEVS (o provisionamento, os fluxos, o `rbac` sincronizado);
- o **runbook** da migração das contas (a v0 → o Zitadel).
