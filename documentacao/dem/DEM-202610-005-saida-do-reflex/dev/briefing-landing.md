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
## 7. O conteúdo condicional vem de um ARQUIVO, não do banco (a decisão do ARQUITECT)

- **A landing NÃO recebe `DATABASE_URL`** e **não tem rede para o banco** — o serviço sobe sem banco.
- O conteúdo vem de **`v1/landing.yaml`** (versionado, no lado da landing): os
  `depoimentos[]` (a seção só renderiza com pelo menos um `ativo: true`), o `contato` (o `email`/o
  `whatsapp` — cada canal só aparece se existir) e o `hero`/`sobre` (opcionais, sobrepõem o texto
  base do template).
- O **JSON/o YAML entra VAZIO** (ou só com o texto base) — **nenhum dado de teste** no arquivo.
- Um depoimento só entra com o **consentimento** de quem o deu, **registrado na jornada**.
- **Mudar um dado é alteração no arquivo, por PR e deploy por tag** (o runbook da landing).
- O **EVAL** confere: o contêiner da landing **sem** variável de banco e **sem** rede para o banco.
## 8. A fonte única é a v1 — e o cache (as correções do ARQUITECT, 22/10)

- **A v1 é a fonte da landing.** O `planner/landing-prototipo/` está **CONGELADO** (o README dele) —
  ele é o histórico do desenho; **não se edita mais**. Todo ajuste visual nasce **direto na v1** e é
  validado na homologação. (A regra anterior, "o protótipo é a fonte da verdade", **saiu** — ela só
  administrava a duplicação.)
- **O cache**: o **HTML** com `Cache-Control: no-cache` + **ETag**; os **assets** (o CSS, os WebP)
  com `max-age` longo + `immutable` **SOMENTE** com o **hash do conteúdo na URL** (o nome
  `logo-88.<hash>.webp` ou o `?v=<hash>`, gerado no build — nunca manual). **Trocar o conteúdo de
  um asset troca a URL dele** — vale para o `srcset`.
- **O EVAL confere**: as 5 decisões do arquivo (o sem-banco; os depoimentos só com o ativo; os canais
  só se existirem; sem dados de teste; o contêiner sem a variável e sem a rede) + o cache + a fonte
  única + os testes dos cabeçalhos e da URL versionada.
