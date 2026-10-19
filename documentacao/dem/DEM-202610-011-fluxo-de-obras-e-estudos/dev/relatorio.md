# DEM-202610-011 — relatório da fatia 1

- **Branch:** `feature/DEM-202610-011-fatia1-dominio`, criada de `develop` (`dbbfc09`).
- **PR:** https://github.com/egarabini/gsi_ebd/pull/4 → `develop`.
- **Commit:** `f202eb6ba1edd5e9c7a74ab732ac77d0d5ad8759`.
- **Alvo:** design v3 encontrado durante a implementação, após a orientação do ARQUITECT de aguardar a correção das assinaturas/instantâneos. O v3 substituiu o `itens_visto` persistido por instantâneo `visto` e definiu `hash_esperado` e conteúdo novo em `alterar`.
- **Arquivos:** `gsi_ebd/models/obra.py`, `gsi_ebd/models/__init__.py`, `gsi_ebd/services/flow.py`, `gsi_ebd/services/fontes.py`, `tests/test_flow.py`, `tests/test_fontes.py`.
- **Entregue:** modelos e registro no metadata; sete operações do domínio; estados/papéis no serviço; assinatura completa; conferência contra conteúdo não visto; licença em duas etapas; snapshots visto/liberado; hash canônico v3; diferença por item com texto; versão publicada preservada ao alterar/contestar; adendos de ambiente excluídos do hash e dos snapshots.
- **Testes:** `.venv/Scripts/python.exe -m pytest -q --basetemp=C:/Windows/Temp/dem011-suite-final`, no diretório do app: **189 passed** (128 existentes + 61 novos), com 18 avisos de depreciação existentes. Cobre F-01..F-09, N-01..N-08 e C-01..C-07, incluindo o gate de páginas da suíte. `git diff --check` passou. Runtime local: Python **3.14.6**; o ambiente disponível não é 3.12. A versão 3.12 é validada pelo CI existente, sem alterar dependências.
- **Fora de escopo:** telas, Study, planejar, vínculo/adoção e adendos em UI, isolamento completo entre ambientes, Compose, deploy, segredos, corpus, inventário e verificador. Sem revisão Alembic, sem merge e sem publicação. Nenhum import de `reflex` em `flow.py`.

## Prova de mutação

Cópias fiéis de código e testes em diretório temporário fora do app. Cada seletor passou na cópia original (exit 0); depois da única mutação, falhou por comportamento (exit 1, sem erro de coleta). O código original permaneceu intacto.

| Remoção | Caso | Falhas no mutante |
|---|---|---|
| Gate `nao_entra` | N-01 | 1 |
| Checagem `revisor_id` | N-03 | 1 |
| Checagem do papel | N-04 | 8 |
| Criação do instantâneo liberado | N-07 | 1 |
| Checagem `hash_esperado` | N-08 | 2 |
| Criação do instantâneo visto | F-08 | 1 |

Logs antes/depois e `resultados.json`: [`evidencias-mutacao/`](evidencias-mutacao/). Os logs são da execução local; não substituem o EVAL cego.

## Contrato de integração

O chamador fornece `Session` e controla commit/rollback. Não há commit interno. Operações de versões existentes bloqueiam a linha da obra com `FOR UPDATE` quando suportado pelo banco. Restrições únicas: obra/número da versão; versão/momento/ordem do capítulo; versão/momento/código do adendo.

`importar` recebe o ID da fonte (por exemplo `F-004`). `alterar` recebe um dicionário com `capitulos` (lista de `ordem`, `titulo`, `conteudo_md`) e `adendos` (lista de `codigo`, `titulo`, `texto`). IDs de itens que mantêm ordem/código são preservados. Conteúdo de ambiente é recusado nessa operação. A diferença usa `capitulo:{ordem}` e `adendo:{codigo}`; adição/remoção conta como diferença. `diferenca(..., atual=True)` oferece a prévia antes da liberação; sem esse argumento, compara os snapshots persistidos.

`contestar` abre uma nova versão em revisão, preservando a versão liberada e suas assinaturas, conforme a tabela da v2; é a salvaguarda v3 sem destruir a evidência publicada. Só um ciclo pendente por obra. Não cria adoção automática nem muda a versão em uso.

## Schema e deploy da v1 — sem execução nesta DEM

A v1 precisa incluir `Obra.status`, `Obra.versao_liberada_id`, `Obra.fonte_id`, `Obra.updated_at`, `Adendo.ambiente_id` e as tabelas `obraversao`, `obraversaocapitulo`, `obraversaoadendo`, com FKs, índices e restrições únicas. `create_all` cria tabelas ausentes, mas não acrescenta colunas a tabelas existentes. O banco próprio da v1 e seu baseline ficam com a DEM-005; não foi alterado banco existente nem criada revisão Alembic.

O inventário precisa estar acessível no contêiner, com `CAMINHO_INVENTARIO` apontando para o CSV. Nenhum ajuste de Compose/imagem foi feito.

## Lacunas e limites para o PLANNER

1. **Carga única × decisão atual:** `liberar` chama `fonte_decisao` novamente, usando o vínculo persistido. O cache é por caminho, como pedido; uma alteração no mesmo CSV só aparece após reinício/invalidação explícita do cache. Não foi inventado polling, TTL ou recarga automática. O teste C-05 substitui o caminho configurado e verifica que a liberação consulta a decisão atual carregada; não afirma hot reload do arquivo.
2. **Trilha imutável de todos os passos:** o design só fornece campos do ciclo e snapshots; não define um log append-only de recusas/reenvios sucessivos. O parecer de uma recusa pode ser substituído no próximo parecer. Os snapshots e assinaturas de versões publicadas são preservados pelas operações, mas não há trigger/ACL de imutabilidade contra SQL direto. Nenhum modelo adicional de auditoria foi inventado.
3. **Remoção de item referenciado:** o design não define política para excluir capítulos/adendos usados por mapa de origem ou adendo de ambiente. Itens mantidos preservam ID; remoções continuam sujeitas às FKs do banco e exigem rollback pelo chamador se houver referência. Não foi criado cascade nem modificada a fatia de Study.
4. **Canonização:** a v3 mudou o algoritmo da primeira proposta, mantendo o prefixo `v1|`; nesta feature ainda não havia assinaturas persistidas. O hash segue literalmente o algoritmo v3 com hashes individuais ordenados. A política de escape do separador em campos não foi definida pelo design; não foi inventada uma canonização divergente.

Documentação e evidências estão no repositório pai `EVANGELICOS`, fora do Git do app; o PR do app contém os seis arquivos de código/testes e descreve os resultados e limites. O EVAL cego e o aceite permanecem com seus responsáveis.

CI **verde** em Python 3.12, no commit `f202eb6ba1edd5e9c7a74ab732ac77d0d5ad8759`: https://github.com/egarabini/gsi_ebd/actions/runs/39315199116. Sem merge ou deploy.
