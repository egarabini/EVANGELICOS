# A landing da v1 — **o marco 2L** (o escopo fechado pelo ARQUITECT, 21/10)

> **Nível 2** (a ADR-018): **uma** rodada de EVAL. A landing **não cresce**: o que não está aqui vira
> item posterior.

## 1. O que é e onde

- A landing é feita **na v1** (o Jinja2 + o HTML/CSS puro, **sem o Reflex**), em **homologação**
  (`homolog.didasko.app.br`); **sem login**.
- **A raiz da homologação passa a ser a landing** — resolve o **401 da raiz** (o achado **A-01**).
- O fluxo: **planejar → construir em homologação → validar → publicar em produção**.

## 2. Os papéis (na landing)

Os **cinco**: Administrador, Revisor, Coordenador, Instrutor e Aluno. **"Gestores" era erro de
cópia** e sai.

## 3. As seções (a ordem)

| # | A seção | O conteúdo |
|---|---|---|
| 1 | **O hero** | o título, o subtítulo e o CTA |
| 2 | **O que é o Didasko** | a origem do nome (o *didasko* grego) e a missão |
| 3 | **As obras e os estudos dirigidos** | **o fundamento** — a obra avaliada antes de chegar às turmas; a Escritura sempre verificada. **Sem listar obras** |
| 4 | **Quem participa** | os **cinco papéis** em linguagem simples |
| 5 | **Os níveis** | a jornada progressiva |
| 6 | **Os depoimentos** | o "em breve" — **sem conteúdo falso** |
| 7 | **As homenagens** | no **mesmo padrão visual da landing** (hoje é a página interna com o menu lateral) |
| 8 | **O rodapé** | o contato, o ©, os links |

**A fonte do conteúdo**: o `gsi_ebd/landing_content/sections` da v0 (o hero, o sobre, o nome, os
níveis, os testemunhos, o rodapé) — o **texto é reaproveitado e refinado**, o componente não.

## 4. As regras de redação (do ARQUITECT)

1. **A voz do visitante**: nada de termo de especificação (a "versão N+1", o "hash", o "snapshot", o
   número do papel). **O texto da interface e o texto da especificação vivem separados.**
2. **A verdade**: a landing vai à produção **com o app v0 ainda por trás**. **Não** prometer a dupla
   assinatura nem as versões. **Pode** afirmar: *"toda obra é avaliada antes de chegar às turmas"* e
   *"a Escritura vem sempre de texto bíblico verificado — nunca gerada por IA"*.
3. **Sem imagens ou textos de terceiros sem direito**; a acessibilidade e a carga leve.

## 5. O formulário de contato — a decisão pendente

O formulário coleta **dados reais de visitantes** (a LGPD). As opções:

| Opção | O quê | O custo | O risco |
|---|---|---|---|
| **(a) Sem formulário na 1ª publicação** | um **e-mail + WhatsApp** de contato no rodapé e no CTA | **zero** — sem campo, sem dado pessoal, sem base de tratamento | o visitante que quer contato usa o canal; nada a vazar |
| **(b) O formulário enviando para a v0** | reusa o `formulario_section`/o `LandingState` da v0 | baixo (a v0 já tem) | a landing da v1 **depende da v0**; o dado entra num fluxo que vai ser **substituído** na virada — e a LGPD é a mesma da v0 |
| **(c) O formulário da v1 com a tabela própria** | a tabela + a tela de leitura no admin da v1 | médio/alto — tabela, rota, admin, retenção, base legal, o aviso de privacidade | **a landing não pode crescer** (o escopo) — e um formulário exige a **política de privacidade**, a base legal e a retenção, que não estão no escopo |

**A recomendação (minha e do AUXILIAR): a (a)** — a primeira publicação **sem formulário**, com o
e-mail e o WhatsApp no rodapé. A landing é **vitrine**; o contato real não precisa de base de dados.
A (c) fica para quando houver a política de privacidade e a base legal — e **não** nesta rodada.

## 6. A publicação em produção — a hipótese a autorizar

A hipótese (a desenhar, **sem executar**): **um serviço estático da v1, sem banco**, atendendo o `/`
e o `/homenagens` no domínio principal por um **roteador de prioridade maior**, com o restante (o
login e o app) na v0.

**Os itens que o ARQUITECT precisa autorizar antes de executar** (a autorização é **específica**):

| O item | O que muda | A volta atrás |
|---|---|---|
| **O roteador** | o rótulo do Traefik: o `/` e o `/homenagens` passam a ir para o serviço da v1; o resto continua na v0 | remover o rótulo do serviço da v1 e recriar **só** o serviço da v1 — **nunca** reiniciar o Traefik |
| **Os limites** | o serviço estático da v1 (a memória/o CPU) — o **menor** possível; sem banco, sem volume | — |
| **A ordem** | primeiro em homologação (o `/` e o `/homenagens` da homologação), depois a autorização da produção | — |
| **O login e o app** | **continuam na v0** até a virada — o roteador novo **não** os toca | — |

**Sem a autorização do roteador, nada é publicado**; a landing fica em homologação e o `v0` segue
como está.

## 7. O processo

- **O nível 2** (a ADR-018): **uma** rodada de EVAL cego.
- O DEVS: a branch `feature/DEM-202610-005-landing`, o PR, o CI verde (a suíte da v1 + a regressão
  269 + o novo teste do render da landing e da acessibilidade).
- O EVAL: a régua do briefing; o PASS/FAIL.

## 8. A fila (a decisão do ARQUITECT, 21/10)

1. **A landing (o 2L)** — a primeira;
2. **As obras** (a fatia 2 da DEM-011): a inclusão; o desenvolvimento e a aprovação; os testes em
   estudos com **alunos fake**;
3. **O acesso (o marco 1b)** — o Zitadel;
4. Os marcos 3–6 (a virada).

## 9. O caminho do `.env.v1-homolog` (a informação pedida)

`/home/didasko-deploy/homolog-v1/.env.v1-homolog` — na raiz do clone da homologação, **modo 600**,
dono `didasko-deploy`, **fora** do git (o `.gitignore` cobre). O `--env-file` é resolvido a partir
dessa raiz — é por isso que o arquivo vive ali, ao lado do `.env` da v0 (que **não** é lido pela v1).
