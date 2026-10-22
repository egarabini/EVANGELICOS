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

**O logo (a decisão do ARQUITECT, 21/10)**: o **`logo-didasko-tec.png`** (o aprovado) convertido para
**WebP com transparência** em **3 resoluções** — o **88** (o topo/o rodapé, o dobro dos 44/34), o
**440** (o hero @1x) e o **880** (o hero @2x) — com o **`srcset`/o `sizes`**, o `width`/o `height`
intrínsecos e a **prioridade só no hero** (`fetchpriority="high"`; o rodapé `lazy`). **Total: 86 KB**
(o SVG de 5 MB **não** entra no diretório servido nem na imagem do Docker — ele é **fonte**, em
`documentacao/design/`). As fontes de design (**o PNG original, o vetor e o `cores-padroes.md`**) foram
movidas de `estudos/UI-UX` (pasta ignorada) para **`documentacao/design/`** — os direitos são nossos.

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

**A substituição (a decisão do ARQUITECT, 21/10): a landing nova substitui a atual na produção desde a
primeira publicação.** Recomendação do AUXILIAR; o ARQUITECT confirma na validação da homologação.

Isso significa: **não há convivência** entre a landing nova e a antiga. No momento da publicação:

- o **`/` da produção** passa a servir a **landing da v1** (o `v0` deixa de servir a landing atual);
- o **`/homenagens`** passa a ser o da v1 (o padrão visual novo);
- o **login e o app continuam na v0** até a virada — o roteador novo **não** os toca;
- **a volta atrás** é remover o rótulo e recriar **só** o serviço da v1 — o `v0` volta a servir a
  landing atual, sem reiniciar o Traefik.

**O ganho**: a partir da publicação, a vitrine já é a da v1 — e o **401 da raiz** (o achado A-01)
deixa de existir **na produção**, porque a raiz passa a ser a landing e não a app.

**O desenho**: **um serviço estático da v1, sem banco**, atendendo o `/` e o `/homenagens` no domínio
principal por um **roteador de prioridade maior**, com o restante (o login e o app) na v0.

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
## 10. As correções da revisão do AUXILIAR (21/10) — aplicadas no protótipo

| # | O item | O que foi feito |
|---|---|---|
| 2.1 | O botão "Quero participar" do topo ilegível | a regra `.menu > a:not(.botao)` deixou de tingir os botões; o `.menu .botao--primario { color: #fff }` e o `.menu .botao--contorno { color: var(--roxo) }` (o contraste AA) |
| 2.2 | O menu quebrando em ~800 px | o corte do hambúrguer subiu de 720 para **1000 px**; os links com `white-space: nowrap`; o intervalo do menu reduzido em 1120 |
| 2.3 | A seção de obras sem a definição | os dois cartões novos: **A obra** (a fonte) e **O estudo dirigido** (a obra aplicada: capítulos + questões + instrutor) |
| 2.4 | A linguagem de bastidor ("no mesmo padrão visual desta casa") | removida; o texto revisado nas seções |
| 2.5 | A página `/homenagens` não existia | criada (`homenagens.html`), no mesmo padrão da landing, com o conteúdo a ser preenchido do banco da v0 |
| 3.1 | Os níveis divergiam do produto | alinhados a **Básico, Médio, Avançado, Master** (o `Study.level`); a hermenêutica/a liderança viraram as descrições de Avançado/Master |
| 3.2 | Os depoimentos com "Em breve" | a seção **removida** até haver depoimentos reais e autorizados |
| 3.3 | A citação de Mateus repetida | ficou **uma** vez (o parágrafo); as aspas curvas “ ” no lugar de « » |
| 3.4 | O link "Entrar" fixo na v0 | todas as ocorrências marcadas com `data-entrar` (a URL vira parâmetro na v1) |
| 3.5 | O logo pesado | só os 3 WebP (98,2 KB); a fonte é o `design/logo.svg` |

## 11. Os bloqueios de publicação (o item 2.6 e a decisão 4.1)

| O bloqueio | O que falta |
|---|---|
| **Os dados de contato** | o WhatsApp (`wa.me/5500000000000`) e o e-mail (`contato@gsi-ebd.com.br`, o domínio antigo) **não** podem ir à produção. O ARQUITECT precisa dar os **reais** (ou confirmar o único canal) — está no HTML com os marcadores `data-email`/`data-whatsapp` |
| **O formulário de contato** | a decisão (a) (sem formulário) está **recomendada**; a seção de contato já a segue. A confirmação é do ARQUITECT |
| **A publicação** | o roteador de produção (o `/` e o `/homenagens` pela v1, o resto na v0) exige a **autorização específica** — os itens da §6 |
| **A raiz da homologação** | o executor sobe a landing no `homolog.didasko.app.br/` (hoje 401) e **avisa o ARQUITECT** para a validação |

## 12. Os critérios do EVAL (o item 6)

1. o **contraste** dos botões (AA) — o do topo, o do hero e o do rodapé;
2. o **menu** em 360, 768, 1024 e 1440 px (com o hambúrguer abaixo de 1000);
3. o **texto de obras e estudos** (a obra + o estudo dirigido);
4. a **ausência de linguagem de bastidor** (versão, hash, snapshot, N+1);
5. os **links sem dados de teste**;
6. o **peso** da página (o orçamento: menos de 500 KB na carga inicial; sem JS de terceiros);
7. a **raiz da homologação** servindo a landing;
8. o **LCP** aceitável em conexão móvel simulada, com a medição registrada.
## 13. O conteúdo condicional vem de um ARQUIVO versionado — não do banco (a decisão do ARQUITECT, 21/10)

A landing **não lê o banco da v0** e **não recebe `DATABASE_URL`** (nem somente leitura). O serviço
segue **sem banco e sem rede para o banco** — a premissa original do plano, mantida.

O conteúdo condicional vem de **`v1/landing.yaml`** (versionado, no lado da landing):

| O bloco | Os campos | A regra |
|---|---|---|
| **`depoimentos[]`** | a cidade, o estado, a profissão de fé, a foto (opcional), o `ativo`, a ordem | a seção **só renderiza** com pelo menos um **`ativo: true`**; um depoimento só entra com o **consentimento** de quem o deu, **registrado na jornada** |
| **`contato`** | o `email`, o `whatsapp` (cada um opcional) | cada canal **só aparece** se existir; sem canais, a seção fica **só com o convite** |
| **`hero`/`sobre`** | o título/o subtítulo, o texto | opcional — o texto base do template; o arquivo **sobrepõe** |

**O arquivo entra VAZIO** (ou só com o texto base) até o ARQUITECT fornecer os dados reais — **nenhum
dado de teste**, nenhum `mailto:`/`wa.me` de exemplo.

**A operação**: **mudar um dado é alteração no arquivo**, por **PR e deploy por tag** — está no
runbook da landing.

**A dívida registrada (o pós-v1)**: depois da virada, os depoimentos e a configuração do site viram
**entidades do `didasko_v1`**, editáveis pelo Admin; **só então** a landing ganha acesso a banco e
passa a lê-los dali. É item da **DEM-005** (ou do pós-v1) — e a decisão de abrir o banco para a
landing é do ARQUITECT.

**O EVAL confere**: o contêiner da landing sobe **sem** variável de banco e **sem** rede para o banco.
## 14. O cache e a fonte única (as correções do ARQUITECT, 22/10)

- **O HTML** da landing: `Cache-Control: no-cache` + o **ETag** (o navegador revalida a cada visita).
- **O CSS e os WebP**: `max-age` longo + o `immutable` **somente** com o **hash do conteúdo na URL**
  (o nome ou o `?v=`), gerado no build. **Mudou o conteúdo, muda a URL** — e o `srcset` acompanha.
- **A fonte única**: a **v1** (`v1/templates/landing` + `v1/static/landing`). O
  `planner/landing-prototipo/` está **CONGELADO** (o README dele); todo ajuste nasce na v1.
- **Os testes do DoD**: os cabeçalhos (o no-cache + o ETag; o max-age + o immutable nos versionados);
  a URL que muda com o conteúdo; a validação em **janela anônima** (sem o `Ctrl+F5`).
