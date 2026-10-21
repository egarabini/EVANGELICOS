# Risco aceito — o H-14 × o `on_password_changed` (o marco 1)

> **Status:** aceito pelo ARQUITECT em 21/10/2026, **desde que o parecer do EVAL registre a
> bifurcação em vez de escondê-la**.

## O que é

O marco 1 implementa o **H-14** (a troca obrigatória da senha de seed) na **implementação própria**:
a troca **zera a flag** `must_change_password`, **mantém o status `ativo`** e **renova a sessão**.
Ela **não chama** o `on_password_changed` do domínio (`gsi_ebd/services`), que **suspende os
não-admins**.

## Por que

Dois requisitos em conflito no marco 1:
- o **H-14** exige que as rotas **abram após a troca** (a sessão continua válida, o usuário ativo);
- o **`on_password_changed`** do domínio, por design, **suspende** quem não é admin — o que
  contrariaria o H-14.

O marco 1 resolve **pelo H-14**: a troca é tratada na implementação própria, e o serviço do domínio
**não é chamado**.

## O que fica em aberto (a bifurcação)

A troca de senha da v1 **bifurca** do serviço do domínio. Enquanto o marco 1b não chegar:
- o `on_password_changed` da v1 **não é chamado**;
- o status `ativo` é mantido **pela implementação própria**, não pelo domínio.

**Isso é uma bifurcação visível, não um defeito escondido** — e é o EVAL que a registra.

## A resolução — o marco 1b

O **marco 1b** (o Zitadel, a ADR-021): a **troca obrigatória é do provedor** (o E-03 do experimento:
o primeiro acesso do instrutor abriu a tela de troca do provedor antes do callback). Com o provedor:
- o `on_password_changed` do domínio **deixa de ser chamado** — ou é alinhado ao status real;
- o H-14 passa a ser a **troca do provedor**, e a v1 não tem a lógica própria.

## A decisão do ARQUITECT (2026-10-21)

- A leitura do PLANNER é **aceita**.
- O EVAL pode marcar o item como **FAIL**; a resposta é **o risco documentado**, não a correção do
  marco 1 — e o **marco 1b** é a resolução.
- O que **não** se aceita: **esconder** a bifurcação no parecer. Se o EVAL não a registrar, o
  parecer é incompleto.

## O que o EVAL deve registrar no parecer

1. que o marco 1 **não chama** o `on_password_changed` do domínio;
2. que a troca **zera a flag, mantém o `ativo` e renova a sessão**;
3. que isso é **bifurcação provisória**, resolvida no **marco 1b**;
4. o **risco**: enquanto o 1b não chega, a regra da troca é a da v1, não a do domínio.
