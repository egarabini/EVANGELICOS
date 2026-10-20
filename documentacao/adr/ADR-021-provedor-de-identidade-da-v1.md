# ADR-021: O provedor de identidade da v1 — o Zitadel adotado

- **Status:** **Accepted** — decisão do ARQUITECT em **2026-10-20**.
- **Data:** 2026-10-20
- **Decisores:** ARQUITECT (Eduardo) · redação do PLANNER
- **Gatilho:** o experimento da **DEM-016** concluído (o E-01..E-07)
- **Emenda:** a **ADR-014 v3** (a v1 na base nova) no ponto da **autenticação**: o RF01 da DEM-005
  deixa de ser "a auth própria" e passa a ser **"a autenticação atrás da interface OIDC-ready,
  implementada pelo provedor"**
- **Não altera:** ADR-002, ADR-003, ADR-008, ADR-009, ADR-016, ADR-018, ADR-020

---

## Contexto

O experimento da DEM-016 testou o **Zitadel v4.19.5** (a API + o Login V2, serviços separados e não
modificados) na **homologação**, com o Let's Encrypt público, sem CA local e sem tocar no Traefik
da v0. O resultado:

| Critério | Resultado |
|---|---|
| **E-01** — o OIDC com o papel e o ambiente no token | **PASS** |
| **E-02** — a provisão por API (o Didasko cria o instrutor, ele entra) | **PASS** (201) |
| **E-03** — a troca obrigatória **pelo provedor** (o D-11) | **PASS** — sem código nosso |
| **E-04** — a memória | **PASS** — 343 MB em repouso, 402 MB de pico (abaixo de 1 GB) |
| **E-05** — a latência com o Ollama ocupado (10 logins) | **PASS no critério original (≤ 5 s)** — mediana 2,474 s, máximo 3,247 s |
| **E-06** — o esforço do fluxo completo | **5–9 dias úteis** de uma pessoa |
| **E-07** — a independência do fornecedor no cliente | **PASS** |

A licença: o núcleo **AGPL-3.0-only**, o login com **exceção MIT**; o uso é como **serviço
separado e não modificado**.

## Decisão

1. **Adotar o Zitadel como o provedor de identidade da v1**, no **marco 1b** (logo depois do
   esqueleto, o marco 1), com a autenticação atrás da **interface OIDC-ready** já prevista
   ("quem é o usuário, qual o papel, qual o ambiente").
2. **A D-10 e a D-11 fecham no provedor**: a criação de usuário **sem senha fixa** (o convite/o
   fluxo do provedor) e a **troca obrigatória no primeiro acesso** — e o login, a recuperação, os
   convites e o bloqueio **deixam de ser código nosso**.
3. **O experimento é reaproveitado** como o provedor da homologação (o host neutro
   `oidc.homolog.didasko.app.br`), **sem desmonte**. A produção da v1, quando houver, sobe numa
   **instância nova e limpa** em `oidc.didasko.app.br`; o host de homologação é descartado.
4. **As obrigações da licença** ficam registradas: o serviço separado e não modificado; as
   alterações do núcleo, se houver, exigem a oferta do fonte correspondente (a seção 13 da AGPL);
   a distribuição exige os avisos/oferta aplicáveis. A avaliação jurídica é do ARQUITECT.
5. **A operação**: o backup do banco do provedor, as atualizações de segurança e os limites de
   CPU/memória (o **RF13** — o issuer alcançável do contêiner; o **RF14** — a emissão do
   certificado; o **RF15** — as CPUs do Ollama) entram no marco 1b.

## Consequências

**Positivas**
- O **D-10 e o D-11 fecham** com código de quem faz só identidade — e não com o nosso, que é onde
  eles nasceram.
- O login, a recuperação, os convites e o bloqueio deixam de ser **código e dívida nossos**.
- O experimento não é descartado: vira a **homologação real**.

**Negativas / trade-offs**
- **Um serviço de infraestrutura a mais** (o provedor + o banco dele) para operar, atualizar e
  fazer backup.
- **5–9 dias úteis** do fluxo completo (os papéis, os convites, o ciclo de vida, o tema).
- A licença **AGPL-3.0-only** no núcleo exige disciplina (não modificar; se modificar, a oferta do
  fonte).
- O acoplamento ao fornecedor é reduzido pela interface, mas não é zero: a URL do emissor pode ter
  o caminho do fornecedor, e trocar de provedor exige reconfigurar o cliente OIDC.

## A decisão sobre as alternativas

A opção **B** (a autenticação própria no marco 1 e o provedor depois) foi **descartada** neste
momento: ela não zera o custo de 5–9 dias — troca "integrar o provedor" por "escrever e manter a
mesma funcionalidade", incluindo justamente a parte onde a D-11 nasceu (a troca obrigatória, o
bloqueio, a recuperação).

## Referências

- O experimento: a **DEM-016** (o relatório, o impedimento do TLS, as evidências)
- O marco 1b: a **DEM-005** (o spec, o design, o plano)
- [ADR-014](ADR-014-saida-do-reflex.md) · [ADR-020](ADR-020-autoridade-e-disponibilidade-da-obra.md)
