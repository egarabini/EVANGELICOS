# ADR-008: Segredos e senhas de demonstração

- **Status:** Accepted
- **Data:** 2026-10-16
- **Decisores:** ARQUITECT (Eduardo)
- **Gatilho:** Novo Horizonte (adoção de método) / decisão já implementada

---

## Contexto e Problema

Os segredos vivem hoje no `.env` da VPS (correto). Mas as **senhas de demonstração
(`senha123`) estão documentadas no repositório** e o site é **público** — ou seja,
acesso administrativo aberto para quem ler o repositório.

## Decisão

Segredos **nunca** no repositório: `.env` na VPS e **GitHub Secrets** no CI. Token
de acesso nunca em chat. As senhas de demonstração devem ser trocadas **antes** de
qualquer divulgação; até lá é uma pendência aberta declarada.

## Consequências

**Positivas:**
- Reduz superfície de exposição; credenciais de CI auditáveis.

**Negativas / trade-offs:**
- Trocar as 5 senhas é trabalho manual imediato.

## Impacto nas DEMs

- Bloqueia divulgação pública.
- ADR-010 move a chave de deploy para secret.
