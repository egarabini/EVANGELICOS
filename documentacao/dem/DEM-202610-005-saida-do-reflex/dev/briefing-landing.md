# Briefing do DEVS — DEM-005, **a landing (o marco 2L)**

> **Nível 2** (a ADR-018): **uma** rodada de EVAL. A landing **não cresce** — o que não está no
> escopo vira item posterior. **O ARQUITECT aprova o texto** antes do despacho.

## 1. O que ler

1. `documentacao/dem/DEM-202610-005-saida-do-reflex/planner/landing.md` — o escopo, o design, as
   seções, o formulário e a hipótese de produção.
2. `.../planner/landing-texto.md` — o **texto final** (a voz do visitante). **Aprovação do ARQUITECT**
   antes de codar.
3. `ESTUDOS_BIBLICOS/GSI_EBD/gsi_ebd/landing_content/sections/` — a **fonte do conteúdo** (o hero, o
   sobre, o nome, os níveis, os testemunhos, o rodapé) da v0. O **texto** é reaproveitado; o
   componente (Reflex) não.

## 2. O escopo

- as rotas **`/`** (a landing) e **`/homenagens`**, na **v1** (o Jinja2 + o HTML/CSS puro, **sem o
  Reflex**), na **homologação**;
- as **8 seções**: o hero; o que é o Didasko; as obras e os estudos; quem participa (os 5 papéis); os
  níveis; os depoimentos (o "em breve"); as **homenagens** no padrão visual da landing (sem o menu
  lateral); o rodapé;
- **a raiz da homologação passa a ser a landing** — o `/` 200, no lugar do 401 (o achado A-01);
- o **contato**: o e-mail + o WhatsApp (a opção **(a)** — **sem formulário** nesta publicação);
- **a carga leve**: sem framework pesado, sem banco, sem volume; o serviço **estático**;
- **a acessibilidade**: o contraste, o foco visível, o `alt`, o `lang`, os títulos semânticos, o
  teclado.

## 3. As regras

- **a voz do visitante**: nada de termo de especificação (a "N+1", o "hash", o "snapshot", o número
  do papel);
- **a verdade**: a landing vai à produção com a **v0 por trás**; **não** prometer a dupla assinatura
  nem as versões; **pode** afirmar a obra avaliada e a Escritura verificada;
- **sem imagens/textos de terceiros sem direito**;
- **sem tocar** no v0, no Traefik ou na produção;
- **sem banco, sem formulário** (a opção a);
- se faltar decisão, **PARE e devolva ao PLANNER**.

## 4. O Definition of Done

- o **`/` 200** na homologação (a landing) e o **`/homenagens`** no padrão visual;
- o **render testado**: o 200, as seções presentes, o título, o `lang`, o `alt`;
- a **acessibilidade** verificada (o contraste, o foco, o teclado);
- a **suíte da v1 verde** + a **regressão da v0 (269)**; o **CI verde**; o **relatório**.

## 5. O que **não** é deste escopo

- o formulário de contato (a decisão é a (a): sem formulário);
- a **publicação em produção** — ela exige a **autorização específica do ARQUITECT** (o roteador/o
  serviço estático/os limites/a volta atrás, na §6 do `landing.md`);
- as obras (a fatia 2) e o acesso (o 1b) — **depois** da landing validada.
## 6. As correções obrigatórias (a revisão do AUXILIAR, 21/10)

O **protótipo já está corrigido** — o DEVS **porta o protótipo** para o Jinja2, não o reescreve:

1. o **contraste** dos botões do menu (o `.menu > a:not(.botao)`; o `#fff` no primário; o roxo no contorno);
2. o **menu** vira hambúrguer **abaixo de 1000 px** (não 720); testar em **360, 768, 1024 e 1440**;
3. a seção de obras **com as duas definições** (a obra = a fonte; o estudo dirigido = a obra aplicada);
4. **sem linguagem de bastidor** (o texto do site é do visitante);
5. a **página `/homenagens`** no padrão da landing (o conteúdo vem do banco da v0; sem imagem/texto de terceiros sem direito);
6. os **dados de contato reais** (os do protótipo são de teste) — o bloqueio está na §11 do `landing.md`.

**Os critérios do EVAL** estão na §12 do `landing.md` — a régua do marco 2L.
## 7. O conteúdo dinâmico vem do banco (a decisão do ARQUITECT)

- **Os depoimentos**: a seção só renderiza com pelo menos um `Testemunho` **ativo** (`is_active`);
  **sem** o "Em breve". O texto/rota do template é o `{% if testemunhos %}`.
- **O contato**: o e-mail, o telefone e o WhatsApp vêm do **`SiteConfig`** (`rodape_email`,
  `rodape_telefone`, `redes_whatsapp`); cada canal só aparece **se a chave existir**. O HTML do
  protótipo já traz os comentários do Jinja2 e a nota "os canais aparecem quando estiverem
  cadastrados" — **nenhum dado de teste**.
- **A leitura do banco da v0**: o serviço da landing lê a v0 **somente leitura** (a `DATABASE_URL`
  no `.env` da v1, 600, sem imprimir) — a v1 não escreve na v0.
