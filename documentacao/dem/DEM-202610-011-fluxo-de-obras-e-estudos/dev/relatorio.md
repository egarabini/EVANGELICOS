# DEM-202610-011 — relatório da fatia 1, delta 3 / v6

- **Branch:** `feature/DEM-202610-011-fatia1-dominio`, criada de `develop` (`dbbfc09`).
- **Mesmo PR:** https://github.com/egarabini/gsi_ebd/pull/4 → `develop`, aberto, sem merge.
- **Commit deste delta:** `27c991b2691ae409715d5cd2a4824d1176779433`.
- **Histórico:** `f202eb6` (inicial), `8f6608a` (v4, reprovado pelo EVAL), `8c2e1bc` (v5, 232 testes e lacuna de novos instantâneos registrada).
- **Alvo:** design §10 (v6) e F-11 do plano. A lacuna da revisão posterior à contestação foi **fechada** pela decisão de rodada; não permanece pendente.
- **Arquivos do delta:** `gsi_ebd/models/obra.py`, `gsi_ebd/services/flow.py`, `tests/test_flow.py`.

## O que mudou

`ObraVersao.rodada` inicia em zero. Após validar papel, estado, parecer, ajustes e hash esperado, `revisar` incrementa a rodada e cria o instantâneo visto correspondente. `liberar` cria o liberado da rodada corrente. As duas tabelas de instantâneos guardam a coluna `rodada`; nenhuma tabela nova foi criada.

A comparação RF11b consulta visto/liberado filtrando **a mesma rodada corrente** para capítulos e adendos. A prévia contra a cópia de trabalho usa o visto da rodada corrente. O evento de liberação continua registrando o tamanho da diferença, agora restrito à rodada atual. O JSON de detalhe dos eventos novos inclui `rodada`, sem atualizar eventos anteriores.

Contestar mantém a própria versão, suspende publicação e preserva os instantâneos anteriores, conforme v5. O próximo parecer abre rodada 2; a nova liberação volta a publicar a mesma versão sem colisão de chaves. Recusa/reenvio não incrementam rodada; o incremento acontece no parecer aprovado (`revisar`). Operações bloqueadas e rollback não consomem rodada. Nada é apagado ou sobrescrito no histórico de instantâneos/eventos.

### Unicidade por item dentro da rodada

Os modelos existentes têm **uma linha por item**, não uma linha por conjunto. A tripla `(versao_id, momento, rodada)` identifica o conjunto de instantâneos, e a restrição SQL inclui a identidade do item:

- Capítulo: `(versao_id, momento, rodada, ordem)`.
- Adendo: `(versao_id, momento, rodada, codigo)`.

Isso acrescenta rodada às restrições já existentes e permite vários capítulos/adendos por momento da mesma rodada. Uma unicidade apenas na tripla bloquearia o segundo item. A interpretação foi informada antes da implementação e conferida com dois capítulos e dois adendos na rodada 2.

## Testes e evidências

Do diretório do app, pelo Python:

`.venv/Scripts/python.exe -m pytest -q --basetemp=C:/Windows/Temp/dem011-v6-suite-validada`

**236 passaram (232 + 4 novos)**, com os 18 avisos de depreciação existentes. Inclui o gate de páginas. Runtime local Python 3.14.6; Python 3.12 validado no CI existente. `git diff --check` passou e linhas novas de código/testes são ASCII.

F-11 cobre:

- Contestação → novo parecer → liberação da mesma versão, rodada 2; também com recusa/reenvio antes do novo parecer (dois casos parametrizados).
- Diferença com o texto da rodada 2 e `tamanho_diferenca` no evento; a rodada 1 tinha outra diferença, que não interfere no resultado atual.
- Preservação integral dos instantâneos da rodada 1 e dos eventos anteriores após commit/refresh, com vários itens na nova rodada.
- Parecer com hash esperado inválido e rollback de um parecer válido não consomem rodada nem deixam instantâneos/eventos novos.
- Consulta com itens exclusivamente históricos e linhas fora da ordem cronológica não inclui rodadas antigas.

**Prova adicional de mutação:** em cópia fiel fora do app, o F-11 de isolamento passou; retirando apenas os filtros de rodada das consultas de diferença, falhou por incluir itens históricos. Baseline exit 0, mutante exit 1 por AssertionError, sem erro de coleta. Logs e JSON: [`evidencias-mutacao-v6/`](evidencias-mutacao-v6/). O primeiro teste apenas com chaves repetidas deixava esse mutante sobreviver porque o mapa sobrescrevia os itens antigos; ele foi reforçado antes da entrega com itens exclusivamente históricos e a prova foi repetida com sucesso.

Provas históricas preservadas, separadas desta execução: seis da entrega inicial em `evidencias-mutacao/`; normalização/evento da v4 em `evidencias-mutacao-delta-v4/`; leitura fresca da importação com cache quente da v5 em `evidencias-mutacao-v5/`. Não se afirma reexecução dessas provas históricas sobre este commit.

## Contratos e limites mantidos

Sete operações de domínio, permissões e estados no serviço; ambos os gates de licença relendo o CSV; JSON canônico LF/NFC; snapshots normalizados; `FonteInvalida` como `FluxoBloqueado`; conteúdo malformado bloqueado antes de gravar; substituição da versão anterior ao liberar uma nova. `alterar` só adiciona/atualiza e conserva os itens omitidos. Remover capítulo/adendo da base continua requisito da próxima fatia.

A camada de rotas é dona de commit/rollback; o domínio só faz flush. Trigger/ACL de imutabilidade contra SQL direto permanece com o deploy da v1. `CAMINHO_INVENTARIO` precisa apontar para CSV acessível no contêiner.

O schema da v1 deve incluir agora `ObraVersao.rodada` e `rodada` nas duas tabelas de snapshots, além das restrições únicas ajustadas e dos modelos/campos anteriores. `create_all` não altera colunas ou constraints existentes. Banco próprio/baseline são da DEM-005; não foi executada alteração de banco nem criada revisão Alembic.

Sem merge, deploy, telas, Alembic, Compose, segredos, corpus ou mudança do inventário/verificador. Study, planejar e multiambiente completo continuam fora. Relatório, jornada, changelog e logs ficam no repositório pai `EVANGELICOS/documentacao`, fora do Git do app. EVAL cego e aceite são posteriores ao delta.

CI do delta 3 / v6 **verde** em Python 3.12, commit `27c991b2691ae409715d5cd2a4824d1176779433`: https://github.com/egarabini/gsi_ebd/actions/runs/39321913528. PR #4 confirmado aberto e árvore do app limpa. Lacuna da v5 encerrada; sem merge/deploy/Alembic.
