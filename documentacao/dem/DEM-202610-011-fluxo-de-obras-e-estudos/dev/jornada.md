# Jornada — DEM-202610-011, fatia 1

## 2026-10-19 — Think e List

Leitura do briefing, intent, spec aprovada, design, plano, guardas e ADRs 011/019. O app estava em `develop`, limpo. Documentação localizada no repositório pai `EVANGELICOS/documentacao`, não dentro do app.

Quatro lacunas encaminhadas ao PLANNER: conteúdo versionado, hashes individuais, fonte persistente e reenvio. O ARQUITECT autorizou iniciar hash, fontes, modelos e testes, aguardando o ajuste das operações. Branch `feature/DEM-202610-011-fatia1-dominio` criada de `develop`.

## 2026-10-19 — Design v2 e ajuste v3

O design v2 passou a existir no disco; depois, a v3 definiu `hash_esperado`, os momentos `visto`/`liberado` e `alterar(obra, conteudo, admin)`. Implementação seguiu a v3, removendo `itens_visto` persistido. Sem revisão Alembic e sem import de Reflex no domínio.

Modelos registrados no `models/__init__.py`; snapshots por momento; fonte persistente; sete operações com papéis e estados verificados no serviço. Transações pertencem ao chamador (commit/rollback). Hash v3 usa UTF-8, prefixo `v1|` e ordenação dos hashes individuais. Chaves da diferença: `capitulo:{ordem}` e `adendo:{codigo}`; duplicatas bloqueadas.

`fontes.py` lê CSV com `;`, cache por caminho e configuração `CAMINHO_INVENTARIO`. Fonte ausente/decisão inválida falha fechada. A licença é consultada na liberação; o cache do mesmo caminho só muda após reinício/invalidação explícita, conforme a carga única do design.

Primeira etapa: 26 testes novos passaram e suíte de 154 testes passou (128 existentes + 26). Após transições v3: 61 testes novos passaram. Em revisão, `alterar` foi ajustado para preservar IDs por ordem/código, evitando quebrar referências quando o item continua presente; validação ocorre antes da atualização. Restrições únicas impedem duplicação de versão e de item por momento.

Próximo passo: prova de mutação em cópias isoladas, suíte final e PR para `develop`.

## 2026-10-19 — Prova de mutação

Seis cópias fiéis de `gsi_ebd/`, `tests/` e `rxconfig.py`, sem caches, criadas fora do app. Em cada cópia o teste selecionado passou antes da alteração; removido apenas um guard/instantâneo, o mesmo teste falhou com exit 1 (sem erro de coleta). Originais intactos.

Resultados: gate `nao_entra` → 1 falha (N-01); `revisor_id` → 1 falha (N-03); papel → 8 falhas (N-04); instantâneo liberado → 1 falha (N-07); `hash_esperado` → 2 falhas (N-08); instantâneo visto → 1 falha (F-08). Logs e JSON em `evidencias-mutacao/`.

## 2026-10-19 — Suíte final e PR

Suíte final: 189 testes passaram (128 + 61), com 18 avisos de depreciação existentes; `git diff --check` passou. Commit `f202eb6ba1edd5e9c7a74ab732ac77d0d5ad8759`, branch enviada ao origin. PR https://github.com/egarabini/gsi_ebd/pull/4 aberto contra `develop`. Relatório e changelog escritos com contratos, evidências, requisitos de schema/inventário da v1 e lacunas remanescentes. Sem merge, Alembic, Compose ou deploy.

CI **verde** em Python 3.12, no commit `f202eb6ba1edd5e9c7a74ab732ac77d0d5ad8759`: https://github.com/egarabini/gsi_ebd/actions/runs/39315199116. Sem merge ou deploy.

## 2026-10-19 — Delta v4 solicitado na revisão do PR #4

Leitura, nesta ordem, do design §8, plano C-08/C-09/C-10/F-10 e despacho §4b. Branch conferida: `feature/DEM-202610-011-fatia1-dominio`, árvore limpa em `f202eb6`. O ARQUITECT autorizou o segundo commit no mesmo PR, sem merge ou deploy.

Lista executada: modelos `obra.py`/registro no `__init__.py`; canonização, normalização, eventos e alteração sem remoção em `services/flow.py`; leitura fresca em `services/fontes.py`; vetores atualizados e 22 testes novos nos dois arquivos de teste existentes. Nenhum arquivo adjacente alterado.

JSON canônico por campos nomeados, textos em LF/NFC; agregado por chave/hash ordenados com prefixo `v1\n`. Chaves de adendo também normalizadas. Eventos são acrescentados à transação da operação com autor, data, hash e detalhes (parecer/ajustes quando existentes); operações bloqueadas não acrescentam evento. `liberar` lê o mesmo CSV novamente com `recarregar=True`, sem depender do cache de exibição. `alterar` conserva itens omitidos e recalcula o hash da obra completa após o upsert.

Verificação dirigida: 83 testes passaram (61 anteriores + 22 novos). Inclui os sete tipos de evento, duas recusas e dois reenvios sucessivos, preservação dos registros após commits, rollback de evento e estado, leitura fresca nas duas direções e conservação dos itens omitidos. Suíte completa e mutações do delta em andamento.

## 2026-10-19 — Validação e segundo commit do delta

Suíte completa: 211 testes passaram (189 + 22), com 18 avisos existentes. Cópias fiéis: sem normalização, os 11 C-10 falharam; sem inserção de evento, F-10 falhou. Os mesmos seletores estavam verdes antes de cada mutação. Logs em `evidencias-mutacao-delta-v4/`.

Segundo commit `8f6608a4bdeab6a381e8db95246a5c8badd5e60f` criado e enviado à mesma branch do PR #4. Nenhum PR novo. Relatório reescrito para o estado final v4, mantendo as evidências históricas da primeira entrega. CI do novo commit será acompanhado; sem merge/deploy.

CI do delta **verde** em Python 3.12, commit `8f6608a4bdeab6a381e8db95246a5c8badd5e60f`: https://github.com/egarabini/gsi_ebd/actions/runs/39317794718. PR #4 confirmado **aberto**, com exatamente os dois commits `f202eb6` e `8f6608a`. Árvore do app limpa. Sem merge ou deploy.

## 2026-10-19 — Correção v5 após reprovação do EVAL

Design §9 e plano F-06/F-06b relidos antes de codar. O teste F-06 anterior afirmava o desvio; foi reescrito para a mesma versão em revisão, catálogo suspenso, ponteiro nulo e evento na contestada. Nenhuma versão é criada na contestação.

Correções aplicadas na ordem do despacho: contestar; importação com leitura fresca; versão anterior substituída ao liberar a seguinte; tamanho da diferença no evento de liberação; payload malformado como FluxoBloqueado antes de gravar; snapshots LF/NFC; FonteInvalida derivada de FluxoBloqueado. Criado `services/erros_fluxo.py` para compartilhar a exceção sem ciclo de importação. Nenhum modelo novo ou revisão Alembic nesta correção.

Testes dirigidos: 104 passaram (83 + 21). O novo N-01 aquece o cache com `entra`, altera o mesmo CSV para `nao_entra`, confirma que a consulta de exibição continua antiga e chama importar sem limpar cache. Payloads malformados não alteram obra, versões ou eventos. Snapshots conferidos diretamente em LF/NFC e hashes recomputados. F-10 continua verificando todos os eventos, agora terminando com a suspensão da v2 após sua liberação.

Lacuna comunicada ao ARQUITECT: a revisão posterior à contestação encontra snapshots da mesma versão, com unicidade versão/momento/item. O §9 define a reabertura, mas não define a identificação de novos instantâneos ou a preservação dos anteriores nesse novo ciclo. Foi pedida definição; não foi inventado um campo de ciclo nem apagada evidência para contornar a restrição.

## 2026-10-19 — Validação v5 e novo commit no PR #4

232 testes passaram (211 + 21); 18 avisos existentes. Mutação nova comprovada: tirar apenas `recarregar=True` de importar faz falhar N-01 com cache quente; baseline verde. Evidências em `evidencias-mutacao-v5/`.

Commit `8c2e1bcc78078cdc36381be4d1b73f22e2407c4f` enviado à mesma branch do PR #4. Nenhum PR novo. Relatório atualizado com a correção e a lacuna de novos snapshots na mesma versão após contestação. CI será acompanhado; sem merge/deploy.

CI da correção v5 **verde** em Python 3.12 no commit `8c2e1bcc78078cdc36381be4d1b73f22e2407c4f`: https://github.com/egarabini/gsi_ebd/actions/runs/39320863779. PR #4 confirmado aberto e árvore do app limpa. Sem merge/deploy. A lacuna de novos instantâneos pós-contestação permanece registrada para definição do ARQUITECT.

## 2026-10-19 — Delta 3, design v6 §10

Leitura do §10 e do F-11 antes de codar. Branch do mesmo PR #4 conferida limpa em `8c2e1bc`. A decisão de rodada fecha a lacuna pós-contestação registrada na v5.

Lista executada: `models/obra.py` (rodada 0 na versão, rodada nas duas snapshots e unicidade por item dentro da rodada); `services/flow.py` (incremento após validação de revisar, snapshots identificados e comparação filtrada por rodada corrente); `tests/test_flow.py` (F-11). Sem tabela nova, Alembic, rotas ou tela.

A snapshot existente é uma linha por item. Por isso `(versao_id, momento, rodada)` identifica o conjunto; a restrição SQL preserva também `ordem`/`codigo`, distinguindo os itens desse conjunto. Uma unicidade apenas na tripla impediria dois capítulos/adendos na mesma rodada. Essa interpretação foi informada antes da implementação e é verificada no F-11 com dois capítulos e dois adendos por momento da rodada 2.

Eventos passam a incluir a rodada no JSON de detalhe, sem alterar os registros anteriores. Testes cobrem contestar → revisar → liberar novamente na mesma versão; também recusar/reenvio antes do novo parecer. Histórico da rodada 1 e eventos anteriores são comparados integralmente após commit. Teste de rollback e hash esperado inválido garante que rodada não é consumida por operação rejeitada/desfeita. Teste com linhas inseridas fora da ordem cronológica verifica seleção por rodada, não pela posição dos registros.

## 2026-10-19 — Validação e commit do delta 3

Suíte final: 236 testes passaram (232 + 4), com 18 avisos existentes. A primeira prova de mutação sem os filtros revelou que o teste com chaves repetidas era insuficiente: o mapa sobrescrevia os itens antigos e o mutante passava. O teste foi reforçado com itens exclusivamente históricos, sem alterar o serviço, e a prova repetida: baseline 1 passou, mutante 1 falhou por AssertionError. Evidências em `evidencias-mutacao-v6/`. Suíte completa repetida após esse reforço, verde.

Commit `27c991b2691ae409715d5cd2a4824d1176779433` enviado à mesma branch do PR #4. Relatório atualizado para a v6; lacuna pós-contestação encerrada. Sem novo PR, merge ou deploy. CI em acompanhamento.

CI do delta 3 / v6 **verde** em Python 3.12, commit `27c991b2691ae409715d5cd2a4824d1176779433`: https://github.com/egarabini/gsi_ebd/actions/runs/39321913528. PR #4 confirmado aberto e árvore do app limpa. Lacuna da v5 encerrada; sem merge/deploy/Alembic.
