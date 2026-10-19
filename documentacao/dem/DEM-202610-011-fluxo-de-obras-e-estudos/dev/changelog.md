# Changelog — DEM-202610-011

## 2026-10-19

- `f202eb6ba1edd5e9c7a74ab732ac77d0d5ad8759` — domínio do fluxo de obras, design v3: modelos, instantâneos, hash, fontes, sete operações e testes.
- PR [#4](https://github.com/egarabini/gsi_ebd/pull/4) → `develop`.
- Suíte local: 189 testes verdes; seis mutações detectadas. Sem merge ou deploy.

CI **verde** em Python 3.12, no commit `f202eb6ba1edd5e9c7a74ab732ac77d0d5ad8759`: https://github.com/egarabini/gsi_ebd/actions/runs/39315199116. Sem merge ou deploy.

## 2026-10-19 — Delta v4 no mesmo PR #4

- `8f6608a4bdeab6a381e8db95246a5c8badd5e60f` — segundo commit: JSON canônico, LF/NFC, eventos append-only, leitura fresca da licença e atualização sem remoção.
- 211 testes verdes (189 + 22); mutações novas C-10 e F-10 detectadas. Remoção de item da base é da próxima fatia.

CI do delta **verde** em Python 3.12, commit `8f6608a4bdeab6a381e8db95246a5c8badd5e60f`: https://github.com/egarabini/gsi_ebd/actions/runs/39317794718. PR #4 confirmado **aberto**, com exatamente os dois commits `f202eb6` e `8f6608a`. Árvore do app limpa. Sem merge ou deploy.

## 2026-10-19 — Correção v5 após EVAL

- `8c2e1bcc78078cdc36381be4d1b73f22e2407c4f` — reabre a própria versão contestada e suspende publicação; importação relê inventário; liberação substitui a anterior e registra tamanho da diferença; snapshots normalizados; payload e fonte usam exceção comum.
- 232 testes passaram (211 + 21), mutação do gate com cache quente detectada. Lacuna da revisão posterior à contestação registrada no relatório. Mesmo PR #4, sem merge/deploy.

CI da correção v5 **verde** em Python 3.12 no commit `8c2e1bcc78078cdc36381be4d1b73f22e2407c4f`: https://github.com/egarabini/gsi_ebd/actions/runs/39320863779. PR #4 confirmado aberto e árvore do app limpa. Sem merge/deploy. A lacuna de novos instantâneos pós-contestação permanece registrada para definição do ARQUITECT.

## 2026-10-19 — Delta 3, rodada de revisão v6

- `27c991b2691ae409715d5cd2a4824d1176779433` — rodada corrente na versão e nos instantâneos; novo parecer abre rodada; liberação e diferença usam a mesma rodada; histórico preservado.
- F-11: contestar/revisar/liberar na mesma versão, recusa/reenvio, rollback e isolamento das rodadas. 236 testes passaram (232 + 4); mutação sem filtro detectada.
- Lacuna da v5 encerrada; mesmo PR #4, sem merge/deploy/Alembic.

CI do delta 3 / v6 **verde** em Python 3.12, commit `27c991b2691ae409715d5cd2a4824d1176779433`: https://github.com/egarabini/gsi_ebd/actions/runs/39321913528. PR #4 confirmado aberto e árvore do app limpa. Lacuna da v5 encerrada; sem merge/deploy/Alembic.
