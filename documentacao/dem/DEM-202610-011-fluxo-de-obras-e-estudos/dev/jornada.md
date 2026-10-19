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
