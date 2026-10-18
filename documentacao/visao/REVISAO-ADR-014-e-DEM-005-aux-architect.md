# Revisão da ADR-014 e do intent da DEM-005

> Autor: AUXILIAR-ARCHITECT (IA) · Para: ARQUITECT e PLANNER · Data: 2026-10-18
> **Só leitura.** Revisei `documentacao/adr/ADR-014-saida-do-reflex.md` e
> `documentacao/dem/DEM-202610-005-saida-do-reflex/planner/intent.md` (versão em disco em 2026-10-18),
> comparando com o código e o compose de produção. Nada foi alterado.
>
> **Veredito:** a ADR-014 pode ser aceita **com duas emendas** (A e F abaixo). O intent da DEM-005
> pode ser assinado depois de acertar a seção 9. Nenhum achado muda a direção (FastAPI + Jinja2 + HTMX).

## O que está bom

- Evidência honesta e curta; custo medido (~3.300 linhas) e reaproveitamento (753 + 898 + 87 linhas sem Reflex) conferem com o que levantei.
- Cerca respeitada: nenhuma linha de código antes do aceite; ADR-001 só muda de status quando a 014 for aceita.
- "Paridade primeiro", "volta atrás a cada rota", "lição por último" e "depende da DEM-004" estão nas restrições.
- A DEM-002 "agora, no Reflex" está escrita na ADR, como recomendado.

## Achados

### A. [Alto] A convivência esconde o problema mais difícil: sessão e login compartilhados

A ADR diz que o Traefik direciona "rota a rota". Verifiquei dois fatos:

- **[F]** `deploy/docker-compose.producao.yml`: há **um** roteador (`didasko`, `Host(didasko.app.br)`) apontando para a porta **3000** (frontend do Reflex).
- **[F]** O login vive em `gsi_ebd/states/auth.py`, como **estado do Reflex**. Não encontrei cookie assinado nem JWT no código; a sessão é o estado do Reflex.

Consequência: uma rota servida pela base nova **não sabe quem está logado**. Sem um mecanismo de sessão
comum, o aluno logaria no Reflex e seria tratado como anônimo na rota migrada (ou o inverso).
Isso afeta **a primeira rota migrada**, não a última, e afeta H-04 (RBAC igual por papel).

**Emenda sugerida (ADR e spec da DEM-005):**
1. Decidir antes da primeira rota o **mecanismo de sessão compartilhado** (por exemplo, cookie assinado
   emitido pelo login e lido pelas duas bases). A ADR só precisa declarar que existe uma decisão pendente;
   o desenho fica na spec.
2. Fazer um **spike descartável**: uma rota trivial na base nova, atrás do Traefik, autenticada pela
   sessão do login atual. Se o spike falhar, a estratégia por rotas precisa ser reaberta.
3. Incluir na matriz papel × rota (baseline H-04) a coluna "base que serve a rota".

### B. [Médio] "A classe de erro do dia 16/10 deixa de existir" está certo, mas incompleto

Sem `Var`, esse erro específico some. Surgem outras classes que a ADR não menciona e que pedem teste desde o dia 1:

| Risco novo | Mitigação sugerida |
|---|---|
| Variável inexistente no Jinja renderiza **vazio**, sem erro | `StrictUndefined` no ambiente Jinja2 |
| Template quebrado só aparece ao renderizar | teste que **renderiza todas as rotas por papel** (substitui o `test_paginas.py`) |
| CSRF em formulários e trocas HTMX | token por sessão, validado em toda requisição que altera estado |
| Cookie de sessão (flags, expiração) e cabeçalhos de segurança | decisão registrada na spec |
| Autorização repetida em cada rota (no Reflex ela passa pelo estado) | dependência única de papel, testada pela matriz papel × rota |

Sugestão: trocar a frase por "a classe de erro de `Var` deixa de existir; as classes novas estão listadas e têm teste".

### C. [Baixo] A opção A (ficar e endurecer) é descartada sem custo comparado

"As cercas são compensação de framework" é argumento, não comparação. Ao lado, o custo da opção B
(2 stacks vivos durante meses; ~3.300 linhas) só aparece em "Negativas". Para a decisão ficar defensável
depois, acrescentar uma linha na tabela de opções com o custo e o risco de cada uma. Não muda a decisão.

### D. [Médio] A ADR depende da DEM-004, mas a DEM-004 só entregou metade

Etapa 1 (CI) existe; a Etapa 2 (CD, com a chave de deploy) ainda não. A migração por rotas **publica o
tempo todo**; sem deploy por pipeline, cada rota migrada seria um deploy manual. Registrar na ADR:
"a primeira rota só migra após a **Etapa 2** da DEM-004".

### E. [Baixo] O intent da DEM-005 está inconsistente com a ADR

- A ADR-014 já responde 9.1 ("DEM-002 agora, no Reflex"), mas o intent ainda lista a 9.1 como aberta.
- O cabeçalho ainda diz "Rascunho do AUXILIAR-ARCHITECT… O número 005 é sugestão". Remover ao assinar.
- Registrar no intent a dependência de **DEM-002** (precede a migração do admin) e da **Etapa 2 da DEM-004**.
- Corrigir `open_questions_open` quando 9.1 fechar (3 → 2).

### F. [Médio] "Substitui a ADR-001" vs "só na parte do framework"

A ADR-014 diz que **substitui** a ADR-001. O intent da DEM-005 e a conversa dizem que muda **só o
framework**; Python, PostgreSQL, a regra "sem Node/TS na aplicação", ChromaDB, Ollama e Docker/Traefik
continuam. Como está escrita, `Superseded by ADR-014` anularia a ADR-001 inteira, inclusive as partes
que ficam.

**Emenda sugerida:** na 014, listar explicitamente as cláusulas da 001 que **permanecem** (e esclarecer que
HTMX e Alpine.js são arquivos estáticos, não Node/TS, e que o Tailwind, se usado, vem pela CLI independente).
Ou marcar a 001 como "substituída em parte". Sem isso, o próximo agente lê a 001 como revogada.

## Resumo de ações

| # | Para quem | Ação | Quando |
|---|---|---|---|
| A | PLANNER | Declarar na ADR a decisão pendente de sessão compartilhada + exigir o spike | antes do aceite |
| F | PLANNER | Listar as cláusulas da ADR-001 que permanecem | antes do aceite |
| B | PLANNER | Acrescentar os riscos novos e a regra de teste | spec da DEM-005 |
| D | PLANNER | Registrar que a 1ª rota só migra após a Etapa 2 da DEM-004 | ADR e intent |
| E | PLANNER | Alinhar o intent à ADR (9.1, cabeçalho, dependências) | antes de assinar |
| C | PLANNER | Linha de custo na tabela de opções | opcional |
| — | ARQUITECT | Aceitar a ADR-014 depois das emendas A e F | decisão sua |

## Rastro

Lido: ADR-014, intent da DEM-005, `deploy/docker-compose.producao.yml` (roteador Traefik),
`gsi_ebd/states/auth.py`, listagem de `states/` e `utils/`. **Não lido:** `utils/rbac.py` por inteiro,
`services/auth_service.py` por inteiro, a spec e o design da DEM-005 (não existem ainda).
O achado A parte de uma busca por `cookie|jwt|token` que não encontrou mecanismo de sessão fora do estado do Reflex;
vale confirmar lendo o fluxo de login completo antes de fechar a emenda.
